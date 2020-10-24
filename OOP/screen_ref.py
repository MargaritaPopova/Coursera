import pygame
import random
import math


class Screen:

    def __init__(self, dimensions: tuple, name: str):
        self.dimensions = dimensions
        self.game_display = pygame.display.set_mode(dimensions)
        pygame.display.set_caption(name)
        self.hue = 0
        self.color = pygame.Color(0)


class Game:
    def __init__(self, screen: Screen):
        self.screen = screen
        self.steps = 35
        self.working = True
        self.points = []
        self.speeds = []
        self.show_help = False
        self.pause = True
        self.polyline = Polyline(self.screen)
        self.knot = Knot(self.screen)

    def draw_help(self):
        """функция отрисовки экрана справки программы"""
        self.screen.game_display.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["", ""])
        data.append([str(self.steps), "Current points"])

        pygame.draw.lines(self.screen.game_display, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.screen.game_display.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.screen.game_display.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

    def game_loop(self):
        while self.working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.working = False
                    if event.key == pygame.K_r:
                        self.points = []
                        self.speeds = []
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                    if event.key == pygame.K_KP_PLUS:
                        self.steps += 1
                    if event.key == pygame.K_F1:
                        self.show_help = not self.show_help
                    if event.key == pygame.K_KP_MINUS:
                        self.steps -= 1 if self.steps > 1 else 0

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.points.append(Vec2d(event.pos))
                    self.speeds.append(Vec2d((random.random() * 2, random.random() * 2)))

            self.screen.game_display.fill((0, 0, 0))
            hue = (self.screen.hue + 1) % 360
            self.screen.color.hsla = (hue, 100, 50, 100)
            self.polyline.draw_points(self.points)
            self.polyline.draw_points(
                self.knot.get_knot(self.points, self.steps), "line", 3, self.screen.color
            )
            if not self.pause:
                self.polyline.set_points(self.points, self.speeds)
            if self.show_help:
                self.draw_help()

            pygame.display.flip()


class Vec2d:

    def __init__(self, position: tuple):
        self.x = position[0]
        self.y = position[1]

    def __sub__(self, other):
        return Vec2d((self.x - other.x, self.y - other.y))

    def __add__(self, other):
        return Vec2d((self.x + other.x, self.y + other.y))

    def __mul__(self, other):
        return Vec2d((self.x * other, self.y * other))

    def __len__(self):
        return int(math.sqrt(self.x**2 + self.y**2))

    def int_pair(self):
        return self.x, self.y


class Polyline:

    def __init__(self, screen: Screen):
        self.screen = screen

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def draw_points(self, points, style="points", width=3, color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(self.screen.game_display, color,
                                 (int(points[p_n].x), int(points[p_n].y)),
                                 (int(points[p_n + 1].x), int(points[p_n + 1].y)), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(self.screen.game_display, color,
                                   (int(p.x), int(p.y)), width)

    def set_points(self, points, speeds):
        """функция перерасчета координат опорных точек"""
        for p in range(len(points)):
            points[p] = points[p] + speeds[p]
            if points[p].x > self.screen.dimensions[0] or points[p].x < 0:
                speeds[p] = Vec2d((- speeds[p].x, speeds[p].y))
            if points[p].y > self.screen.dimensions[1] or points[p].y < 0:
                speeds[p] = Vec2d((speeds[p].x, -speeds[p].y))


class Knot(Polyline):

    def get_knot(self, points, count):
        if len(points) < 3:
            return []
        res = []
        for i in range(-2, len(points) - 2):
            ptn = []
            ptn.append((points[i] + points[i + 1]) * 0.5)
            ptn.append(points[i + 1])
            ptn.append((points[i + 1] + points[i + 2]) * 0.5)

            res.extend(self.get_points(ptn, count))
        return res


def run():
    pygame.init()
    sc = Screen((800, 600), 'MyScreenSaver')
    g = Game(sc)
    g.game_loop()
    pygame.display.quit()
    pygame.quit()
    exit(0)


if __name__ == '__main__':
    run()
