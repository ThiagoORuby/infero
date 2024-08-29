from pathlib import Path

from rich.console import Console
from rich.padding import Padding
from rich.table import Table
from typer import Argument, Context, Exit, Option, Typer, echo

from infero import __app_name__, __version__
from infero.parser import Parser
from infero.solver import solve

console = Console()
app = Typer()


def version_func(flag):
    if flag:
        print(f"{__app_name__} v{__version__}")
        raise Exit(code=0)


@app.callback(invoke_without_command=True)
def main(
    ctx: Context, version: bool = Option(False, callback=version_func, is_flag=True)
):
    message = """Forma de uso: [b]infero [SUBCOMANDO] [ARGUMENTOS][/]

 Existem 3 subcomandos disponíveis para essa aplicação

- [b]compile[/]: Compila um arquivo .ifo, fornecendo a solução da derivação
- [b]tokenize[/]: Fornece os tokens presentes no arquivo
- [b]ast[/]: Fornece a árvore sintática do arquivo

[b]Exemplo de uso:[/]

infero compile examples/example.ifo

[b]Para mais informações rápidas: [red]infero --help[/]
"""
    if ctx.invoked_subcommand:
        return
    console.print(Padding(message, pad=(0, 0, 0, 2)))


@app.command()
def compile(file: Path = Argument(help="arquivo .ifo a ser compilado")):

    extensao = ".ifo"

    if file.suffix != extensao:
        echo("Erro: extensão de arquivo desconhecida")
        raise Exit(1)

    data = file.read_text()

    parser = Parser(data)
    parser.start()

    query = parser.program["query"][0]

    finded, path = solve(parser.program["rules"], query, parser.symhash)

    console.print(
        Padding("\n[b]==+==+==+== SOLUTION ==+==+==+==[/]\n", pad=(0, 0, 0, 2))
    )

    if finded is None:
        console.print(
            Padding(
                "\n[b bright_yellow] Solution not finded :( [/]\n", pad=(0, 0, 0, 2)
            )
        )
    elif finded is False:
        console.print(
            Padding("\n[b bright_red] Contradiction finded!! [/]\n", pad=(0, 0, 0, 2))
        )
    else:
        for step in path:
            console.print(Padding(str(step), pad=(0, 0, 0, 2)))

        console.print(Padding(f"\n[b]Then[/] {query.formula()}\n", pad=(0, 0, 0, 2)))

    table = Table()

    for key in parser.symhash.keys():
        table.add_column(key)

    table.add_row(*list(map(str, parser.symhash.values())))
    console.print(Padding(table, pad=(0, 0, 0, 1)))
