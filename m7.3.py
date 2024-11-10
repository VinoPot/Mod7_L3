import tkinter as tk
from tkinter import messagebox, colorchooser, filedialog
from PIL import Image, ImageDraw, ImageTk


class Paint:
    def __init__(self, root):
        self.root = root
        self.root.title("Графический редактор")

        self.canvas = tk.Canvas(root, bg='white', width=500, height=500)
        self.canvas.pack()

        self.image = Image.new("RGB", (500, 500), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Начальная толщина пера и цвет
        self.pen_thickness = 1
        self.pen_color = 'black'

        # Поле ввода для толщины пера
        self.thickness_frame = tk.Frame(root)
        self.thickness_frame.pack(side=tk.TOP, pady=5)

        self.thickness_label = tk.Label(self.thickness_frame, text="Толщина пера:")
        self.thickness_label.pack(side=tk.LEFT)

        self.thickness_entry = tk.Entry(self.thickness_frame, width=5)
        self.thickness_entry.pack(side=tk.LEFT)

        # Кнопка установки толщины пера
        self.set_thickness_button = tk.Button(self.thickness_frame, text="Установить", command=self.set_thickness)
        self.set_thickness_button.pack(side=tk.LEFT)

        # Кнопка выбора цвета
        self.color_button = tk.Button(root, text="Выбрать цвет", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT)

        # Кнопка очистки холста
        self.clear_button = tk.Button(root, text="Очистить холст", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)

        # Кнопка сохранения рисунка
        self.save_button = tk.Button(root, text="Сохранить рисунок", command=self.save_image)
        self.save_button.pack(side=tk.LEFT)

        # Привязка событий рисования
        self.canvas.bind("<B1-Motion>", self.paint)

    def set_thickness(self):
        try:
            # Получаем значение из поля ввода
            thickness = int(self.thickness_entry.get())

            if thickness > 0:
                self.pen_thickness = thickness
            else:
                messagebox.showerror("Ошибка", "Толщина пера должна быть положительным числом.")

        except ValueError:
            messagebox.showerror("Ошибка", "Толщина пера должна быть целым числом.")

    def choose_color(self):
        # Выбор цвета с помощью диалогового окна
        color = colorchooser.askcolor()[1]
        if color:
            self.pen_color = color

    def clear_canvas(self):
        # Очистка холста и изображения
        self.canvas.delete("all")
        self.image = Image.new("RGB", (500, 500), "white")
        self.draw = ImageDraw.Draw(self.image)

    def paint(self, event):
        # Используем текущую толщину и цвет пера для рисования
        x, y = event.x, event.y
        self.draw.line((x, y, x + self.pen_thickness, y + self.pen_thickness), fill=self.pen_color, width=self.pen_thickness)

        # Обновление отображения на холсте
        self.update_canvas()

    def update_canvas(self):
        # Обновление объектов Canvas
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image, tags="bg")

    def save_image(self):
        # Предоставление форматов файлов для выбора
        filetypes = [("PNG файл", "*.png"), ("JPEG файл", "*.jpg"), ("Все файлы", "*.*")]

        # Диалоговое окно выбора места сохранения и формата
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=filetypes)

        if file_path:  # Если  указал место для сохранения
            try:
                # Определение формата по расширению
                file_format = file_path.split('.')[-1].upper()
                self.image.save(file_path, file_format)
                messagebox.showinfo("Успех", f"Изображение сохранено как {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить изображение: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Paint(root)
    root.mainloop()