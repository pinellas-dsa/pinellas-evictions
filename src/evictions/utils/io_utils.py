from pathlib import Path
import yaml


def load_query(query_path: Path) -> dict:
    """Reads the query configuration file from YAML format
    and renders it as a dictionary.
    Args:
        query_path (Path): The path to the YAML file
    Returns:
        dict: Python dictionary containing instructions for how to run the query
    """
    with open(query_path, "rt", encoding="utf-8") as file:
        query = yaml.safe_load(file)
        return query
