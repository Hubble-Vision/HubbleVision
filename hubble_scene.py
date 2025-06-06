import numpy as np
import pandas as pd
from manimlib import *

class HubbleIntro(Scene):
    def construct(self):
        title = Text('Estimating Hubble\'s Constant', font = 'Helvetica', font_size = 48)
        subtitle = Text('Using a CNN trained on red-shifted galaxy images', font = 'Helvetica', font_size = 32)
        subtitle.next_to(title, DOWN)
        self.play(Write(title), FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

class HubbleLawComparison(Scene):
    def construct(self):
        df = pd.read_csv('hubble_data.csv').dropna()
        C = 299792.458
        slope = 63.0165

        df['vel_actual'] = C * df['z_actual']
        df['vel_pred'] = df['velocity']
        max_distance = df['distance'].max() * 1.1
        max_velocity = max(df['vel_actual'].max(), df['vel_pred'].max()) * 1.1

        origin = np.array([0, 0, 0])
        x_end = np.array([6, 0, 0])
        y_end = np.array([0, 3, 0])
        axes = VGroup(Line(origin, x_end), Line(origin, y_end))
        center_point = np.array([3, 1.5, 0])
        axes.shift(-center_point)
        self.play(ShowCreation(axes))

        x_label = Text('Distance (Mpc)', font_size = 36).next_to(axes[0], DOWN, buff = 0.2)
        y_label = Text('Velocity (km/s)', font_size=36).next_to(axes[1], LEFT, buff = 0.2)
        self.play(FadeIn(x_label), FadeIn(y_label))

        actual_dots = VGroup(*[Dot(self.coords(r['distance'], r['vel_actual'], max_distance, max_velocity, center_point), radius = 0.05, color = GREY) for _, r in df.iterrows()])
        predicted_dots = VGroup(*[Dot(self.coords(r['distance'], r['vel_pred'], max_distance, max_velocity, center_point), radius = 0.05, color = BLUE) for _, r in df.iterrows()])

        self.play(LaggedStartMap(FadeIn, actual_dots, lag_ratio = 0.02))
        self.wait(0.5)
        self.play(LaggedStartMap(FadeIn, predicted_dots, lag_ratio = 0.02))
        self.wait(0.5)

        connectors = VGroup(*[Line(self.coords(r['distance'], r['vel_actual'], max_distance, max_velocity, center_point), self.coords(r['distance'], r['vel_pred'], max_distance, max_velocity, center_point), stroke_width = 2, color = YELLOW) for _, r in df.iterrows()])
        self.play(LaggedStartMap(ShowCreation, connectors, lag_ratio=0.005))
        self.wait(1)
        self.play(FadeOut(connectors), run_time = 1)

        hubble_end = self.coords(max_distance, slope * max_distance, max_distance, max_velocity, center_point)
        hubble_line = Line(origin - center_point, hubble_end, color = YELLOW)
        slope_label = Text(f'H0 = {slope:.2f}', font_size = 48).next_to(hubble_line, UP, buff = 0.3)
        self.play(ShowCreation(hubble_line), FadeIn(slope_label))
        self.wait(2)
    
    def coords(self, d, v, max_distance, max_velocity, center_point):
        return np.array([d / max_distance * 6, v / max_velocity * 3, 0]) - center_point