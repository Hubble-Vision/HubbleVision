import numpy as np
import pandas as pd
from manimlib import *

class HubbleIntro(Scene):
    def construct(self):
        title = Text('Estimating Hubble\'s Constant', font_size = 48)
        subtitle = Text('Using a CNN trained on red-shifted galaxy images', font_size = 32)
        subtitle.next_to(title, DOWN)
        self.play(Write(title), FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

class HubbleLawComparison(Scene):
    def construct(self):
        title = Text('Comparing Expected and Actual Results', font_size = 48)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

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
        y_label = Text('Velocity (km/s)', font_size = 36).next_to(axes[1], LEFT, buff = 0.2)
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

class RedShiftScene(Scene):
    def construct(self):
        title = Text('Redshift / Doppler Effect Simulated', font_size = 48)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))
        self.total_duration = 15
        self.ripple_interval = 0.5
        self.num_ripples = int(self.total_duration / self.ripple_interval)
        self.elapsed = 0
        self.emitted = 0

        self.galaxy = Circle(radius = 0.2, fill_color = WHITE, fill_opacity = 1, stroke_color = WHITE, stroke_width = 1)
        self.galaxy.stretch_to_fit_height(0.25)
        self.galaxy.stretch_to_fit_width(0.5)
        self.galaxy.move_to(LEFT * 5)
        self.add(self.galaxy)
        self.galaxy.add_updater(self.move_galaxy)

        clock = Dot(color = BLACK, fill_opacity = 0)
        clock.add_updater(self.ripple_timer)
        self.add(clock)

        self.wait(self.total_duration)
        self.galaxy.clear_updaters()
        clock.clear_updaters()

    def move_galaxy(self, m, dt):
        m.shift(RIGHT * (12 / self.total_duration) * dt)

    def ripple_timer(self, m, dt):
        self.elapsed += dt
        if self.emitted < self.num_ripples and self.elapsed >= self.emitted * self.ripple_interval:
            t = self.emitted / max(self.num_ripples - 1, 1)
            color = interpolate_color(BLUE, RED_A, t)
            ripple = Circle(radius = 0.2, stroke_color = color, stroke_width = 2, fill_opacity = 0)
            ripple.move_to(self.galaxy.get_center())
            self.add(ripple)
            total_ripple_time = self.total_duration - self.emitted * self.ripple_interval
            ripple.add_updater(lambda m, dt, t = total_ripple_time: self.update_ripple(m, dt, t))
            self.emitted += 1

    def update_ripple(self, m, dt, total_ripple_time):
        if not hasattr(m, 'age'):
            m.age = 0
        m.age += dt
        progress = m.age / total_ripple_time
        radius = 0.2 + (3.0 - 0.2) * progress
        m.set_width(radius * 2)
        m.set_height(radius * 2)
        m.set_stroke(opacity = 1 - progress)
        if progress >= 1:
            m.clear_updaters()
            m.set_opacity(0)