from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini Pro model and get repsonses
def get_gemini_email(notes,tone,length):
    prompt = f"""
    you are an expert email writer. convert following notes into polished email.
    Notes = {notes}
    Tone = {tone}
    Length = {length}

    provide:
    1.A professional subject line
    2.A complete email body
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text

##initialize our streamlit app

st.set_page_config(page_title="Smart Email writer", page_icon="📧")
st.title(" 📧 Smart Email Writer")
st.write("Turn your bullet points into professional emails instantly!")

# user inputs
notes = st.text_area('Enter your notes or bullet points:')
tone = st.selectbox('Chosse the tone:',['Formal','Friendly','Casual'])
length = st.radio('Choose Email length:',['Short','Detailed'])

# submit button
if st.button("Generate email"):
    if notes.strip():
        with st.spinner('Writing your Email...'):
            response = get_gemini_email(notes,tone,length)
        st.subheader('Generated Email')
        st.write(response)

        # copy or save option
        st.download_button('Download Email',response,file_name='email.txt')

    else:
        st.warning('Please Enter notes')
    



    

