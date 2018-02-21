import time
from scipy import fftpack
import matplotlib.pyplot as plt

directory = "Data" 
sensor = "accelerometer"
activity = "driving"
position = "carsidepocket"
phone_owner = "SAURABH"
file_format = ".txt"

INPUT_FILE_PATH = directory + "/" + sensor + "_" + activity + "_" + position + "_" + phone_owner + file_format

SKIP_LINE1 = "accelerometer.txt"
SKIP_LINE2 = "All values are in SI units (m/s^2)."
SKIP_LINE3 = "http://developer.android.com/guide/topics/sensors/sensors_overview.html"
SKIP_LINE4 = "elapsed-time-system elapsed-time-sensor x y z"

SKIP_LINE_ARRAY = [SKIP_LINE1,SKIP_LINE2,SKIP_LINE3,SKIP_LINE4]
# def fft(self,x,t):
# 		f = 50
# 		f_s = 50
# 		fig, ax = plt.subplots()
# 		ax.plot(t, x)
# 		ax.set_xlabel('Time [s]')
# 		ax.set_ylabel('Signal amplitude');
# 		X = fftpack.fft(x)
# 		freqs = fftpack.fftfreq(len(x)) * f_s
# 		fig, ax = plt.subplots()
# 		ax.stem(freqs, np.abs(X))
# 		ax.set_xlabel('Frequency in Hertz [Hz]')
# 		ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
# 		ax.set_xlim(-f_s / 2, f_s / 2)
# 		ax.set_ylim(-5, 110)

class Chart(object):

    def __init__(self):
        self.senses = 0
        self.sb, self.xbuf, self.ybuf, self.zbuf = 0, 0, 0, 0
        plt.ion()
        self.fig = plt.figure(1, figsize=(19, 6))
        plt.ylim([-20, 20])
        plt.xlim([0, 300])

    def plot(self, x, y, z,t):
        # self.senses += 1
        plt.plot(x,t, color='r', label='X')
        plt.plot(y,t, color='r', label='Y')
        plt.plot(z,t, color='r', label='Z')
        # plt.plot([self.sb, self.senses], [self.xbuf, x], color='r', label='X')
        # plt.plot([self.sb, self.senses], [self.ybuf, y], color='g', label='Y')
        # plt.plot([self.sb, self.senses], [self.zbuf, z], color='b', label='Z')
        self.fig.canvas.draw()
        # self.sb, self.xbuf, self.ybuf, self.zbuf = self.senses, x, y, z

if __name__ == "__main__":
    chart = Chart()
        
    with open(INPUT_FILE_PATH,"r") as input_file:
        for line in input_file:
            
            line = line.strip()

            #check if line is None or not
            if line:
                
                # skip lines that you're not interested in
                if line in SKIP_LINE_ARRAY:
                    # print "SKIPPING"
                    pass
                
                else:
                    line_list = line.split(" ")

                    x = float(line_list[2])
                    y = float(line_list[3])
                    z = float(line_list[4])
                    t = float(line_list[1])

                    chart.plot(x, y, z,t)
                    # chart.fft(x,t)