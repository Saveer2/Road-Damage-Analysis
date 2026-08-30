from utils.video_processor import extract_frames


video_path = "uploads/videos/test.mp4"

output_folder = "frames/extracted"

frames = extract_frames(
    video_path,
    output_folder,
    frame_interval=5
)

print("\nFirst 5 extracted frames:")

for frame in frames[:5]:
    print(frame)