import math
import matplotlib.pyplot as plt
import numpy as np
import random
import networkx as nx
import sys
import time

# class DataCenter(object):
# 	"""DataCenter"""
# 	def __init__(self, name, dbs, slots):
# 		super(DataCenter, self).__init__()
# 		self.name = name
# 		self.dbs = dbs
# 		self.slots = slots # available slots
		

# class Job(object):
# 	"""Job consisting of multi-tasks"""
# 	def __init__(self, name, tasks):
# 		super(Job, self).__init__()
# 		self.name = name
# 		self.tasks = tasks


# class Task(object):
# 	"""rtime: running time, ndata: needed data amount, dc: the data center where executing this task"""
# 	def __init__(self, name, rtime, ndata):
# 		super(Task, self).__init__()
# 		self.name = name
# 		self.rtime = rtime
# 		self.ndata = ndata
# 		self.dc = None


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
	

def Floyd(A, n):
	for k in range(n):
		for i in range(n):
			for j in range(n):
				if A[i][k] + A[k][j] < A[i][j]:
					A[i][j] = A[i][k] + A[k][j]
	return A


def GenerateDataCenter(n, njob): # n: # of data centers
	if njob > 26:
		return
    # generate a strongly connected graph
	DCBG = [[math.inf]*n for i in range(n)]
	G = nx.Graph() # plot this graph
	for i in range(n):
		G.add_node("DC" + str(i+1))
		DCBG[i][i] = 1000 # inside bandwidth 1000 MB/s

	# a connected graph for undirected graph: |E| = |V| - 1
	# sparse graph << |V|^2
	# dense graph ~= |V|^2
	E = n-1 # |V|-1
	while E > 0:
		for i in range(n):
			for j in range(n):
				if DCBG[i][j] == math.inf and random.random() < 0.2:
					DCBG[i][j] = random.randint(20, 500) # bandwidth
					DCBG[j][i] = random.randint(20, 500)
					G.add_edge("DC"+str(i+1),"DC"+str(j+1))
					E -= 1

	options = {
	    "node_color": "black",
	    "node_size": 50,
	    "linewidths": 0,
	    "width": 0.1,
	}
	nx.draw(G, **options)
	plt.show()


	# generate data center slots 1-4
	DCS = [random.randint(1,4) for i in range(n)]

	# generate DBDict
	DBDict = {}
	for i in range(njob):
		for j in range(random.randint(2,9)): # num of databases of each job 2-9
			DBDict[chr(ord('A')+i) + str(j+1)] = "DC" + str(random.randint(1,n))

	return DCBG, DCS, DBDict


def GenerateJob(n, DBDict): # n: # of jobs, maximum to 26, A-Z
	if n > 26:
		return
	JobDict = {}
	for i in range(n):
		job_name = chr(ord('A')+i)
		JobDict[job_name] = {}
		for j in range(random.randint(2,20)): # sub-tasks
			task_name = "t" + job_name + str(j+1)
			JobDict[job_name][task_name] = {"completed": None, "scheduled": False}
			JobDict[job_name][task_name]["rtime"] = random.uniform(1,10) # float number between 1-10
			JobDict[job_name][task_name]["ndata"] = []
			for DB in DBDict:
				if DB[0] == job_name and random.random() < 0.2: # add database with probability ~= 0.2
					JobDict[job_name][task_name]["ndata"].append((DB, random.randint(25, 500))) # data amount 25-500
			for k in range(j): # add precedence constraints, only point to previous tasks 0~j-1/1~j, avoid death lock
				if random.random() < 0.2:
					JobDict[job_name][task_name]["ndata"].append(("t"+job_name+str(k+1), random.randint(25, 500)))
	return JobDict


