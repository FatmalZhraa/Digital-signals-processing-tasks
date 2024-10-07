import tkinter as tk
from tkinter import filedialog
import numpy as np

from Compare_Signals import Compare_Signals
from conv_test import ConvTest
from forier import DFT, IDFT


def dft(signal):
    N = len(signal)
    frequency_spectrum = np.zeros(N, dtype=complex)

    for k in range(N):
        for n in range(N):
            frequency_spectrum[k] += signal[n] * np.exp(-2j * np.pi * k * n / N)

    return frequency_spectrum


def idft(frequency_spectrum):
    N = len(frequency_spectrum)
    inverse_signal = np.zeros(N, dtype=complex)

    for n in range(N):
        for k in range(N):
            inverse_signal[n] += frequency_spectrum[k] * np.exp(2j * np.pi * k * n / N)
    inverse_signal = inverse_signal / N
    inverse_signal = np.real(inverse_signal)

    # Round the inverse signal values to the nearest integer
    inverse_signal = np.round(inverse_signal).astype(int)

    return inverse_signal

def fast_convolution(signal1, signal2):

    # Pad the signals with zeros to ensure they have the same length
    padded_length = len(signal1) + len(signal2) - 1
    signal1_padded = np.pad(signal1, (0, padded_length - len(signal1)))
    signal2_padded = np.pad(signal2, (0, padded_length - len(signal2)))

    # Perform the DFT
    dft_signal1 = dft(signal1_padded)
    dft_signal2 = dft(signal2_padded)

    # Multiply the frequency domain representations pointwise
    multiplied_signal = [a * b for a, b in zip(dft_signal1, dft_signal2)]

    # Perform the IDFT
    convolved_signal = idft(multiplied_signal)

    # Return the real part of the convolved signal
    return np.real(convolved_signal)

def upload_signal_file():
    file_path = filedialog.askopenfilename()
    return file_path

def perform_convolution():
    # Get the file paths of the two signal files
    signal1_file = upload_signal_file()
    signal2_file = upload_signal_file()

    # Read the signal files
    signal1_samples = np.loadtxt(signal1_file, usecols=1)
    signal2_samples = np.loadtxt(signal2_file, usecols=1)
    # Convert the signals to NumPy arrays
    signal1 = np.array(signal1_samples).flatten()
    signal2 = np.array(signal2_samples).flatten()
    result_indices = []
    result_samples = fast_convolution(signal1, signal2)

    print("Result Samples:", result_samples)

    ConvTest(result_indices, result_samples)
    # Display the output signal
    # output_label.config(text="Output Signal: " + str(result_samples))

def calculate_correlation(samples1, samples2):
    N = len(samples1)
    # Compute DFT of both signals
    amplitude_spectrum1, phase_spectrum1, f_samples1 = DFT(samples1)
    amplitude_spectrum2, phase_spectrum2, f_samples2 = DFT(samples2)

    # Conjugate the second sample (time-domain signal)
    samples1_conj = np.conj(f_samples1)

    # Compute cross-correlation using DFT and inverse DFT
    x = samples1_conj * f_samples2
    y = IDFT(x)
    cross_corr = y/N
    return cross_corr

def compute_correlation():
    # Get file paths
    file1_path = filedialog.askopenfilename(title="Select First File")
    file2_path = filedialog.askopenfilename(title="Select Second File")

    # Read data from files
    data1 = np.loadtxt(file1_path)
    data2 = np.loadtxt(file2_path)

    # Extract samples from the loaded data
    samples1 = data1[:, 1]
    samples2 = data2[:, 1]

    print("samples1", samples1, "\n")
    print("samples2", samples2, "\n")

    # Calculate cross-correlation using the function
    correlation_result = calculate_correlation(samples1, samples2)
    print("cross-correlation", correlation_result, "\n")

    # Call the comparison function
    Compare_Signals(r'D:\signals\task8\Corr_Output.txt', np.arange(len(correlation_result)), correlation_result)

root = tk.Tk()
root.title("Signal Convolution")

#

# Create the convolution button
convolution_button = tk.Button(root, text="Perform Convolution", command=perform_convolution)
convolution_button.pack(pady=20)

compute_button = tk.Button(root, text="Compute Fast-Correlation", command=compute_correlation)
compute_button.pack(pady=20)
# Create the output label
# output_label = tk.Label(root, text="Output Signal: ")
# output_label.pack()

# Run the GUI event loop
root.mainloop()