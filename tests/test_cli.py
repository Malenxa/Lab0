"""Integration tests between the CLI commands and the preprocessing logic."""

# pylint: disable=redefined-outer-name

import math
from click.testing import CliRunner
import pytest
from src.cli import cli


@pytest.fixture
def runner():
    """Provide a Click CliRunner instance."""
    return CliRunner()


# ====================================================
# CLEAN GROUP
# ====================================================
def test_cli_clean_remove_missing(runner):
    """Test 'clean remove-missing' command with missing and valid strings."""
    result = runner.invoke(cli, ["clean", "remove-missing", "a", "", "b", "c"])
    assert result.exit_code == 0
    assert "['a', 'b', 'c']" in result.output


def test_cli_clean_fill_missing_default_and_custom(runner):
    """Test 'clean fill-missing' command with default and custom fill values."""
    default_res = runner.invoke(cli, ["clean", "fill-missing", "a", "", "b"])
    assert default_res.exit_code == 0
    assert "['a', '0', 'b']" in default_res.output

    custom_res = runner.invoke(
        cli, ["clean", "fill-missing", "a", "", "b", "--fill-value", "N/A"]
    )
    assert custom_res.exit_code == 0
    assert "['a', 'N/A', 'b']" in custom_res.output


# ====================================================
# NUMERIC GROUP
# ====================================================
def test_cli_numeric_normalize_default_and_custom(runner):
    """Test 'numeric normalize' command with default and custom min/max options."""
    default_res = runner.invoke(cli, ["numeric", "normalize", "10", "20", "30"])
    assert default_res.exit_code == 0
    assert "[0.0, 0.5, 1.0]" in default_res.output

    custom_res = runner.invoke(
        cli,
        [
            "numeric",
            "normalize",
            "10",
            "20",
            "30",
            "--min-val",
            "0",
            "--max-val",
            "10",
        ],
    )
    assert custom_res.exit_code == 0
    assert "[0.0, 5.0, 10.0]" in custom_res.output


def test_cli_numeric_standardize(runner):
    """Test 'numeric standardize' command output and zero-variance handling."""
    result = runner.invoke(cli, ["numeric", "standardize", "10", "20", "30"])
    assert result.exit_code == 0
    assert "Standardized values:" in result.output

    const_res = runner.invoke(cli, ["numeric", "standardize", "5", "5", "5"])
    assert const_res.exit_code == 0
    assert "[0.0, 0.0, 0.0]" in const_res.output


def test_cli_numeric_clip_default_and_custom(runner):
    """Test 'numeric clip' command with default and custom clipping bounds."""
    default_res = runner.invoke(cli, ["numeric", "clip", "--", "-2", "0.5", "3"])
    assert default_res.exit_code == 0
    assert "[0.0, 0.5, 1.0]" in default_res.output

    custom_res = runner.invoke(
        cli,
        [
            "numeric",
            "clip",
            "--min-val",
            "-1",
            "--max-val",
            "2",
            "--",
            "-2",
            "0.5",
            "3",
        ],
    )
    assert custom_res.exit_code == 0
    assert "[-1.0, 0.5, 2.0]" in custom_res.output


def test_cli_numeric_to_integers(runner):
    """Test 'numeric to-integers' command filtering non-numeric strings."""
    result = runner.invoke(cli, ["numeric", "to-integers", "10", "hello", "25", "3.5"])
    assert result.exit_code == 0
    assert "[10, 25]" in result.output


def test_cli_numeric_log_scale(runner):
    """Test 'numeric log-scale' command filtering non-positive numbers."""
    result = runner.invoke(cli, ["numeric", "log-scale", "--", "-5", "0", "1", "10"])
    assert result.exit_code == 0
    expected_log_10 = math.log(10)
    assert "[0.0," in result.output
    assert str(expected_log_10) in result.output


# ====================================================
# TEXT GROUP
# ====================================================
def test_cli_text_tokenize(runner):
    """Test 'text tokenize' command."""
    result = runner.invoke(cli, ["text", "tokenize", "Hello, World 2026!"])
    assert result.exit_code == 0
    assert "['hello', 'world', '2026']" in result.output


def test_cli_text_remove_punctuation(runner):
    """Test 'text remove-punctuation' command."""
    result = runner.invoke(cli, ["text", "remove-punctuation", "Hello, World #1!"])
    assert result.exit_code == 0
    assert "Hello World 1" in result.output


def test_cli_text_remove_stopwords_default_and_custom(runner):
    """Test 'text remove-stopwords' with default and custom -s options."""
    default_res = runner.invoke(
        cli, ["text", "remove-stopwords", "The quick brown fox in a house"]
    )
    assert default_res.exit_code == 0
    assert "quick brown fox house" in default_res.output

    custom_res = runner.invoke(
        cli,
        [
            "text",
            "remove-stopwords",
            "The quick brown fox",
            "-s",
            "the",
            "-s",
            "fox",
        ],
    )
    assert custom_res.exit_code == 0
    assert "quick brown" in custom_res.output


# ====================================================
# STRUCT GROUP
# ====================================================
def test_cli_struct_shuffle(runner):
    """Test 'struct shuffle' command with and without seed."""
    no_seed = runner.invoke(cli, ["struct", "shuffle", "a", "b", "c", "d"])
    assert no_seed.exit_code == 0
    assert "Shuffled list:" in no_seed.output

    res1 = runner.invoke(cli, ["struct", "shuffle", "a", "b", "c", "d", "--seed", "42"])
    res2 = runner.invoke(cli, ["struct", "shuffle", "a", "b", "c", "d", "--seed", "42"])
    assert res1.exit_code == 0
    assert res1.output == res2.output


def test_cli_struct_flatten(runner):
    """Test 'struct flatten' command with valid JSON and invalid input."""
    valid = runner.invoke(cli, ["struct", "flatten", "[[1, 2], [3, 4]]"])
    assert valid.exit_code == 0
    assert "[1, 2, 3, 4]" in valid.output

    invalid = runner.invoke(cli, ["struct", "flatten", "not-a-json"])
    assert invalid.exit_code != 0


def test_cli_struct_unique_values(runner):
    """Test 'struct unique-values' command."""
    result = runner.invoke(cli, ["struct", "unique-values", "a", "b", "a", "c", "b"])
    assert result.exit_code == 0
    assert "['a', 'b', 'c']" in result.output
