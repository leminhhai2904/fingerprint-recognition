import imageio_ffmpeg, subprocess

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

cmd = [
    ffmpeg, '-y',
    '-i', 'media/videos/scene01_intro/480p15/Scene01Intro.mp4',
    '-i', 'dist/voice_scene01.mp3',
    '-c:v', 'copy',
    '-c:a', 'aac', '-b:a', '192k',
    '-shortest',
    'dist/scene01_final.mp4'
]
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    print('Merged OK -> dist/scene01_final.mp4')
else:
    print('Error:', result.stderr[-500:])

# uv run python scratch/merge_video_audio.py