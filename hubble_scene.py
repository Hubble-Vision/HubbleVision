from manimlib import *

class HubbleIntro(Scene):
    def construct(self):
        title = Text('Estimating Hubble\'s Constant', font = 'Helvetica', font_size = 48)
        subtitle = Text('Using a CNN trained on red-shifted galaxy images', font = 'Helvetica', font_size = 32)
        subtitle.next_to(title, DOWN)
        self.play(Write(title), FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
