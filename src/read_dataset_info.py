from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
README_PATH = BASE_DIR / "road_dataset" / "README.md"

text = README_PATH.read_text(encoding="utf-8")

print(text)
