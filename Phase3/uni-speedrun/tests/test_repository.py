from uni_speedrun.database.repository import StudienplanRepository


def test_repository_hat_speichern_und_laden():
    assert hasattr(StudienplanRepository, "speichern")
    assert hasattr(StudienplanRepository, "laden")