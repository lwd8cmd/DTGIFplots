import datetime
import numpy as np
import matplotlib.pyplot as plt
from dateutil import parser
import matplotlib
from matplotlib.dates import DateFormatter
from os import walk
import re

scan = 2

timestamps = []
currents = []
voltages = []
wire_strs = ["wire0", "wire1", "strip", "cathode"]
superlayer_strs = ['phi1', 'theta', 'phi2']

path = "txt/{}/".format(scan)
_, _, files = walk(path).next()
for file in files:
	m = re.search("^(.+?)\.txt$", file)
	if not m:# filename is not in the correct form: eg a.txt
		continue
	
	# load data from file
	with open(path + file) as fp:
		for line_nr, line in enumerate(fp):
			if line_nr == 0:
				continue
			else:
				data = line.split()
				timestamps.append(parser.parse(data[0]+' '+data[1]))
				currents.append([float(i) for i in data[2::2]])
				voltages.append([float(i) for i in data[3::2]])

# use numpy arrays (easier to manipulate)
currents = np.array(currents)
voltages = np.array(voltages)
timestamps = np.array(timestamps)

if len(currents) == 0:
	print("Input file not found in dir {}. Check scan nr in line 10".format(path))
	exit()

if scan == 1:
	def getAttenuation(time):# map time to attenuation
		if time > parser.parse("2015-08-13 20:35:00") \
			and time < parser.parse("2015-08-13 20:37:59"):
			return 46420
		if time > parser.parse("2015-08-13 20:39:00") \
			and time < parser.parse("2015-08-13 20:41:59"):
			return 4642
		if time > parser.parse("2015-08-13 20:43:00") \
			and time < parser.parse("2015-08-13 20:46:59"):
			return 464
		if time > parser.parse("2015-08-13 20:48:30") \
			and time < parser.parse("2015-08-13 20:51:59"):
			return 100
		if time > parser.parse("2015-08-13 20:53:00") \
			and time < parser.parse("2015-08-13 20:56:30"):
			return 100
		if time > parser.parse("2015-08-13 20:57:00") \
			and time < parser.parse("2015-08-13 21:00:30"):
			return 10
		if time > parser.parse("2015-08-13 21:00:00") \
			and time < parser.parse("2015-08-13 21:02:59"):
			return 0# close upstream?
		if time > parser.parse("2015-08-13 21:06:00") \
			and time < parser.parse("2015-08-13 21:08:59"):
			return 0# open upstream?
		if time > parser.parse("2015-08-13 21:13:30") \
			and time < parser.parse("2015-08-13 21:13:59"):
			return 4.6
		if time > parser.parse("2015-08-13 21:16:30") \
			and time < parser.parse("2015-08-13 21:16:59"):
			return 2.2
		if time > parser.parse("2015-08-13 21:22:00") \
			and time < parser.parse("2015-08-13 21:23:30"):
			return 1.5
		if time > parser.parse("2015-08-13 21:25:30") \
			and time < parser.parse("2015-08-13 21:31:30"):
			return 1
		return 0
elif scan == 2:
	def getAttenuation(time):# map time to attenuation
		if time > parser.parse("2015-08-14 18:00:30") \
			and time < parser.parse("2015-08-14 18:03:59"):
			return 46420
		if time > parser.parse("2015-08-14 18:04:30") \
			and time < parser.parse("2015-08-14 18:06:59"):
			return 4642
		if time > parser.parse("2015-08-14 18:08:30") \
			and time < parser.parse("2015-08-14 18:11:59"):
			return 464
		if time > parser.parse("2015-08-14 18:13:00") \
			and time < parser.parse("2015-08-14 18:15:30"):
			return 100
		if time > parser.parse("2015-08-14 18:17:30") \
			and time < parser.parse("2015-08-14 18:19:59"):
			return 100
		if time > parser.parse("2015-08-14 18:20:30") \
			and time < parser.parse("2015-08-14 18:24:59"):
			return 10
		return 0
elif scan == 3:
	def getAttenuation(time):# map time to attenuation
		if time > parser.parse("2015-08-17 11:28:00") \
			and time < parser.parse("2015-08-17 11:30:59"):
			return 46
		if time > parser.parse("2015-08-17 12:59:30") \
			and time < parser.parse("2015-08-17 13:01:59"):
			return 33
		if time > parser.parse("2015-08-17 13:39:00") \
			and time < parser.parse("2015-08-17 13:40:59"):
			return 100
		return 0
	
attenuations = np.array(map(getAttenuation, timestamps))
mask = attenuations > 0

time = timestamps[np.argmax(attenuations>0)].strftime("%Y-%m-%d %H:%M")
plt.figure(figsize=(6, 6), dpi=100)

