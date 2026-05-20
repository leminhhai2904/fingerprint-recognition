"""
Custom Manim Mobjects for fingerprint visualization.
Includes: ridge patterns, minutiae, singular regions, etc.
"""
from manim import *
import numpy as np
from utils.colors import *


def create_ridge_lines(num_ridges=12, width=5, height=4, curvature=0.3, 
                       color=RIDGE_COLOR, stroke_width=3):
    """
    Create a set of curved parallel ridge lines simulating a fingerprint pattern.
    Returns a VGroup of curves.
    """
    ridges = VGroup()
    for i in range(num_ridges):
        t = (i / (num_ridges - 1)) - 0.5  # -0.5 to 0.5
        y_offset = t * height

        # Create a wavy curve
        points = []
        num_points = 50
        for j in range(num_points):
            x = (j / (num_points - 1) - 0.5) * width
            # Add curvature - more curve near center
            curve_amount = curvature * np.sin(np.pi * j / (num_points - 1))
            y = y_offset + curve_amount * np.cos(2 * np.pi * t)
            points.append([x, y, 0])

        curve = VMobject()
        curve.set_points_smoothly([np.array(p) for p in points])
        curve.set_stroke(color=color, width=stroke_width, opacity=0.8)
        ridges.add(curve)

    return ridges


def create_loop_pattern(center=ORIGIN, scale=1.0, color=RIDGE_COLOR, stroke_width=2.5):
    """Create a loop singularity pattern (∩ shape)."""
    ridges = VGroup()
    num_ridges = 8
    for i in range(num_ridges):
        t = i / num_ridges
        radius = (0.3 + t * 0.8) * scale
        arc = Arc(
            radius=radius,
            start_angle=PI * 0.15,
            angle=PI * 0.7,
            arc_center=center + DOWN * 0.3 * scale,
            color=color,
            stroke_width=stroke_width,
        )
        ridges.add(arc)
    return ridges


def create_delta_pattern(center=ORIGIN, scale=1.0, color=RIDGE_COLOR, stroke_width=2.5):
    """Create a delta singularity pattern (∆ shape)."""
    ridges = VGroup()
    # Three converging sets of lines
    for angle_offset in [0, 2 * PI / 3, 4 * PI / 3]:
        for i in range(4):
            t = (i - 1.5) * 0.15 * scale
            start = center + np.array([
                np.cos(angle_offset) * 1.2 * scale + np.cos(angle_offset + PI/2) * t,
                np.sin(angle_offset) * 1.2 * scale + np.sin(angle_offset + PI/2) * t,
                0
            ])
            end = center + np.array([
                np.cos(angle_offset) * 0.2 * scale + np.cos(angle_offset + PI/2) * t * 0.3,
                np.sin(angle_offset) * 0.2 * scale + np.sin(angle_offset + PI/2) * t * 0.3,
                0
            ])
            line = Line(start, end, color=color, stroke_width=stroke_width)
            ridges.add(line)
    return ridges


def create_whorl_pattern(center=ORIGIN, scale=1.0, color=RIDGE_COLOR, stroke_width=2.5):
    """Create a whorl singularity pattern (O/spiral shape)."""
    ridges = VGroup()
    num_ridges = 6
    for i in range(num_ridges):
        radius = (0.2 + i * 0.15) * scale
        circle = Circle(
            radius=radius,
            color=color,
            stroke_width=stroke_width,
            arc_center=center,
        )
        # Slightly deform to make it look more natural
        circle.stretch(1.0 + 0.1 * np.sin(i), 0)
        circle.stretch(1.0 + 0.1 * np.cos(i), 1)
        ridges.add(circle)
    return ridges


def create_termination_minutia(position=ORIGIN, angle=0, scale=1.0):
    """
    Create a termination minutia visualization.
    A ridge that abruptly ends with a highlighted dot.
    """
    ridge_length = 1.2 * scale
    end_point = position + np.array([
        np.cos(angle) * ridge_length,
        np.sin(angle) * ridge_length,
        0
    ])

    ridge = Line(
        position - np.array([np.cos(angle), np.sin(angle), 0]) * ridge_length * 0.5,
        end_point,
        color=RIDGE_COLOR,
        stroke_width=4,
    )
    dot = Dot(end_point, color=MINUTIA_TERM, radius=0.08 * scale)
    glow = Dot(end_point, color=MINUTIA_TERM, radius=0.15 * scale).set_opacity(0.3)

    return VGroup(ridge, glow, dot)


