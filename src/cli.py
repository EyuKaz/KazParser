import typer
import orjson
from rich.progress import Progress
from .core import Omniparser
from .exporters import SQLExporter

app = typer.Typer()

@app.command()
def parse(
    input_file: str = typer.Argument(..., help="Input file path"),
    output_format: str = typer.Option("json", "--format", "-f", help="Output format (json/csv/sql)"),
    delimiter: str = typer.Option("auto", "--delimiter", "-d", help="Field delimiter"),
    validate: bool = typer.Option(False, "--validate", help="Enable schema validation"),
    schema_file: str = typer.Option(None, "--schema", help="JSON Schema file path")
):
    parser = Omniparser(input_file, delimiter=delimiter)
    
    if validate and not schema_file:
        typer.echo("Schema file required for validation", err=True)
        raise typer.Exit(code=1)
    
    if schema_file:
        with open(schema_file, 'r') as f:
            schema = orjson.loads(f.read())
        validator = SchemaValidator(schema)
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Processing...", total=self._get_file_size(input_file))
        
        for batch in parser.stream():
            if validate:
                batch = validator.validate_stream(batch)
            
            if output_format == 'json':
                print(orjson.dumps(batch, option=orjson.OPT_INDENT_2).decode())
            elif output_format == 'sql':
                exporter = SQLExporter('my_table')
                print(exporter.export(batch))
            
            progress.update(task, advance=len(batch)*1024)  # Approximate

if __name__ == "__main__":
    app()