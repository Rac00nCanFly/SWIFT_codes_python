from prometheus_fastapi_instrumentator import Instrumentator

def add_monitoring(app):
    Instrumentator().instrument(app).expose(app)
