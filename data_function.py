import streamlit as st
from konlpy.tag import Okt  # Komoran을 쓸 수도 있다.
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import requests

# nltk 설치할 거 받기
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# 한국어 불용어 사전
url = "https://raw.githubusercontent.com/yoonkt200/FastCampusDataset/master/korean_stopwords.txt"
r = requests.get(url, stream=True)
kr_stopwords = r.text.replace("\\t", "\\n").split('\\n')

# 영어 불용어 사전
en_stopwords = stopwords.words('english')

# 한국어 토크나이저
okt = Okt()

# 영어 토크나이저는 word_tokenize를 씀
# 영어 단어 변형 툴(복수 -> 단수 등은 word_tokenize에서 지원 안하기에 추가 모델 필요)
wlem = nltk.WordNetLemmatizer()


def tokenize(sentence, kr_add=[], en_add=[]):
    kr_tokens = okt.pos(sentence)

    extracted_words = []
    for word, pos in kr_tokens:
        if pos == 'Noun' and word not in kr_stopwords + kr_add and len(word) > 1:
            extracted_words.append(word)
        elif pos == 'Alpha':
            extracted_words.append(word)

    extracted_sentence = ' '.join(extracted_words)

    en_tokens = pos_tag(word_tokenize(extracted_sentence.lower()))

    result = []
    for word, pos in en_tokens:
        if '가' <= word[0] <= '힣':
            result.append(word)
        elif pos[:2] == 'NN' and word not in en_stopwords + en_add and len(word) > 2:
            new_word = wlem.lemmatize(word)
            result.append(new_word)

    return result


if __name__ == '__main__':
    sentence = "이것은 테스트 the sentence입니다."
    result = tokenize(sentence)
    print(result)