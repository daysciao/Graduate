# -*- coding: UTF-8 -*-

import numpy as np
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


def GA_routing(toponet, src, dst):
    NODE_NUM = toponet.shape[0]
    CROSS_RATE = 0.4
    MUTATE_RATE = 0.1
    POP_SIZE = 6 * NODE_NUM
    GA_GENERATIONS = NODE_NUM * (NODE_NUM-1) /2
    DNA_size = NODE_NUM - 2
    ga = GA(net=toponet,DNA_size=DNA_size, cross_rate=CROSS_RATE, mutation_rate=MUTATE_RATE, pop_size=POP_SIZE, route_source=src, route_destination=dst)
    return ga.route(GA_GENERATIONS)

def AC_routing(toponet, src, dst):
    NODE_NUM = toponet.shape[0]
    ANT_NUM = 4 * NODE_NUM #蚂蚁个数  
    PHEROMONE_MAX = 0.9
    PHEROMONE_MIN = 0.1
    RHO = 0.9   #信息素的挥发速度
    AC_GENERATIONS = NODE_NUM * (NODE_NUM-1) /2
    ants = Ant(net=toponet, node_num=NODE_NUM, ant_num=ANT_NUM, p_max=PHEROMONE_MAX, p_min=PHEROMONE_MIN, route_source=src, route_destination=dst, Rho = RHO)
    return ants.route(AC_GENERATIONS)

def GAC_routing(toponet, src, dst):
    NODE_NUM = toponet.shape[0]
    CROSS_RATE = 0.4
    MUTATE_RATE = 0.1
    POP_SIZE = 6 * NODE_NUM
    GA_GENERATIONS = NODE_NUM * (NODE_NUM-1) / 8
    DNA_size = NODE_NUM - 2
    
    ANT_NUM = 4 * NODE_NUM #蚂蚁个数  
    PHEROMONE_MAX = 0.9
    PHEROMONE_MIN = 0.1
    RHO = 0.9   #信息素的挥发速度
    AC_GENERATIONS = NODE_NUM
    
    ga = GA(net=toponet,DNA_size=DNA_size, cross_rate=CROSS_RATE, mutation_rate=MUTATE_RATE, pop_size=POP_SIZE, route_source=src, route_destination=dst)
    GA_route = ga.route(GA_GENERATIONS)
    gac_system = Ant(net=toponet, node_num=NODE_NUM, ant_num=ANT_NUM, p_max=PHEROMONE_MAX, p_min=PHEROMONE_MIN, route_source=src, route_destination=dst, Rho = RHO)
    gac_system.adapter(GA_route)
    return ant_system.route(AC_GENERATIONS)