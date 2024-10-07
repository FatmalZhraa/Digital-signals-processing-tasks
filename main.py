from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
from tkinter.ttk import Combobox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

import quant


class SignalProcessor:
    def __init__(self):

        self.signal = []
        self.selected_signals = []  # Initialize the selected signals list


        self.root = Tk()
        self.root.title("Signal Processor")

        self.menu_bar = Menu(self.root)
        signal_generation_menu = Menu(self.menu_bar, tearoff=0)

        signal_generation_menu.add_command(label="Sin signal", command=self.display_sin_signal)
        signal_generation_menu.add_command(label="Cos signal", command=self.display_cos_signal)
        self.menu_bar.add_cascade(label="Signal Generation", menu=signal_generation_menu)
        arithmetic_menu = Menu(self.menu_bar, tearoff=0)
        arithmetic_menu.add_command(label="Operations" , command=self.display_signal)
        self.menu_bar.add_cascade(label="Quantization", menu=arithmetic_menu,command=quant)


        self.menu_bar.add_cascade(label="Arithmetic Operations", menu=arithmetic_menu,command=self.display_signal)

        self.root.config(menu=self.menu_bar)

        b1 = Button(
            self.root, text='Open File', command=self.open_file_dialog, font=("Arial", 13, "bold"), width=15, height=2,
            background='purple', foreground='white'
        )
        b1.pack()

    def display_signal(self):
        self.signal_window = Toplevel(self.root)
        self.signal_window.title("Signal Operations")

        self.operation_label = Label(self.signal_window, text="Select Operation:")
        self.operation_label.pack()

        self.operation_combobox = Combobox(self.signal_window, values=["Add", "Subtract", "Multiply","Square","Accumulation"],font=("Arial", 9, "bold"))
        self.operation_combobox.current(0)
        self.operation_combobox.pack()

        add_button = Button(self.signal_window, text='Select Signals',
                            command=self.open_files,background='purple', foreground='white',font=("Arial", 13, "bold"))
        add_button.pack()


        self.signals_listbox = Listbox(self.signal_window, selectmode=MULTIPLE)
        self.signals_listbox.pack()

        self.operation_button = Button(self.signal_window, text="Apply Operation",
                                       command=self.apply_operation, background='purple', foreground='white',font=("Arial", 13, "bold"))
        self.operation_button.pack()

        clear_button = Button(self.signal_window, text="Clear",
                              command=lambda: self.signals_listbox.delete(0, END),background='purple', foreground='white',font=("Arial", 13, "bold"))
        clear_button.pack()

    def open_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[('Text Files', '*.txt')])
        for file_path in file_paths:
            self.signals_listbox.insert(END, file_path)

    def apply_operation(self):

        # Get the selected operation
        operation = self.operation_combobox.get()

        # Get the selected signal files
        signal_file_paths = self.signals_listbox.get(0, END)

        # Check if at least two signal files have been selected
        if len(signal_file_paths) < 1:
            messagebox.showinfo(title="Error", message="Please select at least two signal files.")
            return

        # Load the signals from the selected files
        signals = []
        for file_path in signal_file_paths:
            signals.append(np.loadtxt(file_path))

        # Extract the y-values of the signals
        y_values = []
        x_values = []

        for signal in signals:
            y_values.append(signal[:, 1])
            x_values.append(signal[:, 0])

        result = y_values[0]
        # Perform the operation on the y-values
        for index in range(1, len(y_values)):

            if operation == "Add":
                result += y_values[index]
            elif operation == "Subtract":
                result -= y_values[index]
                result = result * -1

        if operation == "Square":
            result = result ** 2

        if operation == "Multiply":
            root = Tk()
            root.withdraw()
            constant = simpledialog.askfloat("Multiply Signal",
                                             "Enter the constant value :")
            amplified_signal = result * constant
            result = amplified_signal

        if operation == "Accumulation":
            result = np.cumsum(result)

        for i, value in enumerate(result):
            print(f" {i}, {value}")  # Plot the result
        # Plot the result
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(signals[0][:, 0], result)
        ax.set_title(operation + " of Signals")
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        canvas = FigureCanvasTkAgg(fig, master=self.signal_window)
        canvas.get_tk_widget().pack()
        canvas.draw()

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
        if file_path:
            self.read_signal_from_file(file_path)
            self.display_signals()
        button = Button(
            self.root, text='Display Both Signals', command=self.plot_signal,
            font=("Arial", 13, "bold"), width=20, height=2,
            background='purple', foreground='white'
        )
        button.pack()

    def read_signal_from_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.signal = [tuple(map(float, line.strip().split())) for line in lines]
            print(self.signal)

    # display two signals in two separated graghs

    def display_signals(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        # Continuous representation
        x_values, y_values = zip(*self.signal)
        ax1.plot(x_values, y_values, label='Continuous Signal')
        ax1.legend()

        # Discrete representation
        ax2.stem(x_values, y_values, linefmt='C1-', markerfmt='C1o', basefmt='k-', label='Discrete Signal')
        ax2.legend()

        # Draw the plots
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def plot_signal(self):
        fig = plt.figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        x_values, y_values = zip(*self.signal)
        ax.plot(x_values, y_values, label='Continuous Signal')
        ax.stem(x_values, y_values, linefmt='C1-', markerfmt='C1o', basefmt='k-', label='Discrete Signal')
        ax.legend()
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def display_sin_signal(self):
        self.generate_signal_window = Toplevel(self.root)
        self.generate_signal_window.title("Generate Sine Signal")

        amplitude_label = Label(self.generate_signal_window, text="Amplitude A:")
        amplitude_label.pack()
        self.amplitude_entry = Entry(self.generate_signal_window)
        self.amplitude_entry.pack()

        phase_shift_label = Label(self.generate_signal_window, text="Phase Shift Theta:")
        phase_shift_label.pack()
        self.phase_shift_entry = Entry(self.generate_signal_window)
        self.phase_shift_entry.pack()

        analog_frequency_label = Label(self.generate_signal_window, text="Analog Frequency:")
        analog_frequency_label.pack()
        self.analog_frequency_entry = Entry(self.generate_signal_window)
        self.analog_frequency_entry.pack()

        sampling_frequency_label = Label(self.generate_signal_window, text="Sampling Frequency:")
        sampling_frequency_label.pack()
        self.sampling_frequency_entry = Entry(self.generate_signal_window)
        self.sampling_frequency_entry.pack()

        generate_button = Button(self.generate_signal_window, text="Generate", command=self.generate_sin_wave)
        generate_button.pack()

    def display_cos_signal(self):
        self.generate_signal_window = Toplevel(self.root)
        self.generate_signal_window.title("Generate Cosine Signal")

        amplitude_label = Label(self.generate_signal_window, text="Amplitude A:")
        amplitude_label.pack()
        self.amplitude_entry = Entry(self.generate_signal_window)
        self.amplitude_entry.pack()

        phase_shift_label = Label(self.generate_signal_window, text="Phase Shift Theta:")
        phase_shift_label.pack()
        self.phase_shift_entry = Entry(self.generate_signal_window)
        self.phase_shift_entry.pack()

        analog_frequency_label = Label(self.generate_signal_window, text="Analog Frequency:")
        analog_frequency_label.pack()
        self.analog_frequency_entry = Entry(self.generate_signal_window)
        self.analog_frequency_entry.pack()

        sampling_frequency_label = Label(self.generate_signal_window, text="Sampling Frequency:")
        sampling_frequency_label.pack()
        self.sampling_frequency_entry = Entry(self.generate_signal_window)
        self.sampling_frequency_entry.pack()

        generate_button = Button(self.generate_signal_window, text="Generate", command=self.generate_cos_wave)
        generate_button.pack()

    def generate_sin_wave(self):
        amplitude_value = self.amplitude_entry.get()
        phase_shift_value = self.phase_shift_entry.get()
        analog_frequency_value = self.analog_frequency_entry.get()
        sampling_frequency_value = self.sampling_frequency_entry.get()

        if not self.validate_input_values():
            return

        amplitude = float(amplitude_value)
        phase_shift = float(phase_shift_value)
        analog_frequency = float(analog_frequency_value)
        sampling_frequency = float(sampling_frequency_value)

        t = np.arange(0, 1, 1 / sampling_frequency)
        y = amplitude * np.sin(2 * np.pi * analog_frequency * t + phase_shift)
        self.generated_signal = y
        for i, sample in enumerate(self.generated_signal):
            print(f"Sample {i + 1}, {sample}")

        with open('wave_values.txt', 'w') as file:
            file.write("SIN WAVE:\n")
            for i, point in enumerate(self.generated_signal):
                file.write(f" {i + 1}' '{point}\n")

        fig = plt.figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.plot(t, y, label='sin Wave')
        ax.legend()
        canvas = FigureCanvasTkAgg(fig, master=self.generate_signal_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

        return True

    def generate_cos_wave(self):
        amplitude_value = self.amplitude_entry.get()
        phase_shift_value = self.phase_shift_entry.get()
        analog_frequency_value = self.analog_frequency_entry.get()
        sampling_frequency_value = self.sampling_frequency_entry.get()

        # Validate the input values
        if not self.validate_input_values():
            return

        # Convert input values to float
        amplitude = float(amplitude_value)
        phase_shift = float(phase_shift_value)
        analog_frequency = float(analog_frequency_value)
        sampling_frequency = float(sampling_frequency_value)

        # Generate the cosine wave
        t = np.arange(0, 1, 1 / sampling_frequency)
        y = amplitude * np.cos(2 * np.pi * analog_frequency * t + phase_shift)
        self.generated_signal = y
        for i, sample in enumerate(self.generated_signal):
            print(f"Sample {i + 1}, {sample}")

        with open('wave_values.txt', 'w') as file:
            file.write("COS WAVE:\n")
            for i, point in enumerate(self.generated_signal):
                file.write(f" {i + 1}' '{point}\n")

        # Plot the cosine wave
        fig = plt.figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.plot(t, y, label='Cosine Wave')
        ax.legend()
        canvas = FigureCanvasTkAgg(fig, master=self.generate_signal_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def validate_input_values(self):
        try:
            amplitude_value = float(self.amplitude_entry.get())
            phase_shift_value = float(self.phase_shift_entry.get())
            analog_frequency_value = float(self.analog_frequency_entry.get())
            sampling_frequency_value = float(self.sampling_frequency_entry.get())
        except ValueError:
            messagebox.showinfo(title="Error", message="Please enter valid numeric values.")
            return False

        return True
    def run(self):
        self.root.mainloop()


signal_processor = SignalProcessor()
signal_processor.run()