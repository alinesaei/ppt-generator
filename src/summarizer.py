from transformers import pipeline


def generate_summary(text, language):
    summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base")
    if language == 'English':
        summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
    elif language == 'Farsi':
        summary = summarizer(text, max_length=100, min_length=30, do_sample=False, model="hossein/Multi-News")
    return summary[0]['summary_text']