"""
	INTELLIGENT WATER DROPS (IWD) ALGORITHM TO SOLVE TSP
	ALGORITHM: Shah-Hosseini
	TRANSLATED TO PYTHON: Duvvuri Surya Rahul
"""

#================================================================================

import sys
import random
import graph
import argparse

#========================================================================================================
# PARAMETERS INITIALIZATION
#========================================================================================================

class parameters_initialization(object):
	"""
		The intelligent water drop algorithm uses a lot of parameters, both static and dynamic.
		This class helps in creating and initializing paramters.
		These parameters would be passed as a list to compute().
	"""

	parameter_list = {}
	def __init__(self):
		self.static_parameter_initialization_for_soil_updating()
		self.static_parameter_initialization_for_velocity_updating()
		self.initialize_maximum_number_of_iterations()
		self.initialize_iteration_count()
		self.initialize_amount_of_soil_on_path()
		self.initialize_velocity()
		self.initialize_value_of_p_n()
		self.initialize_value_of_p_iwd()

	#=======================================================================================================
	# STATIC PARAMETERS INITIALIZATION
	#=======================================================================================================

	def static_parameter_initialization_for_soil_updating(self, a_s = 1, b_s = 0.01, c_s = 1.0):
		"""
			Static Parameters for soil comprise the constants: a_s, b_s, c_s
			Default initialization: a_s = 1.0, b_s = 0.01, c_s = 1.0
			Returns the initialized parameter list.
		"""
		self.parameter_list['soil_parameters'] = [a_s, b_s, c_s]
		return [a_s, b_s, c_s]

	def static_parameter_initialization_for_velocity_updating(self, a_v = 1, b_v = 0.01, c_v = 1.0):
		"""
			Static Parameters for velocity comprise the constants: a_v, b_v, c_v
			Defalut initialization: a_v = 1.0, b_v = 0.01, c_v = 1.0
			Returns the initialized parameter list.
		"""
		self.parameter_list['velocity_parameters'] = [a_v, b_v, c_v]
		return [a_v, b_v, c_v]

	def initialize_maximum_number_of_iterations(self, maximum_iterations = 1000):
		"""
			If argument is supplied, the argument is returned.
			Otherwise, a default value is returned.
		"""
		self.parameter_list['maximum_iterations'] = maximum_iterations
		return maximum_iterations

	def initialize_iteration_count(self, iteration_count = 0):
		"""
			If argument is supplied, the argument is returned.
			Otherwise, a default value is returned.
		"""
		self.parameter_list['iteration_count'] = iteration_count
		return iteration_count

	def initialize_amount_of_soil_on_path(self, amount_of_soil = 10000):
		"""
			If argument is supplied, the argument is returned.
			Otherwise, a default value is returned.
		"""
		self.parameter_list['initial_amount_of_soil'] = amount_of_soil
		return amount_of_soil

	def initialize_velocity(self, init_vel = 200):
		"""
			If argument is supplied, the argument is returned.
			Otherwise, a default value is returned.
		"""
		self.parameter_list['init_vel'] = init_vel
		return init_vel

	def initialize_value_of_p_n(self, p_n = 0.9):
		"""
			If argument is supplied, the argument is returned.
			Otherwise, a default value is returned.
		"""
		self.parameter_list['p_n'] = p_n
		return p_n

	def initialize_value_of_p_iwd(self, p_iwd = 0.9):
		"""
			If argument is supplied, the argument is returned.
			Otherwise, a default value is returned.
		"""
		self.parameter_list['p_iwd'] = p_iwd
		return p_iwd

	#==================================================================================================================
	# NO DEFAULT, PARAMETERS ARE EXPECTED
	#==================================================================================================================
	def initialize_graph(self, number_of_nodes, distance):
		"""
			Mandatory to provide the arguments.
			Takes the number of nodes or cities.
			returns the number of iwds.
		"""
		self.parameter_list['number_of_nodes'] = number_of_nodes
		self.parameter_list['distance'] = distance

		self.set_heuristic_undesirability(distance)
		self.initialize_soil_between_nodes(self.parameter_list['initial_amount_of_soil'], number_of_nodes, distance)

		return [number_of_nodes, distance]

	#=================================================================================================================
	# SET HEURISTIC UNDESIRABILITY (IMPORTANT)
	#=================================================================================================================
	def set_heuristic_undesirability(self, distance):
		"""
			Takes various parameters. 
			Composition of these parameters is used to set undesirability.
			In the case of TSP, the undesirability is the distance, i.e. 
			more the distance between nodes, less desirable.
			Undesirability Matrix is returned.
		"""
		HUD = distance
		self.parameter_list['HUD'] = HUD
		return HUD

	#===========================================================================================
	# INITIALIZE SOIL BETWEEN NODES (DYNAMIC PARAMETER)
	#===========================================================================================
	def initialize_soil_between_nodes(self, initial_amount_of_soil, number_of_iwds, graph):
		"""
			Sets amount of soil on each path to intitial_amount_of_soil
			returns soil (Dictionary)
		"""
		soil={}
		for i in range(number_of_iwds):
			soil[i] = {}
			for j in graph[i]:
				soil[i][j] = initial_amount_of_soil
		self.parameter_list['soil'] = soil
		return soil

