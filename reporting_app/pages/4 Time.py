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
    st.image('results/RR_time.png')
with col3:
    st.markdown("<h3 style='text-align: center;'>Q-Learning Agent</h3>", unsafe_allow_html=True)
with col4:
    st.markdown("<h3 style='text-align: center;'>Minimax Agent</h3>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<h3 style='text-align: right;'>Q-Learning Agent</h3>", unsafe_allow_html=True)  
with col2:
    st.image('results/QR_time.png')
with col3:
    st.image('results/QQ_time.png')
with col4:
    st.text('')

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<h3 style='text-align: right;'>Minimax Agent</h3>", unsafe_allow_html=True)  
with col2:
    st.image('results/RM_time.png')
with col3:
    st.image('results/QM_time.png')
with col4:
    st.image('results/MM_time.png')