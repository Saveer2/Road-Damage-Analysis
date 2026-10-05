from pathlib import Path
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_YAML = BASE_DIR / "processed_dataset" / "data.yaml"
MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(exist_ok=True)

model = YOLO("yolo11n.pt")

if __name__ == "__main__":
    model.train(
        data=str(DATASET_YAML),
        epochs=100,
        imgsz=640,
        batch=16,
        workers=0,
        device=0,
        project=str(MODEL_DIR),
        name="road_damage_detector"
    )