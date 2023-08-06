import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
import joblib
import arabic_reshaper
from pyarabic.araby import strip_tatweel, strip_tashkeel


def classify(abstract):
    # clean input text
    stopwords = set(nltk.corpus.stopwords.words('english')) | set(nltk.corpus.stopwords.words('french')) | set(
        nltk.corpus.stopwords.words('arabic'))
    text = ' '.join([word for word in word_tokenize(abstract) if word.lower() not in stopwords])  # remove stop-words
    tokens = word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    tags = ['NN', 'NNP', 'NNS', 'NNPS', 'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ',
            'FW', 'CD']
    text = ' '.join([t[0] for t in tagged if t[1] in tags])
    text = arabic_reshaper.reshape(text)  # reshape arabic characters
    text = strip_tatweel(text)  # remove arabic diactrics
    text = strip_tashkeel(text)
    text = text.split('\n')
    text = ' '.join(text)  # replace line breaks by space
    # predict label by model
    model = joblib.load('doc_classifier.pkl')  # call the model
    label = model.predict([text])[0]  # predict
    return label