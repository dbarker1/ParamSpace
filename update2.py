import os
from decimal import Decimal
import subprocess as sp

USER = "da330"

if (USER == "da330"):
        RES_PATH = "/home/" + USER + "/Dedalus/figs_rot_new_code"
elif (USER == "nbh202"):
        RES_PATH = "/home/" + USER + "/dedalus/all/figs_rot_new_code"
elif (USER == "djb236"):
        RES_PATH = "/home/" + USER + "/TESTS"

def make_folder(Np, Ra, Ta, Phi):
	return RES_PATH + "/" + Np + "/" + Ra + "/" + Ta + "/" + Phi

def find_params(str, params):
	retval = []
	rows = str.split("\n")
	for param in params:
		i = 0
		for row in rows:
			if (row == param):
				retval.append(rows[i+1])
			i += 1
	return retval

def print_list(list):
	for item in list:
		print(item.Np, item.Ra, item.Ta, item.Phi, item.E_def)

def to_2dp(n):
	num = float(n)
	retval = '%.2f' % num
	return str(retval)

def to_exp(n):
	num = float(n)
	return '%.2E' % Decimal(num)

class _param:
	def __init__(self, Np_in, Ra_in, Ta_in, Phi_in, E_def_in):
		self.Np = str(to_2dp(Np_in))
		self.Ra = str(to_exp(Ra_in))
		self.Ta = str(to_exp(Ta_in))
		self.Phi = str(Phi_in)
		self.E_def = str(E_def_in)

found = 0
folders = []

Np_dirs = os.listdir(RES_PATH)
for Np_dir in Np_dirs:
	Ra_dirs = os.listdir(RES_PATH + "/" + Np_dir)
	for Ra_dir in Ra_dirs:
		Ta_dirs = os.listdir(RES_PATH + "/" + Np_dir + "/" + Ra_dir)
		for Ta_dir in Ta_dirs:
			Phi_dirs = os.listdir(RES_PATH + "/" + Np_dir + "/" + Ra_dir + "/" + Ta_dir)
			for Phi_dir in Phi_dirs:
				folders.append(make_folder(Np_dir, Ra_dir, Ta_dir, Phi_dir))
				found += 1

if (found == 0):
	print("No folders found")
	exit(1)
else:
	print(str(found) + " folders found")

done = []

for folder in folders:
	f_op = open(folder + "/results.txt", "r")
	f_op_txt = f_op.read()
	Np, Ra, Ta, Phi, Edef = find_params(f_op_txt, ["Np", "Ra", "Ta", "Phi", "E_def"])
	done.append(_param(Np, Ra, Ta, Phi, Edef))
	f_op.close()

poss_op = open("parametergrid.csv", "r")
poss_txt = poss_op.read()
poss_op.close()

poss = []
i = 0
for row in poss_txt.split("\n"):
	if (i != 0):
		raw_param = row.split(",")
		poss.append(_param(raw_param[0], raw_param[1], raw_param[2], raw_param[3], 0))
	i += 1

ss_r = open("spreadsheet.dat", "r")
ss_r_txt = ss_r.read()
ss_r.close()
i = 0
leave_no = []
leave_line = []
for line in ss_r_txt.split("\n"):
	if (len(line.split(",")) > 5):
		leave_no.append(i)
		leave_line.append(line)
		print(i, line)
	i += 1

ss_op = open("spreadsheet.dat", "w")

i = 0
leave = 0
for possible in poss:
	poss_path = make_folder(possible.Np, possible.Ra, possible.Ta, possible.Phi)

	if i in leave_no:
		print(i)
		ss_op.write(leave_line[leave] + "\n")
		leave += 1
		continue

	found = 1

	for complete in done:
		comp_path = make_folder(complete.Np, complete.Ra, complete.Ta, complete.Phi)
		if (comp_path == poss_path):
			to_write = complete.Np + "," + complete.Ra + "," + complete.Ta + "," + complete.Phi + "," + complete.E_def + "," + USER + "\n"
			found = 0
			break

	if (found == 1):
		to_write = possible.Np + "," + possible.Ra + "," + possible.Ta + "," + possible.Phi + "," + possible.E_def + "\n"

	ss_op.write(to_write)

	i += 1

ss_op.close()
