import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def DFT(signal):
    N = len(signal)
    frequency_spectrum = np.zeros(N, dtype=complex)

    for k in range(N):
        for n in range(N):
            frequency_spectrum[k] += signal[n] * np.exp(-2j * np.pi * k * n / N)

    amplitude_spectrum = np.abs(frequency_spectrum)
    phase_spectrum = np.angle(frequency_spectrum)

    return amplitude_spectrum, phase_spectrum, frequency_spectrum


def IDFT(frequency_spectrum):
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

def open_file():
    # Retrieve the sampling frequency entered by the user
    sampling_frequency = float(sampling_entry.get())

    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        try:
            signal = np.loadtxt(filepath, usecols=1)
            # Apply Fourier transform
            amplitude_spectrum, phase_spectrum, frequency_spectrum = DFT(signal)

            # Save frequency components in polar form to a text file
            with open("frequency_components.txt", "w") as file:
                for amplitude, phase in zip(amplitude_spectrum, phase_spectrum):
                    file.write(f"{amplitude},{phase}\n")

            messagebox.showinfo("Success", "Frequency components saved to 'frequency_components.txt'")

            # Plot frequency versus amplitude
            time = np.arange(len(amplitude_spectrum)) / sampling_frequency
            fig1, ax1 = plt.subplots(figsize=(4, 4))
            plt.stem(amplitude_spectrum)
            plt.xlabel("Frequency")
            plt.ylabel("Amplitude")
            plt.title("Frequency versus Amplitude")
            canvas1 = FigureCanvasTkAgg(fig1, master=window)
            canvas1.draw()
            canvas1.get_tk_widget().grid(row=0, column=0)

            # Plot frequency versus phase
            time = np.arange(len(phase_spectrum)) / sampling_frequency
            fig2, ax2 = plt.subplots(figsize=(4, 4))
            plt.stem(phase_spectrum)
            plt.xlabel("Frequency")
            plt.ylabel("Phase")
            plt.title("Frequency versus Phase")
            canvas2 = FigureCanvasTkAgg(fig2, master=window)
            canvas2.draw()
            canvas2.get_tk_widget().grid(row=0, column=1)

            components_text1.delete(1.0, tk.END)
            for amplitude, phase in zip(amplitude_spectrum, phase_spectrum):
                components_text1.insert(tk.END, f"{amplitude},{phase}\n")

            # Perform IDFT and plot the reconstructed signal
            inverse_signal = IDFT(frequency_spectrum)
            time = np.arange(len(inverse_signal)) / sampling_frequency  # Generate time axis based on sampling frequency
            fig3, ax3 = plt.subplots(figsize=(6, 4))
            plt.plot(time, inverse_signal)
            plt.xlabel("Time")
            plt.ylabel("Amplitude")
            plt.title("Reconstructed Signal")
            canvas3 = FigureCanvasTkAgg(fig3, master=window)
            canvas3.draw()
            canvas3.get_tk_widget().grid(row=0, column=2)

            # Display frequency components in a text box
            components_text2.delete(1.0, tk.END)
            for n, phase in enumerate( inverse_signal):
                components_text2.insert(tk.END, f"{n} {phase}\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))

def save_edits():
    edited_text = components_text1.get(1.0, tk.END)  # Get the edited text from the text box
    edited_text = components_text2.get(1.0, tk.END)  # Get the edited text from the text box

    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if filepath:
        try:
            with open(filepath, "w") as file:
                file.write(edited_text)

            messagebox.showinfo("Success", "Edits saved successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Create the GUI window
window = tk.Tk()
window.title("Signal Processing")

# Create a label and an entry field for the sampling frequency
sampling_label = tk.Label(window, text="Sampling Frequency (Hz):")
sampling_label.grid(row=1, column=0)
sampling_entry = tk.Entry(window)
sampling_entry.grid(row=1, column=1)


# Create a button to open the file and perform signal processing
open_button = tk.Button(window, text="Open File", command=open_file)
open_button.grid(row=4, column=0, columnspan=2)

# Create a text box to display the frequency components
components_text1 = tk.Text(window, height=10, width=40)
components_text1.grid(row=5, column=0, columnspan=2)

components_text2 = tk.Text(window, height=10, width=40)
components_text2.grid(row=5, column=2, columnspan=2)

# Create a button to save the edits in the components_text text box
save_button = tk.Button(window, text="Save Edits", command=save_edits)
save_button.grid(row=6, column=0, columnspan=2)

# Start the GUI event loop
window.mainloop()