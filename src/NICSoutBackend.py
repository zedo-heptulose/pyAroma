import readFile
import sys

# Save tensors into 11 lists, with different compounents
def save_tensor(file_name, bq_numbers, icss_flag):
	with open(file_name, 'r') as usr_output_file:
		usr_output = usr_output_file.readlines()

	iso_ten = []
	ani_ten = []
	xx_ten = []
	yx_ten = []
	zx_ten = []
	xy_ten = []
	yy_ten = []
	zy_ten = []
	xz_ten = []
	yz_ten = []
	zz_ten = []

	bq_start_flag = 0
	for line_no in range(len(usr_output)):
		if 'Bq   Isotropic =' in usr_output[line_no] and 'Anisotropy =' in usr_output[line_no]:
			bq_start_flag = line_no
			break

	for bq_i in range(bq_numbers):
		iso_ten.append(icss_flag * float(usr_output[bq_start_flag + bq_i * 5].split()[4]))
		ani_ten.append(icss_flag * float(usr_output[bq_start_flag + bq_i * 5].split()[7]))
		xx_ten.append(icss_flag * float(usr_output[bq_start_flag + bq_i * 5 + 1].split()[1]))
		yx_ten.append(icss_flag * float(usr_output[bq_start_flag + bq_i * 5 + 1].split()[3]))
		zx_ten.append(icss_flag * float(usr_output[bq_start_flag + bq_i * 5 + 1].split()[5]))
		xy_ten.append(icss_flag * float(usr_output[bq_start_flag + bq_i * 5 + 2].split()[1]))
		yy_ten.append(icss_flag * float(usr_output[bq_start_flag + bq_i * 5 + 2].split()[3]))
		zy_ten.append(icss_flag * float(usr_output[bq_start_flag + bq_i * 5 + 2].split()[5]))
		xz_ten.append(icss_flag * float(usr_output[bq_start_flag + bq_i * 5 + 3].split()[1]))
		yz_ten.append(icss_flag * float(usr_output[bq_start_flag + bq_i * 5 + 3].split()[3]))
		zz_ten.append(icss_flag * float(usr_output[bq_start_flag + bq_i * 5 + 3].split()[5]))

	return iso_ten, ani_ten, xx_ten, yx_ten, zx_ten, xy_ten, yy_ten, zy_ten, xz_ten, yz_ten, zz_ten
