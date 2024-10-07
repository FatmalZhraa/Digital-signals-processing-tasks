import os
import numpy as np
from scipy import signal, fft
import matplotlib.pyplot as plt
from tkinter import filedialog

class ECGAnalyzer:
    def __init__(self):
        pass

    def open_folder(self, title):
        folder_path = filedialog.askdirectory(title=f"Select {title} Folder")
        return self.process_folder(folder_path)

    def process_folder(self, folder_path):
        processed_signals = []
        files = os.listdir(folder_path)
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            signal_data = self.process_file(file_path)
            processed_signal = self.process_signal(signal_data)
            processed_signals.append(processed_signal)
        return processed_signals

    def process_file(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            return np.array(content.split(), dtype=float)

    def process_signal(self, signal_data, Fs, miniF, maxF, newFs):
        filtered_signal = self.filter_signal(signal_data, Fs, miniF, maxF)
        if newFs < Fs:
            resampled_signal = self.resample_signal(filtered_signal, Fs, newFs)
        else:
            resampled_signal = filtered_signal
        dc_removed_signal = self.remove_dc_component(resampled_signal)
        normalized_signal = self.normalize_signal(dc_removed_signal, -1, 1)
        return normalized_signal

    def filter_signal(self, signal_data, Fs, miniF, maxF):
        nyquist_freq = 0.5 * Fs
        normalized_miniF = miniF / nyquist_freq
        normalized_maxF = maxF / nyquist_freq
        b, a = signal.firwin(numtaps=101, cutoff=[normalized_miniF, normalized_maxF], fs=Fs, pass_zero=False)
        filtered_signal = signal.lfilter(b, a, signal_data)
        return filtered_signal

    def resample_signal(self, signal_data, Fs, newFs):
        if newFs > Fs:
            print("newFs is not valid")
            return signal_data
        resampled_signal = signal.resample(signal_data, int(len(signal_data) * newFs / Fs))
        return resampled_signal

    def remove_dc_component(self, signal):
        mean = np.mean(signal)
        result = signal - mean
        return result

    def normalize_signal(self, signal, lower_bound, upper_bound):
        min_val = np.min(signal)
        max_val = np.max(signal)
        normalized_signal = (signal - min_val) / (max_val - min_val)
        if lower_bound != 0 or upper_bound != 1:
            normalized_signal = (upper_bound - lower_bound) * normalized_signal + lower_bound
        return normalized_signal

    def calculate_autocorrelation(self, signal):
        autocorr = np.correlate(signal, signal, mode='full')
        return autocorr[len(autocorr) // 2:]

    def compute_dct(self, signal):
        N = len(signal)
        dct_result = np.zeros_like(signal)
        for k in range(N):
            for n in range(N):
                dct_result[k] += np.sqrt(2 / N) * signal[n] * np.cos((np.pi / (4 * N)) * (2 * n - 1) * (2 * k - 1))
        return dct_result

    def choose_folders(self):
        folder_path_A = self.open_folder("Subject A")
        folder_path_B = self.open_folder("Subject B")
        folder_path_test = self.open_folder("Test")

        if folder_path_A and folder_path_B and folder_path_test:
            signals_A = self.process_folder(folder_path_A)
            signals_B = self.process_folder(folder_path_B)
            signals_test = self.process_folder(folder_path_test)

            for i, test_signal in enumerate(signals_test):
                print("Test Signal", i+1)
                # Compute the autocorrelation for the test signal
                autocorr_test = self.calculate_autocorrelation(test_signal)
                # Preserve only the needed coefficients for the computed autocorrelation
                preserved_autocorr_test = autocorr_test[:100]
                # Compute the DCT for the preserved autocorrelation
                dct_test = self.compute_dct(preserved_autocorr_test)

                # Initialize variables to store the best match and its score
                best_match_subject = None
                best_match_score = -np.inf

                for signal_A in signals_A:
                    autocorr_A = self.calculate_autocorrelation(signal_A)
                    preserved_autocorr_A = autocorr_A[:100]
                    dct_A = self.compute_dct(preserved_autocorr_A)
                    non_zero_A = dct_A[np.nonzero(dct_A)]
                    non_zero_test = dct_testHere