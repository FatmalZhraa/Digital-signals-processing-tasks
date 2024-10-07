import tkinter as tk
from tkinter import filedialog

import numpy as np


def quantize_signal():
    # Read the input file
    file_path = filedialog.askopenfilename()
    with open(file_path, 'r') as file:
        lines = file.readlines()[3:]
        data = [line.split() for line in lines]
        samples = [int(row[0]) for row in data]
        signal_values = [float(row[1]) for row in data]

    # Calculate the interval index, quantized signal, quantization error, and encoded signal
    interval_index = []
    quantized_signal = []
    quantization_error = []
    encoded_signal = []
    min_amp =min(signal_values)
    max_amp =max(signal_values)


    if input_type.get() == "Number of Bits":
        # Calculate the step size
        num_bits = int(num_entry.get())
        num_levels = 2 ** num_bits
        step_size = (max_amp - min_amp) / num_levels

        # Quantize the signal
        for i, value in enumerate(signal_values):
            # Calculate interval index
            if value == max_amp:
                index = num_levels - 1
            else:
                index = int((value - min_amp) / step_size)

            interval_index.append(index)

            # Calculate quantized signal
            quantized_value = round(min(signal_values) + (index * step_size) + (step_size / 2), 2)
            quantized_signal.append(quantized_value)

            # Calculate quantization error
            error = value - quantized_value
            quantization_error.append(error)

            # Calculate encoded signal
            if 0 <= index < len(samples):  # Check if index is within the valid range
                binary_string = bin(samples[index])[2:]  # Convert decimal to binary string
                binary_string = binary_string.zfill(num_bits)  # Add leading zeros based on the number of bits
                encoded_signal.append(binary_string)
            else:
                encoded_signal.append("0")  # Handle the case when index is out of range

    elif input_type.get() == "Number of Levels":
        # Calculate the number of levels
        num_levels = int(num_entry.get())
        num_bits = int(np.log2(num_levels))
        # Calculate the step size
        step_size = (max_amp - min_amp) / num_levels

        # Quantize the signal
        for i, value in enumerate(signal_values):
            # Calculate interval index
            if value == max_amp:
                index = num_levels - 1
            else:
                index = int((value - min_amp) / step_size)

            interval_index.append(index)

            # Calculate quantized signal
            quantized_value = round(min_amp + (index * step_size) + (step_size / 2), 3)
            quantized_signal.append(quantized_value)

            # Calculate quantization error
            error = round((quantized_value - value), 3)
            quantization_error.append(error)

            # Calculate encoded signal
            if 0 <= index < len(samples):  # Check if index is within the valid range
                binary_string = bin(samples[index])[2:]  # Convert decimal to binary string
                binary_string = binary_string.zfill(num_bits)  # Add leading zeros based on the number of levels
                encoded_signal.append(binary_string)
            else:
                encoded_signal.append("0")  # Handle the case when index is out of range

    # Display the output lists
    output_text.delete(1.0, tk.END)
    if input_type.get() == "Number of Bits":
        output_text.insert(tk.END, "Encoded Signal\tQuantized Signal\n")
        for i in range(len(signal_values)):
            output_text.insert(tk.END, f"{encoded_signal[i]}\t\t{quantized_signal[i]}\n")
    else:
        output_text.insert(tk.END, "Interval Index\tEncoded Signal\tQuantized Signal\tQuantization Error\n")
        for i in range(len(signal_values)):
            output_text.insert(tk.END,
                               f"{interval_index[i] + 1}\t\t{encoded_signal[i]}\t\t{quantized_signal[i]}\t\t{quantization_error[i]}\n")


# Create the GUI
root = tk.Tk()
root.title("Signal Quantization")
root.geometry("700x500")

# Input Type
input_type = tk.StringVar()
input_type.set("Number of Bits")
input_type_label = tk.Label(root, text="Input Type:")
input_type_label.pack()
input_type_menu = tk.OptionMenu(root, input_type, "Number of Bits", "Number of Levels")
input_type_menu.pack()

# Number Entry
num_label = tk.Label(root, text="Number:")
num_label.pack()
num_entry = tk.Entry(root)
num_entry.pack()

# Quantize Button
quantize_button = tk.Button(root, text="Quantize Signal", command=quantize_signal)
quantize_button.pack()

# Output Text
output_text = tk.Text(root)
output_text.pack()

root.mainloop()