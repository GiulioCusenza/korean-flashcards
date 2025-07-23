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

csv_path = st.sidebar.text_input("CSV file path", "flashcards.csv")
data = load_data(csv_path)

categories = ["All"] + sorted(data['category'].unique())
selected_categories = st.sidebar.multiselect("Categories", categories, default=["All"])

if "All" not in selected_categories:
    data = data[data['category'].isin(selected_categories)]

if len(data) == 0:
    st.warning("No flashcards available for the selected categories.")
else:
    if 'card_idx' not in st.session_state:
        st.session_state.card_idx = random.randint(0, len(data)-1)
    if 'show_clicked' not in st.session_state:
        st.session_state.show_clicked = False

    card = data.iloc[st.session_state.card_idx]

    st.markdown(f"*{card['category']}*")
    st.markdown(f"# {card['korean']}")
    st.markdown(f"### Ex.: {card['example']}")

    with st.form(key='flashcard_form'):
        if not st.session_state.show_clicked:
            if st.form_submit_button("Show"):
                st.session_state.show_clicked = True
                st.experimental_rerun()
        else:
            st.markdown(f"## {card['english']}")
            st.markdown(f"### Ex.: {card['example_translation']}")

        if st.form_submit_button("Next"):
            st.session_state.card_idx = random.randint(0, len(data)-1)
            st.session_state.show_clicked = False
            st.experimental_rerun()
