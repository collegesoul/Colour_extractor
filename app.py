from customtkinter import *
from PIL import Image
from tkinter import filedialog
import tkinter as tk
import extractor
import save_delete_colours as sdc


# declaration for the app window
app = CTk()
app.title("Colour Extractor")
app.geometry("675x450+700+200")
app.resizable(False, False)

# constants for colours and fonts
FONT = "Arial"
DARK_GRAY = "gray15"
MEDIUM_GRAY = "gray13"
GRAYISH = "#818589"
DARKER_GRAY = "gray10"
DEFAULT_COLOUR = "transparent"
DEFAULT_HEX = "#FFFFFF"

image_file = ""
extracted_colours = []
saved_indexes, load_saved_colours = sdc.preload_from_json()
colour_palette = []
saved_palette = []

rgb = {"red": "", "green": "", "blue": ""}
hsl = {"hue": "", "sat": "", "light": ""}


# ------------ Button Command Functions ----------- #


def choose_image_file():
    global image_file
    image_file = filedialog.askopenfilename(initialdir="/Downloads",
                                            title="Select a file",
                                            filetypes=(("PNG", "*.png"),))

    my_image = CTkImage(dark_image=Image.open(image_file),
                        size=(182, 200))

    image_label.configure(text="",
                          image=my_image,
                          fg_color=DEFAULT_COLOUR)


def slider_event(value):
    number.configure(text=f"{int(value)}")


def extract_colour():
    global extracted_colours
    global image_file
    number_of_colours = int(slider.get())

    if colour_palette:
        for cells in colour_palette:
            cells.configure(fg_color=DEFAULT_COLOUR, border_color="white")

    if image_file and number_of_colours:
        extracted_colours = extractor.get_colour(image_file, number_of_colours)
        for num in range(number_of_colours):
            colour_palette[num].configure(fg_color=extracted_colours[num]["hex"],
                                          border_color=extracted_colours[num]["hex"])
    else:
        pass


def change_menu_option(event):
    if colour_value_menu.get() == "RGB":
        value1.configure(text=f"Red: {rgb['red']}")
        value2.configure(text=f"Green: {rgb['green']}")
        value3.configure(text=f"Blue: {rgb['blue']}")
    else:
        value1.configure(text=f"Hue: {hsl['hue']}")
        value2.configure(text=f"Sat: {hsl['sat']}")
        value3.configure(text=f"Light: {hsl['light']}")


def save_colour():
    current_colour = colour_palette[ColourCell.clicked].cget("fg_color")
    if current_colour == DEFAULT_COLOUR:
        pass
    else:
        for empty_cell in saved_palette:
            if empty_cell.cget("fg_color") != DEFAULT_COLOUR:
                pass
            else:
                empty_cell.configure(fg_color=current_colour)
                empty_cell.index = saved_palette.index(empty_cell)
                empty_cell.saved_colour_value = ColourCell.clicked
                empty_cell.colour_list_to_return(extracted_colours)
                sdc.save_to_json(
                    empty_cell.index,
                    extracted_colours[empty_cell.saved_colour_value]['rgb'],
                    extracted_colours[empty_cell.saved_colour_value]['hsl'],
                    extracted_colours[empty_cell.saved_colour_value]['hex']
                )
                break


def delete_saved_colour():
    for empty_cell in saved_palette:
        if Palette.palette_colour == saved_palette.index(empty_cell):
            sdc.delete_from_json(Palette.palette_colour)
            empty_cell.delete_palette_colour()
            break


# ------------ Frame for choosing Image and extracting colours ----------- #


first_frame = CTkFrame(app, fg_color="gray13")
first_frame.grid(column=0, row=0, sticky="nsew")

image_label = CTkLabel(first_frame,
                       text="Upload Image",
                       width=200,
                       height=200,
                       fg_color=GRAYISH,
                       text_color="black",
                       corner_radius=10,
                       font=(FONT, 20))

image_label.pack(padx=40, pady=25)

choose_file_btn = CTkButton(first_frame,
                            text="Choose Image file",
                            command=choose_image_file)

choose_file_btn.pack(pady=18)

prompt = CTkLabel(first_frame, text="Select number of colours to extract")
prompt.pack()

slider_frame = CTkFrame(first_frame)
slider_frame.pack(pady=10)

