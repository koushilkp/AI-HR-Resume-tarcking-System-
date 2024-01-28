from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image 
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text    

def input_pdf_setup(uploaded_file):
    ##convert pdf file to image 

    image = pdf2image.convert_from_bytes(uploaded_file.read())

    first_page=image[0]

    ##convert into bytes
    if uploaded_file is not None:
        img_byte_arr =io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts= [
            {
                "mine_type" : "image/jpeg",
                "data"      : base64.b64encode(img_byte_arr).decode()
            }
        ]

        return pdf_parts
    else:
        raise FileExistsError("NO file uploaded")


##streamlit APP
    
st.set_page_config(page_title="ATS Resume Expert")
st.header("AI ATS tracking system")
input_text=st.text_area("Job Description:",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me about the Resume")
# submit2 = st.button("How can i Improvise you skills")
# submit3 = st.button("What are the key words missing")
submit2 = st.button("Percentage Match")

input_prompt1= """ you are Good Experience HR  in this we are happy see max matching with my AI tool"""

input_prompt2= """ You are the techinacl Expert  in data field and we will happy guied you too improve best to"""


if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file) 
        response    = get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader ("the Response is")
        st.write(response)

    else:
        st.write("Please upload the resume in PDF format only")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response    = get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader ("the Response is")
        st.write(response)

    else:
        st.write("Please upload the resume in PDF format only")