import streamlit as st
import pdf2final_list
import text2ppt
import shutil
import os
from summarizer import generate_summary

def main():
    st.set_page_config(page_title="PDF2PPT Generator", page_icon="📚")
    st.title("PDF2PPT Generator")

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
            text2ppt.presentate(x)

            file_path = st.file_uploader("Save PPT", type=['pptx'], key="file_uploader")
            if file_path is not None:
                with open("PPT.pptx", "wb") as file:
                    file.write(file_path.getvalue())

                shutil.copy("PPT.pptx", file_path.name)
                st.success("File Saved Successfully")
                os.startfile(file_path.name)
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
