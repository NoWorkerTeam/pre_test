'''
    한국어AI 경진대회 2023 제출 코드 입출력 예시
'''

import argparse

import json, wave, os
import numpy as np
from pydub import AudioSegment, silence

def arg_parse():
    parser = argparse.ArgumentParser(description='Korean SR Contest 2023')
    parser.add_argument('audiolist', type=str, default='pcmlist.txt', nargs='?')
    parser.add_argument('outfile', type=str, default='../output/Q3.json', nargs='?')

    args = parser.parse_args()

    return args


'''
    - file_list : audio file list (pcmlist.txt)
    - out_file : output file (Q3.json)
'''

def filePaths(file_list):
    paths, names, extensions = [], [], []
    for p in file_list:
        temp = p.split('/')
        path = '/'.join(temp[ : -1])
        name = temp[-1]
        if '.' in name:
            name, extension = name.rsplit('.')

        paths.append(path)
        names.append(name)
        extensions.append(extension)

    return paths, names, extensions

def process(fp, fn, fe):
    for p, n, e in zip(fp, fn, fe): 
        with open(f'{p}/{n}.{e}', 'rb') as pcmfile:
            pcmdata = pcmfile.read()

        pcmdata = np.frombuffer(pcmdata, dtype = np.int16)

        with wave.open(f'{p}/{n}.wav', 'w') as wavfile:
            wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
            wavfile.writeframes(pcmdata.tobytes())

def detect_silence(file_list, out_file):
    silence_info = {}
    for file in file_list:
        # Load the audio file
        audio = AudioSegment.from_wav(file)

        # Find the start and end times of silence longer than 4 seconds
        silences = silence.detect_silence(audio, min_silence_len=4000, silence_thresh=-39.5)

        # Convert the times to seconds
        silences = [[round(t / 1000.0, 3) for t in s] for s in silences]

        # Add the start and end times of silence to the dictionary
        silence_info[file] = silences

    # Write the dictionary to a JSON file
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(silence_info, f, ensure_ascii=False, indent=4)

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    args = arg_parse()

    with open(args.audiolist, 'r') as f:
        file_list = [line.strip() for line in f.readlines()]
    fp, fn, fe = filePaths(file_list)
    process(fp, fn, fe)

    
    detect_silence([f'{fp[i]}/{fn[i]}.wav' for i in range(len(fp))], args.outfile)

    # detect_silence(args.audiolist, args.outfile)


if __name__ == "__main__":
    main()