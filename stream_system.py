#!/usr/bin/env python
# encoding: utf-8

import numpy as np
import subprocess
import atexit
import socket

host = '127.0.0.1'
port = 55580
buff = 1024

# openSMILE で特徴量を抽出するクラス
class SMILE():
    def __init__(self,cmd):
        self._is_running = True
        self.proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


    def get_lines(self):
        while self._is_running:
            line = self.proc.stdout.readline()
            if line:
                yield line

# 正規化するクラス
class Data_manager():
    def __init__(self):
        self.mean_list = []
        self.norm_list = np.zeros(105)
        self.norm_flag = True
        self.norm_count = 0

    def get_norm_list(self,X):
        if self.norm_flag:
            self.norm_count += 1
            self.mean_list = X
            self.norm_list = self.mean_list
            self.norm_flag = False

        elif X[0] > 0.0:
            self.norm_count += 1
            self.mean_list = (X + ((self.norm_count - 1) * self.mean_list))/self.norm_count
            self.norm_list = X - self.mean_list

        if self.norm_count > 10000:
            self.norm_list = X
            self.norm_count = 0

        return self.norm_list

    def normalize_plot_log(self,norm_list,X):
        with open("mean_data_write.csv","a") as f:
            f.write("{},{}".format(self.norm_list[0],X[0]))
            f.write("\n")

# 識別するクラス
class Recognition_unit():
    def __init__(self):
        self.speek_flag = True #
        self.plot_flag = True#False
        self.y = None

    def run(self):
        print("start openSMILE")
        while True:
            smile = SMILE(cmd='./opensmile-2.3.0/SMILExtract -C opensmile-2.3.0/emobase2010_stream.conf')
            for line in smile.get_lines():
                s.send(line)
                print(len(line.split(',')))

def make_connection(host_, port_):
    """
    serverと通信をconnectする関数
    host, portを指定
    """
    try:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      sock.connect((host_, port_))
      print('connected')
      return sock
    except socket.error as e:
      print('failed to connect, try reconnect')


if __name__ == '__main__':
    s = make_connection(host, port)
    #data_manager = Data_manager()
    recognition = Recognition_unit()
    recognition.run()
