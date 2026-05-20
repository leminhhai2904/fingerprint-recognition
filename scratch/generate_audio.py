import os
import re
import sys
import subprocess
import argparse

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Package '{package}' not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Ensure edge-tts is installed
install_and_import("edge_tts")
import asyncio
from edge_tts import Communicate

# Fix Windows console encoding for print statements
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def extract_script_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    script_content = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Skip titles, comments, headers
        if line.startswith("---") or line.startswith("(") or "kịch bản" in line.lower() or "voiceover" in line.lower():
            continue
        # Remove surrounding quotes if they exist
        if (line.startswith('"') and line.endswith('"')) or (line.startswith('“') and line.endswith('”')):
            line = line[1:-1]
        script_content.append(line)
    
    return " ".join(script_content)

async def generate_voice(text, output_path, voice="vi-VN-NamMinhNeural", rate="+0%", pitch="+0Hz"):
    """
    vi-VN-NamMinhNeural is a high-quality Vietnamese male neural voice.
    Rate modifies speed (e.g. '+10%', '-10%').
    Pitch modifies pitch (e.g. '+5Hz', '-5Hz', '+5%', '-5%').
    """
    # Normalize special characters that might cause edge-tts API issues
    text = text.replace("–", "-").replace("—", "-")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("‘", "'").replace("’", "'")
    
    import time
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            communicate = Communicate(text, voice, rate=rate, pitch=pitch)
            await communicate.save(output_path)
            print(f"Audio file saved to: {output_path}")
            return
        except Exception as e:
            print(f"Attempt {attempt} failed with error: {e}")
            if attempt < max_retries:
                print("Retrying in 2 seconds...")
                await asyncio.sleep(2)
            else:
                raise e

def main():
    parser = argparse.ArgumentParser(description="Generate high-quality Vietnamese TTS voiceover using edge-tts.")
    parser.add_argument("script_path", help="Path to the script text file (e.g., dist/script_scene01.txt)")
    parser.add_argument("--voice", default="vi-VN-NamMinhNeural", help="Voice model (default: vi-VN-NamMinhNeural)")
    parser.add_argument("--rate", default="+0%", help="Voice speed rate adjustment, e.g. +5% or -10% (default: +0%)")
    parser.add_argument("--pitch", default="+0Hz", help="Voice pitch adjustment, e.g. +5Hz or -5Hz (default: +0Hz)")
    parser.add_argument("--output", help="Custom output path for the audio file")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.script_path):
        print(f"File not found: {args.script_path}")
        sys.exit(1)
        
    if args.output:
        output_path = args.output
    else:
        script_dir = os.path.dirname(args.script_path)
        base_name = os.path.splitext(os.path.basename(args.script_path))[0]
        out_name = base_name.replace("script_", "voice_") + ".mp3"
        output_path = os.path.join(script_dir if script_dir else "dist", out_name)
    
    print(f"Parsing script: {args.script_path}...")
    text = extract_script_text(args.script_path)
    print(f"Extracted Text:\n{text}\n")
    
    print(f"Generating audio...")
    print(f"Voice: {args.voice}")
    print(f"Rate: {args.rate}")
    print(f"Pitch: {args.pitch}")
    
    asyncio.run(generate_voice(text, output_path, voice=args.voice, rate=args.rate, pitch=args.pitch))

if __name__ == "__main__":
    main()
