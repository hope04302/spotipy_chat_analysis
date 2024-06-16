import streamlit as st
import pickle


def pickle2df(filename):
    with open(f"use_data/{filename}", "rb") as f:
        a = pickle.load(f)
    return a