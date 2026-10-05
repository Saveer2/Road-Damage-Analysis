from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LABEL_DIR = BASE_DIR / "road_dataset" / "labels-YOLO"

invalid_count = 0

for label_path in LABEL_DIR.rglob("*.txt"):
    try:
        lines = label_path.read_text(encoding="utf-8").splitlines()

        for line_number, line in enumerate(lines, start=1):
            values = line.strip().split()

            if len(values) != 5:
                print(f"\nInvalid annotation:")
                print(f"File: {label_path}")
                print(f"Line: {line_number}")
                print(f"Content: {line}")
                print(f"Reason: Expected 5 values, found {len(values)}")
                invalid_count += 1
                continue

            try:
                class_id = int(values[0])
                x_center = float(values[1])
                y_center = float(values[2])
                width = float(values[3])
                height = float(values[4])

                if class_id < 0:
                    print(f"\nInvalid annotation:")
                    print(f"File: {label_path}")
                    print(f"Line: {line_number}")
                    print(f"Content: {line}")
                    print("Reason: Negative class ID")
                    invalid_count += 1

                elif not all(0 <= value <= 1 for value in [x_center, y_center, width, height]):
                    print(f"\nInvalid annotation:")
                    print(f"File: {label_path}")
                    print(f"Line: {line_number}")
                    print(f"Content: {line}")
                    print("Reason: Coordinate outside 0-1 range")
                    invalid_count += 1

                elif width <= 0 or height <= 0:
                    print(f"\nInvalid annotation:")
                    print(f"File: {label_path}")
                    print(f"Line: {line_number}")
                    print(f"Content: {line}")
                    print("Reason: Width or height is zero/negative")
                    invalid_count += 1

            except ValueError:
                print(f"\nInvalid annotation:")
                print(f"File: {label_path}")
                print(f"Line: {line_number}")
                print(f"Content: {line}")
                print("Reason: Non-numeric value")
                invalid_count += 1

    except Exception as error:
        print(f"\nCould not read: {label_path}")
        print(f"Error: {error}")

print("\n========================================")
print(f"Total invalid annotations: {invalid_count}")
