import numpy as np
import matplotlib.pyplot as plt
import statistics

BATCH_TIME_PERIOD_IN_SECONDS = 1.0
# SKIP_LINE_LIST = ["linear-acceleration.txt","All values are in SI units (m/s^2).","http://developer.android.com/guide/topics/sensors/sensors_overview.html","elapsed-time-system elapsed-time-sensor x y z"]
SKIP_LINE_LIST = ["accelerometer.txt","All values are in SI units (m/s^2).","http://developer.android.com/guide/topics/sensors/sensors_overview.html","elapsed-time-system elapsed-time-sensor x y z"]
FROM_SECOND = 10.0
TO_SECOND = 200.0
VERBOSE = True
# INPUT_FILE_SAURABH = "Data/linear-acceleration_81_Trial2_SAURABH.txt"
# INPUT_FILE_NITISH = "Data/linear-acceleration_Trial2_81_NITISH.txt"
# INPUT_FILE_MALICIOUS = "Data/linear-acceleration_81c_Trial1_SAURABH.txt"
INPUT_FILE_SAURABH = "Data/accelerometer_81_Trial2_SAURABH.txt"
INPUT_FILE_NITISH = "Data/accelerometer_Trial2_81_NITISH.txt"
INPUT_FILE_MALICIOUS = "Data/accelerometer_driving_inbus_NITISH.txt"

def median(list1):
	med = 0
	med = statistics.median(list1)
	return med

def graph_plot(threshold_list, fp_simlist1):
	'''
	Plot graph between Fingerprint Similarity vs Threshold values
	'''
	plt.bar(threshold_list,fp_simlist1)
	plt.xlabel('Threshold Values')
	plt.ylabel('Fingerprint Similarity')
	plt.title('Fingerprint Similarity vs. Threshold')
	#plt.axis([(min(threshold_list), max(threshold_list), min(fp_simlist1), max(fp_simlist1)])
	#plt.axis()
	plt.show()
	# plt.figure(2)

def compare_fingerprints(fp1, fp2):
	'''
	Takes two 128-bit fingerprints and compares their hamming distance.
	Returns percentage_similarity = (1 - hamming distance/128) * 100
	'''
	#assert len(fp1) == len(fp2)
	count,z = 0,int(fp1,2)^int(fp2,2)
	while z:
		count += 1
		z &= z-1 
	percentage_similarity = (1 - float(count)/float(len(fp1))) * 100   # 'count' is the hamming distance value

	return percentage_similarity

def threshold_estimation(integral_list_1, integral_list_2, median):
	max_element = max(max(integral_list_1),max(integral_list_2))

	threshold_list = []
	fp_simlist = []

	#for threshold in range(50,int(max_element)):
	for threshold in range((median-10),(median+10)):
		fp1 = ''
		fp2 = ''

		threshold_list.append(threshold)

		for integral_value_1 in integral_list_1:
			if integral_value_1 > float(threshold):
				fp1 = fp1 + '1'
			elif integral_value_1 < float(threshold):
				fp1 = fp1 + '0'

		for integral_value_2 in integral_list_2:
			if integral_value_2 > float(threshold):
				fp2 = fp2 + '1'
			elif integral_value_2 < float(threshold):
				fp2 = fp2 + '0'

		fp_similarity = compare_fingerprints(fp1,fp2)
		fp_simlist.append(fp_similarity)

		if VERBOSE:
			print("\nThreshold is: " + str(float(threshold)))
			print("Fingerprint 1 is: " + fp1)
			print("Fingerprint 2 is: " + fp2)
			print("SIMILARITY: " + str(fp_similarity) + "%")
			#d = raw_input("Press any key")

	return threshold_list, fp_simlist

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

		total_samples = 0

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
						total_samples = total_samples + 1
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

	med = 0 
	integral_list_saurabh = parse_file_and_compute_integrals(INPUT_FILE_SAURABH)
	integral_list_nitish = parse_file_and_compute_integrals(INPUT_FILE_NITISH)
	integral_list_malicious = parse_file_and_compute_integrals(INPUT_FILE_MALICIOUS)

	normalized_saurabh_list = integral_list_saurabh[:128]
	normalized_nitish_list = integral_list_nitish[:128]
	normalized_malicious_list = integral_list_malicious[:128]
	med  = median(normalized_saurabh_list)
	if VERBOSE:
		#print(np.median(normalized_saurabh_list))
		print(normalized_saurabh_list)
		print(normalized_nitish_list)
		print(normalized_malicious_list)
		print ("Median****************************************************", median(normalized_saurabh_list))
		#d = raw_input("\nPress any key\n")
	
	threshold_list, fp_simlist_legit = threshold_estimation(normalized_nitish_list,normalized_saurabh_list,int(med))
	threshold_list, fp_simlist_mal = threshold_estimation(normalized_malicious_list,normalized_saurabh_list, int(med))

	#threshold_list, fp_simlist_legit = threshold_estimation(integral_list_nitish,integral_list_saurabh)
	#threshold_list, fp_simlist_mal = threshold_estimation(integral_list_malicious,integral_list_saurabh)

	# COMMENT OR UNCOMMENT ONE OF THE LINES BELOW TO SWITCH BETWEEN THE LEGIT AND MALIICIOUS SCENARIOS
	graph_plot(threshold_list,fp_simlist_legit)
	# plt.figure(1)
	graph_plot(threshold_list,fp_simlist_mal)




