from pathlib import Path
import cv2
import random

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = BASE_DIR / "road_dataset" / "images"
LABEL_DIR = BASE_DIR / "road_dataset" / "labels-YOLO"
OUTPUT_DIR = BASE_DIR / "road_dataset" / "visualized"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class_names = {
    0: "class_0",
    1: "class_1",
    2: "class_2"
}

images = [
    file for file in IMAGE_DIR.rglob("*")
    if file.is_file() and file.suffix.lower() in {".jpg", ".jpeg", ".png"}
]

random.seed(42)

sample_size = min(20, len(images))
selected_images = random.sample(images, sample_size)

for image_path in selected_images:
    label_path = LABEL_DIR / f"{image_path.stem}.txt"

    image = cv2.imread(str(image_path))

    if image is None:
        continue

    height, width = image.shape[:2]

    if not label_path.exists():
        continue

    lines = label_path.read_text(encoding="utf-8").splitlines()

    for line in lines:
        values = line.strip().split()

        if len(values) != 5:
            continue

        class_id = int(values[0])
        x_center = float(values[1])
        y_center = float(values[2])
        box_width = float(values[3])
        box_height = float(values[4])

        x_center *= width
        y_center *= height
        box_width *= width
        box_height *= height

        x1 = int(x_center - box_width / 2)
        y1 = int(y_center - box_height / 2)
        x2 = int(x_center + box_width / 2)
        y2 = int(y_center + box_height / 2)

        x1 = max(0, min(x1, width - 1))
        y1 = max(0, min(y1, height - 1))
        x2 = max(0, min(x2, width - 1))
        y2 = max(0, min(y2, height - 1))

        label = class_names.get(class_id, f"class_{class_id}")

        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            (255, 255, 255),
            2
        )

        cv2.putText(
            image,
            label,
            (x1, max(y1 - 8, 15)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

    output_path = OUTPUT_DIR / image_path.name
    cv2.imwrite(str(output_path), image)


print("ANNOTATION VISUALIZATION COMPLETE")
print(f"Images visualized: {sample_size}")
print(f"Output directory: {OUTPUT_DIR}")
