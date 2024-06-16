import streamlit as st
from konlpy.tag import Okt  # Komoran을 쓸 수도 있다.
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import requests


class YoonTokenizer:

    print("tokenizer ready")

    _url = "https://raw.githubusercontent.com/yoonkt200/FastCampusDataset/master/korean_stopwords.txt"
    _r = requests.get(_url, stream=True)
    kr_stopwords = _r.text.replace("\t", "\n").split('\n')

    en_stopwords = stopwords.words('english')

    okt = Okt()
    wlem = nltk.WordNetLemmatizer()

    print("complete ready")

    def __init__(self):
        self.kr_add = []
        self.en_add = []

    def set_stopwords(self, kr_add=(), en_add=()):
        self.kr_add = list(kr_add)
        self.en_add = list(en_add)

    def tokenize(self, sentence):

        kr_tokens = self.okt.pos(sentence)

        extracted_words = []
        for word, pos in kr_tokens:
            if pos == 'Noun' and word not in self.kr_stopwords + self.kr_add and len(word) > 1:
                extracted_words.append(word)
            elif pos == 'Alpha':
                extracted_words.append(word)

        extracted_sentence = ' '.join(extracted_words)

        en_tokens = pos_tag(word_tokenize(extracted_sentence.lower()))

        result = []
        for word, pos in en_tokens:
            if '가' <= word[0] <= '힣':
                result.append(word)
            elif pos[:2] == 'NN' and word not in self.en_stopwords + self.en_add and len(word) > 2:
                new_word = self.wlem.lemmatize(word)
                result.append(new_word)

        return result


if __name__ == '__main__':

    sentence = "이것은 테스트 the sentence입니다."

    tokenizer = YoonTokenizer()
    result = tokenizer.tokenize(sentence)
    print(result)
