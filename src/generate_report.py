from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent

LABELS_DIR = BASE_DIR / "models" / "inference_results" / "test_predictions" / "labels"
REPORT_PATH = BASE_DIR / "models" / "inference_results" / "test_report.json"

CLASS_NAMES = {
    0: "Potholes",
    1: "Cracks",
    2: "Manholes"
}


def generate_report():
    if not LABELS_DIR.exists():
        raise FileNotFoundError(f"Labels directory not found: {LABELS_DIR}")

    detections = []
    class_counts = {}

    label_files = sorted(LABELS_DIR.glob("*.txt"))

    for label_file in label_files:
        image_detections = []

        lines = label_file.read_text().strip().splitlines()

        for line in lines:
            values = line.split()

            if len(values) < 6:
                continue

            class_id = int(values[0])
            x_center = float(values[1])
            y_center = float(values[2])
            width = float(values[3])
            height = float(values[4])
            confidence = float(values[5])

            class_name = CLASS_NAMES.get(
                class_id,
                f"Class_{class_id}"
            )

            detection = {
                "class_id": class_id,
                "class_name": class_name,
                "confidence": confidence,
                "bounding_box": {
                    "x_center": x_center,
                    "y_center": y_center,
                    "width": width,
                    "height": height
                }
            }

            image_detections.append(detection)

            class_counts[class_name] = class_counts.get(
                class_name,
                0
            ) + 1

        if image_detections:
            detections.append({
                "image": label_file.stem + ".jpg",
                "detections": image_detections
            })

    report = {
        "total_images": len(label_files),
        "images_with_damage": len(detections),
        "total_detections": sum(class_counts.values()),
        "class_counts": class_counts,
        "detections": detections
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(REPORT_PATH, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print(f"Report generated: {REPORT_PATH}")


if __name__ == "__main__":
    generate_report()