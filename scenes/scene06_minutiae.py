"""
Scene 6: Đối sánh dựa trên Minutiae (Minutiae-based Matching) - Cải tiến v2
- Quy trình đối sánh điểm đặc trưng & Định nghĩa toạ độ m = {x, y, theta}
- Thuật toán Hough Transform + Trực quan hóa hạt bỏ phiếu
- Đối sánh cục bộ vs toàn cục
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
        self.intro_and_points()
        self.hough_transform_voting()
        self.local_vs_global()
        self.fingercode_and_texture()

    def ct(self, text_str, font_size=18, color=TEXT_COLOR, weight=NORMAL, **kwargs):
        """create_text với CMU Serif kerning workaround (render to lớn rồi scale xuống)."""
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

    def section_title(self):
        # Segment 1 (0.42s - 3.96s, dur 3.54s)
        num = self.ct("05", font_size=80, color=PRIMARY, weight=BOLD, font="Consolas")
        title = self.ct("Minutiae & Đặc Trưng Đường Vân", font_size=36, color=TEXT_BRIGHT, weight=BOLD)
        subtitle = self.ct("Đối sánh dựa trên cấu trúc hình học cục bộ và toàn cục", font_size=18, color=TEXT_DIM)
        group = VGroup(num, title, subtitle).arrange(DOWN, buff=0.3)
        
        self.play(FadeIn(num, scale=1.5), run_time=0.5)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.7)
        self.wait(1.54) # Wait remaining for Segment 1
        
        self.play(FadeOut(group), run_time=0.8)
        self.wait(0.2)

    def intro_and_points(self):
        # Segment 2 (5.58s - 11.06s, dur 5.48s)
        section = self.get_section_hdr("Đối Sánh Dựa Trên Minutiae")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)
        self.wait(1.02) # Gap wait
        
        # Hiện hai Card đại diện cho Template T và Input I
        left_box = create_rounded_box(width=4.8, height=3.8, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=CHART_BLUE, stroke_width=1.5).shift(LEFT * 3.4 + DOWN * 0.4)
        right_box = create_rounded_box(width=4.8, height=3.8, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=CHART_ORANGE, stroke_width=1.5).shift(RIGHT * 3.4 + DOWN * 0.4)
        
        lbl_t = self.ct("Template (T)", font_size=13, color=CHART_BLUE, weight=BOLD).next_to(left_box, UP, buff=0.15)
        lbl_i = self.ct("Input (I)", font_size=13, color=CHART_ORANGE, weight=BOLD).next_to(right_box, UP, buff=0.15)
        
        left_center = left_box.get_center()
        right_center = right_box.get_center()
        
        # Điểm đặc trưng Template (T)
        t_pts = VGroup(
            create_minutia_point(left_center + np.array([0.5, 0.6, 0]), "termination", PI/4, scale=1.1),
            create_minutia_point(left_center + np.array([-0.8, 0.8, 0]), "bifurcation", -PI/6, scale=1.1),
            create_minutia_point(left_center + np.array([-0.3, -0.8, 0]), "termination", PI*0.8, scale=1.1),
            create_minutia_point(left_center + np.array([0.6, -0.6, 0]), "bifurcation", -PI*0.4, scale=1.1),
        )
        
        # Điểm đặc trưng Input (I) - bị dịch chuyển (0.3, -0.2) và xoay +0.25 rad
        i_pts = VGroup(
            create_minutia_point(right_center + np.array([0.8, 0.4, 0]), "termination", PI/4 + 0.25, scale=1.1),
            create_minutia_point(right_center + np.array([-0.5, 1.0, 0]), "bifurcation", -PI/6 + 0.25, scale=1.1),
            create_minutia_point(right_center + np.array([-0.0, -0.6, 0]), "termination", PI*0.8 + 0.25, scale=1.1),
            create_minutia_point(right_center + np.array([0.9, -0.4, 0]), "bifurcation", -PI*0.4 + 0.25, scale=1.1),
        )
        
        self.play(
            FadeIn(left_box), FadeIn(right_box),
            FadeIn(lbl_t), FadeIn(lbl_i),
            FadeIn(t_pts), FadeIn(i_pts),
            run_time=1.2
        )
        
        # Phóng to một điểm và hiện toạ độ cục bộ m_i = {x_i, y_i, theta_i}
        # Tạo vòng tròn zoom ảo
        zoom_circle = Circle(radius=0.7, color=PRIMARY, stroke_width=1.5).move_to(left_center + np.array([0.5, 0.6, 0]))
        zoom_bg = create_rounded_box(width=1.7, height=0.6, fill_color=SECONDARY, fill_opacity=0.9, stroke_color=PRIMARY, stroke_width=1.0).move_to(left_center + np.array([-1.2, 1.5, 0]))
        zoom_text = MathTex(r"m_i = \{x_i, y_i, \theta_i\}", font_size=19, color=PRIMARY).move_to(zoom_bg.get_center())
        
        # Tính toán điểm tiếp xúc chính xác của mũi tên
        c_c = zoom_circle.get_center()
        c_b = zoom_bg.get_center()
        v_dir = c_b - c_c
        u_dir = v_dir / np.linalg.norm(v_dir)
        p_circle = c_c + u_dir * 0.7  # Chạm viền hình tròn bán kính 0.7
        p_box = c_b + np.array([0.78, -0.3, 0])  # Chạm viền góc dưới bên phải của hộp công thức (width=1.7, height=0.6)
        
        zoom_arrow = Arrow(start=p_circle, end=p_box, color=PRIMARY, stroke_width=1.5, buff=0)
        zoom_group = VGroup(zoom_circle, zoom_bg, zoom_text, zoom_arrow)
        
        self.play(FadeIn(zoom_group), run_time=1.0)
        self.wait(3.28) # Remaining wait for Segment 2
        
        # Segment 3 (11.44s - 14.00s, dur 2.56s)
        # Ẩn zoom và di chuyển tập điểm khớp nhau
        self.play(FadeOut(zoom_group), run_time=0.38) # Gap wait
        
        # Tịnh tiến các điểm Input khớp với Template
        aligned_i_positions = [
            right_center + np.array([0.5, 0.6, 0]),
            right_center + np.array([-0.8, 0.8, 0]),
            right_center + np.array([-0.3, -0.8, 0]),
            right_center + np.array([0.6, -0.6, 0])
        ]
        
        align_anims = []
        for pt, target_pos in zip(i_pts, aligned_i_positions):
            shift_val = target_pos - pt[0].get_center()
            align_anims.append(pt[0].animate.shift(shift_val))
            if len(pt) > 1:
                align_anims.append(pt[1].animate.shift(shift_val).rotate(-0.25, about_point=target_pos))
                
        self.play(*align_anims, run_time=1.5)
        
        # Nháy xanh lá báo thành công
        flash_rect = right_box.copy().set_color(MATCH_COLOR).set_fill(MATCH_COLOR, opacity=0.15).set_stroke(width=2.5)
        self.play(FadeIn(flash_rect), run_time=0.4)
        self.play(FadeOut(flash_rect), run_time=0.28)
        self.wait(0.38) # Remaining wait for Segment 3
        
        # Chuyển cảnh dọn dẹp
        self.play(
            FadeOut(section),
            FadeOut(left_box), FadeOut(right_box),
            FadeOut(lbl_t), FadeOut(lbl_i),
            FadeOut(t_pts), FadeOut(i_pts),
            run_time=1.4
        )

    def hough_transform_voting(self):
        # Segment 4 (15.40s - 18.94s, dur 3.54s)
        section = self.get_section_hdr("Bộ Tích Lũy Hough Transform")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)
        
        # Chia đôi màn hình: Bên trái là không gian ảnh, Bên phải là không gian tích lũy
        left_box = create_rounded_box(width=5.0, height=3.8, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=PRIMARY, stroke_width=1.5).shift(LEFT * 3.4 + DOWN * 0.4)
        left_lbl = self.ct("Không gian ảnh (Minutiae)", font_size=13, color=PRIMARY, weight=BOLD).next_to(left_box, UP, buff=0.15)
        
        right_box = create_rounded_box(width=5.0, height=3.8, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=CHART_BLUE, stroke_width=1.5).shift(RIGHT * 3.4 + DOWN * 0.4)
        right_lbl = self.ct("Không gian tích lũy (Δx, Δy, θ)", font_size=13, color=CHART_BLUE, weight=BOLD).next_to(right_box, UP, buff=0.15)
        
        # Lưới không gian Hough
        grid_center = right_box.get_center() + DOWN * 0.2
        hough_grid = VGroup()
        grid_rows, grid_cols = 5, 5
        cell_size = 0.45
        for i in range(grid_rows):
            for j in range(grid_cols):
                cell = Square(
                    side_length=cell_size,
                    stroke_color=TEXT_DIM,
                    stroke_width=0.8,
                    fill_opacity=0.08,
                    fill_color=SECONDARY
                ).move_to(grid_center + np.array([(j - 2) * cell_size, (2 - i) * cell_size, 0]))
                hough_grid.add(cell)
                
        # Hai đám mây điểm lệch nhau bên trái
        lc = left_box.get_center()
        t_cloud = VGroup(*[Dot(lc + np.array([x, y, 0]), color=CHART_BLUE, radius=0.05) for x, y in [[-0.8, 0.6], [0.5, 0.4], [-0.3, -0.6], [0.8, -0.8]]])
        i_cloud = VGroup(*[Dot(lc + np.array([x + 0.3, y - 0.2, 0]), color=CHART_ORANGE, radius=0.05) for x, y in [[-0.8, 0.6], [0.5, 0.4], [-0.3, -0.6], [0.8, -0.8]]])
        
        self.play(
            FadeIn(left_box), FadeIn(left_lbl),
            FadeIn(right_box), FadeIn(right_lbl),
            FadeIn(hough_grid),
            FadeIn(t_cloud), FadeIn(i_cloud),
            run_time=1.4
        )
        self.wait(1.54) # Wait remaining for Segment 4
        
        # Gap (18.94s - 19.54s, dur 0.6s)
        self.wait(0.6)
        
        # Segment 5 (19.54s - 26.52s, dur 6.98s)
        # Voting ray animation: các hạt ánh sáng bay dồn dập từ trái sang phải
        peak_cell = hough_grid[12] # Central cell
        
        # Tạo hiệu ứng hạt bay
        particles = VGroup()
        for idx in range(16):
            start_pt = random.choice(list(t_cloud)).get_center()
            p = Dot(start_pt, color=PRIMARY, radius=0.05).set_opacity(0.8)
            particles.add(p)
            
        self.add(particles)
        
        vote_anims = []
        random.seed(2026)
        for idx, p in enumerate(particles):
            if idx < 8:
                # Land in peak cell
                target_pos = peak_cell.get_center() + np.array([random.uniform(-0.08, 0.08), random.uniform(-0.08, 0.08), 0])
            else:
                # Land in other cells
                target_cell = random.choice(list(hough_grid))
                target_pos = target_cell.get_center() + np.array([random.uniform(-0.08, 0.08), random.uniform(-0.08, 0.08), 0])
            vote_anims.append(p.animate(rate_func=smooth).move_to(target_pos).set_opacity(0.25))
            
        self.play(LaggedStart(*vote_anims, lag_ratio=0.08), run_time=4.0)
        
        # Làm các ô lưới sáng lên đồng thời fade out các hạt
        glow_cells = VGroup()
        for idx in [7, 11, 12, 13, 17]:
            glow_cells.add(hough_grid[idx].copy().set_fill(PRIMARY, opacity=0.35))
        self.play(
            FadeIn(glow_cells),
            FadeOut(particles),
            run_time=1.0
        )
        
        self.wait(1.98) # Wait remaining for Segment 5
        
        # Gap (26.52s - 27.44s, dur 0.92s)
        self.wait(0.92)
        
        # Segment 6 (27.44s - 30.58s, dur 3.14s)
        # Đỉnh cao nhất trồi lên
        peak_glow = peak_cell.copy().set_fill(MATCH_COLOR, opacity=0.85).set_stroke(MATCH_COLOR, width=2.5)
        peak_lbl = self.ct("Đỉnh Tích Lũy", font_size=10, color=MATCH_COLOR, weight=BOLD).next_to(peak_cell, UP, buff=0.1)
        self.play(
            FadeIn(peak_glow),
            FadeIn(peak_lbl),
            run_time=1.0
        )
        self.play(Indicate(peak_glow, color=MATCH_COLOR), run_time=0.8)
        self.wait(1.34)
        
        # Chuyển cảnh dọn dẹp (gap: 30.58s - 32.98s, dur 2.40s)
        self.play(
            FadeOut(section),
            FadeOut(left_box), FadeOut(left_lbl),
            FadeOut(right_box), FadeOut(right_lbl),
            FadeOut(hough_grid), FadeOut(t_cloud), FadeOut(i_cloud),
            FadeOut(glow_cells), FadeOut(peak_glow), FadeOut(peak_lbl),
            run_time=1.5
        )
        self.wait(0.9)

    def local_vs_global(self):
        # Segment 7 (32.98s - 35.96s, dur 2.98s)
        section = self.get_section_hdr("Đối Sánh Cục Bộ vs Toàn Cục")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)
        
        # Hai khối so khớp độc lập
        left_box = create_rounded_box(width=5.0, height=3.8, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=CHART_BLUE, stroke_width=1.5).shift(LEFT * 3.4 + DOWN * 0.4)
        left_lbl = self.ct("Đối Sánh Cục Bộ", font_size=13, color=CHART_BLUE, weight=BOLD).next_to(left_box, UP, buff=0.15)
        
        right_box = create_rounded_box(width=5.0, height=3.8, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=CHART_ORANGE, stroke_width=1.5).shift(RIGHT * 3.4 + DOWN * 0.4)
        right_lbl = self.ct("Đối Sánh Toàn Cục", font_size=13, color=CHART_ORANGE, weight=BOLD).next_to(right_box, UP, buff=0.15)
        
        # Khối Cục bộ: Star structure
        lc = left_box.get_center() + UP * 0.2
        c_pt = Dot(lc, color=CHART_BLUE, radius=0.08)
        n1 = lc + np.array([-0.8, 0.6, 0])
        n2 = lc + np.array([0.9, 0.4, 0])
        n3 = lc + np.array([-0.2, -0.8, 0])
        n_pts = VGroup(Dot(n1, color=RIDGE_COLOR), Dot(n2, color=RIDGE_COLOR), Dot(n3, color=RIDGE_COLOR))
        lines = VGroup(
            Line(lc, n1, color=TEXT_DIM, stroke_width=1.5),
            Line(lc, n2, color=TEXT_DIM, stroke_width=1.5),
            Line(lc, n3, color=TEXT_DIM, stroke_width=1.5),
        )
        # Thêm các ký hiệu d1, d2, d3
        lbl_d = VGroup(
            MathTex(r"d_1", font_size=14, color=TEXT_DIM).next_to(lines[0].get_center(), UR, buff=0.03),
            MathTex(r"d_2", font_size=14, color=TEXT_DIM).next_to(lines[1].get_center(), UL, buff=0.03),
            MathTex(r"d_3", font_size=14, color=TEXT_DIM).next_to(lines[2].get_center(), LEFT, buff=0.04),
        )
        local_structure = VGroup(c_pt, n_pts, lines, lbl_d)
        
        self.play(
            FadeIn(left_box), FadeIn(left_lbl),
            FadeIn(right_box), FadeIn(right_lbl),
            FadeIn(local_structure),
            run_time=1.4
        )
        self.wait(0.98) # Wait remaining for Segment 7
        
        # Gap (35.96s - 37.48s, dur 1.52s)
        self.wait(1.52)
        
        # Segment 8 (37.48s - 41.08s, dur 3.60s)
        # Di chuyển cấu trúc cục bộ và chứng minh tính bất biến hình học (các d và góc không đổi)
        self.play(
            local_structure.animate.shift(RIGHT * 0.4 + DOWN * 0.3).rotate(20 * DEGREES, about_point=c_pt.get_center()),
            run_time=2.0
        )
        self.wait(1.60) # Wait remaining for Segment 8
        
        # Gap (41.08s - 41.64s, dur 0.56s)
        self.wait(0.56)
        
        # Segment 9 (41.64s - 46.00s, dur 4.36s)
        # Khối Toàn cục: Delaunay constellation mesh
        rc = right_box.get_center() + UP * 0.2
        g_pts_data = [
            rc + np.array([-0.9, 0.7, 0]),
            rc + np.array([0.9, 0.8, 0]),
            rc + np.array([-1.0, -0.6, 0]),
            rc + np.array([0.8, -0.5, 0]),
            rc + np.array([0.0, 0.2, 0])
        ]
        g_pts = VGroup(*[Dot(pos, color=CHART_ORANGE, radius=0.06) for pos in g_pts_data])
        # Thay thế bằng always_redraw và ValueTracker để kết nối luôn bám sát điểm di chuyển
        global_distortion_tracker = ValueTracker(0.0)
        
        def get_global_lines():
            d_val = global_distortion_tracker.get_value()
            lines = VGroup()
            pts = [pt.get_center() for pt in g_pts]
            for i in range(len(pts)):
                for j in range(i+1, len(pts)):
                    color = interpolate_color(ManimColor(CHART_ORANGE), ManimColor(RED), d_val)
                    stroke_w = interpolate(1.0, 1.5, d_val)
                    op = interpolate(0.35, 0.70, d_val)
                    line = Line(pts[i], pts[j], color=color, stroke_width=stroke_w).set_opacity(op)
                    lines.add(line)
            return lines
            
        g_lines = always_redraw(get_global_lines)
        global_structure = VGroup(g_pts, g_lines)
        self.play(FadeIn(global_structure), run_time=1.2)
        
        self.play(
            g_pts[0].animate.shift(RIGHT * 0.3 + DOWN * 0.2),
            g_pts[2].animate.shift(LEFT * 0.2 + UP * 0.3),
            global_distortion_tracker.animate.set_value(1.0),
            run_time=1.3
        )
        self.wait(1.86) # Wait remaining for Segment 9
        
        # Gap (46.00s - 46.60s, dur 0.60s)
        self.wait(0.60)
        
        # Segment 10 (46.60s - 48.10s, dur 1.50s)
        # Show banner đối sánh kết hợp ở cạnh dưới
        hybrid_banner = create_rounded_box(width=6.8, height=0.7, fill_color=MATCH_COLOR, fill_opacity=0.15, stroke_color=MATCH_COLOR, stroke_width=1.5).shift(DOWN * 3.0)
        hybrid_lbl = self.ct("Giải pháp hiện đại: Đối sánh kết hợp", font_size=13, color=MATCH_COLOR, weight=BOLD).move_to(hybrid_banner)
        self.play(FadeIn(hybrid_banner), FadeIn(hybrid_lbl), run_time=0.8)
        self.wait(0.70)
        
        # Chuyển cảnh dọn dẹp (gap: 48.10s - 51.14s, dur 3.04s)
        g_lines.clear_updaters()
        self.play(
            FadeOut(section),
            FadeOut(left_box), FadeOut(left_lbl),
            FadeOut(right_box), FadeOut(right_lbl),
            FadeOut(local_structure),
            FadeOut(g_pts), FadeOut(g_lines),
            FadeOut(hybrid_banner), FadeOut(hybrid_lbl),
            run_time=1.5
        )
        self.wait(1.54)

    def fingercode_and_texture(self):
        # Segment 11 (51.14s - 58.14s, dur 7.00s)
        section = self.get_section_hdr("Trích Xuất Đặc Trưng Kết Cấu FingerCode")
        section.to_edge(UP, buff=0.6)
        self.play(FadeIn(section, shift=DOWN * 0.3), run_time=0.6)
        
        # Điểm lõi Core Point nằm tại trung tâm
        core_box = create_rounded_box(width=4.8, height=3.8, fill_color=SECONDARY, fill_opacity=0.15, stroke_color=PRIMARY, stroke_width=1.5).shift(UP * 0.4)
        core_lbl = self.ct("Tessellation quanh điểm Core", font_size=13, color=PRIMARY, weight=BOLD).next_to(core_box, UP, buff=0.15)
        
        core_center = core_box.get_center() + DOWN * 0.1
        core_pt = Dot(core_center, color=CORE_POINT, radius=0.08)
        core_pt_lbl = self.ct("Core", font_size=9, color=CORE_POINT, weight=BOLD).next_to(core_pt, UP, buff=0.05)
        
        # Chia lưới hình quạt (sectors) quanh điểm core
        sectors = VGroup()
        colors_palette = [CHART_BLUE, CHART_ORANGE, CHART_PURPLE, PRIMARY]
        for r_idx in range(3):
            r_in = 0.3 + r_idx * 0.4
            r_out = 0.7 + r_idx * 0.4
            for s_idx in range(8):
                sector = AnnularSector(
                    arc_center=core_center,
                    inner_radius=r_in,
                    outer_radius=r_out,
                    angle=PI/4,
                    start_angle=s_idx * (PI/4),
                    color=colors_palette[(r_idx + s_idx) % len(colors_palette)],
                    fill_opacity=0.18,
                    stroke_color=TEXT_DIM,
                    stroke_width=0.8
                )
                sectors.add(sector)
                
        # Quét Gabor để tạo FingerCode
        gabor_scan = Circle(radius=0.15, color=PRIMARY, stroke_width=2.5).move_to(core_center)
        
        self.play(
            FadeIn(core_box), FadeIn(core_lbl),
            FadeIn(core_pt), FadeIn(core_pt_lbl),
            GrowFromCenter(sectors),
            FadeIn(gabor_scan),
            run_time=1.4
        )
        
        # Tạo đường đi quét xoắn ốc (spiral scan path)
        scan_points = [
            core_center + np.array([np.cos(ang) * (0.3 + ang*0.08), np.sin(ang) * (0.3 + ang*0.08), 0])
            for ang in np.linspace(0, 3.5*PI, 60)
        ]
        scan_path = VMobject()
        scan_path.set_points_smoothly(scan_points)
        
        sector_flashes = [s.animate.set_fill(opacity=0.55) for s in sectors]
        
        self.play(
            MoveAlongPath(gabor_scan, scan_path),
            LaggedStart(*sector_flashes, lag_ratio=0.08),
            run_time=2.6,
            rate_func=linear
        )
        
        # 1D Feature Vector FingerCode rơi xuống cạnh dưới (với cường độ thực tế)
        vector_box1 = VGroup()
        np.random.seed(42)
        for idx in range(12):
            val = np.random.uniform(0.15, 0.85)
            cell = Square(
                side_length=0.35,
                color=CHART_ORANGE,
                fill_color=CHART_ORANGE,
                fill_opacity=val,
                stroke_width=1.0
            ).shift(DOWN * 2.8 + LEFT * 2.2 + idx * 0.4 * RIGHT)
            vector_box1.add(cell)
        vector_lbl1 = self.ct("FingerCode Vector T", font_size=10, color=CHART_ORANGE, weight=BOLD).next_to(vector_box1, UP, buff=0.1)
        
        self.play(
            LaggedStart(*[FadeIn(cell, scale=0.8) for cell in vector_box1], lag_ratio=0.08),
            FadeIn(vector_lbl1),
            FadeOut(gabor_scan),
            run_time=1.2
        )
        self.wait(1.2) # Wait remaining for Segment 11 (7.0s duration exactly)
        
        # Gap (58.14s - 58.64s, dur 0.5s)
        self.wait(0.5)
        
        # Segment 12 (58.64s - 59.96s, dur 1.32s)
        # Vector FingerCode thứ hai (Input I) và đường Euclid
        vector_box2 = VGroup()
        np.random.seed(43) # seed khác để tạo giá trị khác
        for idx in range(12):
            val = np.random.uniform(0.15, 0.85)
            cell = Square(
                side_length=0.35,
                color=CHART_BLUE,
                fill_color=CHART_BLUE,
                fill_opacity=val,
                stroke_width=1.0
            ).shift(DOWN * 3.4 + LEFT * 2.2 + idx * 0.4 * RIGHT)
            vector_box2.add(cell)
        vector_lbl2 = self.ct("FingerCode Vector I", font_size=10, color=CHART_BLUE, weight=BOLD).next_to(vector_box2, DOWN, buff=0.1)
        
        # Đường thẳng ảo nối khoảng cách Euclid
        dist_line = DashedLine(vector_box1.get_right() + RIGHT * 0.2, vector_box2.get_right() + RIGHT * 0.2, color=MATCH_COLOR, stroke_width=1.5)
        dist_lbl = MathTex(r"d_{Euclidean} \approx 0.05 \rightarrow \text{MATCH}", font_size=22, color=MATCH_COLOR).next_to(dist_line, RIGHT, buff=0.2)
        
        self.play(
            FadeIn(vector_box2),
            FadeIn(vector_lbl2),
            Create(dist_line),
            FadeIn(dist_lbl),
            run_time=1.0
        )
        self.wait(0.32) # Wait remaining for Segment 12
        
        # Xóa toàn bộ các thành phần liên quan đến FingerCode để chuyển sang Segment 13
        self.play(
            FadeOut(section),
            FadeOut(core_box), FadeOut(core_lbl),
            FadeOut(core_pt), FadeOut(core_pt_lbl),
            FadeOut(sectors),
            FadeOut(dist_line), FadeOut(dist_lbl),
            FadeOut(vector_box1), FadeOut(vector_lbl1),
            FadeOut(vector_box2), FadeOut(vector_lbl2),
            run_time=1.0
        )
        self.wait(0.74)
        
        # Segment 13 (61.70s - 67.14s, dur 5.44s)
        # Trực quan hoá kết hợp đa đặc trưng (minutiae, trường hướng, mật độ vân) tạo thành các thẻ Dashboard
        section = self.get_section_hdr("Hệ Thống Đối Sánh Đa Đặc Trưng Kết Hợp")
        section.to_edge(UP, buff=0.6)
        
        # Thẻ 1: Đặc trưng điểm (Blue)
        card1_bg = create_rounded_box(width=3.6, height=2.4, fill_color=CHART_BLUE, fill_opacity=0.08, stroke_color=CHART_BLUE, stroke_width=1.5)
        card1_title = self.ct("Đặc trưng điểm", font_size=13, color=CHART_BLUE, weight=BOLD)
        card1_lines = VGroup(
            self.ct("Tọa độ x, y", font_size=10.5, color=TEXT_COLOR),
            self.ct("Góc hướng θ", font_size=10.5, color=TEXT_COLOR)
        ).arrange(DOWN, buff=0.12)
        card1_content = VGroup(card1_title, card1_lines).arrange(DOWN, buff=0.25).move_to(card1_bg.get_center())
        card1 = VGroup(card1_bg, card1_content)
        
        # Thẻ 2: Đặc trưng kết cấu (Orange)
        card2_bg = create_rounded_box(width=3.6, height=2.4, fill_color=CHART_ORANGE, fill_opacity=0.08, stroke_color=CHART_ORANGE, stroke_width=1.5)
        card2_title = self.ct("Đặc trưng kết cấu", font_size=13, color=CHART_ORANGE, weight=BOLD)
        card2_lines = VGroup(
            self.ct("Mã hóa FingerCode", font_size=10.5, color=TEXT_COLOR),
            self.ct("Khoảng cách Euclid", font_size=10.5, color=TEXT_COLOR)
        ).arrange(DOWN, buff=0.12)
        card2_content = VGroup(card2_title, card2_lines).arrange(DOWN, buff=0.25).move_to(card2_bg.get_center())
        card2 = VGroup(card2_bg, card2_content)
        
        # Thẻ 3: Đặc trưng đường vân (Purple)
        card3_bg = create_rounded_box(width=3.6, height=2.4, fill_color=CHART_PURPLE, fill_opacity=0.08, stroke_color=CHART_PURPLE, stroke_width=1.5)
        card3_title = self.ct("Đặc trưng đường vân", font_size=13, color=CHART_PURPLE, weight=BOLD)
        card3_lines = VGroup(
            self.ct("Trường hướng cục bộ", font_size=10.5, color=TEXT_COLOR),
            self.ct("Tần số & mật độ vân", font_size=10.5, color=TEXT_COLOR)
        ).arrange(DOWN, buff=0.12)
        card3_content = VGroup(card3_title, card3_lines).arrange(DOWN, buff=0.25).move_to(card3_bg.get_center())
        card3 = VGroup(card3_bg, card3_content)
        
        cards_group = VGroup(card1, card2, card3).arrange(RIGHT, buff=0.4).shift(DOWN * 0.4)
        
        self.play(
            FadeIn(section, shift=DOWN * 0.3),
            run_time=0.8
        )
        self.play(
            LaggedStart(
                AnimationGroup(Create(card1_bg), FadeIn(card1_content, shift=UP * 0.2)),
                AnimationGroup(Create(card2_bg), FadeIn(card2_content, shift=UP * 0.2)),
                AnimationGroup(Create(card3_bg), FadeIn(card3_content, shift=UP * 0.2)),
                lag_ratio=0.25
            ),
            run_time=2.2
        )
        
        self.wait(2.44) # Wait remaining for Segment 13 (total 5.44s exactly)
        
        # Kết thúc phân cảnh: Fade out toàn bộ
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
