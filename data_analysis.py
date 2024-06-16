import pandas as pd
import streamlit as st
import pickle
import gdown
import os


def pickle2var(filename):
    with open(f"data/{filename}", "rb") as f:
        a = pickle.load(f)
    return a


# your_df
your_df = pickle2var("your_dict.pickle")

# song_df
_song_df = pickle2var("song_df.pickle")
song_df = _song_df.set_index("song_id")

# song_df 중 기본 행들
BASIC_COL = ['name', "album", "year", "month", "day", "artist", "genre", "lyric_writer", "composer", "arranger",
             "lyrics_row", "lyrics"]

# rank_df
rank_df = pickle2var("rank_df.pickle")

# other_data
_other_data = pickle2var("other_data.pickle")
cluster_df = pd.DataFrame({"cluster_id": range(len(_other_data["cluster_centers"])),
                           "cluster_center": [i for i in _other_data["cluster_centers"]],
                           "keyword": _other_data["keyword_list"]})
k_means_result_df = pd.DataFrame(data={"elbow_res": _other_data["elbow_res"],
                                       "sil_res": _other_data["sil_res"]},
                                 index=range(2, len(_other_data["elbow_res"]) + 2))


# lda_result_df
if os.path.isfile("data/lda_result.pickle"):
    lda_result_dict = pickle2var("lda_result.pickle")

else:
    _google_path = 'https://drive.google.com/uc?id='
    _file_id = '1VCsZYH1MI-melbNd9kGKK-GN4SfNdNy8'
    _output_name = 'data/lda_result.pickle'
    gdown.download(_google_path + _file_id, _output_name, quiet=False)

    lda_result_dict = pickle2var("lda_result.pickle")

lda_result_df = pd.DataFrame(lda_result_dict.values(), index=lda_result_dict.keys())
