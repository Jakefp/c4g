
import streamlit as st
import plotly.graph_objects as go
import numpy
import random
import pandas as pd
import plotly.express as px
import os

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
            athlete_row[categories[4]].values[0],
            athlete_row[categories[5]].values[0],
            athlete_row[categories[6]].values[0],
            athlete_row[categories[7]].values[0]
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
            athlete_row[categories[4]].values[0],
            athlete_row[categories[5]].values[0]
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

### Combining heights to a height matrix
def combined_heights(data):
    names = data['Name']
    heights = data['Height'].values
    height_matrix = heights[:, None] + heights  # Adds each height to every other height

    # Convert to DataFrame for Plotly compatibility
    height_sum_df = pd.DataFrame(height_matrix, index=names, columns=names)

    # Create a mask for the diagonal cells (same athlete)
    mask_df = pd.DataFrame(0, index=names, columns=names)
    for i in range(len(names)):
        mask_df.iloc[i, i] = 1  # Set the diagonal cells to 1 to indicate same athlete


    # Create the heatmap using Plotly Graph Objects for annotation support
    fig = go.Figure(data=go.Heatmap(
        z=height_sum_df.round(0).values,  # Round values to 0 decimal places
        x=names,
        y=names,
        colorscale=['red', 'white', 'green'],
        colorbar_title="Height Sum",
        text=height_sum_df.round(0).astype(int).values,  # Round values for text
        hoverinfo="z"
    ))

    # Add a layer to grey out the diagonal cells
    for i in range(len(names)):
        fig.add_shape(
            type="rect",
            x0=i - 0.5, x1=i + 0.5,
            y0=i - 0.5, y1=i + 0.5,
            fillcolor="grey",
            opacity=0.6,
            line=dict(width=0)
        )

    # Add annotations with rounded numbers
    for i in range(len(names)):
        for j in range(len(names)):
            if i != j:  # Only add annotations for non-diagonal cells
                fig.add_annotation(
                    text=str(int(height_sum_df.iloc[i, j])),
                    x=names[j],
                    y=names[i],
                    showarrow=False,
                    font=dict(color="black")
                )

    fig.update_layout(
        title="Combined Crew Heights",
        xaxis_title="Athlete",
        yaxis_title="Athlete",
        xaxis=dict(tickmode="array", tickvals=names),
        yaxis=dict(tickmode="array", tickvals=names),
    )

    # Display the heatmap in Streamlit
    st.plotly_chart(fig)

def team_lever_matrix(data):

    names = data['Name']
    moments = data['Moment'].values
    body_weights = data['Body Weight'].values

    # Calculate the team lever matrix using the provided formula
    lever_matrix = 1.45 + (moments[:, None] + moments) / (body_weights[:, None] + body_weights)

    # Convert to DataFrame for Plotly compatibility
    lever_df = pd.DataFrame(lever_matrix, index=names, columns=names)

    # Create a mask for the diagonal cells (same athlete)
    mask_df = pd.DataFrame(0, index=names, columns=names)
    for i in range(len(names)):
        mask_df.iloc[i, i] = 1  # Set the diagonal cells to 1 to indicate same athlete

    # Create the heatmap using Plotly Graph Objects for annotation support
    fig = go.Figure()

    # Main heatmap layer with the custom color scale
    fig.add_trace(go.Heatmap(
        z=lever_df.round(2).values,  # Rounded to 2 decimal places for display
        x=names,
        y=names,
        colorscale=['red', 'white', 'green'],
        colorbar_title="Team Lever Value",
        text=lever_df.round(2).astype(float).values,
        hoverinfo="z"
    ))

    # Add a layer to grey out the diagonal cells
    for i in range(len(names)):
        fig.add_shape(
            type="rect",
            x0=i - 0.5, x1=i + 0.5,
            y0=i - 0.5, y1=i + 0.5,
            fillcolor="grey",
            opacity=0.6,
            line=dict(width=0)
        )

    # Add annotations with rounded numbers
    for i in range(len(names)):
        for j in range(len(names)):
            if i != j:  # Only add annotations for non-diagonal cells
                fig.add_annotation(
                    text=f"{lever_df.iloc[i, j]:.2f}",  # Format to 2 decimal places
                    x=names[j],
                    y=names[i],
                    showarrow=False,
                    font=dict(color="black")
                )

    fig.update_layout(
        title="Team Lever Matrix",
        xaxis_title="Athlete",
        yaxis_title="Athlete",
        xaxis=dict(tickmode="array", tickvals=names),
        yaxis=dict(tickmode="array", tickvals=names),
    )

    # Display the heatmap in Streamlit
    st.plotly_chart(fig)

def specific_athlete(data, selected_athlete):
    # Filter the data for the selected athlete
    athlete_data = data[data["Name"] == selected_athlete]

    if athlete_data.empty:
        st.warning("Athlete not found in the data.")
        return

    # Path to the athlete's image
    image_path = f"athlete_profiles/{selected_athlete}.jpg"

    # Create two columns for layout
    col1, col2 = st.columns(2)

    # Display image if it exists
    with col1:
        if os.path.exists(image_path):
            st.image(image_path, caption=f"{selected_athlete}'s Profile Image")
        else:
            st.subheader("No image available for this athlete")
    
    # Display DOB information
    with col2:
        dob = athlete_data["DOB"].values[0] # Extract the DOB value
        Partner = athlete_data["Partner"].values[0]
        Boat = athlete_data["Boat"].values[0]
        Trainability_score = athlete_data["Trainability Score"].values[0]
        Fitness_rank = athlete_data["Fitness Rank"].values[0]
        Potential_score = athlete_data["Potential Score"].values[0]
        Potential_rank = athlete_data["Potential Rank"].values[0]
        Behaviour_score = athlete_data["Behaviour Score"].values[0]
        Behaviour_rank = athlete_data["Behaviour Rank"].values[0]

        st.write(f"DOB: {dob}"),
        st.write(f"Current Crew: {Partner}"),
        st.write(f"Boat Ownership: {Boat}"),
        st.write(f"Trainability: {Trainability_score}"),
        st.write(f"Fitness Rank: {Fitness_rank}"),
        st.write(f"Potential Score: {Potential_score}")
        st.write(f"Potential Rank: {Potential_rank}")
        st.write(f"Behaviour Score: {Behaviour_score}")
        st.write(f"Behaviour Rank: {Behaviour_rank}")

    # Who sails with
    # Boat Owner
    # Rankings
    # Profile Pic
    # Fitness Matrix