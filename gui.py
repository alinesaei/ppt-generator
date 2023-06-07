import streamlit as st
import src.pdf2final_list
import src.text2ppt
import shutil
import os
from src.summarizer import generate_summary
import requests
from streamlit_lottie import st_lottie


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def main():
    st.set_page_config(page_title="PowerPoint Generator", page_icon=":books:", layout="wide")

    # --- HEADER SECTION ---
    with st.container():
        left_col, right_col = st.columns(2)
        with left_col:
            st.subheader("Welcome to Presentation Generator!")
            st.title("Presentation Generator 💻 :book:")
            st.write(
                """
                **Presentation Generator is a powerful web application that empowers
                you to create stunning PowerPoint presentations and generate concise text summaries effortlessly.
                Whether you need to deliver a compelling presentation or extract key information from lengthy texts,
                this application is here to simplify your workflow.**
                """
                )
            st.markdown("[:link:](https://github.com/alinesaei/ppt-generator)")
        with right_col:
           # st.image('images/presentation-logo2.jpg', use_column_width="always")
           st_lottie("https://assets2.lottiefiles.com/private_files/lf30_0dui3jqg.json")
    st.divider()
    with st.container():
        image_container, text_container = st.columns((1, 2))
        #with image_container:
            #TODO
            #st.image('images/summarizer.jpg', use_column_width='always')
        #with text_container:
            #TODO
            #st.image('images/gptlogo.png', use_column_width='always')
    
    menu = ["Generate PPT", "Summarizer"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Generate PPT":
        generate_ppt()
    elif choice == "Summarizer":
        summarizer()

def generate_ppt():
    st.write("Enter comma-separated topics:")
    input_text = st.text_input("Topics")
    #author_name = st.text_input("Author Name")
    #presentation_title = st.text_input("Presentation Title")
    if st.button("Generate PPT", key="generate_button"):
        try:
            topics = [topic.strip() for topic in input_text.split(",")]
            st.write(f"Topics: {', '.join(topics)}")
            st.info("Generating PPT... Please wait.")

            x = pdf2final_list.process(topics)
            prs = text2ppt.presentate(x)
            #save_ppt(prs, '/media/ali/New Volume/znu/term 10/AI-presentation-generator/app/presentation-generator')
                
        except Exception as e:
            st.error(str(e))

def summarizer():
    st.write("Enter text to summarize:")
    input_text = st.text_area("Text")

    if st.button("Summarize", key="summarize_button"):
        try:
            summarized_text = generate_summary(input_text)
            st.subheader("Summarized Text:")
            st.write(summarized_text)
        except Exception as e:
            st.error(str(e))

if __name__ == '__main__':
    main()
