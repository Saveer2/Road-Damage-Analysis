
import cv2
from pathlib import Path


def extract_frames(video_path, output_folder, frame_interval=5):

    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print("FPS:", fps)
    print("Total Frames:", total_frames)

    frame_number = 0
    saved_count = 0

    while True:

        success, frame = cap.read()

        if not success:
            break

        if frame_number % frame_interval == 0:

            filename = output_folder / f"frame_{saved_count:05d}.jpg"

            cv2.imwrite(str(filename), frame)

            saved_count += 1

        frame_number += 1

    cap.release()

    print("Extracted Frames:", saved_count)




video_path = "uploads/videos/test.mp4"
output_folder = "frames/extracted"

extract_frames(
    video_path,
    output_folder,
    frame_interval=5
)

