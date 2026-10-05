from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = BASE_DIR / "road_dataset" / "images"
LABEL_DIR = BASE_DIR / "road_dataset" / "labels-YOLO"

sample_name = "vlcsnap-00058"

print("SAMPLE INSPECTION")

images = [
    file for file in IMAGE_DIR.rglob("*")
    if file.is_file() and file.stem == sample_name
]

labels = [
    file for file in LABEL_DIR.rglob("*")
    if file.is_file() and file.stem == sample_name
]

print("\nImages found:")

for image in images:
    print(image)

print("\nLabels found:")

for label in labels:
    print(label)

    print("\nAnnotations:")

    lines = label.read_text(encoding="utf-8").splitlines()

    for number, line in enumerate(lines, start=1):
        print(f"Line {number}: {line}")

