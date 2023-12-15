import tkinter as tk
from tkinter import ttk
from colormath.color_objects import sRGBColor, CMYKColor, LabColor, HSVColor
from colormath.color_conversions import convert_color
from tkcolorpicker import askcolor
import pyperclip
from ttkthemes import ThemedTk

class ColorTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ColorTranslator")

        # Variables
        self.from_color_type_var = tk.StringVar()
        self.to_color_type_var = tk.StringVar()
        self.input_color_var = tk.StringVar()
        self.converted_color_var = tk.StringVar()

        # Logo
        self.logo = tk.PhotoImage(file="logo.png")  # Assurez-vous de remplacer ceci par le chemin de votre fichier logo
        self.root.iconphoto(True, self.logo)

        # Interface
        self.create_widgets()

    def create_widgets(self):
        # Appliquer un thème plus clair (adapta)
        self.root.set_theme("adapta")

        # Emoji pour le titre
        emoji_label = tk.Label(self.root, text="🌈 ColorTranslator 🎨", font=("Helvetica", 16))
        emoji_label.grid(column=0, row=0, columnspan=3, pady=10)

        # Labels
        ttk.Label(self.root, text="De type:").grid(column=0, row=1, padx=10, pady=10, sticky=tk.W)
        ttk.Label(self.root, text="Vers type:").grid(column=0, row=2, padx=10, pady=10, sticky=tk.W)
        ttk.Label(self.root, text="Couleur à convertir:").grid(column=0, row=3, padx=10, pady=10, sticky=tk.W)
        ttk.Label(self.root, text="Couleur convertie:").grid(column=0, row=5, padx=10, pady=10, sticky=tk.W)

        # Combobox pour le choix du type de couleur (de et vers)
        from_combobox = ttk.Combobox(self.root, values=("RGB", "HEX", "CMYK", "LAB", "HSV"), textvariable=self.from_color_type_var)
        from_combobox.grid(column=1, row=1, padx=10, pady=10, sticky=tk.W)
        from_combobox.set("RGB")  # Définir la valeur par défaut

        to_combobox = ttk.Combobox(self.root, values=("RGB", "HEX", "CMYK", "LAB", "HSV"), textvariable=self.to_color_type_var)
        to_combobox.grid(column=1, row=2, padx=10, pady=10, sticky=tk.W)
        to_combobox.set("RGB")  # Définir la valeur par défaut

        # Entry pour la couleur à convertir
        entry_color = ttk.Entry(self.root, textvariable=self.input_color_var, width=20)
        entry_color.grid(column=1, row=3, padx=10, pady=10, sticky=tk.W)

        # Bouton de conversion
        convert_button = ttk.Button(self.root, text="Convertir 🔄", command=self.convert_color)
        convert_button.grid(column=2, row=3, padx=10, pady=10, sticky=tk.W)

        # Label pour afficher la couleur convertie
        result_label = ttk.Label(self.root, textvariable=self.converted_color_var)
        result_label.grid(column=1, row=5, columnspan=2, pady=10, sticky=tk.W)

        # Bouton de copie
        copy_button = ttk.Button(self.root, text="Copier 📋", command=self.copy_to_clipboard)
        copy_button.grid(column=0, row=6, columnspan=3, pady=10, sticky=tk.W)

        # Bouton pour choisir une couleur avec la roue des couleurs
        color_picker_button = ttk.Button(self.root, text="Choisir une couleur 🎨", command=self.choose_color)
        color_picker_button.grid(column=0, row=7, columnspan=3, pady=10, sticky=tk.W)

    def convert_color(self):
        from_color_type = self.from_color_type_var.get()
        to_color_type = self.to_color_type_var.get()
        input_color = self.input_color_var.get()

        try:
            converted_color = self.convert_color_type(input_color, from_color_type, to_color_type)
            self.converted_color_var.set(f"Couleur convertie: {converted_color}")

        except ValueError as e:
            self.converted_color_var.set(f"Erreur: {str(e)}")

    def convert_color_type(self, color, from_type, to_type):
        if from_type == to_type:
            return color

        if from_type == "RGB":
            rgb_color = self.parse_rgb(color)
        elif from_type == "HEX":
            rgb_color = self.hex_to_rgb(color)
        elif from_type == "CMYK":
            rgb_color = self.cmyk_to_rgb(color)
        elif from_type == "LAB":
            rgb_color = self.lab_to_rgb(color)
        elif from_type == "HSV":
            rgb_color = self.hsv_to_rgb(color)
        else:
            raise ValueError("Type de couleur source non pris en charge")

        if to_type == "RGB":
            return f"RGB: {rgb_color}"
        elif to_type == "HEX":
            return f"HEX: {self.rgb_to_hex(rgb_color)}"
        elif to_type == "CMYK":
            return f"CMYK: {self.rgb_to_cmyk(rgb_color)}"
        elif to_type == "LAB":
            return f"LAB: {self.rgb_to_lab(rgb_color)}"
        elif to_type == "HSV":
            return f"HSV: {self.rgb_to_hsv(rgb_color)}"
        else:
            raise ValueError("Type de couleur cible non pris en charge")

    def parse_rgb(self, rgb_string):
        return tuple(map(int, rgb_string.split(',')))

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    def cmyk_to_rgb(self, cmyk_color):
        c, m, y, k = map(float, cmyk_color.split(','))
        rgb_color = convert_color(CMYKColor(c, m, y, k), sRGBColor)
        return tuple(int(round(x * 255)) for x in rgb_color.get_value_tuple())

    def lab_to_rgb(self, lab_color):
        l, a, b = map(float, lab_color.split(','))
        rgb_color = convert_color(LabColor(l, a, b), sRGBColor)
        return tuple(int(round(x * 255)) for x in rgb_color.get_value_tuple())

    def hsv_to_rgb(self, hsv_color):
        h, s, v = map(float, hsv_color.split(','))
        rgb_color = convert_color(HSVColor(h, s, v), sRGBColor)
        return tuple(int(round(x * 255)) for x in rgb_color.get_value_tuple())

    def rgb_to_hex(self, rgb_color):
        return "#{:02x}{:02x}{:02x}".format(*rgb_color)

    def rgb_to_cmyk(self, rgb_color):
        rgb_color_normalized = tuple(x / 255.0 for x in rgb_color)
        cmyk_color = convert_color(sRGBColor(*rgb_color_normalized), CMYKColor)
        return ",".join(str(round(x, 2)) for x in cmyk_color.get_value_tuple())

    def rgb_to_lab(self, rgb_color):
        rgb_color_normalized = tuple(x / 255.0 for x in rgb_color)
        lab_color = convert_color(sRGBColor(*rgb_color_normalized), LabColor)
        return ",".join(str(round(x, 2)) for x in lab_color.get_value_tuple())

    def rgb_to_hsv(self, rgb_color):
        rgb_color_normalized = tuple(x / 255.0 for x in rgb_color)
        hsv_color = convert_color(sRGBColor(*rgb_color_normalized), HSVColor)
        return ",".join(str(round(x, 2)) for x in hsv_color.get_value_tuple())

    def copy_to_clipboard(self):
        result_text = self.converted_color_var.get()
        pyperclip.copy(result_text)

    def choose_color(self):
        color = askcolor(color="#ffffff", parent=self.root, title="Choisir une couleur")[1]
        if color:
            self.input_color_var.set(self.rgb_to_hex(self.hex_to_rgb(color)))
            self.convert_color()

if __name__ == "__main__":
    root = ThemedTk(theme="adapta")
    app = ColorTranslatorApp(root)
    root.mainloop()
