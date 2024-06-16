import streamlit as st
from common_container import menu
from data_analysis import cluster_df, song_df


menu()

for cluster_id, cluster_row in cluster_df.iterrows():

    with st.container(border=True):

        col1, col2, col3 = st.columns(3)

        with col1:
            st.title(cluster_id)

        with col2:
            show_eg_songs = song_df[song_df["cluster"] == cluster_id].iloc[:2]
            st.write(f"{show_eg_songs.iloc[0]['name']}({show_eg_songs.iloc[0]['artist']})",
                     f"{show_eg_songs.iloc[1]['name']}({show_eg_songs.iloc[1]['artist']})", "등등")

        with col3:
            summit_btn = st.button("To Songs", key=f"summit_btn_{cluster_id}")
            if summit_btn:
                st.session_state.cluster_id = cluster_id
                st.switch_page("pages/songs.py")

        st.write('#' + '#\t'.join(cluster_row["keyword"]))