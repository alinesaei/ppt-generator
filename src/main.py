import nltk
from transformers import BartTokenizer, BartForConditionalGeneration
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import torch

def generate_bullet_points(paragraph, max_words=10, num_sentences=5):
    # Load pre-trained BART model and tokenizer
    model_name = 'facebook/bart-base'
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)

    # Split paragraph into sentences
    sentences = nltk.sent_tokenize(paragraph)

    bullet_points = []
    # Generate bullet points for each sentence
    for sentence in sentences:
        # Tokenize input sentence
        input_ids = tokenizer.encode(sentence, return_tensors='pt')

        # Generate summary using BART model
        with torch.no_grad():
            outputs = model.generate(input_ids, num_beams=4, max_length=50, early_stopping=True)

        # Decode the generated summary
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Parse the summary with TextRank
        parser = PlaintextParser.from_string(summary, Tokenizer('english'))
        summarizer = TextRankSummarizer()
        ranked_sentences = summarizer(parser.document, num_sentences=1)

        # Truncate the sentence to the desired maximum length
        bullet_point = truncate_text(str(ranked_sentences[0]), max_words)
        bullet_points.append(bullet_point)

    return bullet_points



# Example usage
paragraph = """Lionel Messi is an Argentinian soccer player who has played for FC Barcelona, Paris Saint-Germain, and the Argentina national team. As a teenager, Messi moved from Argentina to Spain after FC Barcelona agreed to pay for medical treatments related to his growth hormone disorder. At the club, he earned renown as one of the greatest players in history, helping FC Barcelona win more than two dozen league titles and tournaments. In 2012, he set a record for most goals in a calendar year and, a decade later, helped the Argentina national team win its third FIFA World Cup. The seven-time Ballon d’Or winner moved to Paris Saint-Germain in 2021 and announced in June 2023 he plans to join MLS’ Inter Miami club."""

bullet_points = generate_bullet_points(paragraph, max_words=7, num_sentences=5)

print(bullet_points)
for bullet in bullet_points:
    print(bullet,'\n')

print("-------------")

# key_points = extract_keyphrases(paragraph)
# print(key_points)
