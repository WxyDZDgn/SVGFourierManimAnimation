import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from manimlib import *
from manimlib.utils.space_ops import complex_to_R3, R3_to_complex
from Fourier import Fourier
from SVG import SVG


class RotatingVectors(Scene):
    def setup(self):
        self.camera.frame.set_width(5000)

    def construct(self):
        repet_count = 2
        slow_ratio = 8
        tail_ratio = 0.8
        max_stroke_width = 3

        svg = SVG('res/QianJianTec1737905305902.svg')
        fourier = Fourier(svg.fitting_parameters(500))
        initial_vectors = [ORIGIN]
        radiuses = []
        # max_length_of_vectors, min_length_of_vectors = None, None
        for vector in fourier.get_vectors(0):
            # if max_length_of_vectors is None or min_length_of_vectors is None:
            #     max_length_of_vectors, min_length_of_vectors = abs(vector), abs(vector)
            # else:
            #     max_length_of_vectors, min_length_of_vectors = max(max_length_of_vectors, abs(vector)), min(min_length_of_vectors, abs(vector))
            initial_vectors.append(initial_vectors[-1] + complex_to_R3(vector))
            radiuses.append(abs(vector))
        # 每个向量的旋转速度（以度每秒为单位）
        rotation_speeds = [(2 * math.pi * k) for k in range(-fourier.level, fourier.level + 1)]

        # 创建向量
        vectors = []
        circles = []
        for i in range(1, len(initial_vectors)):
            # rg = math.sqrt(max_length_of_vectors) - math.sqrt(min_length_of_vectors)
            # current = R3_to_complex(initial_vectors[i])
            # rt = math.sqrt(abs(current)) - math.sqrt(min_length_of_vectors)
            vector = Arrow(start=initial_vectors[i - 1], end=initial_vectors[i], buff=0).set_stroke(
                width=(max_stroke_width * (1 - i / len(initial_vectors)))).set_opacity(1 - i / len(initial_vectors))
            vectors.append(vector)
        for i in range(len(radiuses)):
            circle = Arc(0, 2 * math.pi, radius=radiuses[i]).set_stroke(
                width=(max_stroke_width * (1 - i / len(radiuses)))).set_opacity(1 - i / len(radiuses)).set_fill(
                opacity=0)
            circles.append(circle)

        # 定义更新函数
        def update_vector(vector, i):
            def updater(mob, dt):
                # 将旋转速度从度每秒转换为弧度每秒
                rotation_speed = rotation_speeds[i] / slow_ratio
                # 旋转向量
                mob.rotate(rotation_speed * dt, about_point=mob.get_start())
                # 更新下一个向量的起始位置
                if i < len(vectors) - 1:
                    next_vector = vectors[i + 1]
                    next_vector.put_start_and_end_on(mob.get_end(),
                                                     mob.get_end() + (next_vector.get_end() - next_vector.get_start()))

            return updater

        def update_circle(circle, i, vector):
            def updater(mob, dt):
                # 更新下一个向量的起始位置
                if i < len(circles) - 1:
                    next_circle = circles[i + 1]
                    next_circle.move_arc_center_to(vector.get_end())

            return updater

        # 为每个向量添加更新函数
        for i, vector in enumerate(vectors):
            vector.add_updater(update_vector(vector, i))
            self.add(vector)
        for i, circle in enumerate(circles):
            circle.add_updater(update_circle(circle, i, vectors[i]))
            self.add(circle)

        tail = TracingTail(
            vectors[-1].get_end,
            stroke_color=YELLOW,
            stroke_width=3,
            time_traced=(slow_ratio * tail_ratio)
        )
        self.add(tail)

        # 播放动画
        self.wait(repet_count * slow_ratio)  # 可以根据需要调整播放时间
