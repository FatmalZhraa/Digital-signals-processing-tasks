import math
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from scipy.signal import convolve
import matplotlib.pyplot as plt

from DerivativeSignal import DerivativeSignal
from comparesignals import SignalSamplesAreEqual
from conv_test import ConvTest
from fold_test import Shift_Fold_Signal
from comparesignal2 import SignalSamplesAreEqual2

def moving_average(signal, num_points):

    x_values = signal[:, 0]
    y_values = signal[:, 1]
    y = []
    indices=[]
    length=len(x_values) - num_points + 1
    for i in range(length):
        result = sum(y_values[i:i+num_points])
        y.append(result/num_points )
        indices.append(i)
    for i, value in enumerate(y):
        print(f"{i} {value}\n")
    file=r'D:\signals\task 6\MovAvgTest1.txt'
    SignalSamplesAreEqual(file, indices, y)

    return y


def shift_signal(x_values, shift_value):
    shifted_x_values = [int(x + shift_value) for x in x_values]
    return shifted_x_values

def fold_signal(input_signal):
    # Step 1: Separate indices and values
    indices = []
    values = []
    for pair in input_signal:
        indices.append(pair[0])
        values.append(pair[1])

    # Step 2: Reverse values list
    for i in range(len(values)//2):
        # Swap values[i] and values[-i-1]
        temp = values[i]
        values[i] = values[-i-1]
        values[-i-1] = temp

    # Step 3: Pair each index with the corresponding value from the reversed list
    output_signal = []
    for i in range(len(indices)):
        output_signal.append(f"{indices[i]} {values[i]}\n")
        print (f"{indices[i]},{values[i]}\n")
    file_name = r'D:\signals\task 6\Output_fold.txt'
    SignalSamplesAreEqual(file_name, indices,values)
    save_signal(output_signal,r'D:\signals\task 6\OUTPUT FOLD.txt')
    return output_signal

def save_signal(signal, file_path):
    with open(file_path, 'w') as file:
        for value in signal:
            file.write(value + '\n')
def sharping():
    DerivativeSignal()

# Function to remove DC component in frequency domain


def remove_dc_component(signal):
    N = len(signal)
    X = np.zeros_like(signal, dtype=complex)
    # dft
    for k in range(N):
        for n in range(N):
            exponential_term = np.exp(1j * 2 * np.pi * k * n / N)
            X[k] += exponential_term * signal[n]
    # idft
    signal_without_dc = np.zeros_like(signal, dtype=complex)
    for k in range(N):
        for n in range(N):
            exponential_term = np.exp(-1j * 2 * np.pi * k * n / N)
            signal_without_dc[k] += exponential_term * X[n]
    signal_without_dc *= 1 / N
    # Remove the mean of the DC-removed signal
    mean = np.sum(signal_without_dc) / N
    for i in range(N):
        signal_without_dc[i] -= mean
    signal_without_dc = np.round(signal_without_dc.real, 3)
    SignalSamplesAreEqual2(r'D:\signals\dct\DC_component_output.txt', signal_without_dc)
    return signal_without_dc

def convolve_signals(signal1, signal2):

  signal1_indices, signal1_samples = signal1[:, 0], signal1[:, 1]
  signal2_indices, signal2_samples = signal2[:, 0], signal2[:, 1]

  result_indices = []
  result_samples = []
  for i in range(len(signal1_indices)):
    for j in range(len(signal2_indices)):
      index = signal1_indices[i] + signal2_indices[j]
      sample = signal1_samples[i] * signal2_samples[j]
      # Check for existing index and add/update sample value
      if index in result_indices:
        index_idx = result_indices.index(index)
        result_samples[index_idx] += sample
      else:
        result_indices.append(index)
        result_samples.append(sample)
  print("Indices:", result_indices)
  print("Samples:", result_samples)
  ConvTest(result_indices,result_samples)
  return result_indices, result_samples

def save_signal(signal, file_path):
    with open(file_path, 'w') as file:
        for value in signal:
            file.write(str(value) + '\n')

def upload_file(operation):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(tk.END, file_path)
    if file_path:
        try:
            signal = np.loadtxt(file_path)  # Assuming signal is stored as a text file
            x_values = signal[:, 0]
            y_values = signal[:, 1]
            if operation == "Smoothing":
                num_points = int(entry_window_size.get())
                signal_path = entry_file_path.get()

                processed_signal = moving_average(signal, num_points)
                plt.plot(signal, label='Original Signal')
                plt.plot(processed_signal, label='Smoothed Signal')
                plt.legend()
                plt.show()
            elif operation == "sharping":
                DerivativeSignal()
            elif operation == "Shift Signal":
                x_values = signal[:, 0]
                y_values = signal[:, 1]
                num_steps = int(input("Enter the number of steps to shift: "))
                shifted_x_values = shift_signal(x_values, num_steps)
                file_name = r'D:\signals\task 6\Output_ShiftFoldedby-500.txt'
                Shift_Fold_Signal(file_name, shifted_x_values,y_values)

                plt.plot(signal, label='Original Signal')
                plt.plot(shifted_x_values, label='Shifted Signal')
                plt.legend()
                plt.show()
            elif operation == "Fold Signal":
                folded_signal = fold_signal(signal)
                plt.plot(signal, label='Original Signal')
                plt.plot(folded_signal, label='Folded Signal')
                plt.legend()
                plt.show()

            elif operation == "Remove DC":
                signal = np.loadtxt(file_path, usecols=1)
                signal = remove_dc_component(signal)
                dc_removed_signal = remove_dc_component(signal)
                plt.plot(signal, label='Original Signal')
                plt.plot(dc_removed_signal, label='DC Removed Signal')
                plt.legend()
                plt.show()
            elif operation == "Convolve Signals":
                file_path2 = filedialog.askopenfilename()
                if file_path2:
                    signal2 = np.loadtxt(file_path2)  # Assuming second signal is stored as a text file
                    convolved = convolve_signals(signal, signal2)
            else:
                print("Invalid operation.")

        except Exception as e:
         messagebox.showerror("Error", str(e))

# Create the main window
window = tk.Tk()
window.title("Signal Processing Tool")

# Create and place widgets
label_title = tk.Label(window, text="Signal Processing Tool", font=("Arial", 16, "bold"))
label_title.pack(pady=10)

label_file_path = tk.Label(window, text="Signal File:")
label_file_path.pack()

entry_file_path = tk.Entry(window, width=50)
entry_file_path.pack()


label_window_size = tk.Label(window, text="Window Size:")
label_window_size.pack()

entry_window_size = tk.Entry(window, width=10)
entry_window_size.pack()

button_smooth = tk.Button(window, text="Smoothing", command=lambda: upload_file("Smoothing"))
button_smooth.pack(pady=10)

button_derivative = tk.Button(window, text="Sharpening", command=sharping)
button_derivative.pack(pady=10)

label_delay_steps = tk.Label(window, text="Delay Steps:")
label_delay_steps.pack()

entry_delay_steps = tk.Entry(window, width=10)
entry_delay_steps.pack()

button_shift = tk.Button(window, text="Shift Signal", command=lambda: upload_file("Shift Signal"))
button_shift.pack(pady=10)

button_fold = tk.Button(window, text="Fold Signal", command=lambda: upload_file("Fold Signal"))
button_fold.pack(pady=10)


button_dc = tk.Button(window, text="Remove DC", command=lambda: upload_file("Remove DC"))
button_dc.pack(pady=10)

label_file_path2 = tk.Label(window, text="Signal File 2 (for convolution):")
label_file_path2.pack()

entry_file_path2 = tk.Entry(window, width=50)
entry_file_path2.pack()


button_convolve = tk.Button(window, text="Convolve Signals", command=lambda: upload_file("Convolve Signals"))
button_convolve.pack(pady=10)

label_status = tk.Label(window, text="", font=("Arial", 12))
label_status.pack(pady=10)

# Start the main loop
window.mainloop()