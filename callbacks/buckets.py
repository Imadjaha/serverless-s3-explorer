from dash import Input, Output, State
from services import s3 as s3svc


def register(app):
    @app.callback(
        Output("bucket-dd", "options"),
        Input("bucket-dd", "id"),
        prevent_initial_call=False,
    )
    def fill_buckets(_):
        return [{"label": b["Name"], "value": b["Name"]} for b in s3svc.list_buckets()]

    @app.callback(
        Output("filter-store", "data"),
        Input("filter-btn", "n_clicks"),
        State("filter-text", "value"),
        prevent_initial_call=True,
    )
    def save_filter(_, txt):
        return (txt or "").strip().lower()
