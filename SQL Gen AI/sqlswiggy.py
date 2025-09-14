from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

import streamlit as st
import os
import sqlite3
import pandas as pd

import google.generativeai as genai
## Configure Genai Key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-2.5-flash')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database

def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df, None
    except Exception as e:
        return None, str(e)

## Define Your Prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the table 'swiggy' with the following columns:
    ID, Area, City, Restaurant, Price, "Avg ratings", "Total ratings", "Food type", Address, "Delivery time".

    Rules:
    - If column name has spaces (like Food type,Avg ratings,Total ratings Delivery time), wrap them in double quotes.
    - Do not include ``` in your answer
    - Do not include the word 'sql' in your answer
    
    Example 1 - How many entries of records are present?, 
    SQL: SELECT COUNT(*) FROM swiggy;

    Example 2 - Find the average delivery time of 'Chinese' food type restaurants in each city?, 
    SQL: SELECT AVG("Delivery time"), City FROM swiggy WHERE "Food type" = 'Chinese' GROUP BY City;

    Example 3 - Calculate the average price of restaurants in each area of 'Bangalore'?, 
    SQL: SELECT AVG(Price), Area FROM swiggy WHERE City = 'Bangalore' GROUP BY Area;
    """
]


## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_area('Enter your SQL Questions:')

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    with st.spinner('Generating answer...'):
        response=get_gemini_response(question,prompt)
    st.subheader("Generated SQL Query")
    st.code(response,language='sql')

    with st.spinner("Running query..."):
        result_df, error = read_sql_query(response, "swiggy.db")
    
    st.subheader("Query Results")
    if error:
            st.error(f"SQL Error: {error}")
    elif result_df is not None and not result_df.empty:
            # Add row numbering like Workbench
            result_df.reset_index(inplace=True)
            result_df.rename(columns={"index": "#"}, inplace=True)
            result_df["#"] = result_df["#"] + 1
            st.dataframe(result_df)
    else:
            st.info("Query executed successfully, but no rows returned.")
        









