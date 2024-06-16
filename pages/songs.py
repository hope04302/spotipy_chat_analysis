import streamlit as st
from common_container import menu
from data_analysis import song_df, rank_df, cluster_df, lda_result_df

from jamo import h2j, j2hcj

menu()

cluster_id = st.session_state.get("cluster_id")
if cluster_id is None:
    st.switch_page("app.py")


def jamo_contains(haystack, needle):
    haystack_jamo = j2hcj(h2j(haystack))
    needle_jamo = j2hcj(h2j(needle))
    return needle_jamo in haystack_jamo


@st.cache_data
def search_songs_by(df, value, value_options, max_count=50):

    song_indices = []

    for idx, row in df.iterrows():
        if row[value_options].astype(str).apply(lambda x: jamo_contains(x, value)).any():
            song_indices.append(idx)
        if len(song_indices) >= max_count:
            return df.loc[song_indices]


with st.form(key=f"form_{cluster_id}"):

    search = st.text_input(label="search")

    targ_options = ['name', "album", "artist", "genre", "lyric_writer", "composer", "arranger", "lyrics"]
    targ = st.multiselect(label="found words in:", options=targ_options, default="name")

    search_btn = st.form_submit_button()
    # if search_btn:
    #     song_df_selected = search_songs_by(song_df, search, targ_options)

song_df_selected = search_songs_by(song_df, search, targ_options)

st.write(song_df_selected)