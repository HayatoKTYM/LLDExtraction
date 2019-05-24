#!/usr/bin/python
# coding: utf-8
import keras
model = keras.models.load_model('./utterance_lld_final10.h5')
import numpy as np
import socket
import time
import matplotlib.pyplot as plt
host = '127.0.0.1'
port = 55580
buff = 2048

##動的に表示するグラフの初期化
feature = [[0]*114]
fig, ax = plt.subplots(1, 1,figsize=(3,2))
x = list(range(1,11))
y = list(0 for i in range(10))
cnt = len(x)+1
ax.set_ylim(-0.2, 1.1)
# 初期化的に一度plotしなければならない
# そのときplotしたオブジェクトを受け取る受け取る必要がある．
# listが返ってくるので，注意
lines, = ax.plot(x, y, color='c')

if __name__ == '__main__':

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind((host, port))

  while True:
    s.listen(1)
    print('Waiting for connection')
    cl, addr = s.accept()
    print('Established connection')

    while True:
        msg = cl.recv(buff)
        #cl.send('c')  # check if connection is alive
        smile_list = msg.rstrip().split(",")
        if len(smile_list) == 114:
            try:
                X = map(float,smile_list) #python2
            except:#index[0]にバグが発生
                smile_list[0] = "0.0"
                X = map(float,smile_list) #python2
            X = np.array(X).astype(np.float32)
            feature.append(X)

        if len(feature) >= 10:
            X = np.array(feature[0:10])
            del feature[0:10]
            y_pred = model.predict(X.reshape(-1,10,114))
            print(y_pred)
            x.append(cnt)
            y.append(y_pred[0])
            del x[0]; del y[0]
            lines.set_data(x, y)
            ax.set_xlim((min(x), max(x)))
            cnt+=1
            plt.savefig('result/vad_'+str(cnt)+'.png')
            plt.pause(.01)
