import time
import matplotlib.pyplot as plt

sensor = "accelerometer"
activity = "driving"
position = "carsidepocket"
phone_owner = "SAURABH"
file_format = ".txt"

INPUT_FILE_PATH = sensor + "_" + activity + "_" + position + "_" + phone_owner + file_format

SKIP_LINE1 = "accelerometer.txt"
SKIP_LINE2 = "All values are in SI units (m/s^2)."
SKIP_LINE3 = "http://developer.android.com/guide/topics/sensors/sensors_overview.html"
SKIP_LINE4 = "elapsed-time-system elapsed-time-sensor x y z"

SKIP_LINE_ARRAY = [SKIP_LINE1,SKIP_LINE2,SKIP_LINE3,SKIP_LINE4]

class Chart(object):

    def __init__(self):
        self.senses = 0
        self.sb, self.xbuf, self.ybuf, self.zbuf = 0, 0, 0, 0
        plt.ion()
        self.fig = plt.figure(1, figsize=(19, 6))
        plt.ylim([-20, 20])
        plt.xlim([0, 300])

    def plot(self, x, y, z):
        self.senses += 1
        plt.plot([self.sb, self.senses], [self.xbuf, x], color='r', label='X')
        plt.plot([self.sb, self.senses], [self.ybuf, y], color='g', label='Y')
        plt.plot([self.sb, self.senses], [self.zbuf, z], color='b', label='Z')
        self.fig.canvas.draw()
        self.sb, self.xbuf, self.ybuf, self.zbuf = self.senses, x, y, z

# Interval between sensing
#dt = 100

# Number of senses
#TotalToSense = 250

# Connect to android and start sensing
#android_address = ("192.168.0.1", 9999)
#droid = android.Android(android_address)
#droid.startSensingTimed(2, dt)

if __name__ == "__main__":
    chart = Chart()
        
    with open(INPUT_FILE_PATH,"r") as input_file:
        for line in input_file:
            
            line = line.strip()

            #check if line is None or not
            if line:
                
                # skip lines that you're not interested in
                if line in SKIP_LINE_ARRAY:
                    print "SKIPPING"
                
                else:
                    line_list = line.split(" ")

                    x = float(line_list[2])
                    y = float(line_list[3])
                    z = float(line_list[4])

                    chart.plot(x, y, z)