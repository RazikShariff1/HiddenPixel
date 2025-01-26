import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def hide_data(image_path, data, output_path):
    # Open the image using Pillow
    img = Image.open(image_path)

    # Convert the data to binary
    binary_data = ''.join(format(ord(char), '08b') for char in data)

    # Check if the data can be hidden in the image
    if len(binary_data) > img.size[0] * img.size[1] * 3:
        raise ValueError("Data is too large to be hidden in the image.")

    # Embed the data in the image
    data_index = 0
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixel = list(img.getpixel((i, j)))
            for k in range(3):  # Iterate over RGB channels
                if data_index < len(binary_data):
                    pixel[k] = pixel[k] & ~1 | int(binary_data[data_index])
                    data_index += 1
            img.putpixel((i, j), tuple(pixel))

    # Save the new image with the hidden data
    img.save(output_path)

def decrypt_data(image_path):
    # Open the image using Pillow
    img = Image.open(image_path)

    # Extract the hidden data
    binary_data = ''
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixel = list(img.getpixel((i, j)))
            for k in range(3):  # Iterate over RGB channels
                binary_data += str(pixel[k] & 1)

    # Convert binary data to ASCII
    data = ''.join([chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)])

    return data

class SteganographyApp:
    def __init__(self, master):
        self.master = master
        master.title("Steganography App")
        master.configure(bg="#ececec")

        # Create GUI elements
        self.label = tk.Label(master, text="Enter Data:", bg="#ececec", font=("Arial", 12))
        self.entry = tk.Entry(master, width=50, font=("Arial", 12))
        self.browse_button = tk.Button(master, text="Browse Image", command=self.browse_image, bg="#3498db", fg="white", font=("Arial", 10))
        self.hide_button = tk.Button(master, text="Hide Data", command=self.hide_data, bg="#27ae60", fg="white", font=("Arial", 10))
        self.decrypt_button = tk.Button(master, text="Decrypt Data", command=self.decrypt_data, bg="#e74c3c", fg="white", font=("Arial", 10))
        self.status_label = tk.Label(master, text="", bg="#ececec", font=("Arial", 12))
        self.image_path_label = tk.Label(master, text="Image Path: ", bg="#ececec", font=("Arial", 10), wraplength=300)

        # Set up image display
        self.image_label = tk.Label(master)
        self.image_label.grid(row=1, column=0, columnspan=3, pady=10)

        # Arrange GUI elements
        self.label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5)
        self.browse_button.grid(row=0, column=3, padx=10, pady=5)
        self.hide_button.grid(row=1, column=3, padx=10, pady=5)
        self.decrypt_button.grid(row=2, column=3, padx=10, pady=5)
        self.status_label.grid(row=3, column=0, columnspan=4, pady=5)
        self.image_path_label.grid(row=4, column=0, columnspan=3, pady=5)

    def browse_image(self):
        file_path = filedialog.askopenfilename(initialdir='~/Desktop')
        if file_path:
            self.image_path = file_path
            self.image_path_label.config(text=f"Image Path: {file_path}")
            self.display_image()

    def display_image(self):
        img = Image.open(self.image_path)
        img.thumbnail((300, 300))
        tk_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=tk_image)
        self.image_label.image = tk_image

    def hide_data(self):
        data = self.entry.get()
        if data and hasattr(self, 'image_path'):
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                try:
                    hide_data(self.image_path, data, save_path)
                    self.status_label.config(text="Data hidden successfully!", fg="#27ae60")
                except Exception as e:
                    self.status_label.config(text=str(e), fg="#e74c3c")

    def decrypt_data(self):
        if hasattr(self, 'image_path'):
            try:
                decrypted_data = decrypt_data(self.image_path)
                self.status_label.config(text=f"Decrypted Data: {decrypted_data}", fg="#3498db")
            except Exception as e:
                self.status_label.config(text=str(e), fg="#e74c3c")

# Create the main application window
root = tk.Tk()

# Create an instance of the SteganographyApp
app = SteganographyApp(root)

# Run the application
root.mainloop()

       

