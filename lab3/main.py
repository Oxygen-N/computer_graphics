# Алгоритм Сазерленда-Коэна
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
offset_r_x, offset_r_y = 0, 0
offset_t_x, offset_t_y = 0, 0

x_cord_rect = np.zeros(4)
y_cord_rect = np.zeros(4)
x_cord_trap = np.zeros(4)
y_cord_trap = np.zeros(4)


def rectangle1(renderer):
    for i in range(4):  # нахождение координат прямоугольник
        if i == 0:
            n = 1
        elif i == 1:
            n = 5
        elif i == 2:
            n = 7
        else:
            n = 11
        x_temp = 50 * np.cos(n * np.pi / 6 + np.pi)
        y_temp = 80 * np.sin(n * np.pi / 6 + np.pi)
        xn = (x_temp * np.cos(f_r) - y_temp * np.sin(f_r))
        yn = (x_temp * np.sin(f_r) + y_temp * np.cos(f_r))
        x_cord_rect[i] = xn * pos_r + screenWight / 2 + kor_x_r
        y_cord_rect[i] = yn * pos_r + screenHeight / 2 + kor_y_r

    for i in range(4):  # рисование прямоугольника
        t = i + 1
        if t == 4:
            t = 0
        renderer.draw_line(((x_cord_rect[i], y_cord_rect[i]),
                            (x_cord_rect[t], y_cord_rect[t])),
                           lib.Color(255, 255, 255))
    rectangle2(renderer)


def rectangle2(renderer):

    for i in range(4):  # нахождение координат трапеции
        X_temp = np.cos(2 * np.pi * i / 6 + np.pi) * 100
        Y_temp = np.sin(2 * np.pi * i / 6 + np.pi) * 100
        xn = (X_temp * np.cos(f_t) - Y_temp * np.sin(f_t))
        yn = (X_temp * np.sin(f_t) + Y_temp * np.cos(f_t))
        x_cord_trap[i] = xn * pos_t + screenWight / 2
        y_cord_trap[i] = yn * pos_t + screenHeight / 2

    for i in range(4):
        t = i + 1
        if i == 3:
            t = 0
        new_x1, new_y1, new_x2, new_y2, accept = cohen_sutherland_clip(renderer, x_cord_trap[i], y_cord_trap[i], x_cord_trap[t],
                                                                       y_cord_trap[t], min(x_cord_rect),
                                                                       min(y_cord_rect), max(x_cord_rect),
                                                                       max(y_cord_rect))
        if not accept:
            renderer.draw_line(((new_x1, new_y1), (new_x2, new_y2)),
                               lib.Color(255, 255, 255))
        elif accept:
            renderer.draw_line(((new_x1, new_y1), (new_x2, new_y2)),
                               lib.Color(255, 0, 0))
            # print(new_x1, new_y1, new_x2, new_y2)


