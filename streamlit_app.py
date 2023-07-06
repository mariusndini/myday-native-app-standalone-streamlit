# Import python packages
import streamlit as st
from snowflake.snowpark.session import Session
from datetime import datetime, timedelta
import numpy as np
import altair as alt
import pandas as pd

st.set_page_config(layout="centered")


# CONNECT TO SNOWFLAKE  
conn_parameters = {
      "account": st.secrets["account"],
      "user": st.secrets["user"],
      "password": st.secrets["password"],
      "role": st.secrets["role"],
      "database": st.secrets["database"],
      "warehouse": st.secrets["warehouse"],
   }


session = Session.builder.configs(conn_parameters).create()



# ASK CHAT GPT A QUESTION
def ask_chatGPT(prompt):
    gpt_data = session.sql(f"""select CORE.GPT('{prompt}')""").to_pandas()
    output = str( gpt_data.iloc[0,0] ).replace("\\n", "\n")[1:-1]
    return f"""{output}""" 


# MAIN PAGE OF APPLICATION - ENTRY WAY
def main_page():
    st.sidebar.markdown("# Insights & Trends")

    st.sidebar.header("MyDay Health")
    pin = st.sidebar.text_input("User Pin", value='SNOW', key='pin')
    start_date =st.sidebar.date_input(key="start_date", label="Start Date", value=datetime.today() - timedelta(days=7))
    end_date = st.sidebar.date_input(key="end_date", label="End Date", value=datetime.today())

    st.header("Health Sense: Your Trends")

    agg = session.sql(f""" SELECT *
                        FROM HK.POP_AGG 
                        WHERE ID ='{pin}' 
                        and DATE between '{start_date}' and '{end_date}' 
                        order by DATE asc""").to_pandas()

    st.write(agg)

    

def goals_page():
    st.sidebar.markdown("# Your Goals")
    st.header("Your Goals")

    st.text_area("Generally Speaking, what are you looking to achieve?", value='', height=None, max_chars=150, key=None)

    option = st.selectbox('Do you have a Specific Weight Goal?', ('Gain Weight', 'Maintain Current Weight', 'Lose Weight'))

    st.text_area("Are there any specific modifications you'd like to make to your diet?", value='', height=None, max_chars=150, key=None)

    
# --------------------------------------------------------------- #
# -------------------  END GOALS   --------------------------- #
# --------------------------------------------------------------- #



def QA_page():
    st.sidebar.markdown("# Health Intelligence")
    st.header("Chat with our Health Intelligence")



# --------------------------------------------------------------- #
# -------------------  END Q & A  --------------------------- #
# --------------------------------------------------------------- #



page_names_to_funcs = {
    "Insights & Trends": main_page,
    "Your Goals": goals_page,
    "Health Intelligence": QA_page,
}


selected_page = st.sidebar.selectbox("", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()















