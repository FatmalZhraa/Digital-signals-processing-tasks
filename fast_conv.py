
import numpy as np

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
    inverse_signal = inverse_signal

    # Round the inverse signal values to the nearest integer
    inverse_signal = inverse_signal

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
    return convolved_signal