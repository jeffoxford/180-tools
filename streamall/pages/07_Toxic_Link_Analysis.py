import streamlit as st
import pandas as pd
import requests





st.title("Toxic Link Analysis")

urls=st.text_area(label='Enter Urls',placeholder='Enter URLs (1 per line)')
lines = urls.split("\n")

auth = (st.secrets['api_key1'], st.secrets['api_key2'])
url = "https://lsapi.seomoz.com/v2/url_metrics"
data = {"targets":lines}
request = requests.post(url, json=data, auth=auth)

try:
     df = pd.DataFrame((request.json()['results']))
except KeyError:
     print("??")

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
