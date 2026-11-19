"""Module containing core data preprocessing functions for cleaning, numerical scaling,
text processing, and list manipulation."""

import math
import random
import re


def _is_missing(val):
    """Check if a value is considered missing (None, empty string, or NaN).

    Args:
        val: The value to evaluate.

    Returns:
        bool: True if the value is missing, False otherwise.
    """
    if val is None or val == "":
        return True
    if isinstance(val, float) and math.isnan(val):
        return True
    return False


def remove_missing(values):
    """Remove missing values (None, '', nan) from a list.

    Args:
        values (list): List of values potentially containing missing entries.

    Returns:
        list: A new list excluding all missing values.
    """
    return [v for v in values if not _is_missing(v)]


def fill_missing(values, fill_value=0):
    """Replace missing values in a list with a specified fill value.

    Args:
        values (list): List of values potentially containing missing entries.
        fill_value (Any, optional): Value used to replace missing entries.
            Defaults to 0.

    Returns:
        list: A new list with missing values replaced by fill_value.
    """
    return [fill_value if _is_missing(v) else v for v in values]


def remove_duplicates(values):
    """Remove duplicated values from a list while preserving original order.

    Args:
        values (list): List of values potentially containing duplicates.

    Returns:
        list: A list of unique values in their original order.
    """
    seen = []
    for v in values:
        if isinstance(v, float) and math.isnan(v):
            if not any(isinstance(x, float) and math.isnan(x) for x in seen):
                seen.append(v)
        elif v not in seen:
            seen.append(v)
    return seen


def normalize_minmax(values, new_min=0.0, new_max=1.0):
    """Normalize numerical values to a target range using the min-max method.

    Args:
        values (list[float]): List of numerical values to normalize.
        new_min (float, optional): Minimum value of the target range.
            Defaults to 0.0.
        new_max (float, optional): Maximum value of the target range.
            Defaults to 1.0.

    Returns:
        list[float]: List of normalized numerical values.
    """
    if not values:
        return []
    old_min = min(values)
    old_max = max(values)
    if old_max == old_min:
        return [float(new_min) for _ in values]
    return [
        new_min + ((v - old_min) * (new_max - new_min)) / (old_max - old_min)
        for v in values
    ]


def standardize_zscore(values):
    """Standardize numerical values using the z-score method.

    Args:
        values (list[float]): List of numerical values to standardize.

    Returns:
        list[float]: List of standardized values with mean 0 and std 1.
    """
    if not values:
        return []
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    std = math.sqrt(variance)
    if std == 0:
        return [0.0 for _ in values]
    return [(v - mean) / std for v in values]


def clip_values(values, min_val, max_val):
    """Clip numerical values to stay within a specified [min_val, max_val] range.

    Args:
        values (list[float]): List of numerical values to clip.
        min_val (float): Minimum allowed threshold.
        max_val (float): Maximum allowed threshold.

    Returns:
        list[float]: List of clipped numerical values.
    """
    return [max(min_val, min(v, max_val)) for v in values]


def convert_to_integers(values):
    """Convert a list of values to integers, excluding non-numerical entries.

    Args:
        values (list): List of values (typically strings) to convert.

    Returns:
        list[int]: List containing only the successfully converted integers.
    """
    result = []
    for v in values:
        try:
            result.append(int(v))
        except (ValueError, TypeError):
            continue
    return result


def log_transform(values):
    """Apply natural logarithmic transformation to strictly positive numbers.

    Args:
        values (list): List of values to transform.

    Returns:
        list[float]: Natural logarithm of each positive number in the input.
    """
    return [
        math.log(v)
        for v in values
        if isinstance(v, (int, float))
        and not isinstance(v, bool)
        and not math.isnan(v)
        and v > 0
    ]


def tokenize_text(text):
    """Tokenize text into lowercased alphanumeric words.

    Args:
        text (str): Input text to tokenize.

    Returns:
        list[str]: List of extracted alphanumeric word tokens in lowercase.
    """
    return re.findall(r"[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ]+", text.lower())


def clean_alphanumeric_spaces(text):
    """Remove all characters from text except alphanumeric ones and spaces.

    Args:
        text (str): Input text to clean.

    Returns:
        str: Processed text containing only alphanumeric characters and spaces.
    """
    return re.sub(r"[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s]", "", text)


def remove_stopwords(text, stop_words):
    """Remove specified stop-words from text and convert the output to lowercase.

    Args:
        text (str): Input text to filter.
        stop_words (list[str]): Collection of stop-words to remove.

    Returns:
        str: Lowercased text without the specified stop-words.
    """
    stop_set = {sw.lower() for sw in stop_words}
    words = text.lower().split()
    filtered_words = [w for w in words if w not in stop_set]
    return " ".join(filtered_words)


def flatten_list(list_of_lists):
    """Flatten a two-dimensional list of lists into a single one-dimensional list.

    Args:
        list_of_lists (list[list]): Nested list to flatten.

    Returns:
        list: Flattened list containing all elements in order.
    """
    return [item for sublist in list_of_lists for item in sublist]


def shuffle_list(values, seed=None):
    """Randomly shuffle a list of values using an optional seed for reproducibility.

    Args:
        values (list): List of values to shuffle.
        seed (int, optional): Random seed for reproducibility. Defaults to None.

    Returns:
        list: A new shuffled copy of the input list.
    """
    shuffled = values.copy()
    rng = random.Random(seed)
    rng.shuffle(shuffled)
    return shuffled