slider = CTkSlider(slider_frame,
                   from_=0, to=10,
                   number_of_steps=10,
                   variable=tk.IntVar(),
                   command=slider_event)

slider.grid(row=0, column=0)

number = CTkLabel(slider_frame, text=f"{int(slider.get())}")
number.grid(row=0, column=1, padx=7)

extract_btn = CTkButton(first_frame, text="Extract", command=extract_colour)
extract_btn.pack(pady=15)


# ------------ Frame for displaying extracted colours and colour values ----------- #


def update_colour_values(num: int, colour_list: list):
    """Updates colours on value labels when menu option is changed"""

    if colour_value_menu.get() == "RGB":
        value1.configure(text=f"Red: {colour_list[num]['rgb'][0]}")
        value2.configure(text=f"Green: {colour_list[num]['rgb'][1]}")
        value3.configure(text=f"Blue: {colour_list[num]['rgb'][2]}")
    else:
        value1.configure(text=f"Hue: {colour_list[num]['hsl'][0]}")
        value2.configure(text=f"Sat: {colour_list[num]['hsl'][1]}")
        value3.configure(text=f"Light: {colour_list[num]['hsl'][2]}")
    hex_value.configure(text=colour_list[num]['hex'])
    for j, key in enumerate(rgb.keys()):
        rgb[key] = colour_list[num]["rgb"][j]
    for j, key in enumerate(hsl.keys()):
        hsl[key] = colour_list[num]["hsl"][j]


# ------------ Colour cell and palette classes ----------- #


class ColourCell(CTkButton):
    clicked = 0
    previous_colour = ""

    def __init__(self, master: any, index=None, border_color="white", fg_color=DEFAULT_COLOUR, **kwargs):
        self.border_color = border_color
        self.fg_color = fg_color
        super().__init__(master, width=30,
                         height=30,
                         fg_color=self.fg_color,
                         border_color=self.border_color,
                         border_width=2,
                         hover=False,
                         text="",
                         command=self.show_colour_value,
                         **kwargs)
        self.index = index

    def show_colour_value(self):
        if not extracted_colours:
            pass
        else:
            if self.index > len(extracted_colours) - 1:
                pass
            else:
                if Palette.is_clicked:
                    Palette.is_clicked = False
                    saved_palette[Palette.palette_colour].configure(border_color=GRAYISH)

                if ColourCell.clicked != self.index:
                    if ColourCell.previous_colour:
                        colour_palette[ColourCell.clicked].configure(border_color=ColourCell.previous_colour)
                    ColourCell.clicked = self.index
                    ColourCell.previous_colour = colour_palette[self.index].cget("border_color")
                    colour_palette[self.index].configure(border_color="red")
                    update_colour_values(self.index, extracted_colours)
                else:
                    ColourCell.previous_colour = colour_palette[self.index].cget("border_color")
                    colour_palette[ColourCell.clicked].configure(border_color="red")
                    update_colour_values(self.index, extracted_colours)


class Palette(ColourCell):
    palette_colour = 0
    is_clicked = False

    def __init__(self, master: any, **kwargs):
        self.saved_colour_value = 0
        self.colour_list = []
        super().__init__(master, **kwargs)

    def colour_list_to_return(self, clist):
        self.colour_list = clist

    def show_colour_value(self):
        if self.index is None:
            pass
        else:
            if ColourCell.previous_colour:
                colour_palette[ColourCell.clicked].configure(border_color=ColourCell.previous_colour)
                ColourCell.previous_colour = ""

            Palette.is_clicked = True

            if Palette.palette_colour != self.index:
                saved_palette[Palette.palette_colour].configure(border_color=GRAYISH)
                Palette.palette_colour = self.index
                saved_palette[self.index].configure(border_color="red")
                update_colour_values(self.saved_colour_value, self.colour_list)
            else:
                saved_palette[self.index].configure(border_color="red")
                update_colour_values(self.saved_colour_value, self.colour_list)

    def delete_palette_colour(self):
        if self.index is None:
            pass
        else:
            Palette.is_clicked = False
            saved_palette[Palette.palette_colour].configure(border_color=GRAYISH)
            saved_palette[Palette.palette_colour].configure(fg_color=DEFAULT_COLOUR)
            self.index = None
            self.colour_list = extracted_colours
            if colour_value_menu.get() == "HSL":
                value1.configure(text="Hue: ")
                value2.configure(text="Sat: ")
                value3.configure(text="Light: ")
            else:
                value1.configure(text="Red: ")
                value2.configure(text="Green: ")
                value3.configure(text="Blue: ")
            for j, key in enumerate(rgb.keys()):
                rgb[key] = ""
            for j, key in enumerate(hsl.keys()):
                hsl[key] = ""
            hex_value.configure(text=DEFAULT_HEX)


