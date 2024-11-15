import streamlit as st
import pandas as pd
import openpyxl
import plotly.graph_objects as go
from functions import *
import hmac
import os

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False
    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True
    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False
if not check_password():
    st.stop()  # Do not continue if check_password is not True.


# ##### Main

st.set_page_config(layout="wide")
####################################

st.image("bst_img.png", width=300)
st.title('Crew 4 Gold 2024 Selections')

st.write("Here you can analyse the performance and potential of the Crew 4 Gold athletes. All graphs are interactive and can go full screen if you are having difficulty with formatting.")

data = pd.read_excel('master_c4g_24.xlsx', engine='openpyxl', sheet_name='overall')

st.write('## Racing Skills')
create_radar_chart_class_racing(data)

st.write('## Behaviour')
create_radar_chart_class_behaviour(data)

st.write('## Fitness')
create_bar_chart_class_fitness(data)

st.divider()


st.write('### Combined heights')
combined_heights_matrix_2(data)

st.write('### Combined Team Lever')
team_lever_matrix_2(data)

st.divider()

st.write(f'## Specific Athlete Deep Dive' )
selected_athlete = st.selectbox("Select Athlete", data["Name"])

specific_athlete(data, selected_athlete)
# st.header("Athlete profiles currently being generated")




# st.image(f"{selected_class}/{selected_athlete}.png")
# st.write("Values and Behaviours Breakdown")
# st.image(f"{selected_class}/{selected_athlete}VB.png")
# st.write("Brilliant Racer Breakdown")
# st.image(f"{selected_class}/{selected_athlete}BR.png")


st.write("Data visuals: Jake Farren-Price")
