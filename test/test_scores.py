import pytest
import file_io
import os
import stat
import quiz

VALID_QUESTION = (
  "Q\tIle zasad azotowych występuje w DNA?\n"
  "A\t2\n"
  "B\t3\n"
  "C\t4\n"
  "D\t5\n"
  "S\tC\n"
)

def test_load_scores_validation(tmp_path):
  p = tmp_path / "wyniki.txt"
  # Imię ze spacją lub brak liczby powinny rzucić ValueError
  p.write_text("Jan Kowalski\t10\n", encoding="utf-8")
  with pytest.raises(ValueError):
    file_io.load_scores(p)


def test_load_scores_readonly_raises_permission_error(tmp_path):
  p = tmp_path / "wyniki.txt"
  p.write_text("Anna\t14\n", encoding="utf-8")
  p.chmod(stat.S_IREAD)  # tylko do odczytu
  try:
    with pytest.raises(PermissionError):
      file_io.load_scores(p)
  finally:
    p.chmod(stat.S_IWRITE | stat.S_IREAD)


def test_top_5_scores_and_name_validation(tmp_path, monkeypatch, capsys):
  q_path = tmp_path / "pytania.txt"
  s_path = tmp_path / "wyniki.txt"
  q_path.write_text(VALID_QUESTION * 3, encoding="utf-8")
  s_path.write_text("A\t10\nB\t8\nC\t6\nD\t4\nE\t1\n", encoding="utf-8")

  # Zdobywamy 2 pkt (wchodzi za E: 1):
  # "C", "C", "A" (błąd -> koniec gry z wynikiem 2)
  # Imię: "" (błąd), "Jan Nowak" (błąd), "Maks" (ok) -> Menu: "3" (wyjście)
  inputs = iter(["C", "C", "A", "", "Jan Nowak", "Maks", "3"])
  monkeypatch.setattr("builtins.input", lambda: next(inputs))

  quiz.main(["-q", str(q_path), "-s", str(s_path)])
  out = capsys.readouterr().out

  assert out.count("Podane imię zawiera niedozwolony znak.") == 2
  saved = file_io.load_scores(s_path)
  assert len(saved) == 5
  assert saved == [("A", 10), ("B", 8), ("C", 6), ("D", 4), ("Maks", 2)]
