from operator import index
from os import sep
from unittest import result
import pandas as pd
import time
import streamlit as st
startTime = time.time()
import nltk
import nltk.data
nltk.download('punkt')

st.title('Internal Linking Tool')

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def get_data (sentences_text , file):
    sentences =tokenizer.tokenize(sentences_text)
    try:
        df = pd.read_csv(file, encoding= 'UTF-16' , on_bad_lines='skip', sep='	')
    except:
        try:
            df = pd.read_csv(file, encoding= 'UTF-8' , on_bad_lines='skip')
        except:
            try:
                df = pd.read_csv(file,  on_bad_lines='skip')
            except:
                df = pd.read_csv(file)

    products_list = df.values.tolist()

    resultList = []

    for p in products_list:
        keyword = str(p[0]).lower()
        for sentence in sentences:
            if keyword in sentence.lower():
                ts = sentence
                resultList.append({
                    'Keyword' : keyword
                    ,'Text Snippet': ts
                    ,'Search Volume': p[2]
                    ,'Rank': p[6]
                    ,'Destination URL': p[7]
                })
            else:
                pass
    return resultList


keywords = st.text_area('Add the article')
file_name = st.file_uploader('Upload upload websites ranking data (csv)')
if st.button('Start Process The Keyword'):
    resultList = get_data(keywords,file_name)


    url = 'https://raw.githubusercontent.com/jeffoxford/internal-linking/main/coefficients.csv'


    coificent =pd.read_csv(url)
    outputDf = pd.DataFrame(resultList)
    result_df = outputDf.merge(coificent, on='Rank', how='left')
    result_df["Opportunity Score"] = result_df["Search Volume"] * result_df["Coeffecient"]
    result_df = result_df.drop('Coeffecient', 1)

    st.dataframe(result_df)
    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv(index=False,).encode('utf-8')
    csv = convert_df(result_df)


    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='data_file.csv',
        mime='text/csv',
    )


    st.text(f"Execution time: { ( time.time() - startTime ) :.2f} sec")
