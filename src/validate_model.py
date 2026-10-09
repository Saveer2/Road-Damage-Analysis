from pathlib import Path
from ultralytics import YOLO


def main():
    base_dir = Path(__file__).resolve().parent.parent

    model_path = base_dir / "models" / "road_damage_detector-4" / "weights" / "best.pt"
    data_yaml = base_dir / "processed_dataset" / "data.yaml"
    output_dir = base_dir / "models" / "evaluation"

    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")

    if not data_yaml.exists():
        raise FileNotFoundError(f"Dataset configuration not found: {data_yaml}")

    model = YOLO(str(model_path))

    metrics = model.val(
        data=str(data_yaml),
        split="test",
        imgsz=640,
        conf=0.001,
        iou=0.6,
        workers=0,
        plots=True,
        device=0,
        project=str(output_dir),
        name="test_evaluation",
        exist_ok=True
    )

    print("\nTest Evaluation Results")
    print(f"Precision: {metrics.box.mp:.4f}")
    print(f"Recall: {metrics.box.mr:.4f}")
    print(f"mAP@0.5: {metrics.box.map50:.4f}")
    print(f"mAP@0.5:0.95: {metrics.box.map:.4f}")
    print(f"Results saved to: {output_dir / 'test_evaluation'}")


if __name__ == "__main__":
    main()