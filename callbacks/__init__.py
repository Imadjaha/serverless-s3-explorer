from . import buckets, directory


def register_callbacks(app):
    buckets.register(app)
    directory.register(app)
