import streamlit as st
from src.pdf2final_list import process
from  src.text2ppt import create_ppt
import shutil
import os
from src.summarizer import generate_summary
from src.gpt import generate_content
import requests
from streamlit_lottie import st_lottie
from PIL import Image
from streamlit_option_menu import option_menu
import tempfile


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def main():
    st.set_page_config(page_title="PowerPoint Generator", page_icon=":books:", layout="wide")


    # 2. horizontal menu
    choice = option_menu(None, ["Home", "Generate PPT", 'Summarizer'], 
        icons=['Home', 'Generate PPT', 'Summarizer'], 
        menu_icon="cast", default_index=0, orientation="horizontal")

    if choice == "Generate PPT":
        generate_ppt()
    elif choice == "Summarizer":
        summarizer()

    elif choice == 'Home': 
        Home()


def Home():
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
        col1, col2 = st.columns([1, 1])
        with col1:
            image_container, text_container = st.columns((1, 2))
            with image_container:
                # gpt_logo = Image.open('images/gptlogo.png', mode='r')
                # st.image(gpt_logo, use_column_width='always')
                with tempfile.TemporaryDirectory() as temp_dir:
                    gpt_logo_path = os.path.join(temp_dir, "gptlogo.png")
                    gpt_logo = Image.open('logo/gptlogo.png', mode='r')
                    gpt_logo.save(gpt_logo_path)
                    st.image(gpt_logo_path, use_column_width='always')

            
            with text_container:
                st.markdown(
                        """
                        The PowerPoint Generator leverages the power of GPT-3.5, an advanced language model developed by OpenAI. By harnessing the capabilities of GPT-3.5, it utilizes artificial intelligence to rapidly generate detailed content for a wide range of topics. This ensures that the generated slides contain accurate and relevant information, saving you time and effort in researching and compiling content for your presentation.
                        """
                    )
           

    #ABOUT SUMMARIZER
    with col2:
            image_container, text_container = st.columns((1, 2))
            with image_container:
                # summarizer_logo = Image.open('images/summarizer.jpg', mode='r')
                # st.image(summarizer_logo, use_column_width='always')
                with tempfile.TemporaryDirectory() as temp_dir:
                    summarizer_logo_path = os.path.join(temp_dir, "summarizer.jpg")
                    summarizer_logo = Image.open('logo/summarizer.jpg', mode='r')
                    summarizer_logo.save(summarizer_logo_path)
                    st.image(summarizer_logo_path, use_column_width='always')

            with text_container:
                st.markdown(
                    """
                    The Summarizer is a powerful text summarization tool that utilizes advanced natural language processing techniques to generate concise summaries of large blocks of text. It helps users extract key information and main points from lengthy documents, articles, or any text input.
                    Using state-of-the-art language models, the Summarizer analyzes the input text, identifies important sentences or passages, and generates a condensed summary that captures the essence of the original content. The summarization process saves time and allows users to quickly grasp the main ideas without having to read through the entire text.
                    With the Summarizer, you can effectively summarize research papers, news articles, blog posts, or any textual content, enabling you to digest information more efficiently and make informed decisions. Simply input your text, click the "Summarize" button, and let the Summarizer do the rest!
                    """
                )
        
 
def generate_ppt():
    st.write("Enter comma-separated topics:")
    input_text = st.text_input("Topics")

    with st.container():
        difficulty_container, color_container = st.columns((3, 1))
        with difficulty_container:
            difficulty = st.select_slider(
                'Select the diffulcty of the content',
                options=['easy', 'medium', 'hard']
            )
        with color_container:
            theme = st.selectbox('Select Theme',(1, 2, 3, 4, 5, 6, 7))
    with st.container():
        keyword_container, language_container = st.columns((1, 1))
        with keyword_container:
            keyword = st.text_input('Keywords')
        with language_container:
            language = st.selectbox(
            'Select the language',
            ('English', 'فارسی'))

            if language == 'فارسی':
                language = 'farsi'

    with st.container():
        author_container, presentation_title_container= st.columns((1, 1))
        with author_container:
            author_name = st.text_input("Author Name")
    if st.button("Generate PPT", key="generate_button"):
        try:
            with open(f'Cache/{input_text}.txt', 'w', encoding='utf-8') as f:
                f.write(generate_content(input_text, process(difficulty, language)))
            with st.spinner('In progress...'):
                prs = create_ppt(f'Cache/{input_text}.txt', theme, input_text, author_name)
            st.success('Done!')

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


