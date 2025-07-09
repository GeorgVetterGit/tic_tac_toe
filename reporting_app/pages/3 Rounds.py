import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("Tic Tac Toe Tournament Report")

st.subheader("Rounds distribution")

# Init Turn diagrams
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.markdown("<h3 style='text-align: right;'>Random Agent</h3>", unsafe_allow_html=True)  
with col2:
    st.markdown("<h3 style='text-align: center;'>Random Agent</h3>", unsafe_allow_html=True)
    st.image('tic_tac_toe/results/RR_rounds.png')
with col3:
    st.markdown("<h3 style='text-align: center;'>Q-Learning Agent</h3>", unsafe_allow_html=True)
with col4:
    st.markdown("<h3 style='text-align: center;'>Minimax Agent</h3>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<h3 style='text-align: right;'>Q-Learning Agent</h3>", unsafe_allow_html=True)  
with col2:
    st.image('tic_tac_toe/results/QR_rounds.png')
with col3:
    st.image('tic_tac_toe/results/QQ_rounds.png')
with col4:
    st.text('')

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<h3 style='text-align: right;'>Minimax Agent</h3>", unsafe_allow_html=True)  
with col2:
    st.image('tic_tac_toe/results/RM_rounds.png')
with col3:
    st.image('tic_tac_toe/results/QM_rounds.png')
with col4:
    st.image('tic_tac_toe/results/MM_rounds.png')