from dash import html, dcc
import dash_bootstrap_components as dbc


def serve_layout():
    return dbc.Container(
        fluid=True,
        children=[
            dbc.NavbarSimple(
                brand=[
                    html.I(className="bi bi-cloud me-2 fs-3 text-light"),
                    "S3 Explorer",
                ],
                color="primary",
                dark=True,
                className="mb-4 shadow-sm",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Bucket"),
                                dcc.Dropdown(
                                    id="bucket-dd",
                                    placeholder="Select a bucket…",
                                    style={"flex": 1},
                                ),
                            ],
                            className="shadow-sm",
                        ),
                        xs=12,
                        md=6,
                        className="mb-2",
                    ),
                    dbc.Col(
                        dbc.InputGroup(
                            [
                                dbc.Input(id="filter-text", placeholder="keyword…"),
                                dbc.Button(
                                    "Filter", id="filter-btn", color="secondary"
                                ),
                            ],
                            className="shadow-sm",
                        ),
                        xs=12,
                        md=6,
                        className="mb-2",
                    ),
                ],
                className="g-3",
            ),
            dcc.Store(id="filter-store", data=""),
            html.Hr(),
            html.Div(id="directory-view"),
        ],
    )
