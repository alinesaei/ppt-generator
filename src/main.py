import nltk
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.feature_extraction.text import TfidfVectorizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.utils import get_stop_words
from gensim.summarization import summarize

def generate_bullet_points(paragraph, num_clusters=3, max_words=6):
    # Tokenize the paragraph into sentences
    sentences = nltk.sent_tokenize(paragraph)
    
    # Step 1: Use LexRank for extractive summarization
    summarizer = LexRankSummarizer()
    parser = PlaintextParser.from_string(paragraph, Tokenizer("english"))
    lexrank_summary = summarizer(parser.document, num_sentences=len(sentences))
    
    # Step 2: Perform sentence clustering
    vectorizer = TfidfVectorizer()
    sentence_vectors = vectorizer.fit_transform(lexrank_summary)
    
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(sentence_vectors)
    
    # Step 3: Generate bullet points from cluster representatives
    bullet_points = []
    for cluster_id in range(num_clusters):
        cluster_sentences = [sentence for idx, sentence in enumerate(lexrank_summary) if kmeans.labels_[idx] == cluster_id]
        
        if len(cluster_sentences) > 0:
            cluster_vector = vectorizer.transform(cluster_sentences)
            centroid = cluster_vector.mean(axis=0)
            closest_sentence_idx = pairwise_distances_argmin_min(centroid, cluster_vector)[0][0]
            closest_sentence = cluster_sentences[closest_sentence_idx]
            
            # Step 4: Apply sentence compression techniques
            compressed_sentence = summarize(closest_sentence, word_count=max_words)
            bullet_points.append(compressed_sentence)
    
    return bullet_points

# Example usage
paragraph = """At first glance, this change may look pointless: we just moved the constructor call from one part of the program to another. However, consider this: now you can override the factory method in a subclass and change the class of products being created by the method. There's a slight limitation though: subclasses may return different types of products only if these products have a common base class or interface. Also, the factory method in the base class should have its return type declared as this interface."""
bullet_points = generate_bullet_points(paragraph)
for bullet in bullet_points:
    print(bullet,'\n')

print("-------------")

# key_points = extract_keyphrases(paragraph)
# print(key_points)