# ------------ Frames  ----------- #


second_frame = CTkFrame(app, fg_color=DARK_GRAY)
second_frame.grid(row=0, column=1, sticky="nsew")

extract_colour_frame = CTkFrame(second_frame, fg_color=DARK_GRAY)
extract_colour_frame.pack(pady=30, anchor="center")

colour_value_frame = CTkFrame(second_frame, fg_color=DARK_GRAY)
colour_value_frame.pack(pady=25, anchor="center")

# ------------ Display colour frame widgets  ----------- #


label1 = CTkLabel(extract_colour_frame, text="Colour", font=(FONT, 16))
label1.grid(row=0, column=0, columnspan=5, pady=5)

for i in range(10):
    cell = ColourCell(extract_colour_frame, index=i)
    colour_palette.append(cell)
    if i < 5:
        cell.grid(row=1, column=i, padx=5, pady=5)
    else:
        cell.grid(row=2, column=i - 5, padx=5, pady=5)

save_colour_btn = CTkButton(extract_colour_frame, text="Save Colour", command=save_colour)
save_colour_btn.grid(row=3, column=0, columnspan=5, pady=15)

# ------------ Colour Value frame widgets  ----------- #


label2 = CTkLabel(colour_value_frame,
                  text="Colour Values",
                  font=(FONT, 16))

label2.grid(column=0, row=0, pady=5, columnspan=2, sticky="nsew")

colour_value_menu = CTkOptionMenu(colour_value_frame, values=["RGB", "HSL"], command=change_menu_option)
colour_value_menu.grid(row=1, column=0, padx=7, pady=3)

hex_value = CTkLabel(colour_value_frame, text=DEFAULT_HEX)
hex_value.grid(row=1, column=1, padx=7)

value1 = CTkLabel(colour_value_frame, text="Red: ")
value1.grid(row=2, column=0, sticky="w", padx=7)

value2 = CTkLabel(colour_value_frame, text="Green: ")
value2.grid(row=3, column=0, sticky="w", padx=7)

value3 = CTkLabel(colour_value_frame, text="Blue: ")
value3.grid(row=4, column=0, sticky="w", padx=7)

# ------------ Frame for saving colours ----------- #


third_frame = CTkFrame(app, height=455, fg_color=MEDIUM_GRAY)
third_frame.grid(row=0, column=2, sticky="nsew")

container_frame = CTkFrame(third_frame, fg_color=DARKER_GRAY)
container_frame.pack()

palette_frame = CTkFrame(third_frame, fg_color=MEDIUM_GRAY)
palette_frame.pack(pady=30)

label3 = CTkLabel(container_frame,
                  text="Colour Palette",
                  font=(FONT, 16))

label3.grid(row=0, column=0, padx=7, pady=5)

bin_image = CTkImage(dark_image=Image.open("bin.png"))

remove_btn = CTkButton(container_frame,
                       image=bin_image,
                       text="",
                       width=30,
                       command=delete_saved_colour
                       )

remove_btn.grid(row=0, column=1, padx=10, pady=5)

row_count = -1
column_count = 0

for i in range(24):
    saved_cell = Palette(palette_frame, border_color=GRAYISH)
    if saved_indexes:
        if i < len(saved_indexes):
            saved_cell.index = saved_indexes[i]
            saved_cell.saved_colour_value = saved_cell.index
            saved_cell.colour_list_to_return(load_saved_colours)
            saved_cell.configure(fg_color=load_saved_colours[i]["hex"])
            saved_palette.append(saved_cell)
        else:
            saved_palette.append(saved_cell)
    else:
        saved_palette.append(saved_cell)
    if i % 3 == 0:
        column_count = 0
        row_count = row_count + 1
        saved_cell.grid(row=row_count, column=column_count, padx=7, pady=7)
    else:
        column_count = column_count + 1
        saved_cell.grid(row=row_count, column=column_count, padx=7, pady=7)


app.mainloop()
