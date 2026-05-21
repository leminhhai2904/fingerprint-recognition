import os
import re
import shutil
import sys
import imageio_ffmpeg
import whisper
from difflib import SequenceMatcher

# Set UTF-8 encoding for console output
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Ensure ffmpeg is in PATH
bin_dir = os.path.abspath("scratch/bin")
os.makedirs(bin_dir, exist_ok=True)
ffmpeg_src = imageio_ffmpeg.get_ffmpeg_exe()
ffmpeg_dst = os.path.join(bin_dir, "ffmpeg.exe")
if not os.path.exists(ffmpeg_dst):
    print(f"Copying {ffmpeg_src} to {ffmpeg_dst}...")
    shutil.copy(ffmpeg_src, ffmpeg_dst)
os.environ["PATH"] = bin_dir + os.path.pathsep + os.environ.get("PATH", "")

def clean_word(w):
    return re.sub(r'[^\w\s]', '', w).lower().strip()

def parse_script_sentences(script_path):
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract all text inside double quotes
    quotes = re.findall(r'"([^"]+)"', content)
    
    sentences = []
    for quote in quotes:
        # Split quote into sentences by . or ? or ! followed by space or end of string
        parts = re.split(r'(?<=[.!?])\s+', quote.strip())
        for p in parts:
            p_clean = p.strip()
            if p_clean:
                sentences.append(p_clean)
    return sentences

def align_scene(scene_num, model):
    script_path = f"dist/script/script_scene{scene_num:02d}.txt"
    audio_path = f"dist/audio/audio_scene_{scene_num}.mp3"
    detect_path = f"dist/detect_audio/detect_scene_{scene_num:02d}.txt"
    
    if not os.path.exists(script_path):
        print(f"Script file {script_path} does not exist. Skipping.")
        return
    if not os.path.exists(audio_path):
        print(f"Audio file {audio_path} does not exist. Skipping.")
        return
        
    print(f"\n--- Aligning Scene {scene_num:02d} ---")
    sentences = parse_script_sentences(script_path)
    print(f"Parsed {len(sentences)} sentences from script.")
    
    print(f"Transcribing {audio_path} with Whisper...")
    result = model.transcribe(audio_path, language="vi", word_timestamps=True)
    
    transcribed_words = []
    for segment in result["segments"]:
        for w_obj in segment.get("words", []):
            transcribed_words.append({
                "word": w_obj["word"].strip(),
                "start": w_obj["start"],
                "end": w_obj["end"]
            })
            
    print(f"Transcribed {len(transcribed_words)} words.")
    
    # Map each script word to its sentence index
    script_words = []
    word_to_sentence_map = []
    for s_idx, sentence in enumerate(sentences):
        words_in_s = sentence.split()
        for w in words_in_s:
            clean_w = clean_word(w)
            if clean_w:
                script_words.append(clean_w)
                word_to_sentence_map.append(s_idx)
                
    trans_words_clean = [clean_word(w["word"]) for w in transcribed_words if clean_word(w["word"])]
    
    # Align using SequenceMatcher
    sm = SequenceMatcher(None, script_words, trans_words_clean)
    matching_blocks = sm.get_matching_blocks()
    
    # Collect matching word times for each sentence
    sentence_word_times = {i: [] for i in range(len(sentences))}
    for block in matching_blocks:
        for i in range(block.size):
            script_idx = block.a + i
            trans_idx = block.b + i
            if script_idx < len(word_to_sentence_map) and trans_idx < len(transcribed_words):
                s_idx = word_to_sentence_map[script_idx]
                w_time = transcribed_words[trans_idx]
                sentence_word_times[s_idx].append(w_time)
                
    # Determine raw start/end times
    start_times = [None] * len(sentences)
    end_times = [None] * len(sentences)
    
    for i in range(len(sentences)):
        times = sentence_word_times[i]
        if times:
            times.sort(key=lambda x: x["start"])
            start_times[i] = times[0]["start"]
            end_times[i] = times[-1]["end"]
            
    # Interpolate missing sentences
    for i in range(len(sentences)):
        if start_times[i] is None or end_times[i] is None:
            # Find last known end time
            prev_end = 0.0
            for prev in range(i - 1, -1, -1):
                if end_times[prev] is not None:
                    prev_end = end_times[prev]
                    break
            
            # Find next known start time
            next_start = None
            for nxt in range(i + 1, len(sentences)):
                if start_times[nxt] is not None:
                    next_start = start_times[nxt]
                    break
                    
            if next_start is None:
                # If no next sentence, estimate based on remaining audio duration or 3s
                next_start = prev_end + 3.0
                
            start_times[i] = prev_end
            end_times[i] = next_start
            print(f"  Sentence {i+1} was interpolated: {start_times[i]:.2f}s - {end_times[i]:.2f}s")
            
    # Monotonize and resolve overlaps
    for i in range(len(sentences)):
        if i > 0:
            if start_times[i] < start_times[i-1]:
                start_times[i] = start_times[i-1]
        if end_times[i] <= start_times[i]:
            end_times[i] = start_times[i] + 0.5
        if i > 0:
            if end_times[i-1] > start_times[i]:
                end_times[i-1] = start_times[i]
                
    # Write output to detect_scene_XX.txt
    print(f"Writing timing details to {detect_path}...")
    with open(detect_path, "w", encoding="utf-8") as f:
        f.write(f"TIMING DETAILS - SCENE {scene_num:02d} (SENTENCE-LEVEL)\n")
        f.write("==================================================\n\n")
        
        for i, sentence in enumerate(sentences):
            start = start_times[i]
            end = end_times[i]
            duration = end - start
            
            f.write(f"Segment {i+1}:\n")
            f.write(f"Start: {start:.2f}s\n")
            f.write(f"End: {end:.2f}s\n")
            f.write(f"Duration: {duration:.2f}s\n")
            f.write(f"Text: {sentence}\n\n")
            
    print(f"Scene {scene_num:02d} alignment complete.")

def main():
    print("Loading Whisper model...")
    model = whisper.load_model("tiny")
    
    for scene_num in range(1, 8):
        try:
            align_scene(scene_num, model)
        except Exception as e:
            print(f"Error aligning scene {scene_num}: {e}")

if __name__ == "__main__":
    main()
