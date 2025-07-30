from dash import Input, Output, State, MATCH
from utils.tree import render_listing


def register(app):
    @app.callback(
        Output("directory-view", "children"),
        Input("bucket-dd", "value"),
        Input("filter-store", "data"),
    )
    def root_view(bucket, flt):
        return (
            render_listing(f"s3://{bucket}/", flt, auto_expand=bool(flt))
            if bucket
            else ""
        )

    @app.callback(
        Output({"type": "content", "idx": MATCH}, "children"),
        Input({"type": "toggle", "idx": MATCH}, "n_clicks"),
        State({"type": "toggle", "idx": MATCH}, "id"),
        State("filter-store", "data"),
        prevent_initial_call=True,
    )
    def expand(n, btn_id, flt):
        return (
            render_listing(btn_id["idx"], flt, auto_expand=True) if n and n % 2 else ""
        )