def ToyDataDataCenter():
	# Data Center Bandwidth Graph (DC1-DC13)
	DCBG = [
		[1000,80,150,math.inf,math.inf,math.inf,math.inf,math.inf,math.inf,math.inf,math.inf,500,math.inf],
		[80,1000,122,250,175,math.inf,math.inf,math.inf,math.inf,math.inf,math.inf,math.inf,math.inf],
		[100,104,1000,210,45,math.inf,math.inf,300,math.inf,math.inf,400,math.inf,math.inf],
		[math.inf,220,205,1000,20,160,math.inf,math.inf,300,math.inf,math.inf,math.inf,math.inf],
		[math.inf,169,36,15,1000,200,190,math.inf,math.inf,math.inf,math.inf,math.inf,math.inf],
		[math.inf,math.inf,math.inf,160,210,1000,math.inf,90,math.inf,math.inf,53,math.inf,500],
		[math.inf,math.inf,math.inf,math.inf,205,math.inf,1000,math.inf,math.inf,66,37,math.inf,math.inf],
		[math.inf,math.inf,300,math.inf,math.inf,78,math.inf,1000,31,87,math.inf,math.inf,math.inf],
		[math.inf,math.inf,math.inf,300,math.inf,math.inf,math.inf,26,1000,math.inf,93,500,math.inf],
		[math.inf,math.inf,math.inf,math.inf,math.inf,math.inf,54,50,math.inf,1000,math.inf,math.inf,math.inf],
		[math.inf,math.inf,400,math.inf,math.inf,42,64,math.inf,67,math.inf,1000,math.inf,math.inf],
		[500,math.inf,math.inf,math.inf,math.inf,math.inf,math.inf,math.inf,500,math.inf,math.inf,1000,500],
		[math.inf,math.inf,math.inf,math.inf,math.inf,500,math.inf,math.inf,math.inf,math.inf,math.inf,500,1000]
	]

	# Data Center Slots
	DCS = [2,1,3,2,1,4,2,1,2,1,1,4,4]

	# Data Center Databases
	# DCD = [
	# 	["A1","B1"], # DC1
	# 	["C1"],      # DC2
	# 	["B2"],      # DC3
	# 	["A2","E1"], # DC4
	# 	["D1"],      # DC5
	# 	["C2","E2"], # DC6
	# 	["D2"],      # DC7
	# 	["E3"],      # DC8
	# 	["D3","F1"], # DC9
	# 	["F3"],      # DC10
	# 	["E4"],      # DC11
	# 	["F4"],      # DC12
	# 	["F2","F5"]  # DC13
	# ]

	DBDict = {
		"A1": "DC1",
		"A2": "DC4",
		"B1": "DC1",
		"B2": "DC3",
		"C1": "DC2",
		"C2": "DC6",
		"D1": "DC5",
		"D2": "DC7",
		"D3": "DC9",
		"E1": "DC4",
		"E2": "DC6",
		"E3": "DC8",
		"E4": "DC11",
		"F1": "DC9",
		"F2": "DC13",
		"F3": "DC10",
		"F4": "DC12",
		"F5": "DC13"
	}

	return DCBG,DCS,DBDict


