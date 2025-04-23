import CONSTANT

def read_out(file_name):
    '''
    used for reading ORCA output file geometries
    '''
# Open .out file
	with open(file_name, 'r') as out_f:
		out_file = out_f.readlines()

# Find geometry section in files
	geom_start_line = 0
	geom_end_line = 0
	for out_line_no in range(len(out_file)):
		if 'CARTESIAN COORDINATES (ANGSTROEM)' in out_file[out_line_no]:
			geom_start_line = out_line_no + 2
            
	for out_line_no_3 in range(geom_start_line, len(out_file)):
		if '------' in out_file[out_line_no_3]:
			geom_end_line = out_line_no_3 - 1
			break

    # Save coordinates into 'atom_list' (including dummy atoms) and 'geom_list' (without dummy atoms)
	atom_list = []
	geom_list = []
	for geom_line in range(geom_start_line, geom_end_line + 1):
		coor_list = []
		coor_list.append(CONSTANT.period_table[int(out_file[geom_line].strip().split()[1])].title())
		coor_list.append(float(out_file[geom_line].strip().split()[3]))
		coor_list.append(float(out_file[geom_line].strip().split()[4]))
		coor_list.append(float(out_file[geom_line].strip().split()[5]))
		atom_list.append(coor_list)
		if coor_list[0].upper() != 'XX':
			geom_list.append(coor_list)

	return atom_list, geom_list

# Save tensors into 11 lists, with different compounents
def orca_save_tensor(file_name, bq_numbers, icss_flag):
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

    #okay, I see what they're doing here.
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