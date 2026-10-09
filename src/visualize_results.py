from pathlib import Path
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "models" / "evaluation" / "test_evaluation"

image_files = sorted(
    list(RESULTS_DIR.glob("*.png")) +
    list(RESULTS_DIR.glob("*.jpg"))
)

if not image_files:
    print(f"No visualization images found in: {RESULTS_DIR}")
else:
    print(f"Found {len(image_files)} visualization images.")

    for image_path in image_files:
        image = plt.imread(image_path)
        plt.figure(figsize=(12, 8))
        plt.imshow(image)
        plt.title(image_path.name)
        plt.axis("off")
        plt.tight_layout()
        plt.show()