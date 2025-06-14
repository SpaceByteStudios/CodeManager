from manim import *
from typing import Any

class CodeManager:
    default_background_config: dict[str, Any] = {
        "buff": 0.3,
        "corner_radius": 0.1,
        "stroke_width": 0.0,
        "fill_opacity": 1.0,
        "fill_color": "#1c2032",
    }
    
    default_highlight_config: dict[str, Any] = {
        "corner_radius": 0.0,
        "stroke_width": 1.0,
        "color" : "#BF285A",
        "fill_opacity": 0.1,
        "fill_color": "#ff3377",
    }

    default_selection_config: dict[str, Any] = {
        "corner_radius": 0.0,
        "stroke_width": 0.0,
        "fill_opacity": 0.0,
        "fill_color": "#E92164",
    }

    def __init__(
            self, 
            scene: Scene, 
            background_config: dict[str, Any] = {}, 
            highlight_config: dict[str, Any] = {},
            selection_config: dict[str, Any] = {}
        ):
            self.scene = scene

            self.buttons = VGroup()
            self.code_lines = VGroup()

            self.background_rect = None
            self.shadows = None
            self.background = VGroup()
            self.full_code = VGroup()


            self.background_config: dict[str, Any] = self.default_background_config.copy()
            self.background_config.update(background_config)
            self.highlight_config: dict[str, Any] = self.default_highlight_config.copy()
            self.highlight_config.update(highlight_config)
            self.selection_config: dict[str, Any] = self.default_selection_config.copy()
            self.selection_config.update(selection_config)

            self.cursor = None
            self.highlight = None
            self.selection = None

            self.setup_manager()
    
    def setup_manager(self):
        self.cursor = Rectangle(
            color = "#e85290",
            fill_color = "#e85290",
            fill_opacity = 1.0,
            height = 0.15,
            width = 0.075,
        )        

        self.highlight = SurroundingRectangle(
            self.code_lines,
            **self.highlight_config
        )

        self.highlight.stretch_to_fit_height(0.2)

        self.selection = SurroundingRectangle(
            self.code_lines,
            **self.selection_config
        )

        self.selection.stretch_to_fit_height(0.25)

    def create_background(self):
        self.buttons = VGroup(
            Dot(radius = 0.1, stroke_width = 0, color = button_color)
            for button_color in ["#ff5f56", "#ffbd2e", "#27c93f"]
        )

        self.buttons.arrange(RIGHT, buff = 0.1)
        self.buttons.next_to(self.code_lines, UP, buff=0.25)
        self.buttons.align_to(self.code_lines, LEFT)

        self.background_rect = SurroundingRectangle(
            VGroup(self.code_lines, self.buttons),
            **self.background_config
        )

        self.shadows = VGroup()
        for i in range(1, 5):
            layer = self.background_rect.copy()
            layer.stretch_to_fit_width(self.background_rect.width + 0.1 * i)
            layer.stretch_to_fit_height(self.background_rect.height + 0.1 * i)
            layer.set_fill(BLACK, opacity = 0.03 * (5 - i))
            self.shadows.add(layer)

        self.background = VGroup(self.shadows, self.background_rect, self.buttons)
        self.full_code = VGroup(self.background, self.code_lines, self.highlight, self.selection)

        self.update_highlight_width()

    def set_code(self, lines):
        self.code_lines = VGroup()

        for line in lines:
            line.set_height(0.21)
            line.arrange(RIGHT, buff = 0.1)

            for part in line:
                part.align_to(line, UP)
            
            self.code_lines.add(line)

        self.code_lines.arrange(DOWN, aligned_edge = LEFT, buff = 0.1)

    def indent_line(self, line_number):
        self.code_lines[line_number - 1].shift(RIGHT * 0.4)

    def set_cursor(self, line_number):
        self.cursor.move_to(self.code_lines[line_number - 1][0][0])
        self.highlight.match_y(self.cursor)

    def type_line(self, line_number):
        self.set_cursor(line_number)
        for part in self.code_lines[line_number - 1]:
            self.scene.play(TypeWithCursor(part, self.cursor, buff = 0.05, time_per_char = 0.05))

    def untype_line(self, line_number):
        self.set_cursor(line_number)
        for part in reversed(self.code_lines[line_number - 1]):
            self.scene.play(UntypeWithCursor(part, self.cursor, buff = 0.05, time_per_char = 0.05))

    def type_part_line(self, line_number, parts):
        self.set_cursor(line_number)
        for part in self.code_lines[line_number - 1][-parts:]:
            self.scene.play(TypeWithCursor(part, self.cursor, buff = 0.05, time_per_char = 0.05))

    def untype_part_line(self, line_number, parts):
        self.set_cursor(line_number)
        for part in reversed(self.code_lines[line_number - 1][-parts:]):
            self.scene.play(UntypeWithCursor(part, self.cursor, buff = 0.05, time_per_char = 0.05))

    def select_line(self, line_number):
        self.highlight.shift(UP * 100)
        self.selection.set_opacity(0.2)
        self.selection.match_y(self.code_lines[line_number - 1])
        self.selection.stretch_to_fit_width(self.code_lines[line_number - 1].width)
        self.selection.align_to(self.code_lines[line_number - 1], LEFT)
        self.cursor.move_to(self.code_lines[line_number - 1][0][0])

    def add_line(self, line_number):
        color = self.background_config["fill_color"]
        new_line = VGroup( MarkupText(f'<span foreground="{color}">i</span>') )
        new_line.set_height(0.21)
        new_line.arrange(RIGHT, buff = 0.1)

        for part in new_line:
            part.align_to(new_line, UP)
        
        new_line.align_to(self.code_lines, LEFT)

        self.code_lines.insert(line_number - 1, new_line)

        for line in self.code_lines:
            print(line.height)

    def remove_line(self, line_number):
        self.scene.play(FadeOut(self.code_lines[line_number - 1], run_time = 0.01))
        self.selection.set_opacity(0.0)
        self.highlight.match_y(self.cursor)
        self.code_lines.remove(self.code_lines[line_number - 1])
        self.set_cursor(line_number - 1)

    def change_line(self, line_number, content):
        self.cursor.move_to(self.code_lines[line_number - 1][0][0])
        self.highlight.match_y(self.cursor)
        for part in reversed(self.code_lines[line_number - 1]):
            self.scene.play(UntypeWithCursor(part, self.cursor, buff = 0.05, time_per_char = 0.05))

        content.arrange(RIGHT, buff = 0.1)

        for part in content:
            part.align_to(content, UP)
        
        content.move_to(self.code_lines[line_number - 1], aligned_edge = LEFT)

        self.code_lines[line_number - 1] = content

        self.scene.wait(0.25)        

        for part in self.code_lines[line_number - 1]:
            self.scene.play(TypeWithCursor(part, self.cursor, buff = 0.05, time_per_char = 0.05))

    def replace_line(self, line_number, content):
        self.scene.play(FadeOut(self.code_lines[line_number - 1], run_time = 0.01))

        content.arrange(RIGHT, buff = 0.1)

        for part in content:
            part.align_to(content, UP)
        
        content.move_to(self.code_lines[line_number - 1], aligned_edge = LEFT)

        self.code_lines[line_number - 1] = content

        self.cursor.move_to(self.code_lines[line_number - 1][0][0])
        self.highlight.match_y(self.cursor)

        for part in self.code_lines[line_number - 1]:
            self.scene.play(TypeWithCursor(part, self.cursor, buff = 0.05, time_per_char = 0.05))

    def resize_background(self):
        animations = []
        
        lines_copy = self.code_lines.copy()
        top_y = lines_copy.get_top()[1]
        lines_copy.arrange(DOWN, buff = 0.1)
        lines_copy.shift(DOWN * (lines_copy.get_top()[1] - top_y))

        new_background_rect = SurroundingRectangle(
            VGroup(lines_copy, self.buttons),
            **self.background_config
        )

        animations.append(self.background_rect.animate.become(new_background_rect))

        for i in range(len(self.shadows)):
            new_shadow = new_background_rect.copy()
            new_shadow.stretch_to_fit_width(new_background_rect.width + 0.1 * (i + 1))
            new_shadow.stretch_to_fit_height(new_background_rect.height + 0.1 * (i + 1))
            new_shadow.set_fill(BLACK, opacity = 0.03 * (4 - i))
            animations.append(self.shadows[i].animate.become(new_shadow))

        self.scene.play(*animations)

        self.update_highlight_width()

    def update_highlight_width(self):
        self.highlight.stretch_to_fit_width(self.background_rect.width)
        self.highlight.align_to(self.background_rect, LEFT)

    def refactor_code(self):
        x_coords = [line.get_x() for line in self.code_lines]
        top_y = self.code_lines.get_top()[1]

        self.code_lines.arrange(DOWN, buff = 0.1)

        for line, x in zip(self.code_lines, x_coords):
            line.set_x(x)
        
        self.code_lines.shift(DOWN * (self.code_lines.get_top()[1] - top_y))