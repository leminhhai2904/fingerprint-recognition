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
    video = r"media/videos/scene06_minutiae_new/480p15/Scene06Minutiae.mp4"
    extract(video, 9.0, r"scratch/frame_scene06_zoom_fixed.png")
    extract(video, 35.5, r"scratch/frame_scene06_local_fixed.png")
    extract(video, 55.0, r"scratch/frame_scene06_tessellation_fixed.png")
    extract(video, 65.0, r"scratch/frame_scene06_hybrid_fixed.png")
