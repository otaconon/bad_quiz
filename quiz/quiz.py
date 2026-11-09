import argparse
import file_io
from game import game_create

def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(prog="quiz")
  parser.add_argument("-q", "--questions_path", type=str, default="pytania.txt")
  parser.add_argument("-s", "--scores_path", type=str, default="wyniki.txt")
  return parser

def main(argv: list[str] | None = None):
  parser = build_parser()
  args = parser.parse_args(argv)
  
  try: questions, err = file_io.load_questions(args.questions_path)
  except OSError: print("ERROR: Failed to open questions file: ", args.questions_path); exit(1)
    
  try: records = file_io.load_scores(args.scores_path)
  except PermissionError: print("ERROR: Couldnt't open records file, permission error: ", args.scores_path); exit(1)
  except ValueError: print("ERROR: Scores file has incorrect format: ", args.scores_path); exit(1)
  except OSError: print("ERROR: Scores file has incorrect format: ", args.scores_path); exit(1)
  
  if err != None: print("ERROR: ", err); exit(1)
  
  game = game_create(questions)
  score = game["play"]()
  
  if len(records)<5 or any(s < score for _, s in records):
    print("Prosze podac imie celem zapisania wyniku: ", end="")
    name = input()
    while not name or any(c.isspace() for c in name):
      print("Podane imię zawiera niedozwolony znak.")
      print("Prosze podac imie celem zapisania wyniku: ", end="")
      name = input()
    records.append((name, score))
  records.sort(key=lambda item: item[1], reverse=True)
  
  try: questions = file_io.write_scores(args.scores_path, records[:min(5, len(records))])
  except OSError: print("ERROR: Failed to write scores: ", args.scores_path); exit(1)

if __name__ == "__main__":
  main()