def ToyDataJob():
	JobDict = {
		"A":{
			"tA1":{"rtime": 2, "ndata": [("A1", 100), ("A2", 200)], "completed": None, "scheduled": False},
			"tA2":{"rtime": 2, "ndata": [("A1", 100), ("A2", 200)], "completed": None, "scheduled": False}
		},
		"B":{
			"tB1":{"rtime": 2, "ndata": [("B1", 200), ("B2", 200)], "completed": None, "scheduled": False},
			"tB2":{"rtime": 1, "ndata": [("B1", 200), ("B2", 300), ("tB1", 100)], "completed": None, "scheduled": False}
		},
		"C":{
			"tC1":{"rtime": 3, "ndata": [("C1", 50), ("C2", 50)], "completed": None, "scheduled": False},
			"tC2":{"rtime": 1, "ndata": [("C2", 70), ("tC1", 25)], "completed": None, "scheduled": False},
			"tC3":{"rtime": 2, "ndata": [("C1", 30), ("tC1", 25), ("tC2", 25)], "completed": None, "scheduled": False}
		},
		"D":{
			"tD1":{"rtime": 2, "ndata": [("D1", 100), ("D2", 200), ("D3", 300)], "completed": None, "scheduled": False},
			"tD2":{"rtime": 2, "ndata": [("D1", 300), ("D2", 200), ("D3", 100)], "completed": None, "scheduled": False},
			"tD3":{"rtime": 1, "ndata": [("D2", 50), ("tD1", 200), ("tD2", 200)], "completed": None, "scheduled": False},
			"tD4":{"rtime": 0.5, "ndata": [("D1", 100), ("D3", 100), ("tD2", 200)], "completed": None, "scheduled": False},
			"tD5":{"rtime": 0.5, "ndata": [("D2", 200), ("tD3", 200)], "completed": None, "scheduled": False}
		},
		"E":{
			"tE1":{"rtime": 6, "ndata": [("E1", 60), ("E2", 80), ("E3", 120)], "completed": None, "scheduled": False},
			"tE2":{"rtime": 2, "ndata": [("E2", 90), ("E4", 120), ("tE1", 150)], "completed": None, "scheduled": False},
			"tE3":{"rtime": 3, "ndata": [("E1", 30), ("E3", 45), ("tE1", 75)], "completed": None, "scheduled": False},
			"tE4":{"rtime": 2, "ndata": [("E2", 160), ("tE2", 100)], "completed": None, "scheduled": False},
			"tE5":{"rtime": 1, "ndata": [("E3", 135), ("E4", 180), ("tE3", 90)], "completed": None, "scheduled": False},
			"tE6":{"rtime": 3, "ndata": [("E1", 50), ("tE3", 45), ("tE5", 180)], "completed": None, "scheduled": False}
		},
		"F":{
			"tF1":{"rtime": 4, "ndata": [("F1", 300)], "completed": None, "scheduled": False},
			"tF2":{"rtime": 2, "ndata": [("F2", 100), ("tF1", 100)], "completed": None, "scheduled": False},
			"tF3":{"rtime": 1, "ndata": [("F3", 200), ("tF1", 120)], "completed": None, "scheduled": False},
			"tF4":{"rtime": 3, "ndata": [("F4", 100), ("tF1", 80)], "completed": None, "scheduled": False},
			"tF5":{"rtime": 0.8, "ndata": [("F1", 50), ("F2", 50), ("F3", 50), ("tF2", 80), ("tF3", 160)], "completed": None, "scheduled": False},
			"tF6":{"rtime": 1.4, "ndata": [("F1", 66), ("F4", 66), ("tF4", 90)], "completed": None, "scheduled": False},
			"tF7":{"rtime": 2.2, "ndata": [("F3", 100), ("F5", 200), ("tF5", 300)], "completed": None, "scheduled": False},
			"tF8":{"rtime": 3.5, "ndata": [("F2", 150), ("F5", 100), ("tF5", 500), ("tF6", 65)], "completed": None, "scheduled": False},
			"tF9":{"rtime": 2, "ndata": [("F1", 225), ("F3", 25), ("F4", 75), ("F5", 200), ("tF7", 300), ("tF8", 300)], "completed": None, "scheduled": False}
		}
	}
	return JobDict


# def promote_task_execution(total_execution_time, slots_occupy_situation, DCS, num_of_tasks, completed_job):
# 	min_execution_time = math.inf
# 	min_execution_task = []
# 	for dc in slots_occupy_situation:
# 		for task in slots_occupy_situation[dc]:
# 			if slots_occupy_situation[dc][task] < min_execution_time:
# 				min_execution_time = slots_occupy_situation[dc][task]
# 				min_execution_task = [(dc, task)]
# 			elif slots_occupy_situation[dc][task] == min_execution_time:
# 				min_execution_task.append((dc, task))
# 	# tasks in 'min_execution_task' are done
# 	for task in min_execution_task:
# 		del slots_occupy_situation[task[0]][task[1]]
# 		# release 1 slot in DCx
# 		DCS[int(task[0][2:])-1] += 1
# 		num_of_tasks -= 1
# 		completed_job[task[1][1]] -= 1 # extract job name, e.g., A in tA1
# 		print(task[1] + " is completed")
# 	# promote time forward
# 	total_execution_time += min_execution_time
# 	return total_execution_time,slots_occupy_situation,DCS,num_of_tasks,completed_job


