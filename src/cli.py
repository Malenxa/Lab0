"""Command Line Interface module for data preprocessing."""

import json
import click
from src import preprocessing as prep


@click.group()
def cli():
    """Command Line Interface for data preprocessing."""


# ====================================================
# CLEAN DATA
# ====================================================
@cli.group()
def clean():
    """Functions related to data cleaning."""


@clean.command()
@click.argument("values", nargs=-1, type=str)
def remove_missing(values):
    """Remove missing values from a list of string values.

    Example: uv run python -m src.cli clean remove-missing a "" b c
    """
    result = prep.remove_missing(list(values))
    click.echo(f"Cleaned data: {result}")


@clean.command()
@click.argument("values", nargs=-1, type=str)
@click.option(
    "--fill-value",
    default="0",
    help="Value used to replace missing values (defaults to 0).",
)
def fill_missing(values, fill_value):
    """Fill missing values in a list with a given value.

    Example: uv run python -m src.cli clean fill-missing a "" b --fill-value N/A
    """
    result = prep.fill_missing(list(values), fill_value=fill_value)
    click.echo(f"Filled data: {result}")


# ====================================================
# NUMERIC DATA
# ====================================================
@cli.group()
def numeric():
    """Functions related to dealing with numerical attributes."""


@numeric.command()
@click.argument("values", nargs=-1, type=float)
@click.option(
    "--min-val",
    default=0.0,
    help="Minimum value of the new range (defaults to 0.0).",
)
@click.option(
    "--max-val",
    default=1.0,
    help="Maximum value of the new range (defaults to 1.0).",
)
def normalize(values, min_val, max_val):
    """Normalize numerical values using the min-max method.

    Example: uv run python -m src.cli numeric normalize 10 20 30 --min-val 0 --max-val 10
    """
    result = prep.normalize_minmax(list(values), new_min=min_val, new_max=max_val)
    click.echo(f"Normalized values: {result}")


@numeric.command()
@click.argument("values", nargs=-1, type=float)
def standardize(values):
    """Standardize numerical values using the z-score method.

    Example: uv run python -m src.cli numeric standardize 10 20 30
    """
    result = prep.standardize_zscore(list(values))
    click.echo(f"Standardized values: {result}")


@numeric.command()
@click.argument("values", nargs=-1, type=float)
@click.option(
    "--min-val",
    default=0.0,
    help="Minimum value to clip (defaults to 0.0).",
)
@click.option(
    "--max-val",
    default=1.0,
    help="Maximum value to clip (defaults to 1.0).",
)
def clip(values, min_val, max_val):
    """Clip numerical values to a certain range.

    Example: uv run python -m src.cli numeric clip -- -2 0.5 3 --min-val 0 --max-val 1
    """
    result = prep.clip_values(list(values), min_val=min_val, max_val=max_val)
    click.echo(f"Clipped values: {result}")


@numeric.command(name="to-integers")
@click.argument("values", nargs=-1, type=str)
def convert_to_integers(values):
    """Convert a list of values to integers, excluding non-numerical ones.

    Example: uv run python -m src.cli numeric to-integers 10 hello 25 3.5
    """
    result = prep.convert_to_integers(list(values))
    click.echo(f"Converted integers: {result}")


@numeric.command(name="log-scale")
@click.argument("values", nargs=-1, type=float)
def log_transform(values):
    """Transform positive numerical values to logarithmic scale.

    Example: uv run python -m src.cli numeric log-scale -- -5 0 1 10 100
    """
    result = prep.log_transform(list(values))
    click.echo(f"Log-transformed values: {result}")


# ====================================================
# TEXT DATA
# ====================================================
@cli.group()
def text():
    """Functions to deal with textual information."""


@text.command()
@click.argument("input_text", type=str)
def tokenize(input_text):
    """Tokenize text into lowercase alphanumeric words.

    Example: uv run python -m src.cli text tokenize "Hello, World 2026!"
    """
    result = prep.tokenize_text(input_text)
    click.echo(f"Tokens: {result}")


@text.command(name="remove-punctuation")
@click.argument("input_text", type=str)
def remove_punctuation(input_text):
    """Keep only alphanumeric characters and spaces from text.

    Example: uv run python -m src.cli text remove-punctuation "Hello, World #1!"
    """
    result = prep.clean_alphanumeric_spaces(input_text)
    click.echo(f"Processed text: {result}")


@text.command(name="remove-stopwords")
@click.argument("input_text", type=str)
@click.option(
    "--stopwords",
    "-s",
    multiple=True,
    default=["the", "a", "an", "is", "of", "and", "to", "in"],
    help="Stopwords to remove (can be passed multiple times, e.g., -s the -s is).",
)
def remove_stopwords(input_text, stopwords):
    """Remove stop-words from lowercased text.

    Example: uv run python -m src.cli text remove-stopwords "The quick brown fox" -s the -s fox
    """
    result = prep.remove_stopwords(input_text, list(stopwords))
    click.echo(f"Filtered text: {result}")


# ====================================================
# STRUCTURAL DATA
# ====================================================
@cli.group()
def struct():
    """Functions related to the structure of data."""


@struct.command()
@click.argument("values", nargs=-1, type=str)
@click.option(
    "--seed",
    default=None,
    type=int,
    help="Integer seed to ensure reproducibility (defaults to None).",
)
def shuffle(values, seed):
    """Randomly shuffle a list of values.

    Example: uv run python -m src.cli struct shuffle a b c d --seed 42
    """
    result = prep.shuffle_list(list(values), seed=seed)
    click.echo(f"Shuffled list: {result}")


@struct.command()
@click.argument("list_of_lists", type=str)
def flatten(list_of_lists):
    """Flatten a list of lists into a single list.

    Example: uv run python -m src.cli struct flatten "[[1, 2], [3, 4]]"
    """
    try:
        parsed_list = json.loads(list_of_lists)
        result = prep.flatten_list(parsed_list)
        click.echo(f"Flattened list: {result}")
    except (json.JSONDecodeError, TypeError) as err:
        raise click.BadParameter(
            "Input must be a valid list of lists, e.g. '[[1, 2], [3, 4]]'"
        ) from err


@struct.command(name="unique-values")
@click.argument("values", nargs=-1, type=str)
def unique_values(values):
    """Remove duplicated values from a list while preserving order.

    Example: uv run python -m src.cli struct unique-values a b a c b
    """
    result = prep.remove_duplicates(list(values))
    click.echo(f"Unique values: {result}")


if __name__ == "__main__":
    cli()
