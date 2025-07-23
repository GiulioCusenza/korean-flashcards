import streamlit as st
import pandas as pd
import random

# Load CSV
@st.cache_data
def load_data(csv_path):
    return pd.read_csv(csv_path)

st.title("Korean Flashcards")

# Custom CSS to center-justify text and buttons
st.markdown(
    """
    <style>
    .stMarkdown, .stButton>button {
        display: block;
        margin-left: auto;
        margin-right: auto;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

data = load_data("flashcards.csv")

categories = sorted(data['category'].unique())

def on_categories_change():
    if len(data) > 0:
        st.session_state.card_idx = min(st.session_state.card_idx, len(data) - 1)
        
selected_categories = st.sidebar.multiselect("Categories", categories, default=categories, on_change=on_categories_change)


if "All" not in selected_categories:
    data = data[data['category'].isin(selected_categories)]

if len(data) == 0:
    st.warning("No flashcards available for the selected categories.")
else:
    # Initialize session state
    if 'card_idx' not in st.session_state:
        st.session_state.card_idx = random.randint(0, len(data)-1)
    if 'show_clicked' not in st.session_state:
        st.session_state.show_clicked = False

    st.session_state.card_idx = min(st.session_state.card_idx, len(data) - 1)
    card = data.iloc[st.session_state.card_idx]

    st.markdown(f"*{card['category']}*")
    st.markdown(f"# {card['korean']}")
    st.markdown(f"### Ex.: {card['example']}")

    if st.session_state.show_clicked:
        st.markdown(f"## {card['english']}")
        st.markdown(f"### Ex.: {card['example_translation']}")

    def show_answer():
        st.session_state.show_clicked = True

    def next_card():
        st.session_state.card_idx = random.randint(0, len(data) - 1)
        st.session_state.show_clicked = False

    cols = st.columns(2)
    with cols[0]:
        st.button("Show", on_click=show_answer, disabled=st.session_state.show_clicked)
    with cols[1]:
        st.button("Next", on_click=next_card)
