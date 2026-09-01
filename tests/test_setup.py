"""Einrichtungstests für die Entwicklungsumgebung."""

import sqlite3

import textual

from uni_speedrun import __version__


def test_paket_kann_importiert_werden() -> None:
    assert __version__ == "0.1.0"


def test_sqlite_ist_verfuegbar() -> None:
    assert sqlite3.sqlite_version


def test_textual_ist_verfuegbar() -> None:
    assert textual.__version__
