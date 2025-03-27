# https://cp321-a7-ewha.onrender.com/

import dash;

import pandas as pd;
import numpy as np;
import plotly.express as px;

from dash import dcc, html, Input, Output;

general_data = pd.read_csv("general_team_data.csv");
winner_runnerup_data = pd.read_csv("winner_runnerup_data.csv");

# Initialize the dash app
app = dash.Dash(__name__);
server = app.server;

app.layout = html.Div([

  html.H1("FIFA World Cup Dashboard", style={"textAlign": "center"}),

  # Create dropdown box
  html.Label("Select a Country:"),
  dcc.Dropdown(
    id="country-dropdown",
    # Adds an All option to the graph
    options=[{"label": "All", "value": "All"}] + [{"label": team, "value": team} for team in winner_runnerup_data["Winners"].unique()],
    value="All",
    clearable=False,
  ),

  # Output who the winner is
  html.Div(id="wins-output"),

  # Display the graph
  dcc.Graph(id="world-cup-map"),

  # To display winner and runner up
  html.Div(id="winner-runner-up-output"),

  # Slider to select World cup year
  dcc.Slider(
    id="year-slider",
    min=winner_runnerup_data["Year"].min(),
    max=winner_runnerup_data["Year"].max(),
    step=4, # The world cup is every 4 years
    marks={year: str(year) for year in winner_runnerup_data["Year"]},
    value=winner_runnerup_data["Year"].min(), # Start at min
  ),


]);

# Update labels when values are updated
@app.callback(
  [Output("wins-output","children"), Output("world-cup-map","figure")],
  Input("country-dropdown","value")
)
def onDropdownUpdated(selected_country):
  # For the wins output 

  # Graph update
  filtered_data = None;
  winner_output = "";
  if (selected_country == "All"):
    filtered_data = general_data;
  else:
    wins = general_data[general_data["Team"] == selected_country]["Winners"].values[0];
    filtered_data = general_data[general_data["Team"] == selected_country];
    winner_output = f"{selected_country} has won the World Cup {wins} amount of times";

  # Create choropleth graph figure
  fig = px.choropleth(
    filtered_data,
    color="Winners",
    locations="ISO Code",
    hover_name="Team",
    color_continuous_scale="Viridis",
    title="FIFA World Cup Winners by Country"
  )


  return winner_output, fig

# Update slider and winners
@app.callback(
  Output("winner-runner-up-output","children"),
  Input("year-slider","value")
)
def updateWinnerRunnerUp(selected_year):
  filtered_data = winner_runnerup_data[winner_runnerup_data["Year"] == selected_year];
  if (not filtered_data.empty):
    row = filtered_data.iloc[0];
    return f"{selected_year} Winner: {row['Winners']} | Runnerup: {row['Runner-up']}";
  else:
    return f"No data found in {selected_year}";

# Run the server  
if __name__ == "__main__":
  app.run(debug=False); # Debug should be false for it to work