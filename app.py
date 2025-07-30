import dash, dash_bootstrap_components as dbc
from layout import serve_layout
from callbacks import register_callbacks

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    title="S3 Explorer",
)

app.layout = serve_layout()
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True, port=8050)