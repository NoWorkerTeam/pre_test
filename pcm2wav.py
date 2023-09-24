import numpy as np
import wave

def process():
    fp, fn, fe =  filePaths()
    for p, n, e in zip(fp, fn, fe): 
        with open(f'{p}/{n}.{e}', 'rb') as pcmfile:
            pcmdata = pcmfile.read()

        pcmdata = np.frombuffer(pcmdata, dtype = np.int16)

        with wave.open(f'{p}/{n}.wav', 'w') as wavfile:
            wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
            wavfile.writeframes(pcmdata.tobytes())
    
def filePaths():
    from tkinter import filedialog, Tk
    import os

    root = Tk()
    root.withdraw()

    fullPaths = filedialog.askopenfilenames(title = 'Select Pcm Files', initialdir = os.getcwd(), filetypes = [("Pcm files", "*.pcm"), ("All files", "*.*")])

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