from pathlib import Path
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "road_damage_detector-4" / "weights" / "best.pt"
OUTPUT_DIR = BASE_DIR / "models" / "inference_results"

model = YOLO(str(MODEL_PATH))


def run_inference(source, output_name="predictions"):
    source = Path(source)

    if not source.exists():
        raise FileNotFoundError(f"Source not found: {source}")

    output_dir = OUTPUT_DIR / output_name
    output_dir.mkdir(parents=True, exist_ok=True)

    model.predict(
        source=str(source),
        imgsz=640,
        conf=0.25,
        save=True,
        save_txt=True,
        project=str(OUTPUT_DIR),
        name=output_name,
        exist_ok=True,
        device=0
    )

    return output_dir


if __name__ == "__main__":
    TEST_IMAGES = BASE_DIR / "processed_dataset" / "images" / "test"

    results_dir = run_inference(
        TEST_IMAGES,
        output_name="test_predictions"
    )

    print(f"Inference completed.")
    print(f"Results saved to: {results_dir}")