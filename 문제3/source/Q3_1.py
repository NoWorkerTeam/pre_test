import argparse
import wave
import numpy as np
import json, os

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
def detect_silence(file_list, out_file):

    total_time_stamps = {}

    with open(file_list, 'r') as files:
        for file in files.readlines():
            file = file.strip()     # pcm
            file = pcm2wav(file)    # wav

            time_stamps = []

            with wave.open(file, 'rb') as wav_file:
                data = np.frombuffer(wav_file.readframes(wav_file.getnframes()), dtype=np.int16)
                sampling_rate = wav_file.getframerate()

                seq = 0
                threshold = 1000
                for idx, d in enumerate(data):
                    if abs(d) < threshold and idx < len(data) - 1:
                        seq += 1
                    else:
                        if seq >= sampling_rate * 4:
                            beg = (idx - seq) / sampling_rate
                            end = idx / sampling_rate
                            time_stamps.append({"beg": beg, "end": end})
                        seq = 0
                
            total_time_stamps[file] = time_stamps

    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(total_time_stamps, f, ensure_ascii=False, indent=4)

def pcm2wav(pcm_file):
    with open(pcm_file, 'rb') as pcmfile:
        pcmdata = pcmfile.read()

    pcmdata = np.frombuffer(pcmdata, dtype=np.int16)

    wav_file = f"{pcm_file.rsplit('.', 1)[0]}.wav"
    with wave.open(wav_file, 'w') as wavfile:
        wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
        wavfile.writeframes(pcmdata.tobytes())

    return wav_file

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    args = arg_parse()
    detect_silence(args.audiolist, args.outfile)

if __name__ == "__main__":
    main()