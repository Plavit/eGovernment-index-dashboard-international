# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import pathlib

from dash.dependencies import Input, Output
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory, send_file

from generators import generate_table, generate_world_map, generate_europe_map

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Used dataset version names
DATA_UN = 'eGov-t5.csv'
DATA_EU = 'eur-t3.csv'

df = pd.read_csv('data/{}'.format(DATA_UN))
dfeu = pd.read_csv('data/{}'.format(DATA_EU))

filtered_df = pd.DataFrame(df[df.Year == df['Year'].max()], columns=['English name', 'UN eGov index'])
# Adding rank and percentile
filtered_df['Rank'] = filtered_df['UN eGov index'].rank(method='min', ascending=False)
filtered_df['Percentile'] = filtered_df['UN eGov index'].rank(pct=True)
filtered_df['Percentile'] = (filtered_df['Percentile'] * 100).round(1).astype(str) + '%'
filtered_df = filtered_df[['Rank', 'English name', 'UN eGov index', 'Percentile']]
filtered_df = filtered_df.rename(columns={'English name': 'Country', 'UN eGov index': 'UN index value'})

filtered_df_eu = pd.DataFrame(dfeu[dfeu.Year == dfeu['Year'].max()], columns=['English name', 'EU eGov index'])
# Adding rank and percentile
filtered_df_eu['Rank'] = filtered_df_eu['EU eGov index'].rank(method='min', ascending=False)
filtered_df_eu['Percentile'] = filtered_df_eu['EU eGov index'].rank(pct=True)
filtered_df_eu['Percentile'] = (filtered_df_eu['Percentile'] * 100).round(1).astype(str) + '%'
filtered_df_eu = filtered_df_eu[['Rank', 'English name', 'EU eGov index', 'Percentile']]
filtered_df_eu = filtered_df_eu.rename(columns={'English name': 'Country', 'EU eGov index': 'EU index value'})

# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__)


@server.route("/data/<path:path>")
def download(path):
    """Downloads the desired file from the data folder."""
    return send_file('data/' + path,
                     mimetype='text/csv',
                     attachment_filename=path,
                     as_attachment=True)


