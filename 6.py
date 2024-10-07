import os
import tkinter as tk
from tkinter import filedialog
import numpy as np
from Compare_Signals import Compare_Signals


def circular_shift(arr, shift):
    return np.roll(arr, shift)


def calculate_correlation(sample1, sample2):
    correlation_values = []
    N = len(sample1)

    for j in range(N):
        correlation_sum = 0

        # Shifting sample2 circularly by j positions
        shifted_sample2 = circular_shift(sample2, -j)

        for n in range(N):
            correlation_sum += sample1[n] * shifted_sample2[n]

        correlation = correlation_sum / N
        correlation_values.append(correlation)
        print(f'r12({j}) = {correlation}')

    return correlation_values

# Function to handle button click for choosing folders
def choose_folders():
    folder_path1 = filedialog.askdirectory()
    folder_path2 = filedialog.askdirectory()

    if folder_path1 and folder_path2:
        result1, result2 = process_signals_in_folders(folder_path1, folder_path2)

        # Prompt the user to select file_path1 and file_path2
        file_path1 = filedialog.askopenfilename(title="Select file for result1")
        file_path2 = filedialog.askopenfilename(title="Select file for result2")

        if file_path1 and file_path2:
            # Load data from file 1
            data1 = np.loadtxt(file_path1)

            # Load data from file 2
            data2 = np.loadtxt(file_path2)

            # Calculate cross-correlation for result1 and file1
            cross_corr_result1_file1 = calculate_correlation(result1, data1)

            # Calculate cross-correlation for result2 and file1
            cross_corr_result2_file1 = calculate_correlation(result2, data1)

            # Calculate cross-correlation for result1 and file2
            cross_corr_result1_file2 = calculate_correlation(result1, data2)

            # Calculate cross-correlation for result2 and file2
            cross_corr_result2_file2 = calculate_correlation(result2, data2)

            # Find max values and calculate differences for file1
            max_corr_result1_file1 = max(cross_corr_result1_file1)
            max_corr_result2_file1 = max(cross_corr_result2_file1)

            diff_file1 = max_corr_result1_file1 - max_corr_result2_file1
            print("Difference between max correlation values for file1:", diff_file1)

            # Determine class based on diff_file1
            if diff_file1 > 0:
                print("Class 1 ⇒ down movement of EOG signal")
            else:
                print("Class 2 ⇒ up movement of EOG signal")

            # Find max values and calculate differences for file2
            max_corr_result1_file2 = max(cross_corr_result1_file2)
            max_corr_result2_file2 = max(cross_corr_result2_file2)

            diff_file2 = max_corr_result1_file2 - max_corr_result2_file2
            print("Difference between max correlation values for file2:", diff_file2)

            # Determine class based on diff_file2
            if diff_file2 > 0:
                print("Class 1 ⇒ down movement of EOG signal")
            else:
                print("Class 2 ⇒ up movement of EOG signal")
def process_signals_in_folders(folder_path1, folder_path2):
    # List all files in the first folder
    signal_files_folder1 = os.listdir(folder_path1)
    signal_files_folder2 = os.listdir(folder_path2)

    # Initialize lists to store the element-wise sums for each folder
    elementwise_sums_folder1 = None
    elementwise_sums_folder2 = None

    # Process files in the first folder
    for file_name in signal_files_folder1:
        file_path = os.path.join(folder_path1, file_name)
        signal_data = read_signal_data(file_path)

        if elementwise_sums_folder1 is None:
            elementwise_sums_folder1 = signal_data
        else:
            elementwise_sums_folder1 = [x + y for x, y in zip(elementwise_sums_folder1, signal_data)]

    # Process files in the second folder
    for file_name in signal_files_folder2:
        file_path = os.path.join(folder_path2, file_name)
        signal_data = read_signal_data(file_path)

        if elementwise_sums_folder2 is None:
            elementwise_sums_folder2 = signal_data
        else:
            elementwise_sums_folder2 = [x + y for x, y in zip(elementwise_sums_folder2, signal_data)]

    # Divide each element of the sum by the number of files in the respective folder
    count_files_folder1 = count_files_in_folder(folder_path1)
    count_files_folder2 = count_files_in_folder(folder_path2)

    elementwise_sums_folder1 = [x / count_files_folder1 for x in elementwise_sums_folder1]
    elementwise_sums_folder2 = [x / count_files_folder2 for x in elementwise_sums_folder2]

    return elementwise_sums_folder1, elementwise_sums_folder2


def read_signal_data(file_path):
    with open(file_path, 'r') as file:
        # Read lines and convert them to floats
        data = [float(line.strip()) for line in file.readlines()]
    return data


def count_files_in_folder(folder_path):
    file_list = os.listdir(folder_path)
    return len(file_list)


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

    # Calculate correlation using the function
    correlation = calculate_correlation(samples1, samples2)

    # Normalize the correlation values
    x = np.sqrt(np.sum(samples1 ** 2) * np.sum(samples2 ** 2))
    normalized_values = correlation / (x / len(samples1))

    # Call the comparison function
    Compare_Signals(r'D:\signals\task7\CorrOutput.txt', np.arange(len(samples1)), normalized_values)


def compute_time_delay():
    # Get file paths
    file1_path = filedialog.askopenfilename(title="Select First File")
    file2_path = filedialog.askopenfilename(title="Select Second File")

    # Read data from files
    data1 = np.loadtxt(file1_path)
    data2 = np.loadtxt(file2_path)

    # Extract samples
    samples1 = data1[:, 1]
    samples2 = data2[:, 1]

    fs = float(entry_fs.get())

    cross_corr = calculate_correlation(samples1, samples2)

    delay_index = np.argmax(np.abs(cross_corr))
    max_abs_corr = np.max(np.abs(cross_corr))

    # Calculate time delay using delay index and sampling frequency
    time_delay = delay_index / fs

    # Display the time delay in a label
    label_result.config(text=f"Time delay between signals: {time_delay} seconds (Max Correlation: {max_abs_corr})")


# Create GUI
root = tk.Tk()
root.title("Signal Analysis")
root.geometry("400x300")

# Add labels and entry for sampling frequency (fs)
label_fs = tk.Label(root, text="Enter Sampling Frequency (fs):")
label_fs.pack()

entry_fs = tk.Entry(root)
entry_fs.pack()

# Add button to choose folders and process signals
choose_folders_button = tk.Button(root, text="Choose Folders and Process Signals", command=choose_folders)
choose_folders_button.pack(pady=10)

# Add button to compute correlation
compute_corr_button = tk.Button(root, text="Compute Correlation", command=compute_correlation)
compute_corr_button.pack(pady=10)

# Add button to compute time delay
compute_delay_button = tk.Button(root, text="Compute Time Delay", command=compute_time_delay)
compute_delay_button.pack(pady=10)

# Add label to display the result
label_result = tk.Label(root, text="")
label_result.pack()

# Start the GUI event loop
root.mainloop()