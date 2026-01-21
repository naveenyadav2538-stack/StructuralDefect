import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import datetime as dt


# Configure the model
gemini_api_key = os.getenv('Google-API-Key3')
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# Lets create sidebar for image upload
st.sidebar.title(':red[Upload the Images Here:]')
uploaded_image = st.sidebar.file_uploader('Images',type=['jpeg','jpg','png','jfif'],
                                          accept_multiple_files=True)
uploaded_image=[Image.open(ing) for ing in uploaded_image]
if uploaded_image:
    st.sidebar.success('Images have been uploaded Successfully')
    st.sidebar.subheader(':blue[Upload Images]')
    st.sidebar.image(uploaded_image)

# Lets create the main page
st.title(':orange[STRUCTURAL DEFECT:-] :blue[AI Assisted Structural defect idendifier]')
st.markdown('#### :yellow[This application takes the images of structural defects from the construction site and prepares the AI assisted report]')
title=st.text_input('Enter the Title of the report:')
name=st.text_input('Enter the Name of the person who has prepared input:')
desig=st.text_input('Enter the designation of person who have prepared the report:')
org=st.text_input('Enter the name of the organisation:')

if st.button('SUBMIT'):
    with st.spinner('Processing...'):
        prompt=f'''
        <Role> You are an expert structural engineer with 20 + expereince in construction industry.
        <Goal> You need to prepare a detailed report on the structural defect shown in the images provided by the user.
        <Context> The images shared by the user has been attached.
        <Format> Follow the steps to prepare the report
        * Add title at the top of the report.The title provided by the user is {title}.
        * Next add name ,designation and  organisation  of a person who has prepared the report also include the date.
        Following are the details provided by the user 
        Name:{name}
        Designation:{desig}
        Organization:{org}
        Date:{dt.datetime.now().date()}
        * Identify and classify the defect for example :crack,spalling,corossion,honeycombing,etc.
        * There could be more than one defects in images.Identify all defects seperatly.
        * For each defect identified provide a short description of the defect and its potential impact on the structure.
        * For each defect measure the severity as low , medium or high .Also mentioning if the defect is inevitable or not.
        * Provide the short term and the long term solution for the repair along with an estimated cost in INR and estimated time.
        * What precautionary measures can be taken to avoid these defects in future.

        
        <Instructions>
        * The report generated should be in word format.
        * Use bullet points and tables wherever possible.
        * Make sure the report doesnot exceeds 3 pages.
'''
        
        response = model.generate_content([prompt,*uploaded_image],
                                          generation_config={'temperature':0.9})
        st.write(response.text)


        if st.download_button(
            label='Click To Download',
            data=response.text,
            file_name='structural_defect_report.txt',
            mime='text/plain'
        ):
            st.success('Your File is Downloaded')
