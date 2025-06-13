from manim import *
from typing import Any

class CodeWithCodeManager(Scene):
    def construct(self):
        self.camera.background_color = "#10121c"

        MarkupText.set_default(font = "Consolas", font_size = 16, color = "#fff7f8")
        TypeWithCursor.set_default(leave_cursor_on = False)
        UntypeWithCursor.set_default(leave_cursor_on = False)
        
        #Individual Code Lines
        line1 = VGroup(
            MarkupText('<span foreground="#ff3377">void </span>'),
            MarkupText('mainImage'),
            MarkupText('<span foreground="#feb43c">(out vec4 </span>'),
            MarkupText('fragColor, '),
            MarkupText('<span foreground="#feb43c">in vec4 </span>'),
            MarkupText('fragCoord'),
            MarkupText('<span foreground="#feb43c">){</span>')
        )

        line2 = VGroup( MarkupText('<span foreground="#1c2032">i</span>') )
        line3 = VGroup(
            MarkupText('fragColor = '),
            MarkupText('<span foreground="#feb43c">vec4(</span>'),
            MarkupText('<span foreground="#75ff85">0.0</span>, '),
            MarkupText('<span foreground="#75ff85">0.5</span>, '),
            MarkupText('<span foreground="#75ff85">1.0</span>, '),
            MarkupText('<span foreground="#75ff85">1.0</span>'),
            MarkupText('<span foreground="#feb43c">)</span>;')
        )

        line4 = VGroup( MarkupText('<span foreground="#feb43c">}</span>') )

        all_lines = [
            line1,
            line2,
            line3,
            line4
        ]

        code_manager = CodeManager(self)

        code_manager.set_code(all_lines)
        code_manager.create_background()

        code_manager.indent_line(2)
        code_manager.indent_line(3)

        self.play(FadeIn(code_manager.background))

        self.add(code_manager.highlight)
        self.add(code_manager.selection)

        code_manager.type_line(1)
        code_manager.type_line(4)
        code_manager.blink_cursor(1)
        code_manager.type_line(3)
        code_manager.blink_cursor(1)

        code_manager.add_line(1)

        code_manager.resize_background()
        code_manager.refactor_code()

        code_manager.blink_cursor(1)

        uv_line = VGroup(
            MarkupText('<span foreground="#feb43c">vec2 </span>'),
            MarkupText('uv = fragCoord / iResolution.xy;')
        )

        code_manager.indent_line(2)
        code_manager.replace_line(2, uv_line)

        code_manager.add_line(100)
        code_manager.add_line(100)
        code_manager.add_line(100)
        code_manager.add_line(100)
        code_manager.add_line(100)

        code_manager.resize_background()
        code_manager.refactor_code()

        new_line = VGroup(
            MarkupText('<span foreground="#ff3377">Colored </span>'),
            MarkupText('<span foreground="#00ff77">TEXT!</span>')
        )

        code_manager.replace_line(10, new_line)

        #code_manager.select_line(10)
        #self.wait(1.0)
        #code_manager.remove_line(10)
        #self.wait(1.0)

        self.play(code_manager.full_code.animate.to_corner(UL))
        self.play(code_manager.full_code.animate.to_corner(DR))
        self.play(code_manager.full_code.animate.center())



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

            self.background_rect = SurroundingRectangle()
            self.shadows = SurroundingRectangle()
            self.background = VGroup()
            self.full_code = VGroup()


            self.background_config: dict[str, Any] = self.default_background_config.copy()
            self.background_config.update(background_config)
            self.highlight_config: dict[str, Any] = self.default_highlight_config.copy()
            self.highlight_config.update(highlight_config)
            self.selection_config: dict[str, Any] = self.default_selection_config.copy()
            self.selection_config.update(selection_config)

            self.cursor = Rectangle()
            self.highlight = SurroundingRectangle()
            self.selection = SurroundingRectangle()

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
        self.update_highlight_width()

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

    def blink_cursor(self, blink_amount):
        self.scene.play(Blink(self.cursor, blinks = blink_amount))

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
        new_line.arrange(RIGHT, buff = 0.1)

        for part in new_line:
            part.align_to(new_line, UP)
        
        new_line.align_to(self.code_lines, LEFT)

        self.code_lines.insert(line_number, new_line)

    def remove_line(self, line_number):
        self.scene.play(FadeOut(self.code_lines[line_number - 1], run_time = 0.01))
        self.selection.move_to(UP * 100)
        self.highlight.match_y(self.cursor)
        self.code_lines.remove(line_number - 1)

    def change_line(self, line_number, content):
        self.cursor.move_to(self.code_lines[line_number - 1][0][0])
        self.highlight.match_y(self.cursor)
        for part in self.code_lines[line_number - 1]:
            self.scene.play(UntypeWithCursor(part, self.cursor, buff = 0.05, time_per_char = 0.05))

        content.arrange(RIGHT, buff = 0.1)

        for part in content:
            part.align_to(content, UP)
        
        content.move_to(self.code_lines[line_number - 1], aligned_edge = LEFT)

        self.code_lines[line_number - 1] = content

        self.cursor.move_to(self.code_lines[line_number - 1][0][0])
        self.highlight.match_y(self.cursor)

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
        x_coords = [m.get_x() for m in self.code_lines]
        top_y = self.code_lines.get_top()[1]

        self.code_lines.arrange(DOWN, buff = 0.1)

        for line, x in zip(self.code_lines, x_coords):
            line.set_x(x)
        
        self.code_lines.shift(DOWN * (self.code_lines.get_top()[1] - top_y))
