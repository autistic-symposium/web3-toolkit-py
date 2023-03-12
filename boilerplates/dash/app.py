# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import os
import dash
import plotly

import pandas as pd
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


# -----------------------------
# ------ Instantiate app ------ 
# -----------------------------
app = dash.Dash(__name__)


# -------------------------------
# ---- Start app HTML layout ----
# -------------------------------

app.layout = html.Div(children=[

    # Main Title
    html.Div([
            html.H1(s.title_h1, 
                style=s.style_title_h1
            )
        ],
    ),

    # Tabs
    dcc.Tabs([

        dcc.Tab(label='tab1', children=[
            html.Div([
                html.H2('title 1', 
                        style=s.style_title_h2
                    )
                ],
            ),
        ]),

        dcc.Tab(label='tab2', children=[
            html.Div([
            html.H2('tab 2', 
                style=s.style_title_h2
                    )
                ],
            ),
        ]),
],  style=s.style_all)


# ---------------------------------
# ----- App Callback methods ------
# ---------------------------------



# ---------------------------------
# ----------- Run web app ---------
# ---------------------------------
if __name__ == '__main__':
    app.scripts.config.serve_locally = True
    app.css.config.serve_locally = True
    app.run_server(debug=True, port=se.PORT)
