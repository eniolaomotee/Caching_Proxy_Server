import typer
from server import start_proxy_server
from cache import clear_cache
from logging_conf import configure_logging

app = typer.Typer()
configure_logging()


@app.command()
def run(port:int = typer.Option(...,"--port", "-p", help="Port to run the proxy server on"), 
    origin:str = typer.Option(...,"--origin","-o", help="Origin server URL")):
    print("Start the caching Server")
    start_proxy_server(port, origin)
    print(f"Starting server on port {port} with origin {origin}")


@app.command()
def clear_cache_cmd():
    "Clear the In memory Cache"
    clear_cache()
    print("Cache cleared")



if __name__ == "__main__":
    app()