import tkinter as tk
from tkinter import filedialog
import numpy as np

from CompareSignal import Compare_Signals
from yarabbb import read_filter_specifications, calculate_h

def convolve_signals(signal1_samples, signal2_samples,signal1_indices,signal2_indices):

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
  #ConvTest(result_indices,result_samples)
  return result_indices, result_samples

def upsample_signal(samples, indices, L):
    upsampled_signal = []
    upsampled_indices = []

    for i in range(len(samples)):
        upsampled_signal.append(samples[i])
        upsampled_indices.append(indices[i] * L)

        if i < len(samples) - 1:
            for j in range(1, L):
                upsampled_signal.append(0)
                upsampled_indices.append(indices[i] * L + j)

    return upsampled_signal, upsampled_indices

def downsample_signal(samples, indices, M):
    downsampled_signal = []
    downsampled_indices = []

    # Downsampling the samples and corresponding indices
    for i in range(0, len(samples), M):
        if i // M < len(indices):  # Check to avoid index out of range error
            downsampled_signal.append(samples[i])
            downsampled_indices.append(indices[i // M])
    return downsampled_signal, downsampled_indices
def process_signal():
    file_path = filedialog.askopenfilename(title="Select Signal File")
    filter_file_path = filedialog.askopenfilename(title="Select Filter Specifications File")

    M_value = int(M_entry.get())
    L_value = int(L_entry.get())

    signal_data = np.loadtxt(file_path)
    indices = signal_data[:, 0]
    samples = signal_data[:, 1]
    filter_specs = read_filter_specifications(filter_file_path)

    if M_value == 0 and L_value != 0: #Upsampling
        upsampled_signal, upsampled_indices = upsample_signal(samples, indices, L_value)
        filtering, indices_h = calculate_h(filter_specs)
        filtered_upsampled_indices, filtered_upsampled_signal = convolve_signals(upsampled_signal, filtering, upsampled_indices, indices_h)
        print('SAMPLING UP DONE \n')
        file_name = r'D:\signals\FIR test cases\Sampling test cases\Testcase 2\Sampling_Up.txt'
        Compare_Signals(file_name, filtered_upsampled_indices, filtered_upsampled_signal)

        processed_signal_label.config(text="Signal processed with upsampling by {}.".format(L_value))

    elif M_value != 0 and L_value == 0: #Downsampling
        filtering, indices_h = calculate_h(filter_specs)
        filtered_indicies, filtered_signal = convolve_signals(samples, filtering, indices, indices_h)

        downsampled_signal, downsampled_indices = downsample_signal(filtered_signal, filtered_indicies, M_value)

        file_name = r'D:\signals\FIR test cases\Sampling test cases\Testcase 1\Sampling_Down.txt'
        print('SAMPLING DOWN DONE \n')
        Compare_Signals(file_name, downsampled_indices, downsampled_signal)
        processed_signal_label.config(text="Signal processed with downsampling by {}.".format(M_value))

    elif M_value != 0 and L_value != 0:
        upsampled_signal, upsampled_indices = upsample_signal(samples, indices, L_value)
        filtering, indices_h = calculate_h(filter_specs)
        filtered_upsampled_indices, filtered_upsampled_signal = convolve_signals(upsampled_signal, filtering, upsampled_indices, indices_h)

        downsampled_signal, downsampled_indices = downsample_signal(filtered_upsampled_signal, filtered_upsampled_indices, M_value)
        print('SAMPLING UP AND DOWN DONE \n')
        file_name = r'D:\signals\FIR test cases\Sampling test cases\Testcase 3\Sampling_Up_Down.txt'
        Compare_Signals(file_name, downsampled_indices, downsampled_signal)

        processed_signal_label.config(text="Signal processed with upsample by {} and downsample by {}.".format(L_value, M_value))

    else:
        processed_signal_label.config(text="Error: M and L cannot be zero.")

def create_file_selector_button(text, command):
    button = tk.Button(root, text=text, command=command)
    button.pack()

def create_label_entry_pair(label_text):
    label = tk.Label(root, text=label_text)
    label.pack()
    entry = tk.Entry(root)
    entry.pack()
    return entry

def create_process_button():
    button = tk.Button(root, text="Process Signal", command=process_signal)
    button.pack()

def create_processed_signal_label():
    label = tk.Label(root, text="")
    label.pack()
    return label

root = tk.Tk()
root.title("Signal Processing Tool")

create_file_selector_button("Select Signal File", process_signal)
create_file_selector_button("Select Filter Specifications File", process_signal)

M_entry = create_label_entry_pair("Enter M:")
L_entry = create_label_entry_pair("Enter L:")

create_process_button()
processed_signal_label = create_processed_signal_label()

root.mainloop()