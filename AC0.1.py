# -*- coding: UTF-8 -*-

import time
import numpy as np

toponet = np.array([[0,100,1,1,1,1,100,1],
                    [100,0,1,100,100,100,100,100],
                    [1,1,0,1,1,1,100,100],
                    [1,100,1,0,100,100,1,1],
                    [1,100,1,100,0,100,1,100],
                    [1,100,1,100,100,0,100,100],
                    [100,100,100,1,1,100,0,100],
                    [1,100,100,1,100,100,100,0]])

ANT_NUM = 12 #蚂蚁个数  
NODE_NUM = toponet.shape[0] #节点个数
PHEROMONE_MAX = 0.9
PHEROMONE_MIN = 0.1
RHO = 0.9   #信息素的挥发速度
N_GENERATIONS = 5
GA_route = np.array([0, 2, 2, 4, 4, 4, 4, 6])
Q = 12

class Ant(object):
    def __init__(self, net, node_num, ant_num, p_max, p_min, route_source, route_destination, GA_route):
        self.node_num = node_num
        self.netikeru_table = ((net - 100) * net).astype(bool)
        self.src = route_source
        self.des = route_destination
        self.net = net
        self.p_max = p_max
        self.p_min = p_min
        self.ant_num = ant_num
        self.create_pheromone_table(GA_route)
        
    def create_pheromone_table(self, GA_route):
        table =  self.p_max * self.netikeru_table
        for i in range(self.node_num - 1):
            table[GA_route[i]][GA_route[i+1]] = table[GA_route[i]][GA_route[i+1]] * 1.33333333
        self.pheromone_table = table
    
    def create_antikeru_list(self):
        table = np.ones(self.node_num, dtype = bool)
        table[self.src] = False
        return table

    def get_path_lenth(self, path):
        lenth = 0
        for i in range(len(path) - 1):
            lenth = self.net[path[i]][path[i+1]] + lenth
        return lenth
        
    def steps(self):
        netikeru_list = self.netikeru_table[self.src]
        antikeru_list = self.create_antikeru_list()
        ikeru_list = netikeru_list & antikeru_list
        position = self.src
        step_path = [position]
        while(ikeru_list.any() and position != self.des):
            pheromone = ikeru_list * self.pheromone_table[position]
            position = np.random.choice(np.arange(self.node_num), size=1, replace=True, p=pheromone/pheromone.sum())[0]
            antikeru_list[position] = False
            step_path.append(position)
            netikeru_list = self.netikeru_table[position]
            ikeru_list = netikeru_list & antikeru_list
        if position == self.des:
            Lenth = self.get_path_lenth(step_path)
            if (Lenth < self.path_lenth):
                self.F = 1
                self.path = step_path
                self.path_lenth = Lenth
        
    def update_pheromone(self, rho, Q):
        self.pheromone_table = self.pheromone_table * rho
        d_pheromone = Q/self.path_lenth
        for i in range(len(self.path) - 1):
            self.pheromone_table[self.path[i]][self.path[i+1]] = self.pheromone_table[self.path[i]][self.path[i+1]] + d_pheromone
        self.pheromone_table[self.pheromone_table < self.p_min] = self.p_min
        self.pheromone_table[self.pheromone_table > self.p_max] = self.p_max
    
    def sys_work(self):
        self.F = 0
        self.path = [self.src]
        self.path_lenth = 100 * self.node_num
        for ants in range(self.ant_num):
            self.steps()
        if self.F == 1:
            self.update_pheromone(0.9, 12)
    

    
    
    
if __name__ == '__main__':
    start = time.clock()
    
    ant_system = Ant(net=toponet, node_num=NODE_NUM, ant_num=ANT_NUM, p_max=PHEROMONE_MAX, p_min=PHEROMONE_MIN, route_source=0, route_destination=6, GA_route=GA_route)


    for generation in range(N_GENERATIONS):
        ant_system.sys_work()
        
    print 'Gen', generation, ': ', ant_system.path, 'Shortest Distance: ', ant_system.path_lenth
    end = time.clock()
    print(end - start)   
