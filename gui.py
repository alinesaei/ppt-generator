import streamlit as st
from src.pdf2final_list import process
from  src.text2ppt import presentate
import shutil
import os
from src.summarizer import generate_summary
import requests
from streamlit_lottie import st_lottie
from PIL import Image

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
    
    #ABOUT POWERPOINT GENERATOR
    with st.container():
        image_container, text_container = st.columns((1, 2))
        with image_container:
        #     #TODO
            gpt_logo = Image.open('images/gptlogo.png', mode='r')
            st.image(gpt_logo, use_column_width='always')
            
        with text_container:
            #TODO
           st.markdown(
                """
                The PowerPoint Generator leverages the power of GPT-3.5, an advanced language model developed by OpenAI. By harnessing the capabilities of GPT-3.5, it utilizes artificial intelligence to rapidly generate detailed content for a wide range of topics. This ensures that the generated slides contain accurate and relevant information, saving you time and effort in researching and compiling content for your presentation.
                """
            )
           
    st.divider()
    #ABOUT SUMMARIZER
    with st.container():
        image_container, text_container = st.columns((1, 2))
        with image_container:
        #     #TODO
            summarizer_logo = Image.open('images/summarizer.jpg', mode='r')
            st.image(summarizer_logo, use_column_width='always')
        with text_container:
            #TODO
            st.markdown(
                """
                The Summarizer is a powerful text summarization tool that utilizes advanced natural language processing techniques to generate concise summaries of large blocks of text. It helps users extract key information and main points from lengthy documents, articles, or any text input.
                Using state-of-the-art language models, the Summarizer analyzes the input text, identifies important sentences or passages, and generates a condensed summary that captures the essence of the original content. The summarization process saves time and allows users to quickly grasp the main ideas without having to read through the entire text.
                With the Summarizer, you can effectively summarize research papers, news articles, blog posts, or any textual content, enabling you to digest information more efficiently and make informed decisions. Simply input your text, click the "Summarize" button, and let the Summarizer do the rest!
                """
            )
        

    
    menu = ["Generate PPT", "Summarizer"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Generate PPT":
        generate_ppt()
    elif choice == "Summarizer":
        summarizer()

def generate_ppt():
    st.write("Enter comma-separated topics:")
    input_text = st.text_input("Topics")
    difficulty = st.select_slider(
        'Select the diffulcty of the content',
        options=['easy', 'medium', 'hard']
    )
    keyword = st.text_input('Keywords')
    color = st.color_picker('Pick A Color for the background', '#00f900').lstrip('#')
    file_name_save = st.text_input('file name')
    #author_name = st.text_input("Author Name")
    #presentation_title = st.text_input("Presentation Title")
    if st.button("Generate PPT", key="generate_button"):
        try:
            topics = [topic.strip() for topic in input_text.split(",")]
            st.write(f"Topics: {', '.join(topics)}")
            st.info("Generating PPT... Please wait.")
            keyword_list = [k.strip() for k in keyword.split(',')]
            x = process(topics, difficulty)
            prs = presentate(x, file_name_save, color)
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


