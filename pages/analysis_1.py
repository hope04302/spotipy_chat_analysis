import streamlit as st
from common_container import menu

menu()

st.write("# 노래 가사 군집화를 하게 된 이유")
st.divider()
st.write("""
어떤 주제로 군집화를 하고 싶었는데, 마침 노래 가사를 군집화하면 좋겠다는 생각이 들었다.
그래서 이 주제를 골랐다.
""")

st.write(" "); st.write(" "); st.write(" ")

st.write("# 노래 가사 군집화의 목적")
st.divider()
st.write("""
노래 가사 간의 유사성과 여러 군집의 키워드를 통해 노래 가사만의 특성이 무엇인지를 파악할 수 있다.

노래 가사만을 통해 별도의 수작업 없이 주제별로 분류함으로써 특정 주제를 원하는 사람들이 해당 노래에 쉽게 접근가능하도록 유도할 수 있다.

노래 가사를 넘어 시, 문학 등을 주제별로 분류하는 것으로 확장할 수 있다.
""")

st.write(" "); st.write(" "); st.write(" ")

st.write("# 노래 가사 군집화의 단계")
st.divider()
st.write("""
1. 데이터셋 분석

2. 텍스트 토큰화

3. 토픽 모델링

4. k-평균 클러스터링

5. 관련 응용 문제 헤결
""")
