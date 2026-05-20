"""
Common styles, fonts and helper functions for the Fingerprint Recognition video.
"""
from manim import *
from utils.colors import *

# Choose your preferred font here (e.g. "Segoe UI", "Cambria", "Arial", or any installed Google Font like "Be Vietnam Pro")
FONT_NAME = "CMU Serif"

# Set default font for Text mobjects to support Vietnamese characters on Windows/Linux/macOS
config.text_font = FONT_NAME

# Force the selected font default in Text constructor to override Pango fallback behavior on Windows
_original_text_init = Text.__init__
def _patched_text_init(self, text, *args, **kwargs):
    if "font" not in kwargs or not kwargs["font"]:
        kwargs["font"] = FONT_NAME
    _original_text_init(self, text, *args, **kwargs)
Text.__init__ = _patched_text_init



def get_title(text, font_size=48):
    """Create a styled title text."""
    return Text(
        text,
        font_size=font_size,
        color=TEXT_BRIGHT,
        weight=BOLD,
    )


def get_subtitle(text, font_size=32):
    """Create a styled subtitle text."""
    return Text(
        text,
        font_size=font_size,
        color=PRIMARY,
    )


def get_body_text(text, font_size=24):
    """Create body text."""
    return Text(
        text,
        font_size=font_size,
        color=TEXT_COLOR,
    )


def get_label(text, font_size=20, color=TEXT_COLOR):
    """Create a small label."""
    return Text(
        text,
        font_size=font_size,
        color=color,
    )


def get_section_title(text, font_size=40):
    """Create a section title with underline decoration."""
    title = Text(text, font_size=font_size, color=TEXT_BRIGHT, weight=BOLD)
    underline = Line(
        start=title.get_left() + DOWN * 0.3,
        end=title.get_right() + DOWN * 0.3,
        color=PRIMARY,
        stroke_width=3,
    )
    return VGroup(title, underline)


def get_formula(latex_str, font_size=36):
    """Create a styled LaTeX formula."""
    return MathTex(
        latex_str,
        font_size=font_size,
        color=TEXT_COLOR,
    )


def create_rounded_box(width=4, height=2, corner_radius=0.2, 
                       fill_color=ACCENT, fill_opacity=0.5,
                       stroke_color=PRIMARY, stroke_width=2):
    """Create a rounded rectangle box for diagrams."""
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=corner_radius,
        fill_color=fill_color,
        fill_opacity=fill_opacity,
        stroke_color=stroke_color,
        stroke_width=stroke_width,
    )


def create_arrow_between(start_mob, end_mob, color=PRIMARY, buff=0.1):
    """Create an arrow between two mobjects."""
    return Arrow(
        start=start_mob.get_right(),
        end=end_mob.get_left(),
        color=color,
        buff=buff,
        stroke_width=3,
        max_tip_length_to_length_ratio=0.15,
    )


def create_pipeline_box(text, width=2.5, height=0.8, color=PRIMARY):
    """Create a box for pipeline diagrams."""
    box = create_rounded_box(
        width=width, height=height,
        fill_color=color, fill_opacity=0.15,
        stroke_color=color, stroke_width=2,
    )
    label = Text(text, font_size=18, color=TEXT_COLOR)
    return VGroup(box, label)


def scene_setup(scene):
    """Common scene setup - set background color."""
    scene.camera.background_color = BG_COLOR
