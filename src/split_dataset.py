from pathlib import Path
from collections import Counter
import random
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent

IMAGE_DIR = BASE_DIR / "road_dataset" / "images"
LABEL_DIR = BASE_DIR / "road_dataset" / "labels-YOLO"
OUTPUT_DIR = BASE_DIR / "processed_dataset"

random.seed(42)

split_names = ["train", "val", "test"]
ratios = {
    "train": 0.80,
    "val": 0.10,
    "test": 0.10
}

images = []

for image_path in IMAGE_DIR.iterdir():
    if image_path.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
        continue

    label_path = LABEL_DIR / f"{image_path.stem}.txt"

    if not label_path.exists():
        continue

    class_counts = Counter()

    with open(label_path, "r") as f:
        for line in f:
            parts = line.strip().split()

            if len(parts) != 5:
                continue

            class_id = int(parts[0])
            width = float(parts[3])
            height = float(parts[4])

            if width <= 0 or height <= 0:
                continue

            class_counts[class_id] += 1

    if sum(class_counts.values()) == 0:
        continue

    images.append((image_path, label_path, class_counts))

total_images = len(images)

target_sizes = {
    "train": int(total_images * 0.80),
    "val": int(total_images * 0.10),
    "test": int(total_images * 0.10)
}

target_sizes["train"] = (
    total_images
    - target_sizes["val"]
    - target_sizes["test"]
)

total_class_counts = Counter()

for _, _, counts in images:
    total_class_counts.update(counts)

target_class_counts = {
    split: {
        class_id: total_class_counts[class_id] * ratios[split]
        for class_id in total_class_counts
    }
    for split in split_names
}

random.shuffle(images)

images.sort(
    key=lambda item: (
        -sum(item[2].values()),
        -len(item[2])
    )
)

splits = {
    "train": [],
    "val": [],
    "test": []
}

split_sizes = {
    "train": 0,
    "val": 0,
    "test": 0
}

split_class_counts = {
    "train": Counter(),
    "val": Counter(),
    "test": Counter()
}

for image_path, label_path, class_counts in images:
    available_splits = [
        split
        for split in split_names
        if split_sizes[split] < target_sizes[split]
    ]

    def score(split):
        size_score = (
            target_sizes[split] - split_sizes[split]
        ) / target_sizes[split]

        class_score = 0

        for class_id, count in class_counts.items():
            target = target_class_counts[split][class_id]

            if target > 0:
                current = split_class_counts[split][class_id]
                class_score += (
                    max(target - current, 0) / target
                ) * count

        return class_score + size_score

    best_split = max(
        available_splits,
        key=score
    )

    splits[best_split].append(
        (image_path, label_path, class_counts)
    )

    split_sizes[best_split] += 1
    split_class_counts[best_split].update(class_counts)

if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)

for split in split_names:
    image_output = OUTPUT_DIR / "images" / split
    label_output = OUTPUT_DIR / "labels" / split

    image_output.mkdir(parents=True, exist_ok=True)
    label_output.mkdir(parents=True, exist_ok=True)

    for image_path, label_path, _ in splits[split]:
        shutil.copy2(
            image_path,
            image_output / image_path.name
        )

        shutil.copy2(
            label_path,
            label_output / label_path.name
        )

print(f"Total images: {total_images}")
print(f"Train images: {len(splits['train'])}")
print(f"Validation images: {len(splits['val'])}")
print(f"Test images: {len(splits['test'])}")