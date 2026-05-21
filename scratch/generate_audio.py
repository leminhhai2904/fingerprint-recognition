import os
import re
import sys
import subprocess
import argparse
import asyncio
import time

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Package '{package}' not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Ensure edge-tts, mutagen, and imageio-ffmpeg are installed
install_and_import("edge_tts")
install_and_import("mutagen")
install_and_import("imageio-ffmpeg")

import imageio_ffmpeg
from mutagen.mp3 import MP3
from edge_tts import Communicate

# Fix Windows console encoding for print statements
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()

def parse_script_segments(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    parts = content.split("--- [")
    segments = []
    
    for part in parts:
        if not part.strip():
            continue
        lines = part.split("\n")
        header = lines[0].split("]")[0].strip() # e.g. "ĐOẠN 1: Tiêu đề mở đầu"
        
        text_lines = []
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            if line.startswith("("):
                continue
            # Try to match text inside quotes
            match = re.search(r'["“]([^"”]+)["”]', line)
            if match:
                text_lines.append(match.group(1))
            else:
                text_lines.append(line)
        
        if text_lines:
            text = " ".join(text_lines)
            text = text.strip('"').strip('“').strip('”').strip()
            segments.append({
                "header": header,
                "text": text
            })
    return segments

async def generate_voice_segment(text, output_path, voice="vi-VN-NamMinhNeural", rate="+0%"):
    # Normalize special characters that might cause edge-tts API issues
    text = text.replace("–", "-").replace("—", "-")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("‘", "'").replace("’", "'")
    
    max_retries = 5
    for attempt in range(1, max_retries + 1):
        try:
            communicate = Communicate(text, voice, rate=rate)
            await communicate.save(output_path)
            return True
        except Exception as e:
            print(f"  Attempt {attempt} failed with error: {e}")
            if attempt < max_retries:
                await asyncio.sleep(3)
            else:
                raise e
    return False

def generate_silence_mp3(duration_seconds, output_path):
    cmd = [
        FFMPEG_PATH, "-y",
        "-f", "lavfi",
        "-i", f"anullsrc=r=24000:cl=mono", # Match edge-tts default sample rate/layout
        "-t", f"{duration_seconds}",
        output_path
    ]
    # Run silently
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def concatenate_audios_ffmpeg(inputs, output_path):
    # inputs is a list of file paths
    # We use the filter complex of ffmpeg to concat them
    cmd = [FFMPEG_PATH, "-y"]
    for inp in inputs:
        cmd.extend(["-i", inp])
    
    filter_complex = "".join(f"[{i}:a]" for i in range(len(inputs)))
    filter_complex += f"concat=n={len(inputs)}:v=0:a=1[a]"
    
    cmd.extend([
        "-filter_complex", filter_complex,
        "-map", "[a]",
        output_path
    ])
    
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def main():
    parser = argparse.ArgumentParser(description="Generate high-quality Vietnamese TTS voiceover segments and concatenate them.")
    parser.add_argument("script_path", help="Path to the script text file (e.g., dist/script_scene01.txt)")
    parser.add_argument("--voice", default="vi-VN-NamMinhNeural", help="Voice model (default: vi-VN-NamMinhNeural)")
    parser.add_argument("--rate", default="+23%", help="Speaking rate adjustment (e.g. +15%%, +25%%). Default: +23%")
    parser.add_argument("--silence-gap", type=float, default=0.8, help="Silence gap between segments in seconds (default: 0.8)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.script_path):
        print(f"File not found: {args.script_path}")
        sys.exit(1)
        
    script_dir = os.path.dirname(args.script_path)
    base_name = os.path.splitext(os.path.basename(args.script_path))[0]
    
    # Create segment output folder
    segments_dir = os.path.join(script_dir if script_dir else "dist", f"{base_name}_segments")
    os.makedirs(segments_dir, exist_ok=True)
    
    print(f"Parsing script: {args.script_path}...")
    segments = parse_script_segments(args.script_path)
    
    if not segments:
        print("No voiceover segments found in the script file.")
        sys.exit(1)
        
    silence_path = os.path.join(segments_dir, "silence_temp.mp3")
    generate_silence_mp3(args.silence_gap, silence_path)
    
    inputs_to_concat = []
    
    print(f"\n--- Voiceover Generation Report (Voice: {args.voice}) ---")
    
    for i, seg in enumerate(segments):
        seg_index = i + 1
        seg_filename = f"seg_{seg_index:02d}.mp3"
        seg_path = os.path.join(segments_dir, seg_filename)
        
        print(f"\nGenerating Segment {seg_index}: {seg['header']}...")
        print(f"Text: \"{seg['text']}\"")
        
        # Generate the audio file for this segment
        asyncio.run(generate_voice_segment(seg['text'], seg_path, voice=args.voice, rate=args.rate))
        
        # Load and measure duration using mutagen
        audio = MP3(seg_path)
        duration = audio.info.length
        print(f"-> Duration: {duration:.2f} seconds")
        
        seg["duration"] = duration
        
        if i > 0:
            inputs_to_concat.append(silence_path)
        inputs_to_concat.append(seg_path)
        
        # Tránh gửi request quá dồn dập làm lỗi API
        time.sleep(1.5)
    
    # Save combined audio
    out_name = base_name.replace("script_", "voice_") + ".mp3"
    output_path = os.path.join(script_dir if script_dir else "dist", out_name)
    
    print(f"\nConcatenating audio segments...")
    concatenate_audios_ffmpeg(inputs_to_concat, output_path)
    
    # Clean up silence file
    if os.path.exists(silence_path):
        os.remove(silence_path)
        
    combined_audio_info = MP3(output_path)
    print(f"Combined audio saved to: {output_path}")
    print(f"Total combined duration: {combined_audio_info.info.length:.2f} seconds")
    
    # Output the exact timing report for Manim configuration
    print("\n--- TIMINGS FOR MANIM CONFIGURATION ---")
    print("Use these exact durations to adjust wait times in your Manim python files:")
    print("-" * 60)
    for i, seg in enumerate(segments):
        print(f"Segment {i+1} ({seg['header']}): {seg['duration']:.2f}s")
    print("-" * 60)

if __name__ == "__main__":
    main()

# python scratch/generate_audio.py dist/script_scene01.txt