def draw_gantt(results_collections, DCS, JobDict, total_execution_time, isSimulate = False):
	if len(JobDict.keys()) > 26:
		return
	colors = {
		"A": '#7FFFD4',
		"B": '#EE82EE',
		"C": '#DAA520',
		"D": '#90EE90',
		"E": '#48D1CC',
		"F": '#FFB6C1',
		"G": '#696969',
		"H": '#008000',
		"I": '#ADFF2F',
		"J": '#CD5C5C',
		"K": '#E6E6FA',
		"L": '#FFFACD',
		"M": '#0000CD',
		"N": '#9370DB',
		"O": '#191970',
		"P": '#808000',
		"Q": '#FFA500',
		"R": '#B0E0E6',
		"S": '#3CB371',
		"T": '#2F4F4F',
		"U": '#6495ED',
		"V": '#5F9EA0',
		"W": '#A52A2A',
		"X": '#BA55D3',
		"Y": '#FFE4E1',
		"Z": '#6A5ACD'
	}
	# draw
	handles = {}
	for task in results_collections:
		# get # of slots before data center x, and reverse the slot_index
		y = sum(DCS[0:int(results_collections[task]["location"][2:])-1]) + (DCS[int(results_collections[task]["location"][2:])-1] - results_collections[task]["slot_index"] + 1)
		width = results_collections[task]["end"] - results_collections[task]["start"]
		left = results_collections[task]["start"]
		l1,=plt.barh(y=y, width=width, left=left, color=colors[task[1]], edgecolor="black")
		if isSimulate == False:
			plt.text(x=left+0.1,y=y-0.3,s=task,fontsize=14)
		if task[1] not in handles.keys():
			handles[task[1]] = l1
	if isSimulate == False: # too many DC, hide yticks for simulation
		yticks = []
		for i in range(len(DCS)):
			for j in range(DCS[i]):
				yticks.append("DC" + str(i+1) + "-Slot" + str(j+1))
		plt.yticks([i+1 for i in range(sum(DCS))], yticks)
	plt.grid(b=True, axis='x')
	xticks = np.arange(0, int(total_execution_time)+1, 5)
	plt.xticks(xticks)
	plt.tick_params(axis='x',which='major')
	plt.xlabel("Seconds", fontsize=14)
	if isSimulate == False:
		plt.title("Max-min fairness scheduling gantt chart", fontsize=18)
		plt.legend(handles=[handles[task] for task in sorted(handles)],labels=[("Job " + job) for job in JobDict], fontsize=14)
	else:
		plt.title("Max-min fairness scheduling gantt chart (# of DC = "+str(len(DCS))+")", fontsize=18)
		plt.legend(handles=[handles[task] for task in sorted(handles)],labels=[("Job " + job) for job in JobDict])
	plt.show()


