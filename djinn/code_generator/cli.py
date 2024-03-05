import typer
from typing_extensions import Annotated
from typing import Optional
from base import Generator
from generators import GenerateView, GenerateSerializer, GenerateUrl

app = typer.Typer()


def parse_model_label(label: str):
    try:
        app_name = label.split(".")[0]
        model_name = label.split(".")[1]

        return app_name, model_name
    except:
        raise Exception("Model name should be like this [ app_name.Model_Name ]")


@app.command()
def create(
    model: Annotated[str, typer.Argument(help="app_name.Model (Model label)")],
):
    app_name, model_name = parse_model_label(model)
    print(app_name, model_name)
    gen = Generator(app_name=app_name, model_name=model_name)
    gen.parse()
    gs = GenerateSerializer(gen)
    gs.generate_serializer()
    gv = GenerateView(gen)
    gv.generate_view()
    gu = GenerateUrl(gen)
    gu.generate_urls()


@app.command()
def startapp(
    app_name: Annotated[str, typer.Argument(help="App name")],
):
    pass


if __name__ == "__main__":
    app()


"""
How it should work?


generate app.Model

generate app.Model --serializer

generate app.Model --v

generate app.Model --u








"""
