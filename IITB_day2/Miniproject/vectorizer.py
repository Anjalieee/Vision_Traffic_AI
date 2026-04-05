from sklearn.feature_extraction.text import TfidfVectorizer

def vectorize_texts(texts):
    vectorizer = TfidfVectorizer(
        max_features=3000,
        stop_words="english"
    )
    X = vectorizer.fit_transform(texts)
    return X, vectorizer
