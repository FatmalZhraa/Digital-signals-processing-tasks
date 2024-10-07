import os
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog, ttk, messagebox
import math
from scipy.signal import resample

from CompareSignal import Compare_Signals


class DSPApp:
    def __init__(self, master):
        self.master = master
        master.title("DSP Application")
        # GUI Elements
        self.fs_var = DoubleVar(master, value=8000)
        self.stop_band_attenuation_var = DoubleVar(master, value=50)
        self.fc_var = DoubleVar(master, value=1500)
        self.fc2_var = DoubleVar(master, value=1500)
        self.transition_band_var = DoubleVar(master, value=500)
        self.input_signal_var = StringVar(master, value='')
        self.resample = BooleanVar(master, value=False)
        self.M = IntVar(master, value=0)
        self.L = IntVar(master, value=0)
        # Task 2 vars ------------------------------------------------------------
        self.Fs = IntVar(master, value=1000)
        self.miniF = IntVar(master, value=500)
        self.maxF = IntVar(master, value=900)
        self.newFs = IntVar(master, value=1200)
        # ------------------------------------------------------------------------

        # Labels
        # Label(master, text="filter").grid(row=0, column=0)
        Label(master, text="type:").grid(row=1, column=0)
        Label(master, text="Sampling frequency:").grid(row=2, column=0)
        Label(master, text="Stop Attenuation:").grid(row=3, column=0)
        Label(master, text="Cutoff frequency:").grid(row=4, column=0)
        Label(master, text="Cutoff frequency 2:").grid(row=5, column=0)
        Label(master, text="Transition band:").grid(row=6, column=0)
        Label(master, text="File:").grid(row=7, column=0)
        # Label(master, text="Resampling options:").grid(row=9, column=0)
        Label(master, text="Fs:").grid(row=19, column=0)
        Label(master, text="miniF:").grid(row=20, column=0)
        Label(master, text="maxF:").grid(row=21, column=0)
        Label(master, text="newFs:").grid(row=22, column=0)
        # Label(master, text="Resample?:").grid(row=10, column=0)
        Label(master, text="Decimation factor (M):").grid(row=11, column=0)
        Label(master, text="Interpolation factor (L):").grid(row=12, column=0)
        Label(master, text="Filters options", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=W)
        Label(master, text="Filter Type:").grid(row=1, column=0, sticky=W)
        Label(master, text="Sampling Frequency (FS):").grid(row=2, column=0, sticky=W)
        Label(master, text="Stop Band Attenuation:").grid(row=3, column=0, sticky=W)
        Label(master, text="Cutoff Frequency (FC):").grid(row=4, column=0, sticky=W)
        Label(master, text="Cutoff Frequency 2 (FC2 for Band):").grid(row=5, column=0, sticky=W)
        Label(master, text="Transition Band:").grid(row=6, column=0, sticky=W)
        Label(master, text="Input Signal File:").grid(row=7, column=0, sticky=W)
        Label(master, text="Resampling options:", font=("Arial", 12, "bold")).grid(row=9, column=0, sticky=W)
        Label(master, text="Fs:").grid(row=19, column=0, sticky=W)
        Label(master, text="miniF:").grid(row=20, column=0, sticky=W)
        Label(master, text="maxF:").grid(row=21, column=0, sticky=W)
        Label(master, text="newFs:").grid(row=22, column=0, sticky=W)
        # Label(master, text="Resample?:").grid(row=10, column=0, sticky=W)
        Label(master, text="Decimation factor (M):").grid(row=11, column=0, sticky=W)
        Label(master, text="Interpolation factor (L):").grid(row=12, column=0, sticky=W)

        # Filter Type Combo-box
        filter_types = ['Low pass', 'High pass', 'Band pass', 'Band stop']
        self.filter_type_var = StringVar(master, value=filter_types[0])
        ttk.Combobox(master, textvariable=self.filter_type_var, values=filter_types).grid(row=1, column=1, columnspan=2)
        # Entry fields
        Entry(master, textvariable=self.fs_var).grid(row=2, column=1, columnspan=2)
        Entry(master, textvariable=self.stop_band_attenuation_var).grid(row=3, column=1, columnspan=2)
        Entry(master, textvariable=self.fc_var).grid(row=4, column=1, columnspan=2)
        Entry(master, textvariable=self.fc2_var).grid(row=5, column=1, columnspan=2)
        Entry(master, textvariable=self.transition_band_var).grid(row=6, column=1, columnspan=2)
        Button(master, command=self.load_input, text="Get File", width=10).grid(row=7, column=1)
        Button(master, command=self.clear_input, text="Remove", width=10).grid(row=7, column=2)
        Button(master, command=self.load_input, text="Import", width=10).grid(row=7, column=1)
        Button(master, command=self.clear_input, text="Clear", width=10).grid(row=7, column=2)
        Label(master).grid(row=8, columnspan=3, pady=3)
        # Checkbutton(master, variable=self.resample).grid(row=10, column=2)
        Entry(master, textvariable=self.M).grid(row=11, column=1, columnspan=2)
        Entry(master, textvariable=self.L).grid(row=12, column=1, columnspan=2)

        # Buttons
        Button(master, text="Filter values", command=self.load_filter_specs, width=10).grid(row=13, column=0,
                                                                                            columnspan=3)
        Button(master, text="Filter", command=self.run_dsp, width=10).grid(row=14, column=0, columnspan=3)
        Button(master, text="resample", command=self.run_resample, width=10).grid(row=15, column=0, columnspan=3)
        # Label(master, text="-------------------------------------------------------------------------").grid(row=16, column=0, columnspan=3)
        # Label(master, text="ECG options:").grid(row=17, column=0, columnspan=3)
        Button(master, text="ECG", command=self.run_ecg, width=10).grid(row=16, column=0, columnspan=3)
        Button(master, text="Load Filter Specs", command=self.load_filter_specs, width=50, height=3).grid(row=13,
                                                                                                          column=0,
                                                                                                          columnspan=3)
        Button(master, text="Filter", command=self.run_dsp, width=50, height=3).grid(row=14, column=0, columnspan=3)
        Button(master, text="Resample", command=self.run_resample, width=50, height=3).grid(row=15, column=0,
                                                                                            columnspan=3)
        Label(master, text="-------------------------------------------------------------------------").grid(row=16,
                                                                                                             column=0,
                                                                                                             columnspan=3)
        Label(master, text="ECG options:", font=("Arial", 12, "bold")).grid(row=17, column=0, columnspan=3, sticky=W)
        Button(master, text="Run ECG", command=self.run_ecg, width=50, height=3).grid(row=18, column=0, columnspan=3)

        Entry(master, textvariable=self.Fs).grid(row=19, column=1, columnspan=2)
        Entry(master, textvariable=self.miniF).grid(row=20, column=1, columnspan=2)
        Entry(master, textvariable=self.maxF).grid(row=21, column=1, columnspan=2)
        Entry(master, textvariable=self.newFs).grid(row=22, column=1, columnspan=2)

    def load_input(self):
        filename = filedialog.askopenfilename()
        self.input_signal_var.set(filename)

    def clear_input(self):
        self.input_signal_var = StringVar(self.master, value="")

    def load_filter_specs(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            filter_specs = read_filter_specifications_from_file(file_path)
            self.filter_type_var.set(filter_specs['FilterType'])
            self.fs_var.set(int(filter_specs['FS']))
            self.stop_band_attenuation_var.set(int(filter_specs['StopBandAttenuation']))
            self.transition_band_var.set(int(filter_specs['TransitionBand']))
            # Update for Band pass and Band stop cases
            if filter_specs['FilterType'] in ['Band pass', 'Band stop']:
                self.fc2_var.set(int(filter_specs['F2']))
                self.fc_var.set(int(filter_specs['F1']))
            else:
                self.fc_var.set(int(filter_specs['FC']))

    def run_dsp(self):
        # Get values from GUI
        filter_type = self.filter_type_var.get()
        fs = self.fs_var.get()
        stop_band_attenuation = self.stop_band_attenuation_var.get()
        fc = self.fc_var.get()
        if filter_type == "Band pass" or filter_type == "Band stop":
            f1 = self.fc_var.get()
            f2 = self.fc2_var.get()
        transition_band = self.transition_band_var.get()
        input_signal_path = self.input_signal_var.get()
        # Design FIR filter
        if filter_type == "Low pass" or filter_type == "High pass":
            indices, filter_res = design_fir_filter(filter_type, fs, stop_band_attenuation, fc, transition_band)
        else:
            indices, filter_res = design_fir_filter(filter_type, fs, stop_band_attenuation, 0, transition_band, f1, f2)
        plot_signal(indices, filter_res, "Filter Coefficients")
        # Read input signal from file
        if input_signal_path:
            input_x = []
            input_y = []
            with open(input_signal_path, 'r') as file:
                for line in file.readlines()[3:]:
                    data = line.split()
                    input_x.append(int(data[0]))
                    input_y.append(float(data[1]))
                file.close()
            # Apply filter
            indices, filter_res = apply_filter(input_x, input_y, indices, filter_res)
            plot_signal(input_x, input_y, "Input Signal")
            plot_signal(indices, filter_res, "Filtered Signal")
        # testing stuff
        file_path = filedialog.askopenfilename()
        Compare_Signals(file_path, indices, filter_res)
        # Save coefficients to a file
        save_coefficients_to_file(list(zip(indices, filter_res)), "filter_coefficients.txt")
        plt.tight_layout()
        plt.show()

    def run_resample(self):
        # filter_type = self.filter_type_var.get()
        fs = self.fs_var.get()
        stop_band_attenuation = self.stop_band_attenuation_var.get()
        fc = self.fc_var.get()
        transition_band = self.transition_band_var.get()
        try:
            input_signal_path = self.input_signal_var.get()
        except Exception as e:
            return messagebox.showerror("no file imported")
        M = self.M.get()
        L = self.L.get()
        # Read input signal from file
        if input_signal_path:
            input_x = []
            input_y = []
            with open(input_signal_path, 'r') as file:
                for line in file.readlines()[3:]:
                    data = line.split()
                    input_x.append(int(data[0]))
                    input_y.append(float(data[1]))
                file.close()
        plot_signal(input_x, input_y, "Original signal")
        resample_res_x, resample_res_y = resample_signal(input_x, input_y, M, L, 'Low pass', fs, stop_band_attenuation,
                                                         fc, transition_band)
        plot_signal(resample_res_x, resample_res_y, "Resampling result")
        # testing stuff
        file_path = filedialog.askopenfilename()
        # Compare_Signals(file_path, indices, filter_res)
        Compare_Signals(file_path, resample_res_x, resample_res_y)
        # Save coefficients to a file
        save_coefficients_to_file(list(zip(resample_res_x, resample_res_y)), "resample.txt")
        plt.tight_layout()
        plt.show()

    def open_folder(self, title):
        folder_path = filedialog.askdirectory(title=f"Select {title} Folder")
        return self.process_folder(folder_path)

    def process_folder(self, folder_path):
        files_contents = []
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                content = self.process_file(file_path)
                files_contents.append(content)
        samples = self.get_samples(files_contents)
        return samples

    def process_file(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            return np.array(content.split(), dtype=float)

    def get_samples(self, files_contents):
        max_samples = max(len(content) for content in files_contents)
        get_samples = np.zeros(max_samples)
        print(files_contents)
        for content in files_contents:
            get_samples[:len(content)] += content
        get_samples /= len(files_contents)
        return get_samples

    def run_ecg(self):
        fs = self.Fs.get()
        minF = self.miniF.get()
        maxF = self.maxF.get()
        newFs = self.newFs.get()
        data_A = self.open_folder("A")
        data_B = self.open_folder("B")
        data_x, data_y = read_file()
        plot_signal(data_x, data_y, "Original Signal")
        filter_x, filter_y = design_fir_filter("Band pass", fs, 50, 0, 500, minF, maxF)
        result_x, result_y = apply_filter(data_x, data_y, filter_x, filter_y)
        if newFs >= 2 * fs:
            M = int(newFs / fs)
            L = int(fs / newFs)
            result_x, result_y = resample_signal(result_x, result_y, M, L, 'Low pass', newFs, 50, 0, 500)
        else:
            messagebox.showwarning("Invalid value for newFs")

        # result_x, result_y = resample_signal(result_x, result_y, fs, newFs)

        result_y = remove_dc_component(result_y)
        result_y = normalize_signal(result_y)
        result_y = cross_correlation(result_y, result_y)
        plot_signal(result_x, result_y, "After Auto-correlation")
        result_y = DCT(result_y)
        plot_signal(result_x, result_y, "After DCT")
        template_matching_result = decide_correlation(result_y, data_A, data_B)
        print("Template Matching Result:\n", template_matching_result)
        print("Data A:", data_A)
        print("Data B:", data_B)
        plt.tight_layout()
        plt.show()


def round_up_to_odd(number):
    rounded_number = math.ceil(number)

    if rounded_number % 2 == 0:
        rounded_number += 1
    return rounded_number


def window_function(stop_band_attenuation, n, N):
    if stop_band_attenuation <= 21:  # Rectangular
        return 1
    elif stop_band_attenuation <= 44:  # Hanning
        return 0.5 + (0.5 * np.cos((2 * np.pi * n) / N))
    elif stop_band_attenuation <= 53:  # Hamming
        return 0.54 + (0.46 * np.cos((2 * np.pi * n) / N))
    elif stop_band_attenuation <= 74:  # Blackman
        return 0.42 + (0.5 * np.cos(2 * np.pi * n / (N - 1))) + 0.08 * np.cos(4 * np.pi * n / (N - 1))

def design_fir_filter(filter_type, fs, stop_band_attenuation, fc, transition_band, f1=None, f2=None):
    # calculate the damn N
    delta_f = transition_band / fs
    if stop_band_attenuation <= 21:  # Rectangular
        N = round_up_to_odd(0.9 / delta_f)
    elif stop_band_attenuation <= 44:  # Hanning
        N = round_up_to_odd(3.1 / delta_f)
    elif stop_band_attenuation <= 53:  # Hamming
        N = round_up_to_odd(3.3 / delta_f)
    elif stop_band_attenuation <= 74:  # Blackman
        N = round_up_to_odd(5.5 / delta_f)
    # the list to hold the filter
    h = []
    # the x values
    indices = range(-math.floor(N / 2), math.floor(N / 2) + 1)
    # get filter
    #   low-pass
    if filter_type == 'Low pass':
        new_fc = fc + 0.5 * transition_band
        new_fc = new_fc / fs
        for n in indices:
            w_n = window_function(stop_band_attenuation, n, N)
            # print("win", w_n)
            if n == 0:
                h_d = 2 * new_fc
            else:
                h_d = 2 * new_fc * (np.sin(n * 2 * np.pi * new_fc) / (n * 2 * np.pi * new_fc))
                # print("hd",h_d)
                # print(new_fc)
            h.append(h_d * w_n)
        # [print(row) for row in list(zip(indices, h))]

    #   high-pass
    elif filter_type == 'High pass':
        new_fc = fc - 0.5 * transition_band
        new_fc /= fs
        for n in indices:
            w_n = window_function(stop_band_attenuation, n, N)
            if n == 0:
                h_d = 1 - 2 * new_fc
            else:
                h_d = -2 * new_fc * (np.sin(n * 2 * np.pi * new_fc) / (n * 2 * np.pi * new_fc))
            h.append(h_d * w_n)
        # [print(row) for row in list(zip(indices, h))]
    #   band-pass
    elif filter_type == 'Band pass':
        new_fc = f1 - 0.5 * transition_band
        new_fc /= fs
        new_fc2 = f2 + 0.5 * transition_band
        new_fc2 /= fs

        for n in indices:
            w_n = window_function(stop_band_attenuation, n, N)
            if n == 0:
                h_d = 2 * (new_fc2 - new_fc)
            else:
                h_d = 2 * new_fc2 * (np.sin(n * 2 * np.pi * new_fc2) / (n * 2 * np.pi * new_fc2)) - 2 * new_fc * (
                            np.sin(n * 2 * np.pi * new_fc) / (n * 2 * np.pi * new_fc))
            h.append(h_d * w_n)
        # [print(row) for row in list(zip(indices, h))]
    #   band-stop
    elif filter_type == 'Band stop':
        new_fc = f1 + 0.5 * transition_band
        new_fc /= fs
        new_fc2 = f2 - 0.5 * transition_band
        new_fc2 /= fs

        for n in indices:
            w_n = window_function(stop_band_attenuation, n, N)
            if n == 0:
                h_d = 1 - 2 * (new_fc2 - new_fc)
            else:
                h_d = 2 * new_fc * (np.sin(n * 2 * np.pi * new_fc) / (n * 2 * np.pi * new_fc)) - 2 * new_fc2 * (
                            np.sin(n * 2 * np.pi * new_fc2) / (n * 2 * np.pi * new_fc2))
            h.append(h_d * w_n)
        # [print(row) for row in list(zip(indices, h))]
    return indices, h


# Convolve from previous tasks
def convolution(x_values1, y_values1, x_values2, y_values2):
    len1 = len(y_values1)
    len2 = len(y_values2)
    result = []
    start_index = int(min(x_values1) + min(x_values2))
    end_index = int(max(x_values1) + max(x_values2))
    x_values = list(range(start_index, end_index + 1))
    for n in range(len1 + len2 - 1):
        sum = 0
        for m in range(min(n, len1 - 1) + 1):
            if 0 <= n - m < len2:
                sum += y_values1[m] * y_values2[n - m]
        result.append(sum)
    return x_values, result


# applying the filters
def apply_filter(input_x, input_y, filter_x, filter_y):
    output_x, output_y = convolution(input_x, input_y, filter_x, filter_y)
    return output_x, output_y


# plotting
def plot_signal(x, y, title):
    fig, ax = plt.subplots()

    ax.plot(x, y)
    ax.set_title(title)
    ax.set_xlabel('Sample')
    ax.set_ylabel('Amplitude')


def save_coefficients_to_file(coefficients, filename):
    with open(filename, 'w') as file:
        file.write("0\n")
        file.write("0\n")
        file.write(f"{len(coefficients)}\n")
        for coefficient in coefficients:
            file.write(f"{coefficient[0]} {coefficient[1]}\n")


def read_filter_specifications_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    filter_specs = {}
    for line in lines:
        key, value = line.strip().split('=')
        filter_specs[key.strip()] = value.strip()
    return filter_specs


def upsample(signal, factor):
    result = []
    for element in signal:
        result.extend([element] + [0] * (factor - 1))
    for i in range(factor - 1):
        result.pop()
        # print (result)
    return result


def resample_signal(input_x, input_y, M, L, filter_type, fs, stop_band_attenuation, fc, transition_band):
    if M == 0 and L != 0:
        # Upsample by inserting L-1 zeros between each sample
        upsampled_signal = upsample(input_y, L)
        print(upsampled_signal)
        filtered_x, filtered_y = design_fir_filter(filter_type, fs, stop_band_attenuation, fc, transition_band)
        return apply_filter(input_x, upsampled_signal, filtered_x, filtered_y)
    elif M != 0 and L == 0:
        # Downsample by taking every Mth sample
        filtered_x, filtered_y = design_fir_filter(filter_type, fs, stop_band_attenuation, fc, transition_band)
        output_x, output_y = apply_filter(input_x, input_y, filtered_x, filtered_y)
        output_x, output_y = output_x[::M], output_y[::M]
        continuous_indices = list(range(min(output_x), min(output_x) + len(output_x)))
        return continuous_indices, output_y

    elif M != 0 and L != 0:
        # Upsample, filter, and then downsample
        upsampled_signal = upsample(input_y, L)
        upsampled_x = upsample(input_x, L)
        upsampled_x = list(range(min(upsampled_x), min(upsampled_x) + len(upsampled_x)))
        filtered_x, filtered_y = design_fir_filter(filter_type, fs, stop_band_attenuation, fc, transition_band)
        filtered_signal_x, filtered_signal_y = apply_filter(upsampled_x, upsampled_signal, filtered_x, filtered_y)
        filtered_signal_x, filtered_signal_y = filtered_signal_x[::M], filtered_signal_y[::M]
        print(filtered_signal_y)
        continuous_indices = list(range(min(filtered_signal_x), min(filtered_signal_x) + len(filtered_signal_x)))
        return continuous_indices, filtered_signal_y
    else:
        return messagebox.showerror("Invalid values for M and L")


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


def remove_dc_component(x):
    x_list = np.array([])
    mean_value = np.mean(x)
    for x_val in x:
        x_list = np.append(x_list, x_val - mean_value)
    return x_list


def normalize_correlation(x1, x2, corr):
    N = len(x1)
    results = []
    for n in range(N):
        n1_sum = 0
        n2_sum = 0
        for j in range(N):
            n1_sum += x1[j] ** 2
            n2_sum += x2[j] ** 2
        results.append(corr[n] / ((1 / N) * math.sqrt(n1_sum * n2_sum)))
    return results


def normalize_signal(signal):
    max_abs_value = np.max(np.abs(signal))
    if max_abs_value != 0:
        normalized_signal = signal / max_abs_value
    else:
        normalized_signal = signal
    return normalized_signal


def cross_correlation(x1, x2):
    N = len(x1)
    results = []
    for n in range(N):
        sum = 0
        for j in range(N):
            sum += x1[j] * x2[(j + n) % N]
        results.append(((1 / N) * sum))
    return results


def DCT(x):
    N = len(x)
    results = np.array([])
    for k in range(N):
        val = []
        for new_n in range(N):
            val.append(x[new_n] * np.cos((np.pi / (4 * N)) * (2 * new_n - 1) * (2 * k - 1)))
        results = np.append(results, np.sum(val))
    results *= np.sqrt(2 / N)
    return results


def calculate_mean_correlation(test_file, class_content):
    num_samples = min(len(test_file), len(class_content))
    correlation = np.corrcoef(test_file[:num_samples], class_content[:num_samples])[0, 1]
    return correlation


def decide_correlation(test_file, class1_content, class2_content):
    correlation_class1 = calculate_mean_correlation(test_file, class1_content)
    correlation_class2 = calculate_mean_correlation(test_file, class2_content)
    result_text = f"Average Correlation with Class A: {correlation_class1:.4f}\nAverage Correlation with Class B: {correlation_class2:.4f}"
    if correlation_class1 > correlation_class2:
        result_text += "\nTemplate matches Subject A"
    else:
        result_text += "\nTemplate matches Subject B"
    return result_text


# def resample_signal(input_x, input_y, fs, new_fs):
# # Use scipy.signal.resample for resampling
# resampled_y = resample(input_y, int(len(input_y) * new_fs / fs))
# # Adjust resampled x values based on the new sampling rate
# resampled_x = np.linspace(input_x[0], input_x[-1], len(resampled_y))
# return resampled_x, resampled_y
window = Tk()
app = DSPApp(window)


def closing_cbk():
    # Shutdown procedure
    window.quit()
    window.destroy()


window.protocol("WM_DELETE_WINDOW", closing_cbk)
window.mainloop()
