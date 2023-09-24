import argparse
import wave
import numpy as np
import json, os

def arg_parse():
    parser = argparse.ArgumentParser(description='Korean SR Contest 2023')
    parser.add_argument('--audiolist', type=str, default='wavlist.txt')
    parser.add_argument('--outfile', type=str, default='../output/Q2.json')

    args = parser.parse_args()

    return args

'''
    - file_list : audio file list (wavlist.txt)
    - out_file : output file (Q2.json)
'''
def detect_wav_error(file_list, out_file):

    error_file_list = []

    with open(file_list, 'r') as files:
        for file in files.readlines():
            file = file.strip()
            try:
                with wave.open(file, 'rb') as wav_file:

                    data = np.frombuffer(wav_file.readframes(wav_file.getnframes()), dtype=np.int16)
                    # 헤더만 있는 경우
                    if wav_file.getnframes() == 0:
                        error_file_list.append(file)
                    # 데이터만 있는 경우
                    elif wav_file.getsampwidth() == 0:
                        error_file_list.append(file)
                    # 데이터 값이 없는 경우
                    elif np.all(data == 0):
                        error_file_list.append(file)
                    # 클리핑 에러
                    elif np.max(data) > 32767 or np.min(data) < -32768:
                        error_file_list.append(file)

            except:
                # 파일 열기 실패(헤더 결함)
                error_file_list.append(file)

    with open(out_file, 'w') as f:
        json.dump({"error_list": error_file_list}, f, indent=4)

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    args = arg_parse()
    detect_wav_error(args.audiolist, args.outfile)

if __name__ == "__main__":
    main()