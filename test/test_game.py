import pytest
from game import game_create
from question import question_create


def make_sample_question(correct="C"):
  return question_create([("Q", "Pytanie?"), ("A", "1"), ("B","2"), ("C", "3"), ("D", "4"), ("S", correct)])


def test_game_win_all_questions(monkeypatch):
  inputs = iter(["C", "A"])
  monkeypatch.setattr("builtins.input", lambda: next(inputs))
  game = game_create([make_sample_question("C"), make_sample_question("A")])
  assert game["play"]() == 2


def test_game_stops_on_first_wrong_answer(monkeypatch):
  # drugie pytanie błędne -> trzecie nie powinno się wykonać
  inputs = iter(["C", "B", "A"])
  monkeypatch.setattr("builtins.input", lambda: next(inputs))
  game = game_create([make_sample_question(
      "C"), make_sample_question("A"), make_sample_question("A")])
  assert game["play"]() == 1


def test_game_lifeline_and_rejected_option(monkeypatch, capsys):
  # "xyz" -> nierozpoznana, "K" -> użycie koła (zostaje A i C),
  # "D" -> odrzucona odpowiedź (powinna być nierozpoznana!), "K" -> brak kół, "C" -> poprawna
  inputs = iter(["xyz", "K", "D", "K", "C"])
  monkeypatch.setattr("builtins.input", lambda: next(inputs))
  game = game_create([make_sample_question("C")])

  score = game["play"]()
  out = capsys.readouterr().out

  assert score == 1
  assert out.count("Nie rozpoznana komenda") == 2
  assert "Brak kol ratunkowych do wykorzystania!" in out


def test_game_exit_command(monkeypatch):
  monkeypatch.setattr("builtins.input", lambda: "exit")
  game = game_create([make_sample_question("C")])
  with pytest.raises(SystemExit):
    game["play"]()
