from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_best_match(question_text, documents):
    """
    question_text: string
    documents: list of document strings
    """

    corpus = [question_text] + documents

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)

    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

    best_index = int(similarity_scores.argmax())
    best_score = similarity_scores[0][best_index]

    return best_index, best_score
