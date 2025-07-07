import typer
from server import start_proxy_server
from cache import clear_cache


app = typer.Typer()

@app.command()
def run(port:int, origin:str):
    "Start the caching Server"
    start_proxy_server(port, origin)

@app.command()
def clear_cache_cmd():
    "Clear the In memory Cache"
    clear_cache()
    print("Cache cleared")





if __name__ == "__main":
    app()