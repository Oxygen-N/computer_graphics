import sys
import sdl2
import numpy as np
import sdl2.ext as lib

screenWight = 700
screenHeight = 700

pos_t, pos_r = 1, 1
f_t, f_r = 0, 0
kor_x_t, kor_y_t = 0, 0
kor_x_r, kor_y_r = 0, 0

x_cord_rect = np.zeros(4)
y_cord_rect = np.zeros(4)
x_cord_trap = np.zeros(4)
y_cord_trap = np.zeros(4)


def trapezoid(renderer):
    for i in range(4):  # нахождение координат трапеции
        X_temp = np.cos(2 * np.pi * i / 6 + np.pi) * 100
        Y_temp = np.sin(2 * np.pi * i / 6 + np.pi) * 100
        xn = (X_temp * np.cos(f_t) - Y_temp * np.sin(f_t))
        yn = (X_temp * np.sin(f_t) + Y_temp * np.cos(f_t))
        x_cord_trap[i] = xn * pos_t + screenWight / 2
        y_cord_trap[i] = yn * pos_t + screenHeight / 2

    for i in range(4):  # рисование трапеции
        t = i + 1
        if t == 4:
            t = 0
        renderer.draw_line(((x_cord_trap[i] + kor_x_t, y_cord_trap[i] + kor_y_t),
                            (x_cord_trap[t] + kor_x_t, y_cord_trap[t] + kor_y_t)),
                           lib.Color(255, 255, 255))


def rectangle(renderer):

    for i in range(4):  # нахождение координат прямоугольник
        if i == 0:
            n = 1
        elif i == 1:
            n = 5
        elif i == 2:
            n = 7
        else:
            n = 11
        x_temp = -50 + 50 * np.cos(n * np.pi / 6 + np.pi)
        y_temp = 50 * np.sin(n * np.pi / 6 + np.pi)
        xn = (x_temp * np.cos(f_r) - y_temp * np.sin(f_r))
        yn = (x_temp * np.sin(f_r) + y_temp * np.cos(f_r))
        x_cord_rect[i] = xn * pos_r + screenWight / 2
        y_cord_rect[i] = yn * pos_r + screenHeight / 2

    for i in range(4):  # рисование прямоугольника
        t = i + 1
        if t == 4:
            t = 0
        renderer.draw_line(((x_cord_rect[i] + kor_x_r, y_cord_rect[i] + kor_y_r),
                            (x_cord_rect[t] + kor_x_r, y_cord_rect[t] + kor_y_r)),
                           lib.Color(255, 255, 255))


def figure(renderer):
    global kor_x_t, kor_y_t, kor_x_r, kor_y_r, pos_t, pos_r, f_r, f_t

    def rend():

        renderer.clear()

        rectangle(renderer)
        trapezoid(renderer)

        renderer.present()

    rend()

    while True:
        for e in lib.get_events():
            if e.key.keysym.sym == sdl2.SDLK_w:  # изменения трапеции
                kor_y_t -= 5
            if e.key.keysym.sym == sdl2.SDLK_s:
                kor_y_t += 5
            if e.key.keysym.sym == sdl2.SDLK_a:
                kor_x_t -= 5
            if e.key.keysym.sym == sdl2.SDLK_d:
                kor_x_t += 5
            if e.key.keysym.sym == sdl2.SDLK_0:  # масштабирование
                pos_t += 0.05
            if e.key.keysym.sym == sdl2.SDLK_9:
                pos_t -= 0.05
            if e.key.keysym.sym == sdl2.SDLK_z:  # вращение
                f_t -= 0.2
            if e.key.keysym.sym == sdl2.SDLK_x:
                f_t += 0.2

            if e.key.keysym.sym == sdl2.SDLK_UP:  # изменения прямоугольника
                kor_y_r -= 5
            if e.key.keysym.sym == sdl2.SDLK_DOWN:
                kor_y_r += 5
            if e.key.keysym.sym == sdl2.SDLK_LEFT:
                kor_x_r -= 5
            if e.key.keysym.sym == sdl2.SDLK_RIGHT:
                kor_x_r += 5
            if e.key.keysym.sym == sdl2.SDLK_EQUALS:  # масштабирование
                pos_r += 0.05
            if e.key.keysym.sym == sdl2.SDLK_MINUS:
                pos_r -= 0.05
            if e.key.keysym.sym == sdl2.SDLK_c:  # вращение
                f_r -= 0.2
            if e.key.keysym.sym == sdl2.SDLK_v:
                f_r += 0.2

            if e.type == sdl2.SDL_QUIT:
                exit(0)
                sys.exit()
            if e.key.keysym.sym == sdl2.SDLK_ESCAPE:
                exit(0)
                sys.exit()

        rend()


def window_start(name):
    lib.init()
    window = lib.Window(name, size=(screenWight, screenHeight))
    window.show()
    return lib.Renderer(window)


def main():
    figure(window_start("project"))


if __name__ == '__main__':
    main()
