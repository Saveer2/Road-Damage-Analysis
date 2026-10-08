from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR / "utils"))

from video_processor import create_video_from_frames

INPUT_FRAMES = BASE_DIR / "models" / "inference_results" / "test_predictions"
OUTPUT_VIDEO = BASE_DIR / "models" / "inference_results" / "test_output.mp4"

create_video_from_frames(
    INPUT_FRAMES,
    OUTPUT_VIDEO,
    fps=10
)