from pathlib import Path
from collections import Counter
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "road_dataset"

IMAGE_DIR = DATASET_DIR / "images"
LABEL_DIR = DATASET_DIR / "labels"
YOLO_LABEL_DIR = DATASET_DIR / "labels-YOLO"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
LABEL_EXTENSIONS = {".txt", ".xml", ".json"}

def get_files(directory, extensions):
    if not directory.exists():
        return []
    return [
        file for file in directory.rglob("*")
        if file.is_file() and file.suffix.lower() in extensions
    ]

def analyze_images():
    images = get_files(IMAGE_DIR, IMAGE_EXTENSIONS)

    valid = 0
    corrupt = 0
    sizes = Counter()

    for image_path in images:
        try:
            with Image.open(image_path) as image:
                image.verify()

            with Image.open(image_path) as image:
                sizes[image.size] += 1

            valid += 1

        except Exception:
            corrupt += 1

    print("\nIMAGE ANALYSIS ")
    print(f"Total images: {len(images)}")
    print(f"Valid images: {valid}")
    print(f"Corrupt images: {corrupt}")

    print("\nImage sizes:")
    for size, count in sizes.most_common():
        print(f"{size[0]} x {size[1]} : {count}")

    return images

def analyze_labels(label_dir):
    labels = get_files(label_dir, LABEL_EXTENSIONS)

    print("\nLABEL ANALYSIS")
    print(f"Directory: {label_dir}")
    print(f"Total label files: {len(labels)}")

    extensions = Counter(file.suffix.lower() for file in labels)

    print("\nLabel formats:")
    for extension, count in extensions.items():
        print(f"{extension}: {count}")

    return labels

def match_images_labels(images, labels):
    image_stems = {file.stem for file in images}
    label_stems = {file.stem for file in labels}

    missing_labels = image_stems - label_stems
    missing_images = label_stems - image_stems

    print("\nIMAGE-LABEL MATCHING ")
    print(f"Images without labels: {len(missing_labels)}")
    print(f"Labels without images: {len(missing_images)}")

    if missing_labels:
        print("\nImages without labels:")
        for name in sorted(missing_labels):
            print(name)

    if missing_images:
        print("\nLabels without images:")
        for name in sorted(missing_images):
            print(name)

def analyze_yolo_labels():
    labels = get_files(YOLO_LABEL_DIR, {".txt"})

    class_counts = Counter()
    total_boxes = 0
    invalid_lines = 0
    empty_files = 0

    for label_path in labels:
        try:
            lines = label_path.read_text(encoding="utf-8").splitlines()

            if not lines:
                empty_files += 1
                continue

            for line in lines:
                values = line.strip().split()

                if len(values) != 5:
                    invalid_lines += 1
                    continue

                try:
                    class_id = int(values[0])
                    coordinates = [float(value) for value in values[1:]]

                    if not all(0 <= value <= 1 for value in coordinates):
                        invalid_lines += 1
                        continue

                    if coordinates[2] <= 0 or coordinates[3] <= 0:
                        invalid_lines += 1
                        continue

                    class_counts[class_id] += 1
                    total_boxes += 1

                except ValueError:
                    invalid_lines += 1

        except Exception:
            invalid_lines += 1

    print("\nYOLO LABEL ANALYSIS ")
    print(f"YOLO label files: {len(labels)}")
    print(f"Total bounding boxes: {total_boxes}")
    print(f"Invalid annotation lines: {invalid_lines}")
    print(f"Empty label files: {empty_files}")

    print("\nClass distribution:")
    for class_id, count in sorted(class_counts.items()):
        print(f"Class {class_id}: {count}")

def main():
    print("       ROAD DAMAGE DATASET ANALYSIS")
 
    print(f"\nDataset path: {DATASET_DIR}")

    if not DATASET_DIR.exists():
        print("\nERROR: road_dataset folder was not found.")
        return

    images = analyze_images()

    labels = analyze_labels(LABEL_DIR)

    match_images_labels(images, labels)

    analyze_yolo_labels()

    print("\nANALYSIS COMPLETE ")

if __name__ == "__main__":
    main()