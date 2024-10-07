import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def shift_signal(x_values, shift_value):
    shifted_x_values = x_values + (shift_value*-1)
    return shifted_x_values


def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        try:
            data = np.loadtxt(filepath)
            x_values = data[:, 0]
            y_values = data[:, 1]
            shift_value = float(shift_entry.get())
            shifted_x_values = shift_signal(x_values, shift_value)
            for i, value in enumerate(shifted_x_values):
                print(f" {i}, {value}")
                # Plot the shifted signal
            fig, ax = plt.subplots(figsize=(6, 4))
            plt.plot(shifted_x_values, y_values)
            plt.xlabel("Sample")
            plt.ylabel("Shifted Value")
            plt.title("Shifted Signal")
            plt.show()
            canvas = FigureCanvasTkAgg(fig, master=window)
            canvas.draw()
            canvas.get_tk_widget().pack()
        except Exception as e:
            messagebox.showerror("Error", str(e))


# Create the GUI window
window = tk.Tk()
window.title("Signal Shifting")

# Create a label and an entry field for the shift value
shift_label = tk.Label(window, text="Shift Value:")
shift_label.pack()
shift_entry = tk.Entry(window)
shift_entry.pack()

# Create a button to open the file and perform signal shifting
open_button = tk.Button(window, text="Open File", command=open_file,font=("Arial", 13, "bold"), width=15,
            background='purple', foreground='white')
open_button.pack()

# Start the GUI event loop
window.mainloop()
