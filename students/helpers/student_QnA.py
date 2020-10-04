import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def qna_response(request):
    f = open('data.txt', 'r', errors='ignore')
    raw = f.read()

    nltk.download('punkt')
    nltk.download('wordnet')

    sent_tokens = nltk.sent_tokenize(raw)

    WNL = nltk.stem.WordNetLemmatizer()

    def LemTokens(tokens):
        return [WNL.lemmatize(token) for token in tokens]

    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

    def LemNormalize(text):
        return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

    LemNormalize(sent_tokens[0])

    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)

    # function to match input to the preprocessed sentences
    def response(user_response):
        robo_response = ''
        new = TfidfVec.transform([user_response])
        vals = cosine_similarity(new[0], tfidf)
        idx = vals.argsort()[0][-1]
        idx_2 = vals.argsort()[0][-2]
        idx_3 = vals.argsort()[0][-3]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-1]
        if req_tfidf == 0:
            robo_response = robo_response + "unable to find answer, please rephrase your question."
            return robo_response
        else:
            robo_response = robo_response + sent_tokens[idx] + sent_tokens[idx_2] + sent_tokens[idx_3]
            return robo_response

    return {'msg': response(request.data['user_request'])}
