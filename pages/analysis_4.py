import streamlit as st
from common_container import menu
from data_analysis import lda_result_df

menu()

st.code("""
from gensim.corpora import Dictionary

# ===============================
# 토픽 모델링 딕셔너리 생성, 단어와 인덱스를 연결하는 역할
# 텍스트를 DTM 행렬로 변환(DTM은 BoW의 조합)

# 참고: 해당 부분에 대신 Tf-idf 벡터화를 사용해도 무방함. (직접 해보지는 않음)
# ===============================
id2word = Dictionary(tokenized_text)

# ===============================
# 5개 이하는 제외(이유: 작업 시간이 줄어듬)
# ===============================
id2word.filter_extremes(no_below=5)
 
# ===============================
# 토픽 모델링에 사용할 말뭉치 생성
# 모든 텍스트를 (인덱스, 개수)의 모음 꼴로 변경
# ===============================
corpus = [id2word.doc2bow(text) for text in tokenized_text]
""")

st.code("""
from gensim.models.ldamodel import LdaModel
from gensim.models.coherencemodel import CoherenceModel

# ===============================
# 매개변수 개수 설정
# ===============================

RANDOM_STATE = 2020
UPDATE_EVERY = 1
CHUNKSIZE = 128     # 배치(batch)랑 비슷한 의미
PASSES = 10         # 에포크(epoch)랑 비슷한 의미
ALPHA = 'auto'

MIN_TOPIC = 2       # 최소 개수
MAX_TOPIC = 50      # 최대 개수
INTERVAL = 1

def topic_modeling(num_topics, per_word_topics=False):

    # per_word_topics - 각 word가 어떤 topic의 결합으로 나타내지는지를 계산할지 여부

    # ===============================
    # 토픽모델링(LDA): (쉽게 표현하자면) 문서들을 토픽의 선형조합으로 표현
    # ===============================

    lda_model = LdaModel(corpus=corpus, id2word=id2word, num_topics=num_topics,
                         random_state=RANDOM_STATE, 
                         update_every=UPDATE_EVERY, chunksize=CHUNKSIZE,
                         passes=PASSES, alpha=ALPHA, per_word_topics=per_word_topics)


    # ===============================
    # 설계한 모델을 계산: Perplexity & Coherence Score
    # ===============================

    perplexity = lda_model.log_perplexity(corpus)

    coherence_model = CoherenceModel(model=lda_model,texts=tokenized_text, dictionary=id2word, coherence='c_v')
    coherence = coherence_model.get_coherence()

    return {'lda_model': lda_model, 'perplexity': perplexity,
            'coherence_model': coherence_model, 'coherence': coherence}
""")

st.code("""from tqdm import tqdm

perplexity = []
coherence = []

for num_topics in tqdm(range(MIN_TOPIC, MAX_TOPIC + 1, INTERVAL), desc="LDA Analysis Running"):
    result = topic_modeling(num_topics)
    perplexity.append(result['perplexity'])
    coherence.append(result['coherence'])""")

col1, col2 = st.columns(2)
col1.line_chart(data=lda_result_df, y="perplexity")
col2.line_chart(data=lda_result_df, y="coherence")

st.code("""
NUM_TOPICS = 15
lda_result = topic_modeling(NUM_TOPICS, per_word_topics=True)
lda_model = lda_result['lda_model']
""")

st.code("""
NUM_TOPIC_WORDS = 20

for topic_id in range(NUM_TOPICS):

    topic_word_probs = lda_model.show_topic(topic_id, NUM_TOPIC_WORDS)
    print(f"Topic ID: {topic_id}")

    for topic_word, prob in topic_word_probs:
        print(f"\t{topic_word}\t{prob}")
    print()""")

st.code("""
COUNT = 10

for doc_num, doc in enumerate(corpus):

    topic_probs = lda_model[doc]
    print(f"Doc num: {doc_num}")

    for topic_id, prob in topic_probs:
        print(f"\t{topic_id}\t{prob}")

    print("\n")  

    if doc_num == COUNT - 1:                               
        break
""")

st.code("""

TERM = "남자"

word_id = id2word.token2id[TERM]
print(lda_model.get_term_topics(word_id))""")


st.code("""import pyLDAvis
import pyLDAvis.gensim_models

def create_vis(model):
    pyLDAvis.enable_notebook()
    vis = pyLDAvis.gensim_models.prepare(model, corpus, id2word, sort_topics=False)
    return vis

create_vis(lda_model)""")
