from typing import Iterator
from dash.html import Span


def build_from_differ_compare(diff: Iterator[str]) -> list[Span]:
    children = []

