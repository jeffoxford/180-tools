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
    i = 1
    try:
        for v in r['organic_results']:
            if i <= 3 :
                position =v['position']
                title    =v['title']
                link     =v['link']
                snippet  =v['snippet']
                total_results = r['search_information']['total_results']

                result_data.append({
                    'input_keyword' : keyword,
                    'position' : position,
                    'title' : title,
                    'link' : link,
                    'snippet' : snippet,
                    'total_results' : total_results
                })

            i = i + 1
    except:
        result_data.append({
            'input_keyword' : keyword,
            'position' : 0,
            'title' : '',
            'link' : '',
            'snippet' : '',
            'total_results': 0
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
            label="Get Relevant Page Finder",
            data=csv,
            file_name='relevant_page_finder.csv',
            mime='text/csv',
        )
    except:
        print("?")

