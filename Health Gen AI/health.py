### Health Management APP
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(Age,Sex,Height_feet,Height_inches,Weight,Diet_Preference,Progress_Pace):

    prompt = f"""
    You are a certified nutritionist and fitness advisor. Based on the user details below, create a safe, concise, and professional health plan:

- Age: {Age}
- Sex: {Sex}
- Height: {Height_feet} ft {Height_inches} in
- Weight: {Weight} kg
- Diet Preference: {Diet_Preference}
- Progress Pace: {Progress_Pace}

output(follow this exact format with fixed line space):

1. BMI and category.  
2. Target weight range and gain/loss needed.  
3. Estimated time (weeks/months) to reach target BMI.  
4. Daily calorie requirement.  
5. Macro ratio (Carbs %, Protein %, Fats %).  
6. 1-day indian meal plan (table format: Time | Meal | Food Items | Portion | Calories).  
7. Light exercises.  
8. Daily water intake.  
9. 2–3 lifestyle tips.  
10. Weekly unique diet plan variations (Week 1, Week 2, etc.) in short table format.  
⚠️Output must be with emojis/icons, no extra line breaks.
⚠️ Keep it crisp, professional, and minimal—no extra explanation.      
⚠️ Output must strictly follow this format, no deviations.
⚠️ Ensure advice is practical, culturally neutral, and safe for a general healthy adult. Do not provide medical treatment.
"""
    model=genai.GenerativeModel('gemini-2.5-flash')
    response=model.generate_content(prompt)
    return response.text

    
##initialize our streamlit app

st.set_page_config(page_title="Personalized Health Plan",page_icon= "🩺",layout="centered")
st.title("📊 Your Personalized Diet & Fitness Plan")
st.write("Fill in your details to get a customized health, diet, and fitness roadmap.")

# user inputs

Age = st.number_input('🧑 Age:', min_value=5, max_value= 100, step=1)
Sex = st.radio('⚧️ Sex',['Male','Female','Others'])
col1,col2 = st.columns(2)
with col1:
    Height_feet = st.number_input('📏 Height (feet)', min_value=3, max_value=8, step=1)
with col2:
    Height_inches = st.number_input('📏 Height (inches)', min_value=0, max_value=11, step=1)
Weight = st.number_input('⚖️ Weight (kg)', min_value=10.0, max_value=300.0, step=0.1, format="%.1f")
Diet_Preference = st.selectbox("🥗 Diet Preference",["Vegetarian", "Non-Veg", "Eggetarian", "Vegan", "Any"])
Progress_Pace = st.select_slider('⏱️ Progress Pace',options=['Slow','Medium','Fast'],value='Medium')

# submit button

if st.button('Generate My Health Plan'):
    with st.spinner('Generating your Plan...'):
        response = get_gemini_repsonse(Age,Sex,Height_feet,Height_inches,Weight,Diet_Preference,Progress_Pace)
    st.subheader('Generated Plan')
    st.write(response)
else:
    st.warning('Please Enter your Details')