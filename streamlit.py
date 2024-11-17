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

st.write('### Key:')
st.write('1 - Lacking')
st.write('2 - Theory')
st.write('3 - Practising')
st.write('4 - Confident')
st.write('5 - Strong')

st.write('NOTE: Karrie Clarke has not been reviewed by Walshy - this may skew the averages slightly.')
st.write('NOTE: Eve Kennedy has been left out of Fitness information, Monique has data from a previous Testing.')

st.write('## Racing Skills')
col1, col2 = st.columns(2)

with col1:
    create_radar_chart_class_racing(data)
with col2:
    racing_cols = ['Name', 'Racing Rank', 'Racing Score', 'Racing Knowledge',  'Driving the boat', 'Startline Skills', 'Prepare the boat for sailing', 'Tack quickly and smoothly', 'Non-dependent learner', 'Bearing away and hoisting', 'Gybe quickly and smoothly', 'Dropping and rounding the bottom mark']
    filtered_data = data[racing_cols]
    sorted_data = filtered_data.sort_values(by='Racing Rank')
    st.dataframe(sorted_data,hide_index=True)

st.write('## Behaviour')
col1, col2 = st.columns(2)

with col1:
    create_radar_chart_class_behaviour(data)
with col2:
    behaviour_cols = ['Name','Behaviour Rank',  'Behaviour Score', 'Decision making under pressure', 'Performing under pressure', 'Will to stretch and challenge themselves', 'Non-dependent learner', 'Commitment and consistency shown', 'Preparing and reviewing training']
    filtered_data = data[behaviour_cols]
    sorted_data = filtered_data.sort_values(by='Behaviour Rank')
    st.dataframe(sorted_data,hide_index=True)

st.write('## Fitness')
col1, col2 = st.columns(2)

with col1:
    create_bar_chart_class_fitness(data)
with col2:
    fitness_cols = ['Name', 'Age', 'Trainability Score', 'Leg Press', 'Bench Pull', '4min Watt Bike', 'Body Weight', 'Height']
    filtered_data = data[fitness_cols]
    sorted_data = filtered_data.sort_values(by='Trainability Score', ascending=False)
    st.dataframe(sorted_data,hide_index=True)



st.divider()


st.write('### Combined Heights')
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
