import cv2
from pathlib import Path


def extract_frames(video_path, output_folder, frame_interval=5):
    

    video_path = Path(video_path)
    output_folder = Path(output_folder)

    output_folder.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise ValueError("Could not open video.")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"FPS: {fps}")
    print(f"Total frames: {total_frames}")

    frame_number = 0
    saved_count = 0

    extracted_frames = []

    while True:

        success, frame = cap.read()

        if not success:
            break

        if frame_number % frame_interval == 0:

            filename = output_folder / f"frame_{saved_count:05d}.jpg"

            cv2.imwrite(str(filename), frame)

            extracted_frames.append(str(filename))

            saved_count += 1

        frame_number += 1

    cap.release()

    print(f"Extracted {saved_count} frames.")

    return extracted_frames