def cohen_sutherland_clip(renderer, x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    """
    Отсекает отрезок (x1, y1) - (x2, y2) с помощью алгоритма Сазерленда-Коэна, чтобы он находился внутри
    прямоугольника (xmin, ymin) - (xmax, ymax).

    Возвращает (new_x1, new_y1, new_x2, new_y2, accept) - координаты отсеченного отрезка и флаг принятия, где
    accept равен True, если отрезок полностью видим, False в противном случае.
    """

    INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8

    def compute_outcode(x, y):
        """
        Вычисляет код отсечения для заданных координат.
        """
        code = INSIDE
        if x < xmin:
            code |= LEFT
        elif x > xmax:
            code |= RIGHT
        if y < ymin:
            code |= BOTTOM
        elif y > ymax:
            code |= TOP
        return code

    # Вычисляем коды отсечения для начала и конца отрезка
    outcode1 = compute_outcode(x1, y1)
    outcode2 = compute_outcode(x2, y2)
    accept = False

    while True:
        # Проверяем, находится ли отрезок полностью внутри текущего окна
        if not (outcode1 | outcode2):
            accept = True
            break

        # Проверяем, не пересекает ли отрезок текущий окно
        if outcode1 & outcode2:
            # break
            return (x1, y1, x2, y2, accept)

        # Если отрезок пересекает текущий прямоугольник, отсекаем его
        x, y = 0, 0
        if outcode1:
            code_out = outcode1
        else:
            code_out = outcode2

        # Находим точку пересечения
        if code_out & TOP:
            x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
            y = ymax
        elif code_out & BOTTOM:
            x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
            y = ymin
        elif code_out & RIGHT:
            y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
            x = xmax
        elif code_out & LEFT:
            y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
            x = xmin
        renderer.draw_line(((x1, y1), (x2, y2)), lib.Color(255, 255, 255))
        # Обновляем начальную или конечную точку отрезка, в зависимости от того, какую мы отсекли
        if code_out == outcode1:
            x1, y1 = x, y
            outcode1 = compute_outcode(x1, y1)
            renderer.draw_line(((x1, y1), (x2, y2)), lib.Color(255, 255, 255))
        else:
            x2, y2 = x, y
            outcode2 = compute_outcode(x2, y2)
            renderer.draw_line(((x1, y1), (x2, y2)), lib.Color(255, 255, 255))

    return (x1, y1, x2, y2, accept)


def window_start(name):
    lib.init()
    window = lib.Window(name, size=(screenWight, screenHeight))
    window.show()
    return lib.Renderer(window)


def figure(renderer):
    global kor_x_t, kor_y_t, kor_x_r, kor_y_r, pos_t, pos_r, f_r, f_t, offset_r_x, offset_r_y, offset_t_x, offset_t_y

    def rend():

        renderer.clear()

        rectangle1(renderer)
        rectangle2(renderer)

        renderer.present()

    rend()
    drag_rect = False
    drag_trap = False
    while True:
        for e in lib.get_events():
            if e.type == sdl2.SDL_KEYDOWN:
                if e.key.keysym.sym == sdl2.SDLK_w:  # изменения квадрата 2 (trap, большой)
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

                if e.key.keysym.sym == sdl2.SDLK_UP:  # изменения квадрата 1 (rect, маленький)
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

            if e.type == sdl2.SDL_MOUSEBUTTONDOWN and e.button.button == sdl2.SDL_BUTTON_LEFT:
                x, y = e.button.x, e.button.y
                if x_cord_rect[0] <= x <= x_cord_rect[2] and y_cord_rect[0] <= y <= y_cord_rect[2]:
                    drag_rect = True
                    offset_r_x = x - kor_x_r
                    offset_r_y = y - kor_y_r
                elif x_cord_trap[0] <= x <= x_cord_trap[3] and y_cord_trap[1] <= y <= y_cord_trap[0] and not (
                        x_cord_rect[0] <= x <= x_cord_rect[2] and y_cord_rect[0] <= y <= y_cord_rect[2]):
                    drag_trap = True
                    offset_t_x = x - kor_x_t
                    offset_t_y = y - kor_y_t
                print(x_cord_trap[0], x_cord_trap[2], y_cord_trap[2], y_cord_trap[0])
                print(x, y)
            if e.type == sdl2.SDL_MOUSEBUTTONUP and e.button.button == sdl2.SDL_BUTTON_LEFT:
                drag_rect = False
                drag_trap = False
            if e.type == sdl2.SDL_MOUSEMOTION:
                if drag_rect:
                    kor_x_r = e.motion.x - offset_r_x
                    kor_y_r = e.motion.y - offset_r_y
                if drag_trap:
                    kor_x_t = e.motion.x - offset_t_x
                    kor_y_t = e.motion.y - offset_t_y

            if e.type == sdl2.SDL_QUIT:
                exit(0)
                sys.exit()
            if e.key.keysym.sym == sdl2.SDLK_ESCAPE:
                exit(0)
                sys.exit()

        rend()


def main():
    figure(window_start("project"))


if __name__ == '__main__':
    main()
