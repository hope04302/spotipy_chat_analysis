import streamlit as st
import nltk
import jpype

def initialize():

    #st.set_page_config(layout="wide")
    if not jpype.isJVMStarted():
        jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=your_classpath", "-Xms1g", "-Xmx2g")

    if st.session_state.get("initialize") is None:
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('stopwords')

        st.session_state["initialized"] = True


def menu():

    st.sidebar.page_link("app.py", label="Home", icon=":material/home:")
    st.sidebar.page_link("pages/analysis_1.py", label="#1. Introduction", icon=":material/info:")
    st.sidebar.page_link("pages/analysis_2.py", label="#2. Dataset Analysis", icon=":material/info:")
    st.sidebar.page_link("pages/analysis_3.py", label="#3. Text Tokenization", icon=":material/info:")
    st.sidebar.page_link("pages/analysis_4.py", label="#4. Topic Modeling: LDA", icon=":material/info:")
    st.sidebar.page_link("pages/analysis_5.py", label="#5. K-Means Clustering", icon=":material/info:")
    # st.sidebar.page_link("pages/analysis_6.py", label="#6. New Project", icon=":material/info:")
    st.sidebar.page_link("pages/clusters.py", label="Webapp Example", icon=":material/database:")