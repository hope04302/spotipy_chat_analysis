import streamlit as st
from common_container import menu
from data_analysis import song_df, cluster_df, k_means_result_df
import pandas as pd


st.set_page_config(layout="wide")
menu()

N_CLUSTER = len(cluster_df)


@st.experimental_fragment
def frag1():
    st.title("k-Means 기법을 통한 군집화 - n을 정하자")
    st.divider()
    st.write("elbow method와 실루엣 계수를 이용해 n을 정해보자")

    col1, col2 = st.columns(2)
    col1.line_chart(data=k_means_result_df, y="elbow_res")

    result = pd.DataFrame(list(k_means_result_df["sil_res"]), columns=["n_clusters", "silhouette_score"])
    pivot_km = pd.pivot_table(result, index="n_clusters", values="silhouette_score")
    col2.line_chart(data=pivot_km, y="silhouette_score")


@st.experimental_fragment
def frag2():
    st.title("k-Means 기법을 통한 군집화 - 각 군집을 확인해보자")
    st.divider()
    st.write("각 군집을 PCA하여 표현해보자")
    choice = st.multiselect(label="cluster", options=[str(i) for i in range(N_CLUSTER)])

    song_df_new = song_df.copy()
    song_df_new["cluster"] = song_df["cluster"].apply(str)
    st.scatter_chart(data=song_df_new[song_df_new["cluster"].isin(choice)], x="pca_x", y="pca_y", color="cluster", height=700)


frag1()
st.write(); st.write(); st.write()
frag2()
st.dataframe(cluster_df)
