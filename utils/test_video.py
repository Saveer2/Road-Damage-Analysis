from pathlib import Path
from video_processor import extract_frames
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR / "src"))

from inference import run_inference

VIDEO_PATH = BASE_DIR / "uploads" / "videos" / "test.mp4"
FRAMES_DIR = BASE_DIR / "frames" / "extracted"


if __name__ == "__main__":
    frames = extract_frames(
        VIDEO_PATH,
        FRAMES_DIR,
        frame_interval=5
    )

    print(f"Frames extracted: {len(frames)}")

    results_dir = run_inference(
        FRAMES_DIR,
        output_name="video_predictions"
    )

    print("Video frame inference completed.")
    print(f"Results saved to: {results_dir}")
