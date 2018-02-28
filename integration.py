import numpy as np

BATCH_TIME_PERIOD_IN_SECONDS = 60.0
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

def compare_fingerprints(fp1, fp2):
	'''
	Takes two 128-bit fingerprints and compares their hamming distance.

	Returns percentage_similarity = (1 - hamming distance/128) * 100
	'''
	assert len(fp1) == len(fp2)
	count,z = 0,int(fp1,2)^int(fp2,2)
	while z:
		count += 1
		z &= z-1 # magic!
	
	percentage_similarity = (1 - float(count)/float(len(fp1))) * 100   # 'count' is the hamming distance value

	return percentage_similarity



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


if __name__ == '__main__':

	print parse_file_and_compute_integrals(INPUT_FILE_SAURABH)
	print parse_file_and_compute_integrals(INPUT_FILE_NITISH)




