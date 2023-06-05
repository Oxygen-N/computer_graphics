import sys
import sdl2
import numpy as np
import sdl2.ext as lib
from variables import *

t = np.arange(0, 2 * np.pi, 0.005)
pos = 1
num = 1
f = 0
kor_x, kor_y = 0, 0


def figure(renderer):
    global pos, num, f, kor_x, kor_y

    def rend():
        global f
        renderer.clear()
        for i in t:
            if num == 1:
                x = A1 * np.cos(i) ** 2 + L1 * np.cos(i)
                y = A1 * np.cos(i) * np.sin(i) + L1 * np.sin(i)
                xn = (x * np.cos(f) - y * np.sin(f))
                yn = (x * np.sin(f) + y * np.cos(f))
                renderer.draw_point([xn * pos + screenWight / 2.3 + kor_x, yn * pos + screenHeight / 2 + kor_y],
                                    lib.Color(255, 255, 255))

            if num == 2:
                x = A2 * np.cos(i) ** 2 + L2 * np.cos(i)
                y = A2 * np.cos(i) * np.sin(i) + L2 * np.sin(i)
                xn = (x * np.cos(f) - y * np.sin(f))
                yn = (x * np.sin(f) + y * np.cos(f))
                renderer.draw_point([xn * pos + screenWight / 2.3 + kor_x, yn * pos + screenHeight / 2 + kor_y],
                                    lib.Color(255, 255, 255))

            if num == 3:
                x = A3 * np.cos(i) ** 2 + L3 * np.cos(i)
                y = A3 * np.cos(i) * np.sin(i) + L3 * np.sin(i)
                xn = (x * np.cos(f) - y * np.sin(f))
                yn = (x * np.sin(f) + y * np.cos(f))
                renderer.draw_point([xn * pos + screenWight / 2.3 + kor_x, yn * pos + screenHeight / 2 + kor_y],
                                    lib.Color(255, 255, 255))
        for x in range(3):
            for y in range(3):
                renderer.draw_point([x + screenWight / 2.3 + kor_x, y + screenHeight / 2 + kor_y], lib.Color(255, 0, 0))
        if f == 360:
            f = 0

        renderer.present()

    rend()

    while True:
        for e in lib.get_events():
            if e.type == sdl2.SDL_QUIT:
                exit(0)
                sys.exit()
            if e.key.keysym.sym == sdl2.SDLK_ESCAPE:
                exit(0)
                sys.exit()
            if e.key.keysym.sym == sdl2.SDLK_EQUALS:
                pos += 0.03
            if e.key.keysym.sym == sdl2.SDLK_MINUS:
                pos -= 0.03
            if e.key.keysym.sym == sdl2.SDLK_1:
                f = 0
                num = 1
                pos = 1
            if e.key.keysym.sym == sdl2.SDLK_2:
                f = 0
                num = 2
                pos = 1
            if e.key.keysym.sym == sdl2.SDLK_3:
                f = 0
                pos = 1
                num = 3
            if e.key.keysym.sym == sdl2.SDLK_r:
                f -= 0.2
            if e.key.keysym.sym == sdl2.SDLK_l:
                f += 0.2
            if e.key.keysym.sym == sdl2.SDLK_LEFT:
                kor_x -= 1
            if e.key.keysym.sym == sdl2.SDLK_RIGHT:
                kor_x += 1
            if e.key.keysym.sym == sdl2.SDLK_UP:
                kor_y -= 1
            if e.key.keysym.sym == sdl2.SDLK_DOWN:
                kor_y += 1

        rend()


def window_start(name):
    lib.init()
    window = lib.Window(name, size=(screenWight, screenHeight))
    window.show()
    return lib.Renderer(window)


def main():
    figure(window_start("Project"))


if __name__ == '__main__':
    main()
