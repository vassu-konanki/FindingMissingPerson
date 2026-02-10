import streamlit as st
from sqlmodel import create_engine

def get_engine():
    db_url = (
        f"postgresql+psycopg2://"
        f"{st.secrets['DB_USER']}:"
        f"{st.secrets['DB_PASSWORD']}@"
        f"{st.secrets['DB_HOST']}:"
        f"{st.secrets['DB_PORT']}/"
        f"{st.secrets['DB_NAME']}"
    )
    return create_engine(db_url, echo=False)