# Download link generation
def file_download_link(filename):
    """Creates a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/data/{}".format(urlquote(filename))
    return html.Div(
        [
            html.A(
                html.Button("Download the full dataset: " + filename),
                href=location,
            )
        ],
        className="download-button"
    )


app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)

server = app.server

app.layout = html.Div(
    children=[
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src='assets/Logo-text-en.png',
                            draggable='False',
                            id="logo",
                            height='auto',
                            width=220,
                        ),
                        html.Img(
                            src='assets/CJSP_logo.png',
                            draggable='False',
                            id="logo-CJSP",
                            height='auto',
                            width=160,
                        ),
                    ],
                    className="three columns",
                ),
                html.Div(
                    [
                        html.H3(
                            "eGovernment index dashboard",
                            style={"margin-bottom": "0px"},
                        ),
                        html.H5(
                            "A simple overview of UN and EU eGovernment benchmark indices",
                            style={"margin-top": "0px"}
                        ),
                        html.I(
                            [
                                "Created as part of a paper submission for the Cambridge Journal of Science and Policy "
                                "by Marek Szeles and Anshumaan Krishnan Ayyangar, expanding on ",
                                html.A(
                                    "previous work done by the former",
                                    href="https://github.com/Plavit/eGovernment-index-dashboard",
                                    target="_blank"
                                )
                            ],
                            style={"margin-top": "0px"}
                        ),

                    ],
                    className="eight columns",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Contact the authors", id="contact-button"),
                            href="mailto:marek.szeles@eforce.cvut.cz",
                        )
                    ],
                    className="three columns",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    children=[
                                        html.Img(
                                            src=
                                            "https://1000logos.net/wp-content/uploads/2018/01/united-nations-logo.png",
                                            draggable='False',
                                            id="logo_un",
                                            height=150,
                                            width='auto',
                                        ),
                                        html.Div(
                                            [
                                                html.H3(
                                                    "UN eGovernment index"
                                                ),
                                                html.P(
                                                    "The e-Government Development Index (EGDI) is being published by "
                                                    "the United Nations since 2001. It is a composite indicator "
                                                    "involving three components – Online Service Index(OSI), "
                                                    "Telecommunication Infrastructure Index (TII) "
                                                    "and Human Capital Index (HCI). The final index is calculated "
                                                    "using the following formula:"
                                                ),
                                                html.I("EGDI = ⅓ × (OSI+TII+HCI)"
                                                       ),
                                                html.H6(
                                                    "The three components of the index are defined like so: "
                                                ),
                                                html.Ul(
                                                    [
                                                        html.Li(
                                                            "OSI is the normalised score between 0 and 1, which"
                                                            " is equal to the difference of the "
                                                            "actual total score and the lowest total score divided by "
                                                            "the range of total score values for all countries. "
                                                        ),
                                                        html.Li(
                                                            [
                                                                "Each country’s TII is the arithmetic average of",
                                                                html.Ul(
                                                                    [
                                                                        html.Li(
                                                                            "Estimated internet users "
                                                                            "per 100 inhabitants;",
                                                                        ),
                                                                        html.Li(
                                                                            "Number of mobile subscribers "
                                                                            "per 100 inhabitants;"
                                                                        ),
                                                                        html.Li(
                                                                            "Active mobile broadband subscriptions"
                                                                            "per 100 inhabitants;"
                                                                        ),
                                                                        html.Li(
                                                                            "Number of fixed broadband subscriptions "
                                                                            "per 100 inhabitants"
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        ),
                                                        html.Li(
                                                            [
                                                                "Each country’s HCI is calculated using:",
                                                                html.Ul(
                                                                    [
                                                                        html.Li(
                                                                            "The adult literacy rate;",
                                                                        ),
                                                                        html.Li(
                                                                            "The combined primary, secondary and "
                                                                            "tertiary gross enrolment ratio;"
                                                                        ),
                                                                        html.Li(
                                                                            "Expected years of schooling;"
                                                                        ),
                                                                        html.Li(
                                                                            "Average years of schooling."
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                ),
                                                html.P(
                                                    [
                                                        "More information about the methodology can be found in ",
                                                        html.A(
                                                            "documents published directly by the UN",
                                                            href="https://www.un.org/development/desa/"
                                                                 "publications/publication/"
                                                                 "2020-united-nations-e-government-survey",
                                                            target="_blank",
                                                        ),
                                                        "."
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    id="un_description",
                                    className="pretty_container description twelve columns flex-display"
                                ),
                            ],
                            className="content_holder row twelve columns flex-display"
                        ),
                        html.Div(
                            [
                                html.Div(
                                    children=[
                                        html.Label(
                                            html.H6('Choose year for visualisation')
                                        ),
                                        dcc.Slider(
                                            id='year-slider',
                                            min=df['Year'].min(),
                                            max=df['Year'].max(),
                                            value=df['Year'].max(),
                                            marks={
                                                str(year): 'Year {}'.format(year) if year == df['Year'].min() else str(
                                                    year)
                                                for year
                                                in
                                                df['Year'].unique()},
                                            step=None,
                                            className='slider'
                                        ),

                                        dcc.Graph(id='world-map-with-slider',
                                                  figure=generate_world_map(df, df['Year'].max())),

                                    ],
                                    className="pretty_container ten columns",
                                ),

                                html.Div(
                                    [
                                        # html.Div(
                                        #     [
                                        #         html.Div(
                                        #             [html.H6(str(int(filtered_df.loc[filtered_df['Země'] == 'Česká republika']['Pořadí']))+". místo", id="un_rank_value"),
                                        #              html.P("Rank of Czechia", id="un_rank_text")],
                                        #             id="un_rank",
                                        #             className="mini_container",
                                        #         ),
                                        #         html.Div(
                                        #             [html.H6(str(np.round(float(filtered_df.loc[filtered_df['Země'] == 'Česká republika']['index eGov OSN']),3))+"", id="un_score_value"),
                                        #              html.P("Score of Czechia", id="un_score_text")],
                                        #             id="un_score",
                                        #             className="mini_container",
                                        #         ),
                                        #         html.Div(
                                        #             [html.H6(filtered_df.loc[filtered_df['Země'] == 'Česká republika']['Percentil']+"", id="un_percentile_value"),
                                        #              html.P("Percentile of Czechia", id="un_percentile_text")],
                                        #             id="un_percentile",
                                        #             className="mini_container",
                                        #         ),
                                        #     ],
                                        #     className="twelve flex-display",
                                        # ),
                                        html.Div(
                                            children=[
                                                html.H4(
                                                    id='top-un-title',
                                                    children='TOP 15 countries in ' + str(df['Year'].max())),
                                                html.Div(
                                                    id='top-un-table',
                                                    children=[
                                                        generate_table(filtered_df, 15)
                                                    ], style={'columnCount': 1}),
                                                html.Div(
                                                    children=[
                                                        file_download_link(DATA_UN)
                                                    ]
                                                )
                                            ],
                                            className="pretty_container",
                                        ),
                                    ],
                                    className="three columns right-column",
                                )
                            ],
                            className="content_holder row twelve columns flex-display"
                        ),
                    ],
                    className="pretty_container_bg twelve columns",
                ),
            ],
            className="row flex-display",
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    children=[
                                        html.Img(
                                            src="https://ec.europa.eu/info/sites/info/themes/europa/images/svg/logo/"
                                                "logo--en.svg",
                                            draggable='False',
                                            id="logo_eu",
                                            height='auto',
                                            width=300,
                                        ),
                                        html.Div(
                                            [
                                                html.H3("EU eGovernment index"),
                                                html.P(
                                                    "The e-Government Benchmark is being published by "
                                                    "the European Union. It is based on a quantitative analysis "
                                                    "of a set of eight so-called life events. Each life event "
                                                    "consists of a user journey representing common public services "
                                                    "that citizens or businesses will go through. Half of the index "
                                                    "consisting of four life events is measured each year, "
                                                    "with the life events alternating as seen in the following table."
                                                    "The final "
                                                    "index value for each country is calculated as a simple average "
                                                    "value of the two latest surveys."
                                                ),
                                                html.Table(
                                                    [

                                                        html.Tr(
                                                            [
                                                                html.Th(
                                                                    ""
                                                                ),
                                                                html.Th(
                                                                    [
                                                                        html.P(
                                                                            "Years"
                                                                        ),
                                                                        html.P(
                                                                            "2012, 2014, 2016, 2018"
                                                                        ),
                                                                    ]
                                                                ),
                                                                html.Th(
                                                                    [
                                                                        html.P(
                                                                            "Years"
                                                                        ),
                                                                        html.P(
                                                                            "2013, 2015, 2017, 2019"
                                                                        ),
                                                                    ]
                                                                )
                                                            ]
                                                        ),
                                                        html.Tr(
                                                            [
                                                                html.Td(
                                                                    html.B(
                                                                        [
                                                                            "Events in",
                                                                            html.Br(),
                                                                            "industry"
                                                                        ]
                                                                    )
                                                                ),
                                                                html.Td(
                                                                    "Business start-up"
                                                                ),
                                                                html.Td(
                                                                    "Regular business operations"
                                                                )
                                                            ]
                                                        ),
                                                        html.Tr(
                                                            [
                                                                html.Td(
                                                                    html.B(
                                                                        [
                                                                            "Events for",
                                                                            html.Br(),
                                                                            "citizens"
                                                                        ]
                                                                    )
                                                                ),
                                                                html.Td(
                                                                    [
                                                                        "Losing and finding a job",
                                                                        html.Br(),
                                                                        "Studying",
                                                                        html.Br(),
                                                                        "Family life (since 2016)"
                                                                    ]
                                                                ),
                                                                html.Td(
                                                                    [
                                                                        "Starting a small claims procedure ",
                                                                        html.Br(),
                                                                        "Moving to a different place",
                                                                        html.Br(),
                                                                        "Ownership and maintenance of a vehicle"
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                ),
                                                html.P(
                                                    "Furthermore, there are other indicators that are also measured "
                                                    "in the publications, such as the online availability of general "
                                                    "public services. These metrics are omitted from this dashboard "
                                                    "for simplicity as they are not directly comparable with the UN "
                                                    "benchmark. "
                                                ),
                                                html.P(
                                                    [
                                                        "More information about the methodology can be found in ",
                                                        html.A(
                                                            "documents published directly by the EU",
                                                            href="https://digital-strategy.ec.europa.eu/en/library/"
                                                                 "egovernment-benchmark-2020-egovernment-works-people",
                                                            target="_blank",
                                                        ),
                                                        "."
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                    id="eu_description",
                                    className="pretty_container description twelve columns flex-display"
                                ),
                            ],
                            className="content_holder row twelve columns flex-display"
                        ),
                        html.Div(
                            [
                                html.Div(
                                    children=[
                                        html.Label(
                                            html.H6('Choose year for visualisation')
                                        ),
                                        dcc.Slider(
                                            id='year-slider-2',
                                            min=dfeu['Year'].min(),
                                            max=dfeu['Year'].max(),
                                            value=dfeu['Year'].max(),
                                            marks={
                                                str(year): 'Year {}'.format(year) if year == df['Year'].min() else str(
                                                    year) for year in
                                                dfeu['Year'].unique()},
                                            step=None,
                                            className='slider'
                                        ),

                                        dcc.Graph(id='europe-map-with-slider',
                                                  figure=generate_europe_map(dfeu, dfeu['Year'].max(), )),

                                    ],
                                    className="pretty_container ten columns",
                                ),
                                html.Div(
                                    [
                                        # html.Div(
                                        #     [
                                        #         html.Div(
                                        #             [html.H6(str(int(filtered_df_eu.loc[filtered_df_eu['Země'] == 'Česká republika']['Pořadí']))+". místo", id="eu_rank_value"),
                                        #              html.P("Rank of Czechia", id="eu_rank_text")],
                                        #             id="eu_rank",
                                        #             className="mini_container",
                                        #         ),
                                        #         html.Div(
                                        #             [html.H6(str(np.round(float(filtered_df_eu.loc[filtered_df_eu['Země'] == 'Česká republika']['index eGov EU']),2)), id="eu_score_value"),
                                        #              html.P("Score of Czechia", id="eu_score_text")],
                                        #             id="eu_score",
                                        #             className="mini_container",
                                        #         ),
                                        #         html.Div(
                                        #             [html.H6(filtered_df_eu.loc[filtered_df_eu['Země'] == 'Česká republika']['Percentil']+"", id="eu_percentile_value"),
                                        #              html.P("Percentile of Czechia", id="eu_percentile_text")],
                                        #             id="eu_percentile",
                                        #             className="mini_container",
                                        #         ),
                                        #     ],
                                        #     className="twelve flex-display",
                                        # ),
                                        html.Div(
                                            children=[
                                                html.H4(
                                                    id='top-eu-title',
                                                    children='TOP 15 countries in ' + str(dfeu['Year'].max())),
                                                html.Div(
                                                    id='top-eu-table',
                                                    children=[
                                                        generate_table(filtered_df, 15)
                                                    ], style={'columnCount': 1}),
                                                html.Div(
                                                    children=[
                                                        file_download_link(DATA_EU)
                                                    ]
                                                )
                                            ],
                                            className="pretty_container",
                                        ),
                                    ],
                                    className="three columns right-column",
                                ),
                            ],
                            className="content_holder row twelve columns flex-display"
                        ),
                    ],
                    className="pretty_container_bg twelve columns",
                ),
            ],
            className="row flex-display",
        ),

    ],
    id="mainContainer",
    style={'columnCount': 1, "display": "flex", "flex-direction": "column"},
)

app.title = 'eGovernment benchmark'


@app.callback(
    [Output('world-map-with-slider', 'figure'),
     Output('top-un-title', 'children'),
     Output('top-un-table', 'children')
     # Output('un_rank_value', 'children'),
     # Output('un_score_value', 'children'),
     # Output('un_percentile_value', 'children')
     ],
    [Input('year-slider', 'value')])
def update_world_map(selected_year):
    filtered_df_update = pd.DataFrame(df[df.Year == selected_year], columns=['English name', 'UN eGov index'])
    filtered_df_update['Rank'] = filtered_df_update['UN eGov index'].rank(method='min', ascending=False)
    filtered_df_update['Percentile'] = filtered_df_update['UN eGov index'].rank(pct=True)
    filtered_df_update['Percentile'] = (filtered_df_update['Percentile'] * 100).round(1).astype(str) + '%'
    filtered_df_update = filtered_df_update[['Rank', 'English name', 'UN eGov index', 'Percentile']]
    filtered_df_update = filtered_df_update.rename(
        columns={'English name': 'Country', 'UN eGov index': 'UN index value'})
    filtered_df_update = filtered_df_update.sort_values('UN index value', ascending=False)
    return generate_world_map(df, selected_year), \
           'TOP 15 countries in ' + str(selected_year), \
           generate_table(filtered_df_update, 15), \
        # str(int(filtered_df.loc[filtered_df['Země'] == 'Česká republika']['Pořadí']))+". místo", \
    # str(np.round(float(filtered_df.loc[filtered_df['Země'] == 'Česká republika']['index eGov OSN']),3))+"", \
    # filtered_df.loc[filtered_df['Země'] == 'Česká republika']['Percentil']


@app.callback(
    [Output('europe-map-with-slider', 'figure'),
     Output('top-eu-title', 'children'),
     Output('top-eu-table', 'children')
     # Output('eu_rank_value', 'children'),
     # Output('eu_score_value', 'children'),
     # Output('eu_percentile_value', 'children')
     ],
    [Input('year-slider-2', 'value')])
def update_europe_map(selected_year):
    filtered_df_eu_update = pd.DataFrame(dfeu[dfeu.Year == selected_year], columns=['English name', 'EU eGov index'])
    filtered_df_eu_update['Rank'] = filtered_df_eu_update['EU eGov index'].rank(method='min', ascending=False)
    filtered_df_eu_update['Percentile'] = filtered_df_eu_update['EU eGov index'].rank(pct=True)
    filtered_df_eu_update['Percentile'] = (filtered_df_eu_update['Percentile'] * 100).round(1).astype(str) + '%'
    filtered_df_eu_update = filtered_df_eu_update[['Rank', 'English name', 'EU eGov index', 'Percentile']]
    filtered_df_eu_update = filtered_df_eu_update.rename(
        columns={'English name': 'Country', 'EU eGov index': 'EU index value'})
    filtered_df_eu_update = filtered_df_eu_update.sort_values('EU index value', ascending=False)
    return generate_europe_map(dfeu, selected_year), \
           'TOP 15 countries in ' + str(selected_year), \
           generate_table(filtered_df_eu_update, 15), \
        # str(int(filtered_df_eu.loc[filtered_df_eu['Země'] == 'Česká republika']['Pořadí'])) + ". místo", \
    # str(np.round(float(filtered_df_eu.loc[filtered_df_eu['Země'] == 'Česká republika']['index eGov EU']), 2)), \
    # filtered_df_eu.loc[filtered_df_eu['Země'] == 'Česká republika']['Percentil']


if __name__ == '__main__':
    app.run_server(debug=True)
