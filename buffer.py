import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.express as px
import pandas as pd
import requests

# Initialize the Dash app
app = dash.Dash(__name__, server=False)

# Define the layout
app.layout = html.Div([
    html.H1("Stories Dashboard", style={'textAlign': 'center', 'fontFamily': 'Arial, sans-serif'}),

    html.Div([
        html.Div([
            html.Label("Select Filter Type:", style={'display': 'block'}),
            dcc.Dropdown(
                id='filter-type-dropdown',
                options=[
                    {'label': 'Assignee', 'value': 'assignee'},
                    {'label': 'Label', 'value': 'labels'},
                    {'label': 'Epic', 'value': 'epic'},
                    {'label': 'Sprint', 'value': 'sprint'}
                ],
                placeholder='Select a filter type',
                style={'width': '100%', 'height': '38px'}
            ),
        ], style={'display': 'inline-block', 'width': '49%', 'verticalAlign': 'top'}),

        html.Div([
            html.Label("Enter Filter Value:", style={'display': 'block'}),
            dcc.Input(
                id='filter-value-input', 
                type='text', 
                placeholder='Enter the value', 
                style={'width': '100%', 'height': '38px'}
            ),
        ], style={'display': 'inline-block', 'width': '49%', 'verticalAlign': 'top'})
    ], style={'marginBottom': '20px', 'width': '100%'}),

    html.Button('Get Stories', id='get-stories-button', className='btn btn-success', style={'marginBottom': '20px'}),

    dcc.Loading(
        id="loading",
        type="default",  # You can use 'circle', 'dot', or 'default'
        children=[
            html.Div([
                dcc.Graph(id='sprint-storypoints-bar'),
                dcc.Graph(id='assignee-storypoints-bar'),
                dcc.Graph(id='project-storypoints-pie')
            ])
        ],
        style={'marginTop': '20px'}
    )
])

# Callback to filter and display stories based on selected dropdown values
@app.callback(
    [Output('sprint-storypoints-bar', 'figure'),
     Output('assignee-storypoints-bar', 'figure'),
     Output('project-storypoints-pie', 'figure')],
    [Input('get-stories-button', 'n_clicks')],
    [State('filter-type-dropdown', 'value'),
     State('filter-value-input', 'value')]
)
def filter_stories(n_clicks, filter_type, filter_value):
    if n_clicks is None or not filter_type or not filter_value:
        return {}, {}, {}

    # Simulate a long processing time (e.g., fetching data from JIRA)
    import time
    time.sleep(2)  # Simulate a delay for demonstration purposes

    # Simulate fetching filtered data from JIRA or your database
    jira_url = 'YOUR_JIRA_URL'  # Replace with your JIRA instance URL

    # Construct JQL with selected filter
    jql_query = 'project = YOUR_PROJECT_KEY AND issuetype = Story AND sprint in openSprints()'
    
    if filter_type == 'epic':
        jql_query += f' AND "Epic Link" = "{filter_value}"'
    else:
        jql_query += f' AND {filter_type} = "{filter_value}"'

    # Make API request
    response = requests.get(f'{jira_url}/rest/api/2/search?jql={jql_query}&fields=summary,assignee,storyPoints,sprint', auth=('your_username', 'your_api_token'))
    
    # Handle the response (this is just a simulation)
    issues = response.json().get('issues', [])

    # Process the response data and create the figures
    df = pd.DataFrame(issues)  # Simplified for example

    # Create example figures
    sprint_storypoints_fig = px.bar(df, x='sprint', y='story_points', title='Sprint vs Story Points')
    assignee_storypoints_fig = px.bar(df, x='assignee', y='story_points', title='Assignee vs Story Points')
    project_storypoints_pie_fig = px.pie(df, names='project', values='story_points', title='Project vs Story Points')

    return sprint_storypoints_fig, assignee_storypoints_fig, project_storypoints_pie_fig

# Running the app
if __name__ == '__main__':
    app.run_server(debug=True)
