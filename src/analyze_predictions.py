from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent.parent

LABELS_DIR = BASE_DIR / "models" / "inference_results" / "test_predictions" / "labels"

CLASS_NAMES = {
    0: "Potholes",
    1: "Cracks",
    2: "Manholes"
}


def analyze_predictions():
    if not LABELS_DIR.exists():
        raise FileNotFoundError(f"Labels directory not found: {LABELS_DIR}")

    counts = Counter()
    total_detections = 0
    images_with_damage = 0

    label_files = list(LABELS_DIR.glob("*.txt"))

    for label_file in label_files:
        lines = label_file.read_text().strip().splitlines()

        if lines:
            images_with_damage += 1

        for line in lines:
            values = line.split()

            if not values:
                continue

            class_id = int(values[0])
            class_name = CLASS_NAMES.get(class_id, f"Class_{class_id}")

            counts[class_name] += 1
            total_detections += 1

    print()
    print("Road Damage Analysis")
    print("--------------------")
    print(f"Images processed: {len(label_files)}")
    print(f"Images with damage: {images_with_damage}")
    print(f"Total detections: {total_detections}")
    print()

    for class_name, count in counts.items():
        print(f"{class_name}: {count}")


if __name__ == "__main__":
    analyze_predictions()