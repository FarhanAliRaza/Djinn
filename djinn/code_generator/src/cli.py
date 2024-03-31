import sys
from typing import List

import typer
from base import Generator
from generators import (
    AppGenerator,
    GenerateSerializer,
    GenerateUrl,
    GenerateView,
    ModelGenerator,
)
from rich import print
from typing_extensions import Annotated

app = typer.Typer()
#


def parse_model_label(label: str):
    try:
        app_name, model_name = label.split(".")
        return app_name, model_name
    except Exception:
        print(
            f"[bold red]'{label}' is not valid label. Valid name is[/bold red][bold green] app_name.ModelName [/bold green]"
        )
        sys.exit()


@app.command()
def generate(
    model: Annotated[str, typer.Argument(help="app_name.Model (Model label)")],
):
    """
    model:[app_name.ModelName] Label of the model for which you want to generate serializers and viewsets for.
    """
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
def create(
    model: Annotated[str, typer.Argument(help="app_name.Model (Model label)")],
    fields: Annotated[List[str], typer.Argument(help="field_name:field_type")],
):
    """
    [djinn create app_name.ModelName name:str is_done:bool, status:valid,invalid] Valid fields are ["str", "text", "int", "float", "bool"]
    For choice the first value will be used as default.
    """

    app_name, model_name = parse_model_label(model)
    mg = ModelGenerator(app_name=app_name, model_name=model_name, fields=fields)
    if mg.check_if_file_exists():
        print(
            f"[bold red]'{model_name}' conflicts with already present {model_name.lower()}.py already exists[/bold red]"
        )
        return
    mg.parse_fields()
    mg.create_model()
    mg.copy_over_code_to_app()
    mg.export_model()
    mg.add_to_admin()


# TODO:add to global urls
@app.command()
def startapp(
    app_name: Annotated[str, typer.Argument(help="App name. A valid django app name")],
):
    """
    app_name: Name of the django app you want to create
    """
    ap = AppGenerator(app_name)
    if ap.check_if_foldername_exists():
        print(
            f"[bold red]'{app_name}' conflicts with already present folder[/bold red]"
        )
        return
    ap.copy_to_temp()
    ap.transform_and_move()
    ap.add_to_setting()


if __name__ == "__main__":
    app()
