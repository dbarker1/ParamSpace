import subprocess as sp
import os

USER = "djb236"

if (USER == "da330"):
	RES_PATH = "/home/" + USER + "/Dedalus/figs_rot_new_code"
elif (USER == "nbh202"):
	RES_PATH = "/home/" + USER + "/dedalus/all/figs_rot_new_code"
elif (USER == "djb236"):
	RES_PATH = "/home/" + USER + "/TESTS"

def get_no(param, str):
	rows = str.split("\n")
	for i in range(len(rows)):
		if (rows[i] == param):
			return float(rows[i+1])

def get_results(file_p):
	raw = file_p.read()
	print(raw)
	file_p.close()
	return get_no("E_def", raw), get_no("Np", raw)

def find_extras(row):
	if (len(row.split(",")) != 5):
		print(row + ": invalid row")
		exit(1)
	Np, Ra, Ta, Phi, temp = row.split(",")
	E_def, Np = get_results(open(RES_PATH+ "/Np=" + str(int(Np)) + "/Ra=" + str(int(float(Ra))) + "/Ta=" + str(int(float(Ta))) + "/Phi=" + str(int(Phi)) + "/results.txt", "r"))
	return E_def + "," + Np

def dir2num(str, param):
	return str.split(param + "=")[1]

done = []
Nps, Ras, Tas, Phis = [], [], [], []

Np_dirs = os.listdir(RES_PATH)

found = 0
for Np_dir in Np_dirs:
	Ra_dirs = os.listdir(RES_PATH + "/" + Np_dir)
	for Ra_dir in Ra_dirs:
		Ta_dirs = os.listdir(RES_PATH + "/" + Np_dir + "/" + Ra_dir)
		for Ta_dir in Ta_dirs:
			Phi_dirs = os.listdir(RES_PATH + "/" + Np_dir + "/" + Ra_dir + "/" + Ta_dir)
			for Phi_dir in Phi_dirs:
				done.append(dir2num(Np_dir, "Np") + "," + dir2num(Ra_dir, "Ra") + "," + dir2num(Ta_dir, "Ta") + "," + dir2num(Phi_dir, "Phi"))
				found += 1


if (found == 0):
	print("No folders found")
	exit(1)

print(done)

poss_str = ""
poss_raw = open("parametergrid.csv", "r")
rows = poss_raw.read().split("\n")
poss_raw.close()

csv_dat = []
i = 0
for row in rows:
	if (i != 0):
		format_row = ""
		for num in row.split(","):
			if (num != ""):
				format_row += str(float(num)) + ","
		csv_dat.append(format_row)
	i += 1

curr_ss_op = open("spreadsheet.dat", "r")
curr_ss = curr_ss_op.read().split("\n")
curr_ss_op.close()

new_ss = ""
for row in curr_ss:
	if (row.split(",")[len(row.split(",")) - 1] == ""):
		new_ss += find_extras(row)
	else:
		new_ss += row

print(new_ss)

ss_op = open("spreadsheet.dat", "w")
ss_op.write(new_ss)
ss_op.close()
