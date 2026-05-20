import os
import sys
import subprocess
import argparse
from pathlib import Path

# Config
SCENES = [
    ("scenes/scene01_intro.py", "Scene01Intro", "scene01_intro"),
    ("scenes/scene02_sensing.py", "Scene02Sensing", "scene02_sensing"),
    ("scenes/scene03_features.py", "Scene03Features", "scene03_features"),
    ("scenes/scene04_extraction.py", "Scene04Extraction", "scene04_extraction"),
    ("scenes/scene05_correlation.py", "Scene05Correlation", "scene05_correlation"),
    ("scenes/scene06_minutiae.py", "Scene06Minutiae", "scene06_minutiae"),
    ("scenes/scene07_conclusion.py", "Scene07Conclusion", "scene07_conclusion"),
]

QUALITY_MAP = {
    "low": {"flag": "-ql", "folder": "480p15"},
    "medium": {"flag": "-qm", "folder": "720p30"},
    "high": {"flag": "-qh", "folder": "1080p60"},
    "4k": {"flag": "-qk", "folder": "2160p60"},
}

def get_python_exe():
    """Find local virtual env python or system python."""
    venv_python = Path(".venv") / "Scripts" / "python.exe" if os.name == "nt" else Path(".venv") / "bin" / "python"
    if venv_python.exists():
        return str(venv_python)
    return sys.executable

def main():
    parser = argparse.ArgumentParser(description="Render and merge all 7 fingerprint recognition scenes.")
    parser.add_argument(
        "--quality", 
        choices=["low", "medium", "high", "4k"], 
        default="medium", 
        help="Rendering quality (default: medium)"
    )
    parser.add_argument(
        "--skip-render", 
        action="store_true", 
        help="Skip rendering and only merge existing files"
    )
    parser.add_argument(
        "--output", 
        default="dist/fingerprint_recognition_full.mp4", 
        help="Path to final output video"
    )
    
    args = parser.parse_args()
    quality_conf = QUALITY_MAP[args.quality]
    python_exe = get_python_exe()
    
    # 1. Rendering
    if not args.skip_render:
        print(f"=== Rendering all scenes in {args.quality} quality ===")
        for i, (file_path, class_name, _) in enumerate(SCENES, 1):
            print(f"\n[{i}/{len(SCENES)}] Rendering {class_name} ({file_path})...")
            cmd = [python_exe, "-m", "manim", quality_conf["flag"], file_path, class_name]
            result = subprocess.run(cmd)
            if result.returncode != 0:
                print(f"Error rendering {class_name}. Exiting.")
                sys.exit(1)
        print("\nAll scenes rendered successfully!\n")
        
    # 2. Collect files and check existence
    video_paths = []
    missing_files = []
    print("=== Checking rendered files ===")
    for _, class_name, folder_name in SCENES:
        video_path = Path("media") / "videos" / folder_name / quality_conf["folder"] / f"{class_name}.mp4"
        if not video_path.exists():
            missing_files.append(str(video_path))
        else:
            video_paths.append(video_path.resolve())
            print(f"Found: {video_path}")
            
    if missing_files:
        print("\nError: The following video files are missing. Please run again without --skip-render:")
        for path in missing_files:
            print(f" - {path}")
        sys.exit(1)
        
    # 3. Merge files using ffmpeg
    print(f"\n=== Merging {len(video_paths)} scenes into {args.output} ===")
    
    # Create dist directory
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write concat list
    concat_list_file = Path("temp_concat_list.txt")
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for path in video_paths:
            # ffmpeg concat needs forward slashes even on Windows
            normalized_path = str(path).replace("\\", "/")
            f.write(f"file '{normalized_path}'\n")
            
    try:
        try:
            import imageio_ffmpeg
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        except ImportError:
            ffmpeg_exe = "ffmpeg"
            print("Warning: imageio_ffmpeg not found. Assuming ffmpeg is in PATH.")

        ffmpeg_cmd = [
            ffmpeg_exe,
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_list_file),
            "-c", "copy",
            "-y",
            str(output_path)
        ]
        
        print("Running ffmpeg command...")
        result = subprocess.run(ffmpeg_cmd)
        if result.returncode == 0:
            print(f"\nSUCCESS! Combined video saved to: {output_path.resolve()}")
        else:
            print("\nError: FFMPEG failed to merge the video files.")
    finally:
        # Clean up temp file
        if concat_list_file.exists():
            concat_list_file.unlink()

if __name__ == "__main__":
    main()