if __name__ == '__main__':
	if ((len(sys.argv) == 2 and sys.argv[1] == "toydata") or (len(sys.argv) == 3 and sys.argv[1] == "simulate") and sys.argv[2].isdigit()) == False:
		print("Wrong input augments: please choose 'toydata' or 'simulate [positive number]'")
		exit(0)
	if sys.argv[1] == "toydata":
		DCBG,DCS,DBDict = ToyDataDataCenter()
		JobDict = ToyDataJob()
	elif sys.argv[1] == "simulate":
		DCBG,DCS,DBDict = GenerateDataCenter(int(sys.argv[2]), 26) # 100 DC, 26 JOB
		JobDict = GenerateJob(26, DBDict)
	DCS_backup = DCS
	num_of_dc = len(DCS)
	total_execution_time = 0
	ST_PROGRAM_TIME = time.time()
	# Data Center Shortest Path Graph (1/Bandwidth)
	DCSG = DCBG
	for x in range(num_of_dc):
		for y in range(num_of_dc):
			if DCSG[x][y] != math.inf:
				DCSG[x][y] = 1/DCSG[x][y]
	# Floyd
	DCSG = Floyd(DCSG, num_of_dc)
	# count # of tasks
	num_of_tasks = 0
	completed_job = {}
	results_collections = {} # e.g., {"tA1": {"start":1, "end": 2, "location": "DC1"}}
	for job in JobDict:
		num_of_tasks += len(JobDict[job].keys())
		completed_job[job] = len(JobDict[job].keys())
		for task in JobDict[job]:
			results_collections[task] = {"start": None, "end": None, "location": None, "slot_index": None}
	# scheduling
	slots_occupy_situation = {} # {"DC1": {"tA1": time}, "DC2": {"tA2": time}, ...}
	for x in range(num_of_dc):
		slots_occupy_situation["DC"+str(x+1)] = {}
	# if >= num_of_tasks, then promote task execution
	isPrecedenceBlocked = 0
	num_of_not_scheduled_tasks = num_of_tasks
	while num_of_tasks > 0:
		for job in JobDict:
			isAssigned = False
			# job has been done
			if completed_job[job] <= 0:
				continue
			# job has not been scheduled
			for task in JobDict[job]:
				# check the # of slots, at least 1
				if sum(DCS) == 0 or isPrecedenceBlocked >= num_of_tasks or num_of_not_scheduled_tasks == 0:
					"""
					slots are all occupied, simulate to wait for any task to be done,
					promote task execution to release a slot
					"""
					min_execution_time = math.inf
					min_execution_task = []
					for dc in slots_occupy_situation:
						for slot_task in slots_occupy_situation[dc]:
							if slots_occupy_situation[dc][slot_task] < min_execution_time:
								min_execution_time = slots_occupy_situation[dc][slot_task]
								min_execution_task = [(dc, slot_task)]
							elif slots_occupy_situation[dc][slot_task] == min_execution_time:
								min_execution_task.append((dc, slot_task))
					# promote time forward
					if min_execution_time == math.inf:
						break
					total_execution_time += min_execution_time
					isPrecedenceBlocked = 0
					# tasks in 'min_execution_task' are done
					for min_task in min_execution_task:
						del slots_occupy_situation[min_task[0]][min_task[1]] # {"DC1": {"tA1": time}, "DC2": {"tA2": time}, ...}
						# release 1 slot in DCx
						DCS[int(min_task[0][2:])-1] += 1
						num_of_tasks -= 1
						completed_job[min_task[1][1]] -= 1 # extract job name, e.g., A in tA1
						JobDict[min_task[1][1]][min_task[1]]["completed"] = min_task[0]
						results_collections[min_task[1]]["end"] = total_execution_time
						print(bcolors.OKBLUE + "- " + min_task[1] + " is completed at " + min_task[0] + bcolors.ENDC)
					# other tasks also run for min_execution_time
					for dc in slots_occupy_situation:
						for remain_task in slots_occupy_situation[dc]:
							slots_occupy_situation[dc][remain_task] -= min_execution_time

				# sub-task has been scheduled
				if JobDict[job][task]["scheduled"] == True:
					continue

				# check if data is ready
				isReady = True
				for ndata in JobDict[job][task]['ndata']:
					# print(job,task)
					# task needs data from other sub-task and data is not ready
					if ndata[0][0] == "t" and JobDict[ndata[0][1]][ndata[0]]["completed"] == None:
						isReady = False
						isPrecedenceBlocked += 1
						break
				if isReady == False:
					continue

				# start to schedule
				ndata_list = JobDict[job][task]['ndata']
				# collect data centers where task gets data (including DBs and previous tasks)
				DC_list = []
				for ndata in ndata_list:
					DC_list.append((int(DBDict[ndata[0]][2:])-1, ndata[1])) # index start from 0, (DC_index, required data amount)
				"""
				'data_transmission_time_at_each_dc' is used to keep the intermidiate results,
				because not all task schedules are optimal, sometimes we need to find a secondary answer
				"""
				data_transmission_time_at_each_dc = {}
				for i in range(num_of_dc):
					tx_time = 0
					for item in DC_list:
						tx_time += DCSG[item[0]][i] * item[1]
					data_transmission_time_at_each_dc["DC"+str(i+1)] = tx_time
				# sort in an non-decreasing order
				data_transmission_time_at_each_dc = dict(sorted(data_transmission_time_at_each_dc.items(), key=lambda item: item[1]))
				for dc in data_transmission_time_at_each_dc:
					dc_index = int(dc[2:])-1
					if DCS[dc_index] > 0:
						DCS[dc_index] -= 1 # occupy 1 slot in DCx
						slots_occupy_situation[dc][task] = data_transmission_time_at_each_dc[dc] + JobDict[job][task]['rtime'] # transmission time + execution time
						JobDict[job][task]["scheduled"] = True # task is scheduled at DCx
						num_of_not_scheduled_tasks -= 1
						DBDict[task] = dc # task data should be retrieved from DCx
						isAssigned = True
						results_collections[task]["start"] = total_execution_time
						results_collections[task]["slot_index"] = DCS[dc_index] + 1
						results_collections[task]["location"] = dc
						print(bcolors.OKGREEN + "+ " + task + " is scheduled at " + dc + ", will cost " + str(slots_occupy_situation[dc][task]) + " seconds" + bcolors.ENDC)
						break # max-min fairness, give resources to next job
					else:
						print(bcolors.FAIL + "* " + task + ": DC" + str(dc_index+1) + " is full now, looking for a secondary choice" + bcolors.ENDC)
				if isAssigned == True:
					break

	ED_PROGRAM_TIME = time.time()
	print("\nTotal execution time is " + str(total_execution_time) + " seconds\n")
	print("The program running time is " + str(ED_PROGRAM_TIME - ST_PROGRAM_TIME) + " seconds\n")
	if sys.argv[1] == "simulate":
		draw_gantt(results_collections, DCS_backup, JobDict, total_execution_time, True)
	else:
		draw_gantt(results_collections, DCS_backup, JobDict, total_execution_time)
