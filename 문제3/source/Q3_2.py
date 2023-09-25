import argparse
import json
import os
import wave
import numpy as np
from pydub import AudioSegment, silence
from pydub.silence import detect_nonsilent

# 상수 정의
MIN_SILENCE_LENGTH = 100 #ms
SILENCE_THRESHOLD = -32.64 #음량 임계값 

def arg_parse():
    parser = argparse.ArgumentParser(description='한국어AI 경진대회 2023')
    parser.add_argument('audiolist', type=str, default='pcmlist.txt', nargs='?')
    parser.add_argument('outfile', type=str, default='../output/Q3.json', nargs='?')
    args = parser.parse_args()
    return args

def file_paths(file_list):
    paths, names, extensions = [], [], []
    for p in file_list:
        temp = p.split('/')
        path = '/'.join(temp[:-1])
        name = temp[-1]
        if '.' in name:
            name, extension = name.rsplit('.')
        paths.append(path)
        names.append(name)
        extensions.append(extension)
    return paths, names, extensions

def process(file_paths, file_names, file_extensions):
    for p, n, e in zip(file_paths, file_names, file_extensions):
        with open(f'{p}/{n}.{e}', 'rb') as pcmfile:
            pcmdata = pcmfile.read()
        pcmdata = np.frombuffer(pcmdata, dtype=np.int16)
        with wave.open(f'{p}/{n}.wav', 'w') as wavfile:
            wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
            wavfile.writeframes(pcmdata.tobytes())

def detect_silence(file_list, out_file):
    silence_info = {}
    
    for file in file_list:
        intervals_temp = []
        audio = AudioSegment.from_wav(file)

        # 오디오 크기 조정, 
        change_in_dBFS = -20.0 - audio.dBFS
        audio_file = audio.apply_gain(change_in_dBFS)

        # 침묵 감지
        intervals = detect_nonsilent(audio_file,
                                      min_silence_len=MIN_SILENCE_LENGTH,
                                      silence_thresh=SILENCE_THRESHOLD)

        # 결과 처리
        non_silence_start = 0
        before_silence_start = 0

        #interval[0] = 시작시간, interval[1] 종료시간
        for interval in intervals:
            silence_duration = (interval[1] - interval[0]) / 1000  # 침묵의 길이를 초 단위로 계산
            if silence_duration >= 2.0:  # 4초 이상의 침묵인 경우에만 추가
                if (interval[0] - before_silence_start) >= 2000:
                    intervals_temp.append({'start': non_silence_start / 1000,
                                           'end': (before_silence_start + 200) / 1000,
                                           'tag': '비침묵'})
                non_silence_start = interval[0] - 200
                intervals_temp.append({'start': before_silence_start / 1000,
                                       'end': interval[0] / 1000,
                                       'tag': '침묵'})
                before_silence_start = interval[1]

        if non_silence_start != len(audio_file):
            intervals_temp.append({'start': non_silence_start / 1000,
                                   'end': len(audio_file) / 1000,
                                   'tag': '비침묵'})
                    # Add the start and end times of silence to the dictionary
        silence_info[file] = intervals_temp

    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(silence_info, f, ensure_ascii=False, indent=4)


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    args = arg_parse()

    with open(args.audiolist, 'r') as f:
        file_list = [line.strip() for line in f.readlines()]
    file_paths_list, file_names_list, file_extensions_list = file_paths(file_list)
    process(file_paths_list, file_names_list, file_extensions_list)

    detect_silence([f'{file_paths_list[i]}/{file_names_list[i]}.wav' for i in range(len(file_paths_list))], args.outfile)

if __name__ == "__main__":
    main()