# END OF CLASS
#=====================================================================================================

#=============================================================================================
# DYNAMIC PARAMETERS INITIALIZATION
#=============================================================================================

"""	
	Dynamic parameters are reinitialized at the end of
	each iteration of the algorithm. Each IWD has a
	visited node list V_c(IWD) which is initially empty:
	Vc(IWD) = { }. The velocity of each IWD is set to
	InitVel. All IWDs initially have zero amount of soil.
"""

class intelligent_water_drop(object):
	"""
		Intelligent water drop is used to create individual water drops.
	"""

	def __init__(self, iwd_number, velocity):
		"""
			Initializes current_node_position to iwd_number
			Initializes current_velocity to velocity
			Initializes amount_of_soil to 0
			Initializes vistied_list 
		"""
		self.id = iwd_number
		self.current = iwd_number
		self.velocity = velocity
		self.amount_of_soil = 0
		self.visited = []

# END OF CLASS
#==============================================================================

#==========================================================================================
# SUPOORT FUNCTIONS
#==========================================================================================

def create_and_initialize_intelligent_water_drops(n_iwd, graph, init_vel):
	"""
		Creates and Initializes all the intelligent water drops.
		In this algorithm, number of intelligent water drops = number of nodes in graph.
		Returns intelligent water drop.
	"""
	iwd = {}
	for iwd_number in range(n_iwd):
		iwd[iwd_number] = intelligent_water_drop(iwd_number, init_vel)
		iwd[iwd_number].current = random.choice(graph.keys())
		iwd[iwd_number].visited.append(iwd[iwd_number].current)
	return iwd

def probability_of_choosing_j(visited, current, j, graph, soil):
	"""probability of choosing node j"""
	sum_fsoil_i_k = 0
	for k in graph:
		if k not in visited:
			sum_fsoil_i_k += f_soil(visited, current, k, graph, soil)
	return f_soil(visited,current,j,graph, soil)/sum_fsoil_i_k

def f_soil(visited,i,j,graph, soil):
	epsilon_s = 0.0001 # Subject to vary
	return 1/(epsilon_s+g_soil(visited,i,j,graph, soil))

def g_soil(visited,i,j, graph, soil):
	minimum = 99999999999	# +infinity
	for l in graph:
		if l not in visited:
			if soil[i][l] < minimum:
				minimum = soil[i][l]
	if minimum >= 0:
		return soil[i][j]
	else:
		return soil[i][j]-minimum

def time(i,j,vel,HUD):
	return HUD[i][j]/vel 

def q(iteration_path, distance):
	total_distance = 0
	prev = iteration_path[len(iteration_path)-1]
	for i in iteration_path:
		now = i
		total_distance += distance[prev][now]
		prev = now
	return 1.0/total_distance

#=======================================================================================================================
# COMPUTATION
#=======================================================================================================================

