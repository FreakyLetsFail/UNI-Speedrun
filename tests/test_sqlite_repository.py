from uni_speedrun.database.sqlite_repository import (
    SQLiteStudienplanRepository,
)


def test_sqlite_repository_kann_erstellt_werden(tmp_path):
    datenbank = tmp_path / "test.db"

    repository = SQLiteStudienplanRepository(str(datenbank))

    assert repository.datenbank_pfad == str(datenbank)