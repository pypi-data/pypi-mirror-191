from pathlib import Path

import click

from baseten.common.files import DatasetTrainingType, upload_dataset


@click.group(name="dataset")
def dataset_cli():
    """Manage datasets stored on Blueprint"""
    pass


@dataset_cli.command()
@click.argument("data_dir", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option("--name", "-n", required=True, type=str, help="Name give to Dataset on Blueprint")
@click.option(
    "--training-type",
    "-t",
    required=True,
    type=click.Choice([t.value for t in DatasetTrainingType], case_sensitive=False),
    help="Types of FinetuningRun that can use this Dataset",
)
def upload(data_dir: Path, name: str, training_type: str):
    """Upload a new dataset to Baseten from DATA_DIR

    DATA_DIR is the path to directory with relevant files.
    """
    dataset_id = upload_dataset(name, Path(data_dir), DatasetTrainingType[training_type.upper()])
    click.echo()
    click.echo(f"Dataset ID:\n{dataset_id}")
