import wave
import numpy as np

def process():
    fp, fn, fe =  filePaths()
    for p, n, e in zip(fp, fn, fe): 
        with wave.open(f'{p}/{n}.{e}', 'rb') as wav_file:
            data = np.frombuffer(wav_file.readframes(wav_file.getnframes()), dtype=np.int16)
            sampling_rate = wav_file.getframerate()

        plot_sound(data, sampling_rate)

def plot_sound(data, sampling_rate):
    import matplotlib.pyplot as plt

    time = np.arange(0, len(data)) / sampling_rate

    plt.figure(figsize=(10, 4))
    plt.plot(time, data)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Sound Wave')

    xticks = np.arange(min(time), max(time)+1, 0.5)
    plt.xticks(xticks, rotation='horizontal')

    for x in xticks:
        plt.axvline(x, color='gray', linewidth=1)
    plt.axhline(0, color='gray', linewidth=0.5)

    plt.show()

def filePaths():
    from tkinter import filedialog, Tk
    import os

    root = Tk()
    root.withdraw()

    fullPaths = filedialog.askopenfilenames(title = 'Select Wav Files', initialdir = os.getcwd(), filetypes = [("Wav files", "*.wav"), ("All files", "*.*")])

    paths, names, extensions = [], [], []
    for p in fullPaths:
        temp = p.split('/')
        path = '/'.join(temp[ : -1])
        name = temp[-1]
        if '.' in name:
            name, extension = name.rsplit('.')

        paths.append(path)
        names.append(name)
        extensions.append(extension)

    return paths, names, extensions

if __name__=="__main__":
    process()