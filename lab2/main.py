import sys
import sdl2
import numpy as np
import sdl2.ext as lib

screenWight = 700
screenHeight = 700

kor_x, kor_y = 0, 0  # перемещение
f = 0  # поворот
pos = 1  # масштаб
corner = 4  # количество углов
number_figure = 0  # количество внутренних фигур
x_cord_first_figure = np.zeros(corner)
y_cord_first_figure = np.zeros(corner)


# def inside_figure(renderer):
#     global x_cord_first_figure, y_cord_first_figure
#
#     X_temp = np.zeros(corner)
#     Y_temp = np.zeros(corner)
#
#     for i in range(number_figure):
#         for j in range(corner):
#             t = j + 1
#             if j == corner-1:
#                 t = 0
#             X_temp[j] = x_cord_first_figure[j] + (x_cord_first_figure[t] - x_cord_first_figure[j]) / 10
#             Y_temp[j] = y_cord_first_figure[j] + (y_cord_first_figure[t] - y_cord_first_figure[j]) / 10
#
#         for j in range(corner):
#             t = j + 1
#             if j == corner-1:
#                 t = 0
#             renderer.draw_line(((X_temp[j], Y_temp[j]), (X_temp[t], Y_temp[t])), lib.Color(255, 255, 255))
#
#         for j in range(corner):
#             x_cord_first_figure[j] = X_temp[j]
#             y_cord_first_figure[j] = Y_temp[j]


def figure(renderer):
    global f, pos, corner, kor_x, kor_y, number_figure, x_cord_first_figure, y_cord_first_figure

    def rend():
        renderer.clear()

        x_cord_first_figure = np.zeros(corner)
        y_cord_first_figure = np.zeros(corner)

        for i in range(corner):  # создание первой фигуры
            X_temp = np.cos(2 * np.pi * i / corner) * 100
            Y_temp = np.sin(2 * np.pi * i / corner) * 100
            xn = (X_temp * np.cos(f) - Y_temp * np.sin(f))
            yn = (X_temp * np.sin(f) + Y_temp * np.cos(f))
            x_cord_first_figure[i] = xn * pos + screenWight / 2
            y_cord_first_figure[i] = yn * pos + screenHeight / 2

        for i in range(corner):  # рисование первой фигуры
            t = i + 1
            if t == corner:
                t = 0
            renderer.draw_line(((x_cord_first_figure[i] + kor_x, y_cord_first_figure[i] + kor_y),
                                (x_cord_first_figure[t] + kor_x, y_cord_first_figure[t] + kor_y)),
                               lib.Color(255, 255, 255))


        X_temp = np.zeros(corner)
        Y_temp = np.zeros(corner)

        for i in range(number_figure):
            for j in range(corner):
                t = j + 1
                if j == corner-1:
                    t = 0
                X_temp[j] = x_cord_first_figure[j] + (x_cord_first_figure[t] - x_cord_first_figure[j]) / 10
                Y_temp[j] = y_cord_first_figure[j] + (y_cord_first_figure[t] - y_cord_first_figure[j]) / 10

            for j in range(corner):
                t = j + 1
                if j == corner-1:
                    t = 0
                renderer.draw_line(((X_temp[j] + kor_x, Y_temp[j] + kor_y), (X_temp[t] + kor_x, Y_temp[t] + kor_y)), lib.Color(255, 255, 255))

            for j in range(corner):
                x_cord_first_figure[j] = X_temp[j]
                y_cord_first_figure[j] = Y_temp[j]

        # inside_figure(renderer)

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
            if e.key.keysym.sym == sdl2.SDLK_UP:
                kor_y -= 5
            if e.key.keysym.sym == sdl2.SDLK_DOWN:
                kor_y += 5
            if e.key.keysym.sym == sdl2.SDLK_LEFT:
                kor_x -= 5
            if e.key.keysym.sym == sdl2.SDLK_RIGHT:
                kor_x += 5
            if e.key.keysym.sym == sdl2.SDLK_EQUALS:
                pos += 0.05
            if e.key.keysym.sym == sdl2.SDLK_MINUS:
                pos -= 0.05
            if e.key.keysym.sym == sdl2.SDLK_r:
                f -= 0.2
            if e.key.keysym.sym == sdl2.SDLK_l:
                f += 0.2
            if e.key.keysym.sym == sdl2.SDLK_q:  # количество углов
                kor_x, kor_y = 0, 0
                corner += 1
                pos = 1
                f = 0
            if e.key.keysym.sym == sdl2.SDLK_w:
                kor_x, kor_y = 0, 0
                corner -= 1
                pos = 1
                f = 0
                if corner < 3:
                    corner = 3
            if e.key.keysym.sym == sdl2.SDLK_x:  # количество фигур
                number_figure += 1
            if e.key.keysym.sym == sdl2.SDLK_z:
                number_figure -= 1
                if number_figure < 1:
                    number_figure = 1

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
