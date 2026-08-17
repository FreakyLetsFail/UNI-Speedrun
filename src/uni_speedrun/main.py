from uni_speedrun.database.sqlite_repository import SQLiteStudienplanRepository
from uni_speedrun.textui.app import UniSpeedrunApp


def main() -> None:
    repository = SQLiteStudienplanRepository("UniSpeedrun.db")

    app = UniSpeedrunApp(repository)
    app.run()


if __name__ == "__main__":
    main()