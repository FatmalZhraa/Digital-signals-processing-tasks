import tkinter as tk
from tkinter import filedialog
import numpy as np
from CompareSignal import Compare_Signals
from fast_conv import fast_convolution

def get_signal_from_user():
    file_path = filedialog.askopenfilename(title="Select Signal File")
    data1 = np.loadtxt(file_path)
    sampled_signal = data1[:, 1]
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

def calculate_h(filter_specs):
    filter_type = filter_specs['FilterType'].lower()

    if filter_type in {"band pass", "band stop"}:
        f1, f2 = (float(filter_specs['F1']), float(filter_specs['F2']))
    else :
        f1= float((filter_specs['FC']))
        f2=0
    stopband = float(filter_specs['StopBandAttenuation'])
    transition_band = float(filter_specs['TransitionBand'])
    f_s = float(filter_specs['FS'])
    fc_normalized = f1 / f_s
    fc_normalized2 = f2 /f_s
    delta_f = transition_band / f_s
    fc = fc_normalized + (delta_f / 2)
    fc2 = fc_normalized2 + (delta_f / 2)
    hd = []
    w = []
    h = []
    indices = []
    file ="file name"
    # Choose window function based on stopband attenuation
    if stopband <= 21:
        N = round(0.9 / delta_f)
        n1 = int(N - 1 / 2)
        n2 = int(-N + 1 / 2)
        if N % 2 == 0:
            N += 1
            n1 = int(N - 1 / 2)
            n2 = int(-N + 1 / 2)
        indices = list(range(n2, n1 + 1))
        for n in range(n2, n1 + 1):
            w.append(np.ones(N))
            if filter_type == "low pass":
                if n == 0:
                    hd.append(2 * fc)
                else:
                    hd.append((2 * fc) * ((np.sin(2 * np.pi * n * fc)) / (2 * np.pi * n * fc)))
            if filter_type == "high pass":
                fc = fc_normalized - (delta_f / 2)
                if n == 0:
                    hd.append(1 - (2 * fc))
                else:
                    hd.append((-2 * fc) * ((np.sin(2 * np.pi * n * fc)) / (2 * np.pi * n * fc)))
            if filter_type == "band pass":
                fc = fc_normalized - (delta_f / 2)
                if n == 0:
                    hd.append(2 * (fc2 - fc))
                else:
                    hd.append(2 * fc2 * (np.sin(n * 2 * np.pi * fc2) / (n * 2 * np.pi * fc2)) - 2 * fc * (
                            np.sin(n * 2 * np.pi * fc) / (n * 2 * np.pi * fc)))
            if filter_type == "band stop":
                fc2 = fc_normalized2 - (delta_f / 2)
                if n == 0:
                    hd.append(1 - (2 * (fc2 - fc)))
                else:
                    hd.append(2 * fc * (np.sin(n * 2 * np.pi * fc) / (n * 2 * np.pi * fc)) - 2 * fc2 * (
                            np.sin(n * 2 * np.pi * fc2) / (n * 2 * np.pi * fc2)))
        for i in range(len(w)):
            h.append(hd[i] * w[i])


    elif stopband <= 44:
        N = round(3.3 / delta_f)
        n1 = int(N - 1 / 2)
        n2 = int(-N + 1 / 2)
        if N % 2 == 0:
            N += 1
            n1 = int(N - 1 / 2)
            n2 = int(-N + 1 / 2)
        indices = list(range(n2, n1 + 1))
        for n in range(n2, n1+1):
            w.append(0.5 + (0.5 * np.cos(2 * np.pi * n / N)))
            if filter_type == "low pass":
                if n == 0:
                    hd.append(2 * fc)
                else:
                    hd.append((2 * fc) * ((np.sin(2 * np.pi * n * fc)) / (2 * np.pi * n * fc)))
            if filter_type == "high pass":
                fc = fc_normalized - (delta_f / 2)
                if n == 0:
                    hd.append(1 - (2 * fc))
                else:
                    hd.append((-2 * fc) * ((np.sin(2 * np.pi * n * fc)) / (2 * np.pi * n * fc)))
            if filter_type == "band pass":
                fc = fc_normalized - (delta_f / 2)
                if n == 0:
                    hd.append(2 * (fc2 - fc))
                else:
                    hd.append(2 * fc2 * (np.sin(n * 2 * np.pi * fc2) / (n * 2 * np.pi * fc2)) - 2 * fc * (
                            np.sin(n * 2 * np.pi * fc) / (n * 2 * np.pi * fc)))
            if filter_type == "band stop":
                fc2 = fc_normalized2 - (delta_f / 2)
                if n == 0:
                    hd.append(1 - (2 * (fc2 - fc)))
                else:
                    hd.append(2 * fc * (np.sin(n * 2 * np.pi * fc) / (n * 2 * np.pi * fc)) - 2 * fc2 * (
                            np.sin(n * 2 * np.pi * fc2) / (n * 2 * np.pi * fc2)))
        for i in range(len(w)):
            h.append(hd[i] * w[i])

    elif stopband <= 53:
        N = round(3.3 / delta_f)
        n1 = int((N - 1) / 2)
        n2 = int((-N + 1) / 2)
        if N % 2 == 0:
            N += 1
            n1 = int((N - 1) / 2)
            n2 = int((-N + 1) / 2)
        indices = list(range(n2, n1 + 1))
        for n in range(n2, n1 + 1):
            w.append(0.54 + (0.46 * np.cos(2 * np.pi * n / N)))
            if filter_type == "low pass":
                if n == 0:
                    hd.append(2 * fc)
                else:
                    hd.append((2 * fc) * ((np.sin(2 * np.pi * n * fc)) / (2 * np.pi * n * fc)))
                file= r'D:\signals\FIR test cases\Testcase 1\LPFCoefficients.txt'
            if filter_type == "high pass":
                fc = fc_normalized - (delta_f / 2)
                if n == 0:
                    hd.append(1 - (2 * fc))
                else:
                    hd.append((-2 * fc) * ((np.sin(2 * np.pi * n * fc)) / (2 * np.pi * n * fc)))
            if filter_type == "band pass":
                fc = fc_normalized - (delta_f / 2)
                if n == 0:
                    hd.append(2 * (fc2 - fc))
                else:
                    hd.append(2 * fc2 * (np.sin(n * 2 * np.pi * fc2) / (n * 2 * np.pi * fc2)) - 2 * fc * (
                            np.sin(n * 2 * np.pi * fc) / (n * 2 * np.pi * fc)))
            if filter_type == "band stop":
                fc2 = fc_normalized2 - (delta_f / 2)
                if n == 0:
                    hd.append(1 - (2 * (fc2 - fc)))
                else:
                    hd.append(2 * fc * (np.sin(n * 2 * np.pi * fc) / (n * 2 * np.pi * fc)) - 2 * fc2 * (
                            np.sin(n * 2 * np.pi * fc2) / (n * 2 * np.pi * fc2)))
        for i in range(len(w)):
            h.append(hd[i] * w[i])

    elif stopband <= 74:

        N = round(5.5 / delta_f)
        n1 = int((N - 1) / 2)
        n2 = int((-N + 1) / 2)
        if N % 2 == 0:
            N += 1
            n1 = int((N - 1) / 2)
            n2 = int((-N + 1) / 2)
        indices = list(range(n2, n1 + 1))

        for n in range(n2, n1 + 1):
            w.append(0.42 + (0.5 * np.cos((2 * np.pi * n) / (N - 1))) + (0.08 * np.cos((4 * np.pi * n) / (N - 1))))
            if filter_type == "low pass":
                if n == 0:
                    hd.append(2 * fc)
                else:
                    hd.append((2 * fc) * ((np.sin(2 * np.pi * n * fc)) / (2 * np.pi * n * fc)))
            if filter_type == "high pass":
                fc = fc_normalized - (delta_f / 2)
                if n == 0:
                    hd.append(1 - (2 * fc))
                else:
                    hd.append((-2 * fc) * ((np.sin(2 * np.pi * n * fc)) / (2 * np.pi * n * fc)))
                file = r'D:\signals\FIR test cases\Testcase 3\HPFCoefficients.txt'

            if filter_type == "band pass":
                fc = fc_normalized - (delta_f / 2)
                if n == 0:
                    hd.append(2 * (fc2 - fc))
                else:
                    hd.append(2 * fc2 * (np.sin(n * 2 * np.pi * fc2) / (n * 2 * np.pi * fc2)) - 2 * fc * (
                                np.sin(n * 2 * np.pi * fc) / (n * 2 * np.pi * fc)))
                file = r'D:\signals\FIR test cases\Testcase 5\BPFCoefficients.txt'
            if filter_type == "band stop":
                fc2 = fc_normalized2 - (delta_f / 2)
                if n == 0:
                    hd.append(1-(2 * (fc2 - fc)))
                else:
                    hd.append(2 * fc * (np.sin(n * 2 * np.pi * fc) / (n * 2 * np.pi * fc)) - 2 * fc2 * (
                                np.sin(n * 2 * np.pi * fc2) / (n * 2 * np.pi * fc2)))
                file = r'D:\signals\FIR test cases\Testcase 7\BSFCoefficients.txt'
        # print("BAND PASS DONE\n")
        for i in range(len(w)):
            h.append(hd[i] * w[i])

    file_name = file
    Compare_Signals(file_name, indices, h)
    return h, indices


