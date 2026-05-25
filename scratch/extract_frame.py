import av
import sys
from PIL import Image

def extract(video_path, time_sec, out_path):
    container = av.open(video_path)
    stream = container.streams.video[0]
    # Set time base
    tb = stream.time_base
    pts = int(time_sec / tb)
    # Seek to nearest keyframe
    container.seek(pts, stream=stream)
    for frame in container.decode(video=0):
        # We check the frame time
        frame_time = float(frame.pts * tb)
        if frame_time >= time_sec:
            img = frame.to_image()
            img.save(out_path)
            print(f"Saved frame at {frame_time:.2f}s to {out_path}")
            break
    container.close()

if __name__ == "__main__":
    extract(
        r"media/videos/scene05_correlation/480p15/Scene05Correlation.mp4",
        58.0,
        r"scratch/frame_58s.png"
    )
