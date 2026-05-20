"""
Fingerprint Recognition - Manim Video
CSC14006 | Pattern Recognition | HCMUS

This file imports all scenes for easy rendering.

Usage:
  Render individual scenes:
    uv run manim -pqh scenes/scene01_intro.py Scene01Intro
    uv run manim -pqh scenes/scene02_sensing.py Scene02Sensing
    uv run manim -pqh scenes/scene03_features.py Scene03Features
    uv run manim -pqh scenes/scene04_extraction.py Scene04Extraction
    uv run manim -pqh scenes/scene05_correlation.py Scene05Correlation
    uv run manim -pqh scenes/scene06_minutiae.py Scene06Minutiae
    uv run manim -pqh scenes/scene07_conclusion.py Scene07Conclusion

  Render all scenes at high quality:
    uv run manim -qh scenes/scene01_intro.py Scene01Intro
    ... (repeat for each scene)

  Render at low quality for preview:
    uv run manim -pql scenes/scene01_intro.py Scene01Intro

  Flags:
    -p  : preview (auto-open after render)
    -q  : quality (l=low, m=medium, h=high, k=4K)
    -a  : render all scenes in a file
"""

# Import all scenes for reference
from scenes.scene01_intro import Scene01Intro
from scenes.scene02_sensing import Scene02Sensing
from scenes.scene03_features import Scene03Features
from scenes.scene04_extraction import Scene04Extraction
from scenes.scene05_correlation import Scene05Correlation
from scenes.scene06_minutiae import Scene06Minutiae
from scenes.scene07_conclusion import Scene07Conclusion