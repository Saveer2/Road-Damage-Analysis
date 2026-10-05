from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LABEL_DIR = BASE_DIR / "road_dataset" / "labels-YOLO"

files_modified = 0
invalid_removed = 0

for label_path in LABEL_DIR.glob("*.txt"):
    valid_lines = []
    file_invalid = 0

    with open(label_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split()

        if len(parts) != 5:
            file_invalid += 1
            continue

        try:
            class_id = int(parts[0])
            x = float(parts[1])
            y = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])
        except ValueError:
            file_invalid += 1
            continue

        if class_id not in [0, 1, 2]:
            file_invalid += 1
            continue

        if not (0 <= x <= 1 and 0 <= y <= 1):
            file_invalid += 1
            continue

        if width <= 0 or height <= 0:
            file_invalid += 1
            continue

        if width > 1 or height > 1:
            file_invalid += 1
            continue

        valid_lines.append(line)

    if file_invalid > 0:
        with open(label_path, "w") as f:
            f.writelines(valid_lines)

        files_modified += 1
        invalid_removed += file_invalid

print(f"Files modified: {files_modified}")
print(f"Invalid annotations removed: {invalid_removed}")