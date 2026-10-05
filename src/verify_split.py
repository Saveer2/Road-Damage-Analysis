from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "processed_dataset"

class_names = {
    0: "Pothole",
    1: "Crack",
    2: "Manhole"
}

total_images = 0
total_boxes = 0
all_image_names = []
split_counts = {}

for split in ["train", "val", "test"]:
    image_dir = DATASET_DIR / "images" / split
    label_dir = DATASET_DIR / "labels" / split

    images = list(image_dir.glob("*"))
    labels = list(label_dir.glob("*.txt"))

    image_names = {
        image.stem
        for image in images
        if image.suffix.lower() in [".jpg", ".jpeg", ".png"]
    }

    label_names = {
        label.stem
        for label in labels
    }

    missing_labels = image_names - label_names
    missing_images = label_names - image_names

    class_counts = Counter()
    box_count = 0

    for label_path in labels:
        with open(label_path, "r") as f:
            for line in f:
                parts = line.strip().split()

                if len(parts) != 5:
                    continue

                class_id = int(parts[0])
                class_counts[class_id] += 1
                box_count += 1

    split_counts[split] = len(image_names)
    total_images += len(image_names)
    total_boxes += box_count
    all_image_names.extend(
        f"{split}/{name}" for name in image_names
    )

    print(f"{split}:")
    print(f"Images: {len(image_names)}")
    print(f"Labels: {len(labels)}")
    print(f"Bounding boxes: {box_count}")
    print(f"Pothole: {class_counts[0]}")
    print(f"Crack: {class_counts[1]}")
    print(f"Manhole: {class_counts[2]}")
    print(f"Missing labels: {len(missing_labels)}")
    print(f"Missing images: {len(missing_images)}")
    print()

duplicates = len(all_image_names) - len(set(all_image_names))

print(f"Total images: {total_images}")
print(f"Total bounding boxes: {total_boxes}")
print(f"Duplicate images across splits: {duplicates}")