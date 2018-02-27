import numpy as np

BATCH_TIME_PERIOD_IN_SECONDS = 6.0
SKIP_LINE_LIST = ["accelerometer.txt","All values are in SI units (m/s^2).","http://developer.android.com/guide/topics/sensors/sensors_overview.html","elapsed-time-system elapsed-time-sensor x y z"]
FROM_SECOND = 20.0
TO_SECOND = 380.0

# variables to build INPUT_FILE_PATH
sensor = "accelerometer"
activity = "driving"    # examples: "walking", "driving"
position = "carsidepocket"    # example values include "stacked", "sidebyside", "carsidepocket"
phone_owner = "SAURABH"  # example values include "NITISH", "SAURABH"
file_format = ".txt"

INPUT_FILE_SAURABH = "Data/" + sensor + "_" + activity + "_" + position + "_" + "SAURABH" + file_format
INPUT_FILE_NITISH = "Data/" + sensor + "_" + activity + "_" + position + "_" + "NITISH"  + file_format

def parse_file_and_compute_integrals(file_path):
	"""
	Calculates the integrals (z^2 * t) for every batch and returns a list
	"""
	with open(file_path,"r") as input_file:

		# intialize batch counter and "current" lists
		batch_counter = 1
		z_current = []  # z_current is the set of z^2 values that constitute a single batch
		t_current = []  # t_current is the set of t values that constitute a single batch
		integral_list = []

		# iterate through file
		for line in input_file:
			
			line = line.strip()
			#print (line)
			if line:

				if line in SKIP_LINE_LIST:
					print ("SKIPPING")
				
				else:

					if line and line not in SKIP_LINE_LIST:
							# extract t,x,y,z from the line

						line_list = line.split(" ")
						t = float(line_list[1])
						x = float(line_list[2])
						y = float(line_list[3])
						z = float(line_list[4])

						if t>FROM_SECOND:
							z_current.append(z*z)
							t_current.append(t)

						if t>(FROM_SECOND + batch_counter*BATCH_TIME_PERIOD_IN_SECONDS):
							integral_value = np.trapz(z_current,t_current,axis=-1)
							integral_list.append(integral_value)
							batch_counter = batch_counter + 1
							z_current = []
							t_current = []

						if t>TO_SECOND:
							break

		integral_value = np.trapz(z_current,t_current,axis=-1)
		integral_list.append(integral_value)

		return integral_list


		z = t_to_z_dict[time]

		multiplier = multiplier + 1

		z_list = []
		t_list = []
		print ("Multiplier is: " + str(multiplier))
		while (time < multiplier*BATCH_TIME_PERIOD_IN_SECONDS):

			z_list.append(z)
			t_list.append(time)

		integral_value = np.trapz(z_list,time_list, axis = -1)

		print ("Integral value is: " + (integral_value))
		d = raw_input("Press any key")

if __name__ == '__main__':

	#Try to find the threshold
	print (parse_file_and_compute_integrals(INPUT_FILE_SAURABH))
	print (parse_file_and_compute_integrals(INPUT_FILE_NITISH))




