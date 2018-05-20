# -*- coding: UTF-8 -*-

import numpy as np
import time

from GA_F import GA
from AC_F import Ant


toponet = np.array([[0,100,1,1,1,1,100,1,1,100,100,100,100,100,100,100],
                            [100,0,1,100,100,100,100,100,100,100,100,100,100,100,100,100],
                            [1,1,0,1,1,1,100,100,100,100,1,100,100,100,100,100],
                            [1,100,1,0,100,100,1,1,100,100,100,100,100,100,100,100],
                            [1,100,1,100,0,100,1,100,100,100,100,100,100,100,100,100],
                            [1,100,1,100,100,0,100,100,100,100,100,100,100,100,100,100],
                            [100,100,100,1,1,100,0,100,100,100,100,100,100,100,100,100],
                            [1,100,100,1,100,100,100,0,100,100,100,100,100,100,100,100],#
                            [1,100,100,100,100,100,100,100,0,100,1,1,1,1,100,1],
                            [100,100,100,100,100,100,100,100,100,0,1,100,100,100,100,100],
                            [100,100,1,100,100,100,100,100,1,1,0,1,1,1,100,100],
                            [100,100,100,100,100,100,100,100,1,100,1,0,100,100,1,1],
                            [100,100,100,100,100,100,100,100,1,100,1,100,0,100,1,100],
                            [100,100,100,100,100,100,100,100,1,100,1,100,100,0,100,100],
                            [100,100,100,100,100,100,100,100,100,100,100,1,1,100,0,100],
                            [100,100,100,100,100,100,100,100,1,100,100,1,100,100,100,0]])
NODE_NUM = toponet.shape[0]


CROSS_RATE = 0.4
MUTATE_RATE = 0.1
POP_SIZE = 6 * NODE_NUM
GA_GENERATIONS = 200
DNA_size = NODE_NUM - 2

ANT_NUM = 3 * NODE_NUM #蚂蚁个数  
PHEROMONE_MAX = 0.9
PHEROMONE_MIN = 0.1
RHO = 0.9   #信息素的挥发速度
AC_GENERATIONS = 10


ga = GA(net=toponet,DNA_size=DNA_size, cross_rate=CROSS_RATE, mutation_rate=MUTATE_RATE, pop_size=POP_SIZE, route_source=1, route_destination=14)
ant_system = Ant(net=toponet, node_num=NODE_NUM, ant_num=ANT_NUM, p_max=PHEROMONE_MAX, p_min=PHEROMONE_MIN, route_source=1, route_destination=14, Rho = RHO)
gac_system = Ant(net=toponet, node_num=NODE_NUM, ant_num=ANT_NUM, p_max=PHEROMONE_MAX, p_min=PHEROMONE_MIN, route_source=1, route_destination=14, Rho = RHO)
a= time.clock()
GA_route = ga.route(GA_GENERATIONS)
b= time.clock()
gac_system.adapter(GA_route)
d= time.clock()
AC_route = ant_system.route(AC_GENERATIONS)
c= time.clock()
e= time.clock()
GAC_route = ant_system.route(AC_GENERATIONS)
f= time.clock()
timega = b-a
timeac = c-d
timegac = f-e
print GA_route,timega,AC_route,timeac,GAC_route,timegac
