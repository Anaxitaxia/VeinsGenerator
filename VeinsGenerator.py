# import tkinter as tk
# from PIL import ImageGrab, Image, ImageDraw
# from tkinter import messagebox as mb
import MakingImages

print('Количество генерируемых изображений: ', end='')
im_ch = int(input())
print('')

print('Количество людей, рисунки вен которых будут сгенерированы: ', end='')
man_ch = int(input())

symb = 'y'
while man_ch > im_ch:
    print('Ожидалось количество человек, меньшее количества изображений. Хотите повторить ввод (Y(y)/N(n))?', end=' ')
    symb = input()
    if symb.lower() == 'y':
        print('Количество людей, рисунки вен которых будут сгенерированы: ', end='')
        man_ch = int(input())
        print()
    else:
        exit()

MakingImages.generate_images(im_ch, man_ch)

'''class MainForm(tk.Frame):
    def __init__(self, master=None, parent=None):
        super().__init__(master)
        self.parent = parent
        self.pack()
        self.center_window()
        self.add_widgets()
        self.master.title('Создание шаблона рисунка вен')
        self.master.resizable(False, False)
        self.focus_set()

    def center_window(self):
        w = 1000
        h = 600
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2 - 45
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def add_widgets(self):
        def print_screen():
            self.update_idletasks()
            x_r = self.master.winfo_x()
            y_r = self.master.winfo_y()
            x_l = x_r + self.master.winfo_width()
            y_l = y_r + self.master.winfo_height()
            picture = ImageGrab.grab(
                (x_r + 10, y_r + 1, x_l, y_l + 45)
            )
            picture.save("screen.png", "PNG")
            mb.showinfo("", "Снимок успешно сделан")

        main_menu = tk.Menu(self.master)
        self.master.config(menu=main_menu)
        main_menu.add_command(label='Скриншот', command=print_screen)
        main_menu.add_command(label='Справка')
        main_menu.add_command(label='Выход', command=quit)

        im_ch_lbl = tk.Label(text="Количество изображений:", bg="LightSteelBlue3")
        one_man_im_lbl = tk.Label(text="Количество изображений вен одного человека:", bg="LightSteelBlue3")
        im_ch_lbl.place(x=30, y=500)
        one_man_im_lbl.place(x=30, y=535)

        global im_ch
        im_ch = tk.IntVar()
        one_man_im = tk.IntVar()
        im_ch.set(1)
        one_man_im.set(1)
        im_ch_entr = tk.Entry(width=10, textvariable=im_ch)
        one_man_im_entr = tk.Entry(width=10, textvariable=one_man_im)
        im_ch_entr.place(x=300, y=500)
        one_man_im_entr.place(x=300, y=535)

        ok_btn = tk.Button(text="Генерировать изображения", width=30, height=3, command=self.press_ok)
        ok_btn.place(x=400, y=500)

    def press_ok(self):
        MakingImages.generate_images(im_ch.get(), 1)
        # MakingImages.create_img(334, 118, 1, 1)


# запускает приложение
def main():
    root = tk.Tk()
    root["bg"] = "LightSteelBlue3"
    app = MainForm(master=root)
    root.mainloop()


if __name__ == '__main__':
    main()'''