def compute(all_parameters):
	"""
		Takes all_parameters, a list consisting of all initialized static and dynamic parameters.
		It implements the intelligent water drops algorithm using the input parameters to compute efficient solution.
		It returns a list consisting of the best solution path, the quality and distance.
	"""

	a_s = all_parameters['soil_parameters'][0]
	b_s = all_parameters['soil_parameters'][1]
	c_s = all_parameters['soil_parameters'][2]
	a_v = all_parameters['velocity_parameters'][0]
	b_v = all_parameters['velocity_parameters'][1]
	c_v = all_parameters['velocity_parameters'][2]
	maximum_iterations = all_parameters['maximum_iterations']
	iteration_count = all_parameters['iteration_count']
	initial_amount_of_soil = all_parameters['initial_amount_of_soil']
	init_vel = all_parameters['init_vel']
	p_n = all_parameters['p_n']
	p_iwd = all_parameters['p_iwd']
	n_iwd = all_parameters['number_of_nodes']
	graph = all_parameters['distance']
	HUD = all_parameters['HUD']
	soil = all_parameters['soil']

	# 'i' = intelligent water drop
	# 'j' = node in graph
	# Initial Total Best Solution = -999
	T_TB = -999
	while iteration_count < maximum_iterations:
		#Instantiate objects IWD
		iwd = create_and_initialize_intelligent_water_drops(n_iwd, graph, init_vel)

		quality = []
		probability = {}
		
		for i in range(n_iwd):
			while(len(iwd[i].visited) < n_iwd):
				node_selected = False

				for j in graph[iwd[i].current]:
					if j not in iwd[i].visited:
						probability[j] = probability_of_choosing_j(iwd[i].visited, iwd[i].current, j, graph, soil)
				#if probability_of_choosing_j(iwd[i].visited,iwd[i].current,j) >= random.random():
				#append the node to the visited set
				random_number = random.random()
				probability_sum = 0
				for t in probability:
					if probability_sum > 1:
						node_selected = False
						break
					if random_number > probability_sum and random_number < probability_sum+probability[t]: 
						j = t
						node_selected = True
						break
					probability_sum += probability[t] 
				if node_selected == True:
					iwd[i].visited.append(j)
					updated_velocity = iwd[i].velocity+a_v/(b_v+c_v*soil[iwd[i].current][j]**2)
					iwd[i].velocity = updated_velocity
					delta_soil = a_s/(b_s+c_s*time(i,j,updated_velocity,HUD)**2)
					soil[iwd[i].current][j] = (1-p_n)*soil[iwd[i].current][j]-p_n*delta_soil
					iwd[i].amount_of_soil = iwd[i].amount_of_soil+delta_soil
					iwd[i].current = j
				probability = {}

			#Completion of solution by making it back to 'i'
			#IWD has completed a cycle
			updated_velocity = iwd[i].velocity+a_v/(b_v+c_v*soil[iwd[i].current][i]**2)
			iwd[i].velocity = updated_velocity
			delta_soil = a_s/(b_s+c_s*time(iwd[i].current,i,updated_velocity,HUD)**2)
			soil[iwd[i].current][i] = (1-p_n)*soil[iwd[i].current][i]-p_n*delta_soil
			iwd[i].amount_of_soil = iwd[i].amount_of_soil+delta_soil
			iwd[i].current = i

			quality.append(q(iwd[i].visited, graph))
		max_quality = max(quality)
		max_quality_index = quality.index(max_quality)

		#Update soil in the Iteration Best solution (IB)
		prev = iwd[max_quality_index].visited[len(iwd[max_quality_index].visited)-1]
		for i in iwd[max_quality_index].visited:
			now = i
			soil[prev][now] = (1+p_iwd)*soil[prev][now]-p_iwd*(1/(n_iwd-1))*iwd[max_quality_index].amount_of_soil
			prev = i

		if T_TB < 0:
			T_TB = iwd[max_quality_index].visited
			highest_quality = max_quality
		elif highest_quality > max_quality:
			pass
		else:
			T_TB = iwd[max_quality_index].visited
			highest_quality = max_quality	
		iteration_count += 1

	solution = [T_TB, highest_quality]
	return solution

# END OF COMPUTE	
#===============================================================================================================

#===============================================================================================================
# MAIN FUNCTION
#===============================================================================================================

def main():
	#=======================================================================================================
	# INITIALIZATION
	#=======================================================================================================
	parameters = parameters_initialization()
	parameters.initialize_graph(graph.number_of_nodes, graph.distance)

	parser = argparse.ArgumentParser(
		description="""
			Automated Code for intelligent water drops algorithm on dynamic nodes.
		"""
		)

	parser.add_argument('-i', '--iterations', nargs=1,
						help='Specify number of iterations\n'
							 'Usages: \n'
							 '--iterations <integer>\n')

	args = parser.parse_args()

	if args.iterations:
			parameters.parameter_list['maximum_iterations'] = int(args.iterations[0])

	#=========================================================================================================
	# SOLUTION AFTER MAX_ITERATIONS
	#=========================================================================================================
	solution = compute(parameters.parameter_list)
	print ''
	print 'THE BEST SOLUTION FOUND:', solution[0]
	print 'MAXIMUM QUALITY:', solution[1]
	print 'TOTAL_DISTANCE:', 1/solution[1]	
	print 'NUMBER OF ITERATIONS:', parameters.parameter_list['maximum_iterations']
	print ''

#===============================================================================================================

if __name__ == "__main__":
	main()

#===============================================================================================================

