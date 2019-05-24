import threading
import subprocess
import numpy as np
#from make_wav import *

class SMILE(threading.Thread):
    def __init__(self,cmd):
        super(SMILE, self).__init__()
        self.mutex = threading.Lock()
        self._is_running = True
        import subprocess
        self.proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE ,stdout=subprocess.PIPE)
        self.lines = []
        self.write_header()
        self.write_first_wav()
        print("###recoeding start###")
        self.start()

    def dummy_wav(self):
        self.proc.stdin.write(b'\x00\x00' * int(16000 * 0.1))
        self.proc.stdin.flush()

    def write_first_wav(self):
        self.proc.stdin.write(b'\x00\x00' * int(16000 * 0.05))
        self.proc.stdin.flush()

    def write_header(self):
        header = b'RIFF\xff\xff\xff\xffWAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80>\x00\x00\x00}\x00\x00\x02\x00\x10\x00data\xff\xff\xff\xff\x00\x00\x00\x00'
        self.proc.stdin.write(header)
        self.proc.stdin.flush()

    def write_wav_data(self, wav): #### 1 #wav = ""
        self.proc.stdin.write(wav)
        self.proc.stdin.flush()
        #print(1)


    def run(self):
        while self._is_running:
            line = self.proc.stdout.readline()
            if line == '':
                return
            self.mutex.acquire()
            self.lines.append(line)
            self.mutex.release()

    def terminate(self):
        self.dummy_wav()
        self.proc.stdin.close()
        time.sleep(0.2)
        self.join()
        print(2)
        self.proc.terminate()

    def get_lines(self):
        flag = 1 ##
        self.mutex.acquire()
        r = self.lines
        self.lines = []
        self.mutex.release()
        if r == []:
            flag = 0
        else:
            #print(r)
            #print(type(r[0]))
            r = [x.decode('utf-8').rstrip().split(',') for x in r]
            r = [float(xx) for x in r for xx in x]

        return flag,r


if __name__ == "__main__":

    cmd = "./SMILExtract -C config/demo/demo1_energy.conf -I /dev/stdin -O /dev/stdout"
    smile = SMILE(cmd = cmd)
    while 1:
        print(smile.get_lines()[1])
