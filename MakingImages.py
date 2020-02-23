import numpy as np
import random
# from PIL import Image, ImageDraw
import time
from wand.image import Image as WandImage
from wand.color import Color
from wand.drawing import Drawing
import pandas as pd
from scipy.optimize import curve_fit


def straight(x, a, b):
    return a * x + b


def square(x, a, b, c):
    return a * (x ** 2) + b * x + c


def forth(x, a, b, c, d, e):
    return a * (x ** 4) + b * (x ** 3) + c * (x ** 2) + d * x + e


def sixth(x, a, b, c, d, e, f, g):
    return a * (x ** 6) + b * (x ** 5) + c * (x ** 4) + d * (x ** 3) + \
           e * (x ** 2) + f * x + g


def chosen_func(x, param):
    if param.shape[0] == 2:
        return param[0] * x + param[1]
    elif param.shape[0] == 3:
        return param[0] * (x ** 2) + param[1] * x + param[2]
    elif param.shape[0] == 5:
        return param[0] * (x ** 4) + param[1] * (x ** 3) + param[2] * (x ** 2) + param[3] * x + param[4]
    else:
        return param[0] * (x ** 6) + param[1] * (x ** 5) + param[2] * (x ** 4) + param[3] * (x ** 3) + \
               param[4] * (x ** 2) + param[5] * x + param[6]


func_dict = {2: forth, 3: forth, 4: sixth, 5: forth, 6: straight, 7: straight, 8: straight, 9: square, 10: forth,
             11: forth, 12: forth, 13: square, 14: forth, 15: straight, 16: forth, 17: sixth, 19: square, 20: forth,
             22: forth, 23: square, 24: forth, 26: forth, 27: forth, 28: forth
             }

change_param_dict = {2: 0.01, 3: 0.005, 4: 1e-8, 5: 1e-3, 6: 0.001, 7: 0.001, 8: 0.01, 9: 0.01, 10: 2e-5, 11: 5e-7,
                     12: 4e-6, 13: 5e-5, 14: 1e-4, 15: 5e-5, 16: 1e-6, 17: 5e-8, 19: 0.001, 20: 1e-5, 22: 1e-5,
                     23: 1e-3, 24: 1e-6, 26: 1e-5, 27: 1e-7, 28: 5e-7}

vein_width_dict = {2: (1.5, 2), 3: (1.5, 2), 5: (1.2, 1.3), 22: (1, 1.2), 23: (1, 1.2), 26: (1, 1.2)}


def create_line_img(x_start, x_finish, brush_width, params, img, filename):
    step = 1.01
    draw_img = Drawing()
    draw_img.stroke_color = Color("white")
    draw_img.fill_color = Color("white")
    draw_img.stroke_width = brush_width
    if x_start > x_finish:
        buf = x_start
        x_start = x_finish
        x_finish = buf
    x = x_start + step
    for i in range(3):
        while x < x_finish:
            x1 = x - step
            y1 = chosen_func(x1, params)
            y2 = chosen_func(x, params)
            draw_img.line((x1, y1), (x, y2))
            x = x + 2 * step
        step -= 0.5
        x = x_start + step
    draw_img.draw(img)
    img.save(filename=filename)


def create_filename(num_man):
    dat = time.gmtime()
    file_name = str(dat[0]) + '-' + str(dat[1]) + '-' + str(dat[2]) + '_' + str(dat[3]) + '_' + str(dat[4])
    file_name += '_' + str(dat[5]) + '_' + str(num_man)
    file_name += '.png'
    return file_name


def find_random_diap(param, num_vein):
    n = 0
    while np.abs(param) < 1:
        param *= 10
        n -= 1
    shift = change_param_dict.get(num_vein)
    return (param - shift) * (10 ** n), (param + shift) * (10 ** n)


def generate_images(im_ch, man_ch):
    data = pd.read_excel('VeinsCoordsV05.xlsx')
    ch = 0
    print('Сгенерированные изображения:', end=' ')
    for i in range(1, man_ch + 1):
        oneman_im_ch = 1
        ch += 1
        filename = create_filename(i)
        draw_img = Drawing()
        draw_img.stroke_color = Color("white")
        img = WandImage(width=334, height=118, background=Color("black"))
        img.save(filename=filename)
        for j in func_dict.keys():
            vein = data.iloc[j - 2, 7:]
            start_coord, finish_coord = data.iloc[j - 2, 1], data.iloc[j - 2, 3]
            x, y = prepare_data(vein)
            popt, _ = curve_fit(func_dict.get(j), x, y)
            for k in range(popt.shape[0]):
                a, b = find_random_diap(popt[k], j)
                popt[k] = random.uniform(a, b)
            if j in vein_width_dict.keys():
                brush_width = random.uniform(vein_width_dict.get(j)[0], vein_width_dict.get(j)[1])
            else:
                brush_width = random.uniform(1, 1.5)
            create_line_img(start_coord, finish_coord, brush_width, popt, img, filename)
        img.blur(radius=0, sigma=1)
        img.crop(46, 25, 321, 90)
        img.save(filename=filename)
        oneman_vein_name = filename
        print(ch, end=' ')
        while (oneman_im_ch < im_ch // man_ch) or ((ch + im_ch % man_ch == im_ch) and (im_ch % man_ch)):
            img = WandImage(filename=oneman_vein_name)
            x1_crop = random.randint(0, 40)
            y1_crop = random.randint(0, 2)
            x2_crop = random.randint(265, 275)
            y2_crop = random.randint(60, 63)
            if random.random() >= 0.4:
                alpha = random.randint(-2, 2)
                img.rotate(alpha, background=Color('black'))
            img.crop(x1_crop, y1_crop, x2_crop, y2_crop)
            if random.random() >= 0.5:
                rad = random.randint(1, 10)
                alpha = random.randint(-45, 45)
                img.motion_blur(radius=rad, sigma=8, angle=alpha)
            filename = oneman_vein_name.replace('.png', '_' + str(oneman_im_ch) + '.png')
            img.save(filename=filename)
            oneman_im_ch += 1
            ch += 1
            print(ch, end=' ')
    print('')
    print('Изображения сгенерированы')


def prepare_data(vein):
    x = vein[0::2]
    x = x.astype(str)
    x = [i for i in x if i != 'nan']
    x = np.array(x)
    x = x.astype(float)

    y = vein[1::2]
    y = y.astype(str)
    y = [i for i in y if i != 'nan']
    y = np.array(y)
    y = y.astype(float)

    return x, y
