import tkinter as tk
from tkinter import filedialog
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from comparesignal2 import SignalSamplesAreEqual2


def remove_dc_component(signal):
    mean = np.mean(signal)
    result = signal - mean

    result = np.round(result, 3)
    for i, value in enumerate(result):
        result_text.insert(tk.END, f"{i} {value}\n")
    SignalSamplesAreEqual2(r'D:\signals\dct\DC_component_output.txt', result)
    return result

def compute_dct(signal, m):
    N = len(signal)
    dct_result = np.zeros_like(signal)
    for k in range(N):
        for n in range(N):
            dct_result[k] += np.sqrt(2 / N) * signal[n] * np.cos((np.pi / (4 * N)) * (2 * n - 1) * (2 * k - 1))
    amplitude = np.abs(dct_result)
    phase = np.angle(dct_result)
    for i, value in zip(phase, amplitude):
        result_text.insert(tk.END, f" {i} {value}\n")
    fig2, ax2 = plt.subplots(figsize=(4, 4))
    plt.plot(dct_result)
    plt.xlabel("amp")
    plt.ylabel("Phase")
    plt.title("DCT")
    canvas2 = FigureCanvasTkAgg(fig2, master=window)
    canvas2.draw()
    canvas2.get_tk_widget().pack()
    selected_coeffs = dct_result[:m]
    np.savetxt("D:\signals\dct\selected_coefficients.txt", selected_coeffs)

    SignalSamplesAreEqual2('D:\signals\dct\DCT_output.txt', dct_result)
    return phase, amplitude


def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        signal = np.loadtxt(file_path, usecols=1, skiprows=3)
        try:
            m = int(m_entry.get())
            result_text.delete("1.0", tk.END)  # Clear previous results
            dct_result = compute_dct(signal, m)
        except ValueError:
            result_text.insert(tk.END, "Please enter a valid value for m.\n")


def upload_file_dct_component():
    file_path = filedialog.askopenfilename()
    if file_path:
        signal = np.loadtxt(file_path, usecols=1, skiprows=3)
        result_text.delete("1.0", tk.END)  # Clear previous results
        signal = remove_dc_component(signal)


# Create the GUI window
window = tk.Tk()

# Create an "Upload File" button for DCT computation
dct_button = tk.Button(window, text="Upload File for DCT", command=upload_file)
dct_button.pack()

# Create an input field for m
m_label = tk.Label(window, text="Enter the value of m:")
m_label.pack()
m_entry = tk.Entry(window)
m_entry.pack()

# Create an "Upload File" button for DC component removal
dc_button = tk.Button(window, text="Upload File for DC Component Removal", command=upload_file_dct_component)
dc_button.pack()

# Create a text widget to display the results
result_text = tk.Text(window, height=15, width=40)
result_text.pack()

# Run the GUI event loop
window.mainloop()