import math
import os
from tkinter import filedialog

import numpy as np
from matplotlib import pyplot as plt
from forier import DFT, IDFT


def open_folder(self, title):
    folder_path = filedialog.askdirectory(title=f"Select {title} Folder")
    return self.process_folder(folder_path)

def process_signals_in_folder(folder_path1, folder_path2):
    # List all files in the first folder
    signal_files_folder1 = os.listdir(folder_path1)
    signal_files_folder2 = os.listdir(folder_path2)

    # Initialize lists to store the processed signals for each folder
    processed_signals_folder1 = []
    processed_signals_folder2 = []

    # Process files in the first folder
    for file_name in signal_files_folder1:
        file_path = os.path.join(folder_path1, file_name)
        signal_data = read_signal_data(file_path)

        # Process the signal for subject A
        processed_signal = process_signal(signal_data)
        processed_signals_folder1.append(processed_signal)

    # Process files in the second folder
    for file_name in signal_files_folder2:
        file_path = os.path.join(folder_path2, file_name)
        signal_data = read_signal_data(file_path)

        # Process the signal for subject B
        processed_signal = process_signal(signal_data)
        processed_signals_folder2.append(processed_signal)

    return processed_signals_folder1, processed_signals_folder2
def read_signal_data(file_path):
    with open(file_path, 'r') as file:
        # Read lines and convert them to floats
        data = [float(line.strip()) for line in file.readlines()]
    return data

def choose_folders():
    folder_path_A = filedialog.askdirectory(title="Select Subject A Folder")
    folder_path_B = filedialog.askdirectory(title="Select Subject B Folder")
    folder_path_test = filedialog.askdirectory(title="Select Test Folder")

    if folder_path_A and folder_path_B and folder_path_test:
        signals_A = process_signals_in_folder(folder_path_A)
        signals_B = process_signals_in_folder(folder_path_B)
        signals_test = process_signals_in_folder(folder_path_test)

        # Perform template matching for each test signal
        for i, test_signal in enumerate(signals_test):
            # Compute the DCT for the test signal
            dct_test = compute_dct(test_signal)

            # Initialize variables to store the best match and its score
            best_match_subject = None
            best_match_score = -np.inf

            # Perform template matching with subject A
            for signal_A in signals_A:
                # Compute the DCT for subject A
                dct_A = compute_dct(signal_A)

                # Compute the non-zero values for subject A and test signal
                non_zero_A = dct_A[np.nonzero(dct_A)]
                non_zero_test = dct_test[np.nonzero(dct_test)]

                # Compute the score for template matching
                score = np.sum(np.abs(non_zero_A - non_zero_test))

                # Update the best match if the score is higher
                if score > best_match_score:
                    best_match_subject = "A"
                    best_match_score = score

            # Perform template matching with subject B
            for signal_B in signals_B:
                # Compute the DCT for subject B
                dct_B = compute_dct(signal_B)

                # Compute the non-zero values for subject B and test signal
                non_zero_B = dct_B[np.nonzero(dct_B)]
                non_zero_test = dct_test[np.nonzero(dct_test)]

                # Compute the score for template matching
                score = np.sum(np.abs(non_zero_B - non_zero_test))

                # Update the best match if the score is higher
                if score > best_match_score:
                    best_match_subject = "B"
                    best_match_score = score

            # Print the label for the test signal
            print("Test Signal", i+1, "belongs to Subject", best_match_subject)

def count_files_in_folder(folder_path):
    file_list = os.listdir(folder_path)
    return len(file_list)

def process_file(self, file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        return np.array(content.split(), dtype=float)


def read_file():
    file_path = filedialog.askopenfilename()
    x_values = []
    y_values = []
    if file_path:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines[3:]:
                values = line.strip().split()
                # x_values.append(float(values[0]))
                y_values.append(float(values[0]))
    x_values = range(len(y_values))
    return x_values, y_values
def plot_signal(x, y, title):
    fig, ax = plt.subplots()

    ax.plot(x, y)
    ax.set_title(title)
    ax.set_xlabel('Sample')
    ax.set_ylabel('Amplitude')


def remove_dc_component(signal):
    mean = np.mean(signal)
    result = signal - mean
    result = np.round(result, 3)
    return result

def normalize_signal(signal, lower_bound, upper_bound):
    min_val = np.min(signal)
    max_val = np.max(signal)

    normalized_signal = (signal - min_val) / (max_val - min_val)
    if lower_bound != 0 or upper_bound != 1:
        normalized_signal = (upper_bound - lower_bound) * normalized_signal + lower_bound

    return normalized_signal
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

def compute_dct(signal):
    N = len(signal)
    dct_result = np.zeros_like(signal)
    for k in range(N):
        for n in range(N):
            dct_result[k] += np.sqrt(2 / N) * signal[n] * np.cos((np.pi / (4 * N)) * (2 * n - 1) * (2 * k - 1))

    return dct_result

