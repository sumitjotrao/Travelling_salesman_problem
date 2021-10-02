
import data_processing as processing
from algorithms import Integer_programming_model

file_path = "data/tsp_5_1"

num_node, co_ord = processing.read_coordinates(file_path)

TSP_IP = Integer_programming_model.integer_program(num_node, co_ord)
ip_x, ip_z = TSP_IP.build_model()


processing.path_plotting(ip_x, co_ord, num_node)




