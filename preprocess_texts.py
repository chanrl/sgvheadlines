import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer

stemmer = SnowballStemmer("english")

def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
    '''
    Tokenize and lemmatize text for LDA model
    '''
    result=[]
    for token in gensim.utils.simple_preprocess(text) :
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 2:
            result.append(lemmatize_stemming(token))
    return result

def preprocess_docs(documents):
    '''
    Preprocess corpus for LDA model
    '''
    preprocessed_docs = []
    for doc in documents:
        preprocessed_docs.append(preprocess(doc))
    return preprocessed_docs