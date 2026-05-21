import imageio_ffmpeg, subprocess
import os
import sys

def merge_assets(scene_list, filter_id=None):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    for scene in scene_list:
        # Neu co truyen so vao thi chi chay scene co output chua so do
        if filter_id and f"scene{filter_id:02d}" not in scene['output']:
            continue

        v_in = scene['video']
        a_in = scene['audio']
        out = scene['output']

        if not os.path.exists(v_in) or not os.path.exists(a_in):
            print(f"Can not find files for: {out}")
            continue

        cmd = [
            ffmpeg, '-y',
            '-i', v_in,
            '-i', a_in,
            '-c:v', 'copy',
            '-c:a', 'aac', '-b:a', '192k',
            '-shortest',
            out
        ]

        print(f"Processing: {out}...")
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

        if result.returncode == 0:
            print(f"Done -> {out}")
        else:
            print(f"Error at {out}: {result.stderr[-200:]}")

# Danh sach cac scene can gop
scenes_to_merge = [
    {
        "video": "media/videos/scene01_intro/480p15/Scene01Intro.mp4",
        "audio": "dist/audio/audio_scene_1.mp3",
        "output": "dist/scene01_final.mp4"
    },
    {
        "video": "media/videos/scene02_sensing/480p15/Scene02Sensing.mp4",
        "audio": "dist/audio/audio_scene_2.mp3",
        "output": "dist/scene02_final.mp4"
    },
    {
        "video": "media/videos/scene03_features/480p15/Scene03Features.mp4",
        "audio": "dist/audio/audio_scene_3.mp3",
        "output": "dist/scene03_final.mp4"
    },
    {
        "video": "media/videos/scene04_extraction/480p15/Scene04Extraction.mp4",
        "audio": "dist/audio/audio_scene_4.mp3",
        "output": "dist/scene04_final.mp4"
    },
    {
        "video": "media/videos/scene05_correlation/480p15/Scene05Correlation.mp4",
        "audio": "dist/audio/audio_scene_5.mp3",
        "output": "dist/scene05_final.mp4"
    },
    {
        "video": "media/videos/scene06_minutiae/480p15/Scene06Minutiae.mp4",
        "audio": "dist/audio/audio_scene_6.mp3",
        "output": "dist/scene06_final.mp4"
    },
    {
        "video": "media/videos/scene07_conclusion/480p15/Scene07Conclusion.mp4",
        "audio": "dist/audio/audio_scene_7.mp3",
        "output": "dist/scene07_final.mp4"
    }
]

if __name__ == "__main__":
    # Lay so tu dong lenh neu co (vi du: 1)
    target_id = None
    if len(sys.argv) > 1:
        target_id = int(sys.argv[1])

    merge_assets(scenes_to_merge, target_id)

# uv run python scratch/merge_video_audio.py 2