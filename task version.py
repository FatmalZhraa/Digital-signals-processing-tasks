import tkinter as tk
from tkinter import filedialog
import soundfile as sf
import numpy as np
from CompareSignal import Compare_Signals
from conv_test import ConvTest
from fast import fast_convolution


def get_signal_from_user():
    file_path = filedialog.askopenfilename(title="Select Signal File")
    data1 = np.loadtxt(file_path)
    sampled_signal = data1[:, 1]
    print(sampled_signal)
    return sampled_signal


def read_filter_specifications(file_path):
    filter_specs = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                filter_specs[key.strip()] = value.strip()
    except Exception as e:
        print(f"Error reading file: {e}")
    return filter_specs

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
  # ConvTest(result_indices,result_samples)
  return  result_samples
def calculate_h(filter_specs):
    filter_type = filter_specs['FilterType'].lower()
    f1, f2 = (float(filter_specs['FC']), float(filter_specs['f2'])) if filter_type in {"bandpass", "bandstop"} else (
        float(filter_specs['FC']), None)
    stopband = float(filter_specs['StopBandAttenuation'])
    transition_band = float(filter_specs['TransitionBand'])
    f_s = float(filter_specs['FS'])
    fc_normalized = f1 / f_s
    delta_f = transition_band / f_s
    fc = fc_normalized + (delta_f / 2)
    # print(filter_type, f1, f2, stopband, transition_band, f_s, fc_normalized, delta_f, fc)

    hd = []
    w = []
    h = []
    indices = []

    # Choose window function based on stopband attenuation
    if stopband <= 21:
        N = round(0.9 / delta_f)
        n1 = int(N - 1 / 2)
        n2 = int(-N + 1 / 2)
        if N % 2 == 0:
            N += 1
        w = np.ones(N)
        indices = list(range(n1, n2 + 1))

    elif stopband <= 44:
        N = round(3.3 / delta_f)
        n1 = int(N - 1 / 2)
        n2 = int(-N + 1 / 2)
        if N % 2 == 0:
            N += 1
            n1 = int(N - 1 / 2)
            n2 = int(-N + 1 / 2)
        indices = list(range(n2, n1+1))

        for n in range(n2, n1):
            w.append(0.5 + (0.5 * np.cos(2 * np.pi * n / N)))

    elif stopband <= 53:
        N = round(3.3 / delta_f)
        n1 = int((N - 1) / 2)
        n2 = int((-N + 1) / 2)
        if N % 2 == 0:
            N += 1
            n1 = int((N - 1) / 2)
            n2 = int((-N + 1) / 2)
        indices = list(range(n2, n1+1))

        for n in range(n2, n1 + 1):
            w.append(0.54 + (0.46 * np.cos(2 * np.pi * n / N)))
            if filter_type == "low pass":
                if n == 0:
                    hd.append(2 * fc)
                else:
                    hd.append((2 * fc) * ((np.sin(2 * np.pi * n * fc)) / (2 * np.pi * n * fc)))
            if filter_type == "high pass":
                if n == 0:
                    hd.append(1 - (2 * fc))
                else:
                    hd.append((-2 * fc) * ((np.sin(2 * np.pi * n * fc)) / (2 * np.pi * n * fc)))

        for i in range(len(hd)):
            h.append(hd[i] * w[i])
        print(len(h))
        for i in range(len(hd)):
            print(f"{i},{h[i]}\n")

    elif stopband <= 74:
        N = round(5.5 / delta_f)
        n1 = int((N - 1) / 2)
        n2 = int((-N + 1) / 2)
        if N % 2 == 0:
            N += 1
            n1 = int((N - 1) / 2)
            n2 = int((-N + 1) / 2)
        indices = list(range(n2, n1+1))

        for n in range(n2, n1 + 1):
            w.append(0.42 + (0.5 * np.cos(2 * np.pi * n / (N - 1))) + (0.08 * np.cos(4 * np.pi * n / (N - 1))))
            if filter_type == "low pass":
                if n == 0:
                    hd.append(2 * fc)
                else:
                    hd.append((2 * fc) * ((np.sin(2 * np.pi * n * fc)) / (2 * np.pi * n * fc)))
            if filter_type == "high pass":
                if n == 0:
                    hd.append(1 - (2 * fc))
                else:
                    hd.append((-2 * fc) * ((np.sin(2 * np.pi * n * fc)) / (2 * np.pi * n * fc)))

        for i in range(len(hd)):
            h.append(hd[i] * w[i])
        print(len(h))
        for i in range(len(hd)):
         print(f"{i},{h[i]}\n")
    file_name = r'D:\signals\FIR test cases\Testcase 1\LPFCoefficients.txt'
    #Compare_Signals(file_name, indices, h)
    return h, indices


def design_fir_filter():
    choice = radio_var.get()

    if choice == "OneFile":
        filter_specs_file_path = filedialog.askopenfilename(title="Select Filter Specifications File")
        if filter_specs_file_path:
            filter_specs = read_filter_specifications(filter_specs_file_path)
            h, indecies = calculate_h(filter_specs)
            print ("your indecies",indecies)


    elif choice == "TwoFiles":
        # Use get_signal_from_user() without passing any arguments
        sampled_signal = get_signal_from_user()
        filter_specs_file_path = filedialog.askopenfilename(title="Select Filter Specifications File")
        if filter_specs_file_path:
            filter_specs = read_filter_specifications(filter_specs_file_path)
            h, indices = calculate_h(filter_specs)
            filtered_signal = fast_convolution(sampled_signal, h)
            output_file = r'D:\signals\FIR test cases\Testcase 2\ecg_low_pass_filtered.txt'
            print(f"Filtered signal  to: {filtered_signal}")
            print("ggg")
            Compare_Signals(output_file, indices, filtered_signal)


# Create the main window
window = tk.Tk()
window.title("FIR Filter Design")
window.geometry("400x500")

# Radio button to select file choice
radio_var = tk.StringVar()
radio_var.set("OneFile")  # Default choice
radio_option_one = tk.Radiobutton(window, text="One File (Filter Specifications)", variable=radio_var, value="OneFile",
                                  command=design_fir_filter)
radio_option_one.pack()
radio_option_two = tk.Radiobutton(window, text="Two Files (Signal and Filter Specifications)", variable=radio_var,
                                  value="TwoFiles", command=design_fir_filter)
radio_option_two.pack()

# Entry field for the signal file path (hidden initially)
signal_entry = tk.Entry(window, state='readonly')
signal_entry.pack()

# Create a button to design the filter
design_button = tk.Button(window, text="Design Filter", command=design_fir_filter)
design_button.pack()

# Start the main event loop
window.mainloop()