import streamlit as st
import openai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = api_key


def askGPT(input):
    prompt = f"""
correct grammatical errors from the text delimited by triple backticks.
```{input}```
"""
    prompt_2 = f"""
Your task is to perform the following actions: 
1 - Summarize the following text delimited by 
  <> with 1 sentence.
2 - Translate the summary into French.
3 - List each name in the French summary.
4 - Output a json object that contains the 
  following keys: french_summary, num_names.

Use the following format:
Text: <text to summarize>
Summary: <summary>
Translation: <summary translation>
Names: <list of names in Italian summary>
Output JSON: <json with summary and num_names>

Text: <{input}>
"""
    messages = [{"role": "user", "content": prompt_2}]
    if input:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
        )
        st.write(response.choices[0].message["content"])


st.title("Your very own Enlgish Tutor")
st.subheader("Keep your mistakes systematically")
input = st.text_area("Write on", height=500)
st.button("Improve", on_click=askGPT(input))