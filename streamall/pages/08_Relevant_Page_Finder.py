import streamlit as st
from serpapi import GoogleSearch
import pandas as pd



st.title("Relevant Page Finder")

domain =st.text_input('Single Domain')
urls =st.text_area(label='Enter Keywords',placeholder='Enter Keywords (1 per line)')
lines = urls.split("\n")

# to insert the api key for serp  like this >>>>>>>>>>> st.secrets['api_key3'] int he strwamlit secrets
def get_data(keyword,domain): 
    query = f'"{keyword}" site:{domain}'
    params = {
    "engine": "Google",
    "q": query,
    "cc": "US",
    "api_key": st.secrets['api_key3']
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return results

result_data = []
for keyword in lines :
    r = get_data(keyword,domain)
    try:
        l1 = r['organic_results'][0]['link']
    except:
        l1 = ''
    try:
        l2 = r['organic_results'][1]['link']
    except:
        l2 = ''
    try:
        l3 = r['organic_results'][2]['link']
    except:
        l3 = ''
    try:
        result_data.append({
            'input_keyword' : keyword,
            '#1 URL' : l1,
            '#2 URL' : l2,
            '#3 URL' : l2,
        })
    except:
        result_data.append({
            'input_keyword' : keyword,
            '#1 URL' : '',
            '#2 URL' : '',
            '#3 URL' : '',
        })

if st.button('Start Process The Keyword'):
    df = pd.DataFrame(result_data)
    st.dataframe(df)
    @st.cache
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')



    try:
        csv = convert_df(df)
        st.download_button(
            label="Download Data",
            data=csv,
            file_name='relevant_page_finder.csv',
            mime='text/csv',
        )
    except:
        print("?")

