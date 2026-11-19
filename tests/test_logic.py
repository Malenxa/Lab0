"""Unit tests for the core data preprocessing functions"""

# pylint: disable=redefined-outer-name
import math
import pytest
from src import preprocessing as prep


@pytest.fixture
def list_with_empty():
    """Return a list containing None, empty strings, and NaN values."""
    return [1, None, "text", "", float("nan"), 2]


@pytest.fixture
def sample_numbers():
    """Return a clean list of numerical values."""
    return [10.0, 20.0, 30.0, 40.0, 50.0]


def test_remove_missing(list_with_empty):
    """Test removal of missing values and empty list handling."""
    result = prep.remove_missing(list_with_empty)
    assert result == [1, "text", 2]
    assert prep.remove_missing([]) == []


def test_fill_missing_default(list_with_empty):
    """Test filling missing values with default 0."""
    result = prep.fill_missing(list_with_empty)
    assert result == [1, 0, "text", 0, 0, 2]
    assert prep.fill_missing([]) == []


def test_fill_missing_custom(list_with_empty):
    """Test filling missing values with a custom value."""
    value = 400
    result = prep.fill_missing(list_with_empty, fill_value=value)
    assert result == [1, value, "text", value, value, 2]


def test_remove_duplicates():
    """Test duplicate removal including NaNs while preserving order and length."""
    data = [1, 2, 2, 3, 1, float("nan"), float("nan"), 4]
    result = prep.remove_duplicates(data)
    assert len(result) == 5
    assert result[:3] == [1, 2, 3]
    assert math.isnan(result[3])
    assert result[4] == 4
    assert not prep.remove_duplicates([])


def test_normalize_minmax(sample_numbers):
    """Test min-max normalization with default, custom ranges, and edge cases."""
    assert prep.normalize_minmax(sample_numbers) == [0.0, 0.25, 0.5, 0.75, 1.0]
    assert prep.normalize_minmax(sample_numbers, -1.0, 1.0) == [
        -1.0,
        -0.5,
        0.0,
        0.5,
        1.0,
    ]
    assert prep.normalize_minmax([]) == []
    assert prep.normalize_minmax([5, 5, 5], new_min=2.0, new_max=10.0) == [
        2.0,
        2.0,
        2.0,
    ]


@pytest.mark.parametrize(
    "values, expected",
    [
        ([10, 20, 30], [-1.224744871391589, 0.0, 1.224744871391589]),
        ([5, 5, 5], [0.0, 0.0, 0.0]),
        ([], []),
    ],
)
def test_standardize_zscore(values, expected):
    """Test z-score standardization across multiple inputs."""
    assert prep.standardize_zscore(values) == pytest.approx(expected)


@pytest.mark.parametrize(
    "values, min_val, max_val, expected",
    [
        ([-5, 0, 5, 10, 15], 0, 10, [0, 0, 5, 10, 10]),
        ([0.1, 0.5, 0.9], 0.2, 0.8, [0.2, 0.5, 0.8]),
        ([], 0, 1, []),
    ],
)
def test_clip_values(values, min_val, max_val, expected):
    """Test clipping values to required min and max thresholds."""
    assert prep.clip_values(values, min_val, max_val) == expected


def test_convert_to_integers():
    """Test conversion of mixed values to integers, ignoring non-numeric ones."""
    data = ["10", "-5", "abc", "3.14", None, "42"]
    assert prep.convert_to_integers(data) == [10, -5, 42]
    assert not prep.convert_to_integers([])


def test_log_transform():
    """Test natural log transformation filtering out <= 0, NaNs, and booleans."""
    data = [-10, 0, 1, math.e, 10, float("nan"), True, False, "text"]
    result = prep.log_transform(data)
    assert result == pytest.approx([0.0, 1.0, math.log(10)])
    assert not prep.log_transform([])


def test_tokenize_text():
    """Test tokenization into lowercased alphanumeric words."""
    text = "¡Hola, Mundo 2026! Testing-123."
    assert prep.tokenize_text(text) == ["hola", "mundo", "2026", "testing", "123"]
    assert not prep.tokenize_text("")


def test_clean_alphanumeric_spaces():
    """Test removal of punctuation while keeping alphanumeric characters and spaces."""
    text = "Hello, World! #1 @Python_2026"
    assert prep.clean_alphanumeric_spaces(text) == "Hello World 1 Python2026"
    assert prep.clean_alphanumeric_spaces("") == ""


def test_remove_stopwords():
    """Test stop-word removal and lowercasing."""
    text = "The quick brown FOX jumps over the lazy dog"
    stopwords = ["the", "over"]
    assert prep.remove_stopwords(text, stopwords) == "quick brown fox jumps lazy dog"
    assert prep.remove_stopwords("Hello World", []) == "hello world"


def test_flatten_list():
    """Test flattening a nested list of lists."""
    nested = [[1, 2], [3, 4], [5]]
    assert prep.flatten_list(nested) == [1, 2, 3, 4, 5]
    assert prep.flatten_list([[], [1], []]) == [1]
    assert prep.flatten_list([]) == []


def test_shuffle_list(sample_numbers):
    """Test list shuffling with seed for reproducibility without mutating input."""
    original = sample_numbers.copy()
    res1 = prep.shuffle_list(sample_numbers, seed=42)
    res2 = prep.shuffle_list(sample_numbers, seed=42)
    assert res1 == res2
    assert sorted(res1) == sorted(original)
    assert sample_numbers == original
    assert not prep.shuffle_list([], seed=42)