if 1:# for every superlayer, layer, wire
	limits = [10**np.floor(np.log10(attenuations[mask].min()-1e-3)), 10**np.ceil(np.log10(attenuations[mask].max()+1e-3))]
	matplotlib.rcParams.update({'font.size': 26})
	for superlayer in [1,2,3]:
		for layer in [1,2,3,4]:
			for wire in [0,1,3]:
				#if superlayer==1 and layer==1 and wire==0:
				#	continue
				
				# plot data
				ys = currents[:,(superlayer-1)*16+(layer-1)*4+wire]
				plt.plot(attenuations[mask], ys[mask], 'x', ms=15, mew=2)
				
				#labels
				plt.xscale('log')
				plt.grid()
				plt.ylabel(r'Current ($\mu A$)', fontsize=16)
				plt.xlabel('Attenuation', fontsize=16)
				#plt.title('GIF_Currents_from13-08-2015_18-59-10\nsuperlayer {sl} layer {l} {w}'.format(sl=superlayer, l=layer, w=wire_strs[wire]))
				plt.suptitle(r'{sl} {w} L{l}'.format(sl=superlayer_strs[superlayer-1], l=layer, w=wire_strs[wire]), y=1.005)
				plt.title("{}".format(time), fontsize=16)
				
				plt.xlim(limits)
				plt.ylim(ymin=0, ymax=(50 if wire==3 else 35))
				
				# plot red horizontal line
				
				plt.plot(limits, [20, 20], '-', c='r')
				
				# save plot
				plt.tight_layout()
				filename = 'plots/{s}/scan{s}SL{sl}L{l}{w}.png'.format(s=scan, sl=superlayer, l=layer, w=wire_strs[wire])
				print("Saving {}".format(filename))
				plt.savefig(filename, bbox_inches='tight')
				plt.clf()
				
if 1:# 2d plot
	# load data
	attenuation = [10, 100, 46][scan-1]
	mask = attenuations == attenuation
	values = np.zeros((3,4,4), dtype=np.float)
	for superlayer in [1,2,3]:
		for layer in [1,2,3,4]:
			for wire in [0,1,3]:
				values[superlayer-1, layer-1, wire] = (currents[:,(superlayer-1)*16+(layer-1)*4+wire][mask]).mean()
	
	matplotlib.rcParams.update({'font.size': 22})
	# plot 1: x=layer, y=layer
	for wire in [0,1,3]:
		fig, ax = plt.subplots()
		fig.set_size_inches(6.0, 6.0)
		im = ax.pcolor(values[:,:,wire], cmap='YlOrBr', edgecolor='black', linestyle='--', lw=1)
		fig.colorbar(im)
		
		ax.xaxis.set(ticks=np.arange(0.5, 4), ticklabels=['L1', 'L2', 'L3', 'L4'])
		ax.yaxis.set(ticks=np.arange(0.5, 3), ticklabels=['phi1', 'theta', 'phi2'])
				
		plt.title("\n{}".format(time), fontsize=16)
		plt.suptitle(r'{w} current ($\mu A$) attenuation={a}'.format(w=wire_strs[wire], a=attenuation))
		
		plt.tight_layout()
		filename = 'plots/{s}/scan{s}2d1{w}.png'.format(s=scan, w=wire_strs[wire])
		print("Saving {}".format(filename))
		plt.savefig(filename, bbox_inches='tight')
		plt.clf()
		
	# plot 2: y=superlayer x layer
	for wire in [0,1,3]:
		fig, ax = plt.subplots()
		fig.set_size_inches(6.0, 6.0)
		im = ax.pcolor(values[:,:,wire].reshape((-1,1))[::-1], cmap='YlOrBr', edgecolor='black')
		fig.colorbar(im)
		
		ax.xaxis.set_ticks([])
		ax.yaxis.set(ticks=np.arange(0.5, 12), ticklabels=['phi1 L1', 'L2', 'L3', 'L4', 'theta L1', 'L2', 'L3', 'L4', 'phi2 L1', 'L2', 'L3', 'L4'][::-1])
		
		plt.title("\n{}".format(time), fontsize=16)
		plt.suptitle(r'{w} current ($\mu A$) attenuation={a}'.format(w=wire_strs[wire], a=attenuation))
		
		plt.tight_layout()
		filename = 'plots/{s}/scan{s}2d2{w}.png'.format(s=scan, w=wire_strs[wire])
		print("Saving {}".format(filename))
		plt.savefig(filename, bbox_inches='tight')
		plt.clf()
		
	# plot 3: y=superlayer x layer, x=wire
	if 1:
		fig, ax = plt.subplots()
		fig.set_size_inches(6.0, 6.0)
		im = ax.pcolor(values[:,:,:2].reshape((-1,2))[::-1], cmap='YlOrBr', edgecolor='black')
		fig.colorbar(im)
		
		ax.xaxis.set(ticks=np.arange(0.5, 2), ticklabels=wire_strs[:2])
		ax.yaxis.set(ticks=np.arange(0.5, 12), ticklabels=['phi1 L1', 'L2', 'L3', 'L4', 'theta L1', 'L2', 'L3', 'L4', 'phi2 L1', 'L2', 'L3', 'L4'][::-1])
				
		plt.title("\n{}".format(time), fontsize=16)
		plt.suptitle(r'Current ($\mu A$) attenuation={a}'.format(a=attenuation))
		
		plt.tight_layout()
		filename = 'plots/{s}/scan{s}2d3.png'.format(s=scan, w=wire_strs[wire])
		print("Saving {}".format(filename))
		plt.savefig(filename, bbox_inches='tight')
		plt.clf()

if 0:# time plot
	#mask = attenuations > -1
	#plt.plot(timestamps[mask], currents.mean(1)[mask], '.')
	#plt.plot(timestamps[mask], attenuations[mask], '.')
	#plt.plot(timestamps[mask], voltages.mean(1)[mask], '.')
	ys = currents.mean(1)
	plt.plot(timestamps[1:], ys[1:]-ys[:-1])
	#plt.yscale('log')
	plt.gcf().axes[0].xaxis.set_major_formatter(DateFormatter('%H:%M'))
	plt.gcf().autofmt_xdate()
	plt.show()