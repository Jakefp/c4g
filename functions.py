
import streamlit as st
import plotly.graph_objects as go
import numpy
import random
import pandas as pd
import plotly.express as px

### First Character

def first_char(cell_value):
    try:
        return int(str(cell_value)[0])
    except ValueError:
        return 0  # Default value if conversion fails

### Wrapping titles on graphs
# def wrap_text(text, width):
#     return '\n'.join([text[i:i+width] for i in range(0, len(text), width)])


### Radar Chart - single athlete
def create_radar_chart(excel_data, athlete_name):

    athlete_row = excel_data[excel_data['Sailor being reviewed (Name or Bib number)'] == athlete_name]
    #I need to add in averaging for each sailor and then move onto putting the whole class on one graph

    categories = [
        'Sailor is fast in all conditions',
        'Sailor is\xa0a Mentally Robust Athlete',
        'Sailor is\xa0a Physically Robust Athlete',
        'Sailor is\xa0an excellent non-dependent decision maker',
        'Sailor\xa0can excel under the most extreme pressure'
    ]

    # Extract the scores for the selected categories
    values = [
        first_char(athlete_row[categories[0]].values[0]),
        first_char(athlete_row[categories[1]].values[0]),
        first_char(athlete_row[categories[2]].values[0]),
        first_char(athlete_row[categories[3]].values[0]),
        first_char(athlete_row[categories[4]].values[0])
    ]
 
    # Ensure the radar chart is circular by repeating the first value
    
    values += values[:1]
    categories += categories[:1]

    #wrapped_categories = [wrap_text(category, 20) for category in categories]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=athlete_name
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickvals=[1, 2, 3, 4, 5],
                ticktext=["1", "2", "3", "4", "5"]
            ),
        ),
        title=f"Performance Metrics: {athlete_name}",
        showlegend=False
    )

    st.plotly_chart(fig)

    return

### Radar Chart - class
def create_radar_chart_class_racing(data):

    athlete_names = data['Name'].unique()

    categories = [
        'Racing Knowledge',
        'Driving the boat',
        'Startline Skills',
        'Prepare the boat for sailing',
        'Tack quickly and smoothly',
        'Bearing away and hoisting',
        'Gybe quickly and smoothly',
        'Dropping and rounding the bottom mark'
    ]

    fig = go.Figure()
    for athlete_name in athlete_names:
        athlete_row = data[data['Name'] == athlete_name]

        # Extract the scores for the selected categories
        values = [
            athlete_row[categories[0]].values[0],
            athlete_row[categories[1]].values[0],
            athlete_row[categories[2]].values[0],
            athlete_row[categories[3]].values[0],
            athlete_row[categories[4]].values[0]
        ]
        
        # Ensure the radar chart is circular by repeating the first value
        values += values[:1]
        categories += categories[:1]

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=athlete_name
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickvals=[1, 2, 3, 4, 5],
                ticktext=["1", "2", "3", "4", "5"]
            ),
        ),
        # title="Potential Metrics",
        showlegend=True
    )

    st.plotly_chart(fig)

def create_radar_chart_class_behaviour(data):

    athlete_names = data['Name'].unique()

    categories = [
        'Decision making under pressure',
        'Performing under pressure',
        'Will to stretch and challenge themselves',
        'Non-dependent learner',
        'Commitment and consistency shown',
        'Preparing and reviewing training'
    ]

    fig = go.Figure()
    for athlete_name in athlete_names:
        athlete_row = data[data['Name'] == athlete_name]

        # Extract the scores for the selected categories
        values = [
            athlete_row[categories[0]].values[0],
            athlete_row[categories[1]].values[0],
            athlete_row[categories[2]].values[0],
            athlete_row[categories[3]].values[0],
            athlete_row[categories[4]].values[0]
        ]
        
        # Ensure the radar chart is circular by repeating the first value
        values += values[:1]
        categories += categories[:1]

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=athlete_name
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickvals=[1, 2, 3, 4, 5],
                ticktext=["1", "2", "3", "4", "5"]
            ),
        ),
        # title="Potential Metrics",
        showlegend=True
    )

    st.plotly_chart(fig)

### Bar Chart Performance for Class
def create_bar_chart_class_fitness(data):

    data = data.sort_values(by='Trainability Score', ascending=True)

    athlete_names = data['Name']
    cmj = data['CMJ']
    leg_press = data['Leg Press']
    bench_pull = data['Bench Pull']
    watt_bike = data['4min Watt Bike']
    trainability = data['Trainability Score'] 


    fig = go.Figure()

    # Add the first set of bars for the Indicator Result
    fig.add_trace(go.Bar(
        y=athlete_names,  # Y-axis will be the athlete names
        x=trainability,  # X-axis will be the indicator result
        name='Trainability Score',
        orientation='h',  # Horizontal bars
        marker=dict(color='dark blue')  # Color for the bars
    ))

    # Add the second set of bars for the 6 Month Result
    fig.add_trace(go.Bar(
        y=athlete_names,  # Y-axis will be the athlete names
        x=cmj,  # X-axis will be the six-month result
        name='CMJ',
        orientation='h',  # Horizontal bars
        marker=dict(color='light blue')  # Color for the bars
    ))
    fig.add_trace(go.Bar(
        y=athlete_names,  # Y-axis will be the athlete names
        x=leg_press,  # X-axis will be the six-month result
        name='Leg Press',
        orientation='h',  # Horizontal bars
        marker=dict(color='green')  # Color for the bars
    ))
    fig.add_trace(go.Bar(
        y=athlete_names,  # Y-axis will be the athlete names
        x=bench_pull,  # X-axis will be the six-month result
        name='Bench Pull',
        orientation='h',  # Horizontal bars
        marker=dict(color='red')  # Color for the bars
    ))
    fig.add_trace(go.Bar(
        y=athlete_names,  # Y-axis will be the athlete names
        x=watt_bike,  # X-axis will be the six-month result
        name='4min Watt Bike',
        orientation='h',  # Horizontal bars
        marker=dict(color='yellow')  # Color for the bars
    ))

    fig.update_layout(
        # barmode='stack',
        title="Athlete Physical Metrics",
        yaxis_title="Athletes",  # Swap x and y
        xaxis_title="Scores",  # Swap x and y
        xaxis=dict(showgrid=True, gridcolor='LightGray'),  # Enable x-axis grid lines
        yaxis=dict(showgrid=True, gridcolor='LightGray'),  # Enable y-axis grid lines
        # yaxis_autorange='reversed',
        showlegend=True
    )

    st.plotly_chart(fig)

def combined_heights(data):
    names = data['Name']
    heights = data['Height'].values
    height_matrix = heights[:, None] + heights  # Adds each height to every other height

    # Convert to DataFrame for Plotly compatibility
    height_sum_df = pd.DataFrame(height_matrix, index=names, columns=names)

    # Create the heatmap
    fig = px.imshow(height_sum_df, labels=dict(x="Athlete", y="Athlete", color="Height Sum"),
                    x=names, y=names, aspect="auto")
    
    fig.update_layout(title="Combined Crew Heights")
    # Display the heatmap in Streamlit
    st.plotly_chart(fig)