def design_fir_filter():
    choice = radio_var.get()

    if choice == "OneFile":
        filter_specs_file_path = filedialog.askopenfilename(title="Select Filter Specifications File")
        if filter_specs_file_path:
            filter_specs = read_filter_specifications(filter_specs_file_path)
            h = calculate_h(filter_specs)


    elif choice == "TwoFiles":
        # Use get_signal_from_user() without passing any arguments
        sampled_signal = get_signal_from_user()
        filter_specs_file_path = filedialog.askopenfilename(title="Select Filter Specifications File")
        if filter_specs_file_path:
            filter_specs = read_filter_specifications(filter_specs_file_path)
            filter_type = filter_specs['FilterType'].lower()
            h, indices = calculate_h(filter_specs)
            filtered_signal = fast_convolution(sampled_signal, h)
            if filter_type == "low pass":
                output_file = r'D:\signals\FIR test cases\Testcase 2\ecg_low_pass_filtered.txt'
                Compare_Signals(output_file, indices, filtered_signal)
            elif filter_type == "high pass":
                output_file = r'D:\signals\FIR test cases\Testcase 4\ecg_high_pass_filtered.txt'
                Compare_Signals(output_file, indices, filtered_signal)
            elif filter_type == "band pass":
                output_file = r'D:\signals\FIR test cases\Testcase 6\ecg_band_pass_filtered.txt'
                Compare_Signals(output_file, indices, filtered_signal)
            elif filter_type == "stop pass":
                output_file = r'D:\signals\FIR test cases\Testcase 8\ecg_band_stop_filtered.txt'
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