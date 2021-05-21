import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as HTML
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = pd.read_csv("Gender_Data.csv")
df = pd.read_csv("National_Total_Deaths_by_Age_Group (1).csv")


#genererar mockup data


int_male = df["Total_ICU_Admissions"][0]
int_female = df["Total_ICU_Admissions"][1]
död_male = df["Total_Deaths"] [0]
död_female = df["Total_Deaths"][1]


antal_döda = df["Total_Deaths"].sum()
antal_intens = df["Total_ICU_Admissions"].sum()

series1 = [3, 5, 4, 8]
series2 = [5, 4, 8, 3]

fall = df["Total_ICU_Admissions"]
död_fall = df["Total_Deaths"]


#skapa fig
df = pd.DataFrame([
    ['Men', död_male , int_male],
    ['Kvinna', död_female, int_female],
], columns=["kön", "intensivvård", "dödfall"])
fig = px.bar(df, x="kön", y=["intensivvård", "dödfall"], color_discrete_sequence=px.colors.sequential.RdBu, barmode='group', title="Antal covid-19 döda respectiv internsivvårda beroende på kön")

labels = "Deaths", "ICU-admissions"
sizes = [antal_döda, antal_intens]
colors = ["lightcoral", "yellowgreen"]
fig = px.pie(values=sizes, names=labels, color_discrete_sequence=px.colors.sequential.RdBu, title="Antal covid-19 döda samt intesivvårda")

fig = px.line(x=[0,10,20,30,40,50,60,70,80,90], y=[fall, död_fall], color_discrete_sequence=px.colors.sequential.RdBu)
fig.update_layout(
    title="Antal döda och intensivvårda",
    xaxis_title = "Ålder",
    yaxis_title="Fall"
)

#utseendet
app.layout = HTML.Div(children=[
    HTML.H1(children = "Statisk över covid-19"),
    dcc.Dropdown(
        id = "drop",
        options = [dict(label = "Antal covid-19 döda respectiv internsivvårda beroende på kön", value="Antal covid-19 döda respectiv internsivvårda beroende på kön"), dict(label="Antal covid-19 döda samt intesivvårda", value="Antal covid-19 döda samt intesivvårda"),
        dict(label="Antal döda och intensivvårda", value="Antal döda och intensivvårda")],
        value="Antal covid-19 döda respectiv internsivvårda beroende på kön"
    ),

    dcc.Graph(
        id = "graph",
        figure = fig
    )
])

@app.callback(
    Output('dropdown', 'options'),
    [Input('button', 'n_clicks')],
    [State('dropdown', 'options')])
def update_options(n_clicks, existing_options):
    option_name = 'Option {}'.format(n_clicks)
    existing_options.append({'label': option_name, 'value': option_name})
    return existing_options


def update_figure(value):
    fig = px.bar(df, y="Närvaro", title=f"Närvarograd för klass {value}")
    fig.update_layout(transition_duration=500)
    return fig

if name == "main":
    app.run_server(debug = True)