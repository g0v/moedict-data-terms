import csv
import json
import typing
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Category:
    category_id: int
    name: str
    last_updated: datetime
    data_url: str
    data_files: list[str] = field(repr=False)


def save(fp: typing.IO, categories: list[Category]) -> None:
    """
    Helper function to save a list of categories to file-like object.
    """
    writer = csv.writer(fp)
    for category in categories:
        writer.writerow([
            category.category_id,
            category.name,
            category.last_updated.isoformat(sep=' '),
            category.data_url,
            json.dumps(category.data_files) if category.data_files else ''
        ])


def restore(fp: typing.IO) -> list[Category]:
    """
    Helper function to load previous category memory when executed
    as a standalone script without specifying the desired category ID.
    """
    return list([
        Category(
            category_id=int(cat_id),
            name=name,
            last_updated=datetime.fromisoformat(last_updated),
            data_url=data_url,
            data_files=(json.loads(data_files) if data_files else [])
        )
        for cat_id, name, last_updated, data_url, data_files in csv.reader(fp)
    ])
