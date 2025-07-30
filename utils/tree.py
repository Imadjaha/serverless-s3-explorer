import os
import base64
import dash_bootstrap_components as dbc
from dash import dcc, html
from services import s3 as s3svc
from utils.format import icon, human_bytes, highlight


def split_s3(path: str):
    p = path[5:].split("/", 1)
    return p[0], p[1] if len(p) > 1 else ""


def render_listing(path: str, flt: str, auto_expand: bool):
    """Recursive directory / file renderer."""
    bucket, key = split_s3(path)
    s3 = s3svc.client_for(bucket)

    if path.endswith("/"):  # ── DIRECTORY
        resp = s3.list_objects_v2(
            Bucket=bucket, Prefix=key, Delimiter="/", MaxKeys=1000
        )
        prefs = resp.get("CommonPrefixes", [])
        objs = [o for o in resp.get("Contents", []) if o["Key"] != key]

        rows = []
        for p in prefs:
            name = p["Prefix"][len(key) :].rstrip("/")
            match_cnt = s3svc.count_keys(bucket, p["Prefix"], flt)
            if flt and match_cnt == 0:
                continue
            badge = dbc.Badge(
                match_cnt if flt else s3svc.count_keys(bucket, p["Prefix"], None),
                color="primary",
                pill=True,
                className="ms-2",
            )
            btn_id = (
                {}
                if auto_expand
                else {"type": "toggle", "idx": f"s3://{bucket}/{p['Prefix']}"}
            )
            header = dbc.Button(
                [html.I(className=icon(path) + " me-2"), *highlight(name, flt), badge],
                id=btn_id,
                n_clicks=1 if auto_expand else 0,
                className="w-100 text-start border-0 item-btn",
                color="light",
            )
            child_div = html.Div(
                (
                    render_listing(f"s3://{bucket}/{p['Prefix']}", flt, auto_expand)
                    if auto_expand
                    else ""
                ),
                id={"type": "content", "idx": f"s3://{bucket}/{p['Prefix']}"},
            )
            rows.append(dbc.ListGroupItem([header, child_div], className="p-0"))

        for o in objs:
            name = o["Key"][len(key) :]
            if flt and flt not in name.lower():
                continue
            rows.append(
                dbc.ListGroupItem(
                    dbc.Button(
                        [
                            html.I(className=icon(o["Key"]) + " me-2"),
                            *highlight(name, flt),
                            html.Small(
                                f"  {human_bytes(o['Size'])}", className="text-muted"
                            ),
                        ],
                        id={"type": "toggle", "idx": f"s3://{bucket}/{o['Key']}"},
                        n_clicks=1,
                        className="w-100 text-start border-0 item-btn",
                        color="light",
                    ),
                    className="p-0",
                )
            )

        return (
            dbc.Alert("No matching items", color="light", className="ms-4")
            if not rows
            else dbc.ListGroup(rows, flush=True, className="ms-4")
        )

    # ── FILE PREVIEW
    head = s3.head_object(Bucket=bucket, Key=key)
    ctype = (
        head.get("ContentType") or mimetypes.guess_type(key)[0] or "binary/octet-stream"
    )
    size = head["ContentLength"]
    dl = s3.generate_presigned_url(
        "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=3600
    )
    header = dbc.Row(
        [
            dbc.Col(html.I(className=icon(key)), width="auto"),
            dbc.Col(html.Code(os.path.basename(key))),
            dbc.Col(
                html.Span(f"{human_bytes(size)} • {ctype}", className="text-muted"),
                width="auto",
            ),
            dbc.Col(
                html.A(
                    "Download",
                    href=dl,
                    target="_blank",
                    className="btn btn-outline-primary btn-sm",
                ),
                width="auto",
            ),
        ],
        align="center",
        className="my-2",
    )

    if ctype.startswith(("text/", "application/json")) and size <= 100_000:
        txt = (
            s3.get_object(Bucket=bucket, Key=key)["Body"]
            .read()
            .decode("utf-8", "replace")
        )
        return [
            header,
            dbc.Card(
                dbc.CardBody(
                    dcc.Markdown(f"```\n{txt}\n```", style={"whiteSpace": "pre"})
                ),
                className="my-2 shadow-sm",
            ),
        ]

    if ctype.startswith("image/"):
        src = (
            (
                f"data:{ctype};base64,"
                + base64.b64encode(
                    s3.get_object(Bucket=bucket, Key=key)["Body"].read()
                ).decode()
            )
            if size <= 5 * 1024 * 1024
            else dl
        )
        return [
            header,
            html.Img(src=src, style={"maxWidth": "100%", "borderRadius": ".25rem"}),
        ]

    return [
        header,
        dbc.Alert("Preview not available.", color="light", className="ms-1"),
    ]