import streamlit as st
import pandas as pd
import requests





st.title("Toxic Link Analysis")

urls=st.text_area(label='Enter Urls',placeholder='Enter URLs (1 per line)')
lines = urls.split("\n")

def split(list_a, chunk_size):
  for i in range(0, len(list_a), chunk_size):
    yield list_a[i:i + chunk_size]

chunk_size = 49
full_list = list(split(lines, chunk_size))

auth = (st.secrets['api_key1'], st.secrets['api_key2'])
url = "https://lsapi.seomoz.com/v2/url_metrics"

appended_data = []
for l in full_list:
    data = {"targets":l}
    request = requests.post(url, json=data, auth=auth)
    try:
        df = pd.DataFrame((request.json()['results']))
        appended_data.append(df)
    except KeyError:
        print("??")

df = pd.concat(appended_data)

@st.cache
def convert_df(df):
     return df.to_csv(index=False).encode('utf-8')



try:
     csv = convert_df(df)
     st.download_button(
          label="Get Spam Scores",
          data=csv,
          file_name='spam_score.csv',
          mime='text/csv',
     )
except:
     print("?")
