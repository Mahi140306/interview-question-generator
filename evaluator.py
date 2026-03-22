from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def evaluate_answer(question, answer):
    if not answer.strip():
        return 0

    corpus = [question, answer]

    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(corpus)

    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

    # Normalize score
    score = round(similarity * 100, 2)

    return score