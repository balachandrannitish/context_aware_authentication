import numpy

BATCH_TIME_PERIOD_IN_SECONDS = 60.0

# variables to build INPUT_FILE_PATH
sensor = "accelerometer"
activity = "driving"    # examples: "walking", "driving"
position = "carsidepocket"    # example values include "stacked", "sidebyside", "carsidepocket"
phone_owner = "SAURABH"  # example values include "NITISH", "SAURABH"
file_format = ".txt"

INPUT_FILE_PATH = "Data/" + sensor + "_" + activity + "_" + position + "_" + phone_owner + file_format

SKIP_LINE1 = "accelerometer.txt"
SKIP_LINE2 = "All values are in SI units (m/s^2)."
SKIP_LINE3 = "http://developer.android.com/guide/topics/sensors/sensors_overview.html"
SKIP_LINE4 = "elapsed-time-system elapsed-time-sensor x y z"
SKIP_LINE_ARRAY = [SKIP_LINE1,SKIP_LINE2,SKIP_LINE3,SKIP_LINE4]

def parse_file():

	t_to_z = {}

	with open(INPUT_FILE_PATH,"r") as input_file:

		for line in input_file:
			line = line.strip()
			print line
			if line:

				if line in SKIP_LINE_ARRAY:
					print "SKIPPING"
				
				else:
					line_list = line.split(" ")

					sensor_time = float(line_list[1])
					x = float(line_list[2])
					y = float(line_list[3])
					z = float(line_list[4])

					t_to_z[sensor_time] = z

	return t_to_z


if __name__ == '__main__':
	
	t_to_z_dict = parse_file()

	#z_batch_array = []
	#t_batch_array = []

	z_list = []
	t_list = []

	multiplier = 0

	for time in t_to_z_dict.keys():

		z = t_to_z_dict[time]

		multiplier = multiplier + 1

		z_list = []
		t_list = []

		while time < multiplier*BATCH_TIME_PERIOD_IN_SECONDS:

			z_list.append(z)
			t_list.append(time)

			print "Multiplier is: " + str(multiplier)
			integral_value = np.trapz(z,time,axis=-1)

			print "Integral value is: " + str(integral_value)
			d = raw_input("Press any key")