def create_bifurcation_minutia(position=ORIGIN, angle=0, scale=1.0):
    """
    Create a bifurcation minutia visualization.
    A ridge that splits into two with a highlighted dot at the split point.
    """
    ridge_length = 1.0 * scale
    branch_angle = PI / 6  # 30 degrees

    start = position - np.array([np.cos(angle), np.sin(angle), 0]) * ridge_length * 0.5
    split_point = position

    end1 = split_point + np.array([
        np.cos(angle + branch_angle) * ridge_length * 0.6,
        np.sin(angle + branch_angle) * ridge_length * 0.6,
        0
    ])
    end2 = split_point + np.array([
        np.cos(angle - branch_angle) * ridge_length * 0.6,
        np.sin(angle - branch_angle) * ridge_length * 0.6,
        0
    ])

    main_ridge = Line(start, split_point, color=RIDGE_COLOR, stroke_width=4)
    branch1 = Line(split_point, end1, color=RIDGE_COLOR, stroke_width=4)
    branch2 = Line(split_point, end2, color=RIDGE_COLOR, stroke_width=4)

    dot = Dot(split_point, color=MINUTIA_BIFUR, radius=0.08 * scale)
    glow = Dot(split_point, color=MINUTIA_BIFUR, radius=0.15 * scale).set_opacity(0.3)
    return VGroup(main_ridge, branch1, branch2, glow, dot)


def create_fingerprint_simple(center=ORIGIN, scale=1.0, color=RIDGE_COLOR):
    """
    Create a highly recognizable, beautiful fingerprint pattern using our SVG asset.
    """
    from pathlib import Path
    svg_path = Path(__file__).resolve().parent / "fingerprint.svg"
    
    fp = SVGMobject(str(svg_path))
    fp.set_color(color)
    fp.scale(scale * 1.5)  # adjust scaling slightly to match the original size
    fp.move_to(center)
    return fp




def create_minutia_point(position, minutia_type="termination", angle=0, show_angle=True, scale=1.0):
    """
    Create a minutia point representation: m = {x, y, θ}
    Used in matching visualizations.
    """
    dot_color = MINUTIA_TERM if minutia_type == "termination" else MINUTIA_BIFUR
    dot = Dot(position, color=dot_color, radius=0.06 * scale)

    group = VGroup(dot)

    if show_angle:
        arrow_length = 0.3 * scale
        arrow_end = position + np.array([
            np.cos(angle) * arrow_length,
            np.sin(angle) * arrow_length,
            0
        ])
        arrow = Arrow(
            position, arrow_end,
            color=dot_color,
            stroke_width=2,
            buff=0,
            max_tip_length_to_length_ratio=0.3,
        )
        group.add(arrow)

    return group


def create_orientation_field(rows=8, cols=10, width=5, height=3.5, center=ORIGIN):
    """
    Create a visualization of the local ridge orientation field.
    Shows small line segments indicating ridge direction at each grid point.
    """
    field = VGroup()
    seg_length = 0.25

    for i in range(rows):
        for j in range(cols):
            x = center[0] + (j / (cols - 1) - 0.5) * width
            y = center[1] + (i / (rows - 1) - 0.5) * height

            # Simulate orientation based on position (simple loop pattern)
            dx = x - center[0]
            dy = y - center[1]
            dist = np.sqrt(dx**2 + dy**2)

            if dist < 0.5:
                angle = np.arctan2(dy, dx) + PI / 2
            else:
                angle = np.arctan2(dy, dx) + PI / 2 * (1 - min(dist / 2, 1))

            start = np.array([x, y, 0]) - np.array([np.cos(angle), np.sin(angle), 0]) * seg_length / 2
            end = np.array([x, y, 0]) + np.array([np.cos(angle), np.sin(angle), 0]) * seg_length / 2

            seg = Line(start, end, color=RIDGE_COLOR, stroke_width=2, stroke_opacity=0.7)
            field.add(seg)

    return field


def create_crossing_number_grid(center=ORIGIN, scale=1.0):
    """
    Create a 3x3 pixel grid showing how crossing number works.
    """
    grid = VGroup()
    cell_size = 0.4 * scale

    # 3x3 grid of squares
    for i in range(3):
        for j in range(3):
            x = center[0] + (j - 1) * cell_size
            y = center[1] + (1 - i) * cell_size
            square = Square(
                side_length=cell_size,
                stroke_color=TEXT_DIM,
                stroke_width=1,
                fill_opacity=0,
            ).move_to([x, y, 0])
            grid.add(square)

    return grid
