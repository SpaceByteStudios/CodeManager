from manim import *
from codeManager import *

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

        self.play(FadeIn(code_manager.background))

        self.add(code_manager.highlight)
        self.add(code_manager.selection)

        code_manager.type_line(1)
        code_manager.type_line(4)
        self.wait(1.0)
        code_manager.indent_line(3)
        code_manager.type_line(3)
        self.wait(0.5)

        code_manager.add_line(1)

        code_manager.resize_background()
        code_manager.refactor_code()

        self.wait(1.0)

        uv_line = VGroup(
            MarkupText('<span foreground="#feb43c">vec2 </span>'),
            MarkupText('uv = fragCoord / iResolution.xy;')
        )

        code_manager.indent_line(2)
        code_manager.replace_line(2, uv_line)

        self.wait(1.0)

        new_frag_line = VGroup(
            MarkupText('fragColor = '),
            MarkupText('<span foreground="#feb43c">vec4(</span>'),
            MarkupText('<span foreground="#ff0022">uv.x</span>, '),
            MarkupText('<span foreground="#00ff22">uv.y</span>, '),
            MarkupText('<span foreground="#75ff85">0.0</span>, '),
            MarkupText('<span foreground="#75ff85">1.0</span>'),
            MarkupText('<span foreground="#feb43c">)</span>;')
        )

        code_manager.change_line(4, new_frag_line)

        code_manager.add_line(100)
        code_manager.add_line(100)

        code_manager.resize_background()
        code_manager.refactor_code()

        comment_line = VGroup(
            MarkupText('<span foreground="#75ff85">//This is a Comment :)</span>'),
        )

        code_manager.replace_line(7, comment_line)
        self.wait(1.0)

        code_manager.select_line(7)
        self.wait(1.0)

        code_manager.remove_line(6)
        code_manager.remove_line(6)

        self.wait(0.5)

        code_manager.resize_background()
        code_manager.refactor_code()

        self.play(code_manager.full_code.animate.to_corner(UL))
        self.play(code_manager.full_code.animate.to_corner(UR))
        self.play(code_manager.full_code.animate.center())

        self.play(FadeOut(code_manager.full_code))