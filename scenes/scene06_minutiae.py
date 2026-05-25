"""
Scene 6: Đối sánh dựa trên Minutiae (Minutiae-based Matching)
- Quy trình đối sánh điểm đặc trưng & Định nghĩa toạ độ m = {x, y, theta}
- Thuật toán Hough Transform + Trực quan hóa hạt bay phiếu bầu biểu đồ không gian Hough
- Đối sánh cục bộ vs toàn cục (Local neighbor-star vs Global constellation mesh)
- Trích xuất đặc trưng vùng vân (FingerCode Gabor scanning + feature vector)
"""
from manim import *
import numpy as np
import sys
import random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.colors import *
from utils.styles import *
from utils.fingerprint_mobjects import *


class Scene06Minutiae(Scene):
    def construct(self):
        scene_setup(self)
        self.section_title()
        self.minutiae_matching_problem()
        self.hough_transform_voting()
        self.local_vs_global()
        self.fingercode_extraction()

    def ct(self, text_str, font_size=18, color=TEXT_COLOR, weight=NORMAL, **kwargs):
        """create_text with CMU Serif kerning workaround (render big → scale down)."""
        return Text(text_str, font_size=36, color=color, weight=weight, **kwargs).scale(font_size / 36)

    def get_section_hdr(self, text):
        title = self.ct(text, font_size=30, color=TEXT_BRIGHT, weight=BOLD)
        underline = Line(
            start=title.get_left() + DOWN * 0.3,
            end=title.get_right() + DOWN * 0.3,
            color=PRIMARY,
            stroke_width=3,
        )
        return VGroup(title, underline)

    def make_glowing(self, mobject, color=PRIMARY, stroke_width_base=3, opacities=[0.1, 0.25, 0.65]):
        """Tạo hiệu ứng phát sáng Neon cao cấp bằng cách xếp lớp chồng lên nhau."""
        glow = VGroup()
        for op, w_mul in zip(opacities, [4, 2, 1]):
            glow.add(
                mobject.copy().set_stroke(color=color, width=stroke_width_base * w_mul, opacity=op)
            )
        return glow

    def section_title(self):
        """Tiêu đề mục — Segment 1 = 15.05s (Title section takes first 3s)."""
        num = self.ct("05", font_size=80, color=PRIMARY, weight=BOLD, font="Consolas")
        title = self.ct("Đối Sánh Vân Tay", font_size=44, color=TEXT_BRIGHT, weight=BOLD)
        subtitle = self.ct("Các phương pháp đối sánh đặc trưng và kết cấu", font_size=22, color=TEXT_DIM)
        group = VGroup(num, title, subtitle).arrange(DOWN, buff=0.4)

        self.play(FadeIn(num, scale=1.5), run_time=0.5)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.8)

        self.wait(1.5)
        self.play(FadeOut(group), run_time=0.8)
        self.wait(0.2)

    def minutiae_matching_problem(self):
        """Bài toán đối sánh điểm minutiae — Phần còn lại của Segment 1 = 15.05s - 4.6s = 10.45s."""
        section = self.get_section_hdr("Bài Toán Đối Sánh Tập Điểm")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6) # Total 0.6s

        # 2 Glassmorphic templates side by side
        left_box = create_rounded_box(width=5.0, height=4.0, fill_color=SECONDARY, fill_opacity=0.2, stroke_color=CHART_BLUE, stroke_width=1.5).shift(LEFT * 3.4 + DOWN * 0.4)
        right_box = create_rounded_box(width=5.0, height=4.0, fill_color=SECONDARY, fill_opacity=0.2, stroke_color=CHART_ORANGE, stroke_width=1.5).shift(RIGHT * 3.4 + DOWN * 0.4)
        
        lbl_t = self.ct("Mẫu Vân Tay Template (T)", font_size=14, color=CHART_BLUE, weight=BOLD).next_to(left_box, UP, buff=0.15)
        lbl_i = self.ct("Mẫu Vân Tay Input (I)", font_size=14, color=CHART_ORANGE, weight=BOLD).next_to(right_box, UP, buff=0.15)

        left_center = left_box.get_center()
        right_center = right_box.get_center()

        # Minutiae points in Template (T)
        t_pts = VGroup(
            create_minutia_point(left_center + np.array([0.5, 0.6, 0]), "termination", PI/4, scale=1.2),
            create_minutia_point(left_center + np.array([-0.8, 0.8, 0]), "bifurcation", -PI/6, scale=1.2),
            create_minutia_point(left_center + np.array([-0.3, -0.8, 0]), "termination", PI*0.8, scale=1.2),
            create_minutia_point(left_center + np.array([0.6, -0.6, 0]), "bifurcation", -PI*0.4, scale=1.2),
        )

        # Minutiae points in Input (I) - shifted by (0.2, -0.2) and rotated by +0.3 rad
        i_pts = VGroup(
            create_minutia_point(right_center + np.array([0.8, 0.3, 0]), "termination", PI/4 + 0.3, scale=1.2),
            create_minutia_point(right_center + np.array([-0.5, 0.9, 0]), "bifurcation", -PI/6 + 0.3, scale=1.2),
            create_minutia_point(right_center + np.array([-0.1, -0.6, 0]), "termination", PI*0.8 + 0.3, scale=1.2),
            create_minutia_point(right_center + np.array([0.8, -0.4, 0]), "bifurcation", -PI*0.4 + 0.3, scale=1.2),
        )

        # Callout for mathematical coordinates m = {x, y, theta}
        callout_box = create_rounded_box(width=2.4, height=0.7, fill_color=SECONDARY, fill_opacity=0.5, stroke_color=PRIMARY, stroke_width=1.0).move_to(left_center + UP * 1.3)
        callout_txt = self.ct("m = {x, y, θ}", font_size=11, color=PRIMARY, weight=BOLD).move_to(callout_box)
        callout_line = DashedLine(t_pts[0][0].get_center(), callout_box.get_bottom(), color=PRIMARY, stroke_width=1.0)
        callout_group = VGroup(callout_box, callout_txt, callout_line)

        # Transformation formula arrow
        arrow = Arrow(left_box.get_right(), right_box.get_left(), color=PRIMARY, stroke_width=2.5, buff=0.15)
        formula = MathTex(r"\mathbf{T} = \mathbf{R} \cdot \mathbf{I} + \mathbf{t}", font_size=24, color=PRIMARY).next_to(arrow, UP, buff=0.15)

        # Play box & point entrance
        self.play(
            FadeIn(left_box), FadeIn(right_box),
            FadeIn(lbl_t), FadeIn(lbl_i),
            run_time=0.8
        ) # Total 1.4s
        self.play(
            LaggedStart(*[FadeIn(p, scale=1.5) for p in t_pts], lag_ratio=0.15),
            LaggedStart(*[FadeIn(p, scale=1.5) for p in i_pts], lag_ratio=0.15),
            run_time=1.0
        ) # Total 2.4s

        # Show coordinate callout
        self.play(FadeIn(callout_group), run_time=0.8) # Total 3.2s
        self.play(Indicate(callout_box, color=PRIMARY), run_time=0.6) # Total 3.8s
        
        # Show formula
        self.play(GrowArrow(arrow), FadeIn(formula), run_time=0.8) # Total 4.6s

        # Align animation: input points translate and rotate to match template configuration
        aligned_i_positions = [
            right_center + np.array([0.5, 0.6, 0]),
            right_center + np.array([-0.8, 0.8, 0]),
            right_center + np.array([-0.3, -0.8, 0]),
            right_center + np.array([0.6, -0.6, 0])
        ]
        
        align_anims = []
        for pt, target_pos in zip(i_pts, aligned_i_positions):
            # Also rotate the arrowhead back
            align_anims.append(pt.animate.move_to(target_pos))
            
        self.play(*align_anims, run_time=1.8) # Total 6.4s

        # Success Match Flash
        flash_rect = right_box.copy().set_color(MATCH_COLOR).set_fill(MATCH_COLOR, opacity=0.15).set_stroke(width=2.5)
        self.play(FadeIn(flash_rect), run_time=0.5) # Total 6.9s
        self.play(FadeOut(flash_rect), run_time=0.4) # Total 7.3s

        # Wait remaining
        # Target = 10.45s. Anim play = 7.3s. Need 3.15s wait.
        self.wait(3.15)
        self.play(FadeOut(VGroup(section, left_box, right_box, lbl_t, lbl_i, t_pts, i_pts, callout_group, arrow, formula)), run_time=1.0)
        self.wait(0.8)

    def hough_transform_voting(self):
        """Hough Transform rời rạc hoá & bỏ phiếu bầu — Segment 2 = 15.55s."""
        section = self.get_section_hdr("Không Gian Tham Số Hough Transform")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6) # Total 0.6s

        # Left: Hough parameter offset calculation card
        calc_box = create_rounded_box(width=5.5, height=4.2, fill_color=SECONDARY, fill_opacity=0.2, stroke_color=PRIMARY, stroke_width=1.5).shift(LEFT * 3.4 + DOWN * 0.4)
        calc_title = self.ct("Tính Toán Tham Số Biến Đổi", font_size=15, color=PRIMARY, weight=BOLD).next_to(calc_box.get_top(), DOWN, buff=0.2)
        
        formula_hough = MathTex(
            r"\begin{bmatrix} \Delta x \\ \Delta y \end{bmatrix} = "
            r"\begin{bmatrix} x_T \\ y_T \end{bmatrix} - "
            r"\begin{bmatrix} \cos\Delta\theta & -\sin\Delta\theta \\ \sin\Delta\theta & \cos\Delta\theta \end{bmatrix} "
            r"\begin{bmatrix} x_I \\ y_I \end{bmatrix}",
            font_size=18, color=TEXT_BRIGHT
        ).move_to(calc_box.get_center() + UP * 0.2)
        
        formula_theta = MathTex(r"\Delta\theta = \theta_T - \theta_I", font_size=20, color=CHART_ORANGE).next_to(formula_hough, DOWN, buff=0.4)
        
        calc_card = VGroup(calc_box, calc_title, formula_hough, formula_theta)

        # Right: Discrete Hough space accumulator grid
        grid_box = create_rounded_box(width=5.5, height=4.2, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=CHART_BLUE, stroke_width=1.5).shift(RIGHT * 3.4 + DOWN * 0.4)
        grid_title = self.ct("Bộ tích lũy không gian Hough (Δx, Δy)", font_size=15, color=CHART_BLUE, weight=BOLD).next_to(grid_box.get_top(), DOWN, buff=0.2)

        grid_center = grid_box.get_center() + DOWN * 0.4
        hough_grid = VGroup()
        grid_rows, grid_cols = 5, 5
        cell_size = 0.5
        for i in range(grid_rows):
            for j in range(grid_cols):
                cell = Square(
                    side_length=cell_size,
                    stroke_color=TEXT_DIM,
                    stroke_width=1,
                    fill_opacity=0.08,
                    fill_color=SECONDARY
                ).move_to(grid_center + np.array([(j - 2) * cell_size, (2 - i) * cell_size, 0]))
                hough_grid.add(cell)

        # Peak Cell in grid is index 12 (center cell)
        peak_cell = hough_grid[12]
        
        peak_glow = peak_cell.copy().set_fill(MATCH_COLOR, opacity=0.8).set_stroke(MATCH_COLOR, width=2.0)
        peak_target = Circle(radius=0.35, color=MATCH_COLOR, stroke_width=2).move_to(peak_cell.get_center())
        peak_lbl = self.ct("Đỉnh tích lũy", font_size=11, color=MATCH_COLOR, weight=BOLD).next_to(peak_target, UR, buff=0.05)
        peak_indicator = VGroup(peak_glow, peak_target, peak_lbl)

        # Animate entrance
        self.play(FadeIn(calc_card, shift=RIGHT * 0.3), run_time=1.0) # Total 1.6s
        self.play(FadeIn(grid_box), FadeIn(grid_title), FadeIn(hough_grid, shift=LEFT * 0.3), run_time=1.2) # Total 2.8s

        # Generate Voting particles flying from formulas into Hough grid cells
        votes_count = 14
        particles = VGroup(*[
            Dot(formula_hough.get_center(), color=PRIMARY, radius=0.06).set_opacity(0.8)
            for _ in range(votes_count)
        ])
        self.play(FadeIn(particles), run_time=0.4) # Total 3.2s

        random.seed(101)
        vote_anims = []
        for idx, p in enumerate(particles):
            if idx < 6:
                # Land in center cell (Peak)
                target_pos = peak_cell.get_center() + np.array([random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), 0])
            else:
                # Land in random cells
                target_cell = random.choice(list(hough_grid))
                target_pos = target_cell.get_center() + np.array([random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), 0])
            
            vote_anims.append(p.animate(rate_func=smooth).move_to(target_pos).set_opacity(0.2))

        # Fly votes across screen
        self.play(LaggedStart(*vote_anims, lag_ratio=0.08), run_time=1.8) # Total 5.0s

        # Flash peak cell
        self.play(FadeIn(peak_indicator, scale=0.8), run_time=1.0) # Total 6.0s
        self.play(Indicate(peak_target, color=MATCH_COLOR), run_time=0.8) # Total 6.8s
        self.remove(particles)

        # Target = 15.55s. Anim play = 6.8s. Need 8.75s wait.
        self.wait(8.75)
        self.play(FadeOut(VGroup(section, calc_card, grid_box, grid_title, hough_grid, peak_indicator)), run_time=1.0)
        self.wait(0.8)

    def local_vs_global(self):
        """Đối sánh Cục bộ vs Toàn cục — Segment 3 = 17.40s."""
        section = self.get_section_hdr("Đối Sánh Cục Bộ vs Toàn Cục")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6) # Total 0.6s

        # Left panel: Local Matching
        local_box = create_rounded_box(width=5.5, height=4.2, fill_color=SECONDARY, fill_opacity=0.2, stroke_color=CHART_BLUE, stroke_width=1.5).shift(LEFT * 3.4 + DOWN * 0.4)
        local_title = self.ct("Đối sánh cục bộ", font_size=15, color=CHART_BLUE, weight=BOLD).next_to(local_box.get_top(), DOWN, buff=0.2)
        
        # Local Star structure simulation
        local_center = local_box.get_center() + UP * 0.2
        c_pt = Dot(local_center, color=CHART_BLUE, radius=0.1)
        c_glow = self.make_glowing(c_pt, color=CHART_BLUE, stroke_width_base=2)
        
        # Neighbors
        n1 = local_center + np.array([-0.9, 0.6, 0])
        n2 = local_center + np.array([1.1, 0.5, 0])
        n3 = local_center + np.array([-0.3, -0.9, 0])
        n_pts = VGroup(Dot(n1, color=TEXT_COLOR), Dot(n2, color=TEXT_COLOR), Dot(n3, color=TEXT_COLOR))
        
        line1 = DashedLine(local_center, n1, color=TEXT_DIM, stroke_width=1.5)
        line2 = DashedLine(local_center, n2, color=TEXT_DIM, stroke_width=1.5)
        line3 = DashedLine(local_center, n3, color=TEXT_DIM, stroke_width=1.5)
        lines = VGroup(line1, line2, line3)
        
        # Labels for local features: d12, d13, d14 and theta1, theta2
        d1_lbl = self.ct("d₁", font_size=10, color=TEXT_DIM).next_to(line1.get_center(), UP, buff=0.05)
        d2_lbl = self.ct("d₂", font_size=10, color=TEXT_DIM).next_to(line2.get_center(), UP, buff=0.05)
        d3_lbl = self.ct("d₃", font_size=10, color=TEXT_DIM).next_to(line3.get_center(), LEFT, buff=0.05)
        d_lbls = VGroup(d1_lbl, d2_lbl, d3_lbl)

        local_bullets = VGroup(
            self.ct("✓ Chịu biến dạng co giãn tốt", font_size=10, color=MATCH_COLOR),
            self.ct("✓ Không cần căn chỉnh trước", font_size=10, color=MATCH_COLOR),
            self.ct("✗ Độ phân biệt thấp hơn", font_size=10, color=DELTA_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(local_box.get_bottom(), UP, buff=0.25).shift(LEFT * 0.8)

        local_mesh = VGroup(c_pt, c_glow, n_pts, lines, d_lbls, local_bullets)

        # Right panel: Global Matching
        global_box = create_rounded_box(width=5.5, height=4.2, fill_color=SECONDARY, fill_opacity=0.2, stroke_color=CHART_ORANGE, stroke_width=1.5).shift(RIGHT * 3.4 + DOWN * 0.4)
        global_title = self.ct("Đối sánh toàn cục", font_size=15, color=CHART_ORANGE, weight=BOLD).next_to(global_box.get_top(), DOWN, buff=0.2)

        # Global Delaunay-like constellation mesh
        global_center = global_box.get_center() + UP * 0.2
        g_pts_data = [
            global_center + np.array([-0.8, 0.7, 0]),
            global_center + np.array([0.9, 0.8, 0]),
            global_center + np.array([-1.0, -0.6, 0]),
            global_center + np.array([0.8, -0.5, 0]),
            global_center + np.array([0.0, 0.2, 0])
        ]
        g_pts = VGroup(*[Dot(pos, color=CHART_ORANGE, radius=0.08) for pos in g_pts_data])
        
        # Connect all points to show the global mesh
        g_lines = VGroup()
        for i in range(len(g_pts_data)):
            for j in range(i+1, len(g_pts_data)):
                dist = np.linalg.norm(g_pts_data[i] - g_pts_data[j])
                if dist < 2.0:
                    g_lines.add(Line(g_pts_data[i], g_pts_data[j], color=CHART_ORANGE, stroke_width=1.0).set_opacity(0.35))

        global_bullets = VGroup(
            self.ct("✓ Độ phân biệt cực kỳ cao", font_size=10, color=MATCH_COLOR),
            self.ct("✗ Nhạy cảm với co giãn, xoay", font_size=10, color=DELTA_COLOR),
            self.ct("✗ Đòi hỏi căn chỉnh chuẩn xác", font_size=10, color=DELTA_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(global_box.get_bottom(), UP, buff=0.25).shift(LEFT * 0.8)

        global_mesh = VGroup(g_pts, g_lines, global_bullets)

        # Hybrid banner at bottom
        hybrid_banner = create_rounded_box(width=6.0, height=0.7, fill_color=MATCH_COLOR, fill_opacity=0.15, stroke_color=MATCH_COLOR, stroke_width=1.5).shift(DOWN * 3.0)
        hybrid_lbl = self.ct("Giải pháp hiện đại: Đối sánh kết hợp", font_size=13, color=MATCH_COLOR, weight=BOLD).move_to(hybrid_banner)

        # Entrance
        self.play(FadeIn(local_box), FadeIn(local_title), FadeIn(global_box), FadeIn(global_title), run_time=1.0) # Total 1.6s
        
        # Show Local structure
        self.play(FadeIn(c_pt), FadeIn(c_glow), LaggedStart(*[FadeIn(n) for n in n_pts], lag_ratio=0.1), run_time=0.8) # Total 2.4s
        self.play(Create(lines), FadeIn(d_lbls), FadeIn(local_bullets), run_time=1.2) # Total 3.6s

        # Show Global structure
        self.play(LaggedStart(*[FadeIn(g) for g in g_pts], lag_ratio=0.1), Create(g_lines), FadeIn(global_bullets), run_time=1.8) # Total 5.4s

        # Show Hybrid solution
        self.play(FadeIn(hybrid_banner), FadeIn(hybrid_lbl), run_time=0.8) # Total 6.2s

        # Target = 17.40s. Anim play = 6.2s. Need 10.20s wait.
        self.wait(10.20)
        self.play(FadeOut(VGroup(section, local_box, local_title, local_mesh, global_box, global_title, global_mesh, hybrid_banner, hybrid_lbl)), run_time=1.0)
        self.wait(0.8)

    def fingercode_extraction(self):
        """Khái niệm FingerCode & Gabor filters — Segment 4 = 17.04s."""
        section = self.get_section_hdr("Đặc Trưng Kết Cấu FingerCode")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6) # Total 0.6s

        # Left side: Core area & tessellation sectors
        core_box = create_rounded_box(width=5.5, height=4.2, fill_color=SECONDARY, fill_opacity=0.2, stroke_color=PRIMARY, stroke_width=1.5).shift(LEFT * 3.4 + DOWN * 0.4)
        core_title = self.ct("Tessellation quanh Điểm lõi", font_size=15, color=PRIMARY, weight=BOLD).next_to(core_box.get_top(), DOWN, buff=0.2)

        core_center = core_box.get_center() + DOWN * 0.2
        core_pt = Dot(core_center, color=CORE_POINT, radius=0.08)
        core_lbl = self.ct("Điểm lõi", font_size=9, color=CORE_POINT, weight=BOLD).next_to(core_pt, UP, buff=0.05)
        
        # Circular sectors around core
        sectors = VGroup()
        colors_palette = [CHART_BLUE, CHART_ORANGE, CHART_PURPLE, PRIMARY]
        for r_idx in range(3):
            r_in = 0.35 + r_idx * 0.45
            r_out = 0.8 + r_idx * 0.45
            for s_idx in range(8):
                sector = AnnularSector(
                    inner_radius=r_in,
                    outer_radius=r_out,
                    angle=PI/4,
                    start_angle=s_idx * (PI/4),
                    color=colors_palette[(r_idx + s_idx) % len(colors_palette)],
                    fill_opacity=0.15,
                    stroke_color=TEXT_DIM,
                    stroke_width=0.8
                ).move_to(core_center, aligned_edge=ORIGIN)
                sectors.add(sector)

        core_group = VGroup(core_box, core_title, core_pt, core_lbl, sectors)

        # Right side: Gabor response feature vector representation
        vector_box = create_rounded_box(width=5.5, height=4.2, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=CHART_ORANGE, stroke_width=1.5).shift(RIGHT * 3.4 + DOWN * 0.4)
        vector_title = self.ct("Véctơ Đặc Trưng FingerCode", font_size=15, color=CHART_ORANGE, weight=BOLD).next_to(vector_box.get_top(), DOWN, buff=0.2)

        # Gabor filter kernel icon representation
        gabor_kernel = Square(side_length=0.9, color=TEXT_DIM, fill_opacity=0.3).shift(RIGHT * 1.5 + UP * 0.3)
        gabor_stripes = VGroup(*[
            Line(gabor_kernel.get_left() + UP * y, gabor_kernel.get_right() + UP * y, color=TEXT_BRIGHT, stroke_width=2)
            for y in np.linspace(-0.35, 0.35, 6)
        ])
        gabor_lbl = self.ct("Bộ lọc Gabor\n(8 Hướng)", font_size=10, color=TEXT_BRIGHT).next_to(gabor_kernel, UP, buff=0.1)
        gabor_group = VGroup(gabor_kernel, gabor_stripes, gabor_lbl)

        # 1D feature vector box cells
        vector_cells = VGroup()
        cell_w, cell_h = 0.35, 0.6
        for c_idx in range(10):
            cell = Square(side_length=0.4, color=CHART_ORANGE, fill_opacity=0.08, stroke_width=1.0).move_to(
                vector_box.get_center() + DOWN * 0.7 + np.array([(c_idx - 4.5) * 0.44, 0, 0])
            )
            vector_cells.add(cell)
        
        vector_lbl = self.ct("v = [v₁, v₂, v₃, ..., v₆₄₀]", font_size=12, color=CHART_ORANGE, weight=BOLD).next_to(vector_cells, UP, buff=0.2)
        vector_desc = self.ct("Euclidean Distance: D = ||v_T - v_I||", font_size=11, color=MATCH_COLOR, weight=BOLD).next_to(vector_cells, DOWN, buff=0.2)

        # Entrance
        self.play(FadeIn(core_group), run_time=1.2) # Total 1.2s
        self.play(FadeIn(vector_box), FadeIn(vector_title), FadeIn(gabor_group), run_time=1.0) # Total 2.2s

        # Scan simulation of Gabor Filter over core sectors
        gabor_scan = Circle(radius=0.15, color=PRIMARY, stroke_width=2.5).move_to(core_center)
        self.play(FadeIn(gabor_scan), run_time=0.4) # Total 2.6s
        
        # Spiral scanning movement
        scan_path_points = [
            core_center + np.array([np.cos(ang) * (0.45 + ang*0.1), np.sin(ang) * (0.45 + ang*0.1), 0])
            for ang in np.linspace(0, 4*PI, 18)
        ]
        scan_anims = []
        for pt in scan_path_points:
            scan_anims.append(gabor_scan.animate.move_to(pt))
            
        # Highlight sectors as scanner passes
        sector_flashes = []
        for s in list(sectors)[::3]:
            sector_flashes.append(s.animate.set_fill(opacity=0.6))
            
        self.play(
            LaggedStart(*scan_anims, lag_ratio=0.08),
            LaggedStart(*sector_flashes, lag_ratio=0.1),
            run_time=3.5
        ) # Total 6.1s

        self.play(FadeOut(gabor_scan), run_time=0.4) # Total 6.5s

        # Fade in vector cells, populating response values
        self.play(
            LaggedStart(*[FadeIn(cell, scale=0.8) for cell in vector_cells], lag_ratio=0.08),
            FadeIn(vector_lbl),
            run_time=1.2
        ) # Total 7.7s
        
        self.play(FadeIn(vector_desc, shift=UP*0.15), run_time=0.8) # Total 8.5s

        # Target = 17.04s. Anim play = 8.5s. Need 8.54s wait.
        self.wait(8.54)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
