import os
import streamlit as st
import pandas as pd


st.set_page_config(layout="wide")

st.title("Tic Tac Toe Tournament Report")

# Load the data
try:
    df_1 = pd.read_csv('results/Q-Learning Agent_vs_Minimax Agent.txt', names=['Game Count', 'Rounds', 'Initial Turn', 'Winner Agent', 'Winner Letter', 'X_Move_Time', 'O_Move_Time'])
    df_2 = pd.read_csv('results/Q-Learning Agent_vs_Random Agent.txt', names=['Game Count', 'Rounds', 'Initial Turn', 'Winner Agent', 'Winner Letter', 'X_Move_Time', 'O_Move_Time'])
    df_3 = pd.read_csv('results/Random Agent_vs_Minimax Agent.txt', names=['Game Count', 'Rounds', 'Initial Turn', 'Winner Agent', 'Winner Letter', 'X_Move_Time', 'O_Move_Time'])
except FileNotFoundError:
    st.error(f"Results file not found. Please run main_tournament.py first. File List: {os.listdir()}")
    st.stop()

def prep_df(df):
    """Prepare the DataFrame by converting columns to appropriate data types."""
    df['Rounds'] = pd.to_numeric(df['Rounds'], errors='coerce')  # Convert 'Rounds' to numeric, handling errors
    df['X_Move_Time'] = pd.to_numeric(df['X_Move_Time'], errors='coerce')  # Convert 'Mean Time X' to numeric, handling errors
    df['O_Move_Time'] = pd.to_numeric(df['O_Move_Time'], errors='coerce')  # Convert 'Mean Time O' to numeric, handling errors
    return df

df_1 = prep_df(df_1)
df_2 = prep_df(df_2)
df_3 = prep_df(df_3)

st.header("Tournament Overview")
st.write(f"Total games played: {len(df_1)}")

st.subheader("Winner Distribution")
st.write("This section shows the distribution of wins among the agents in the tournament.")

st.header("Game Statistics")
st.write("This section provides a detailed overview of the game statistics, including the number of rounds played, the initial turn, and the winner of each game.")
df_concat = pd.concat([df_1, df_2, df_3], ignore_index=True)
st.dataframe(df_concat[['Game Count', 'Rounds', 'Initial Turn', 'Winner Agent', 'Winner Letter', 'X_Move_Time', 'O_Move_Time']], use_container_width=True)
