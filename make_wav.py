#! /usr/bin/python
# -*- coding:utf-8 -*-
from lld_demo import SMILE
"""
pyaudioを用いて標準入力からLLD特徴量を抽出する

"""
import wave     #wavファイルを扱うためのライブラリ
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import keras
model = keras.models.load_model('utterance_lld_final10.h5')

def MakeWavFile(RATE = 16000,
               chunk = 1024,
               CHANNELS = 1,
               FileName = "record.wav",
               Record_Seconds = 2):

    cmd = "./opensmile-2.3.0/SMILExtract -C opensmile-2.3.0/emobase2010_csv_lld.conf -I /dev/stdin -O /dev/stdout"
    smile = SMILE(cmd = cmd)
    """
    標準入力をwavに書き出す関数
    """
    FORMAT = pyaudio.paInt16

    p = pyaudio.PyAudio()

    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = chunk)

    #レコード開始
    print("Now Recording...")
    all = []
    for i in range(0, int(RATE / chunk * Record_Seconds)):

        data = stream.read(chunk) #音声を読み取って、 ######ここをSmile instanceに渡す
        all.append(data) #データを追加
        smile.write_wav_data(wav = data)
        flag, feature = smile.get_lines()
        if not flag:
            continue
        try:
            feature = np.reshape(feature,(-1,114))
            if len(feature) > 10:
                X = feature[:len(feature) // 10 * 10]
                y_pred = model.predict(X.reshape(-1,10,114)).reshape(-1)
                for j in range(len(y_pred)):
                    print((int(y_pred[j]*10) + 2) * "*")

        except Exception as e:
            print(e)

    #レコード終了
    print("Finished Recording.")
    f.close()
    stream.close()
    p.terminate()
    wavFile = wave.open(FileName, 'wb')
    wavFile.setnchannels(CHANNELS)
    wavFile.setsampwidth(p.get_sample_size(FORMAT))
    wavFile.setframerate(RATE)
    #wavFile.writeframes(b''.join(all)) #Python2 用
    wavFile.writeframes(b"".join(all)) #Python3用

    wavFile.close()

if __name__ == "__main__":
    #WAVファイル作成, 引数は（ファイル名, 録音する秒数）
    MakeWavFile(FileName = "record.wav", Record_Seconds = 20, chunk = 1024)
