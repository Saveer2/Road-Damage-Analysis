from pathlib import Path
from collections import Counter
import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = BASE_DIR / "road_dataset" / "images"
LABEL_DIR = BASE_DIR / "road_dataset" / "labels-YOLO"

class_names = {
    0: "Pothole",
    1: "Crack",
    2: "Manhole"
}

class_counts = Counter()
objects_per_image = []
box_widths = []
box_heights = []
box_areas = []
class_images = Counter()

image_count = 0
label_count = 0

for image_path in IMAGE_DIR.glob("*"):
    if image_path.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
        continue

    image_count += 1

    label_path = LABEL_DIR / f"{image_path.stem}.txt"

    if not label_path.exists():
        continue

    label_count += 1

    image_classes = set()
    object_count = 0

    with open(label_path, "r") as f:
        for line in f:
            parts = line.strip().split()

            if len(parts) != 5:
                continue

            class_id = int(parts[0])
            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])

            class_counts[class_id] += 1
            image_classes.add(class_id)

            box_widths.append(width)
            box_heights.append(height)
            box_areas.append(width * height)

            object_count += 1

    objects_per_image.append(object_count)

    for class_id in image_classes:
        class_images[class_id] += 1

print(f"Images: {image_count}")
print(f"Images with labels: {label_count}")
print()

print("Class distribution:")
for class_id in sorted(class_names):
    print(f"{class_names[class_id]}: {class_counts[class_id]}")

print()

print("Images containing each class:")
for class_id in sorted(class_names):
    print(f"{class_names[class_id]}: {class_images[class_id]}")

print()

print("Objects per image:")
print(f"Minimum: {min(objects_per_image)}")
print(f"Maximum: {max(objects_per_image)}")
print(f"Average: {np.mean(objects_per_image):.2f}")

print()

print("Bounding box statistics:")
print(f"Average width: {np.mean(box_widths):.4f}")
print(f"Average height: {np.mean(box_heights):.4f}")
print(f"Minimum width: {np.min(box_widths):.4f}")
print(f"Minimum height: {np.min(box_heights):.4f}")
print(f"Maximum width: {np.max(box_widths):.4f}")
print(f"Maximum height: {np.max(box_heights):.4f}")

print()

print("Bounding box area:")
print(f"Minimum: {np.min(box_areas):.6f}")
print(f"Maximum: {np.max(box_areas):.6f}")
print(f"Average: {np.mean(box_areas):.6f}")