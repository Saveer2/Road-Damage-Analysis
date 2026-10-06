from pathlib import Path
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "road_damage_detector-4" / "weights" / "best.pt"
DATASET_YAML = BASE_DIR / "processed_dataset" / "data.yaml"
RESULTS_DIR = BASE_DIR / "models"

model = YOLO(str(MODEL_PATH))

if __name__ == "__main__":
    model.val(
        data=str(DATASET_YAML),
        split="test",
        imgsz=640,
        batch=16,
        workers=0,
        device=0,
        project=str(RESULTS_DIR),
        name="road_damage_test_evaluation"
    )