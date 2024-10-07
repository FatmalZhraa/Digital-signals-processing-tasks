import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def normalize_signal(signal, lower_bound, upper_bound):
    min_val = np.min(signal)
    max_val = np.max(signal)

    normalized_signal = (signal - min_val) / (max_val - min_val)
    if lower_bound != 0 or upper_bound != 1:
        normalized_signal = (upper_bound - lower_bound) * normalized_signal + lower_bound

    return normalized_signal


def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        try:
            signal = np.loadtxt(filepath)
            lower_bound = float(lower_entry.get())
            upper_bound = float(upper_entry.get())
            normalized_signal = normalize_signal(signal, lower_bound, upper_bound)
            for i,value in normalized_signal:
                print(value)
            # Plot the normalized signal
            fig, ax = plt.subplots(figsize=(6, 4))
            plt.plot(normalized_signal)
            plt.xlabel("Sample")
            plt.ylabel("Normalized Value")
            plt.title("Normalized Signal")
            plt.show()
            canvas = FigureCanvasTkAgg(fig, master=window)
            canvas.draw()
            canvas.get_tk_widget().pack()
        except Exception as e:
            messagebox.showerror("Error", str(e))


# Create the GUI window
window = tk.Tk()
window.title("Signal Normalization")

# Create labels and entry fields for lower and upper bounds
lower_label = tk.Label(window, text="Lower Bound:")
lower_label.pack()
lower_entry = tk.Entry(window)
lower_entry.pack()

upper_label = tk.Label(window, text="Upper Bound:")
upper_label.pack()
upper_entry = tk.Entry(window)
upper_entry.pack()

# Create a button to open the file and perform signal normalization
open_button = tk.Button(window, text="Open File", command=open_file,font=("Arial", 13, "bold"), width=15, height=2,
            background='purple', foreground='white')
open_button.pack()

# Start the GUI event loop
window.mainloop()