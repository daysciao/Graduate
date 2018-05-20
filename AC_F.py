# -*- coding: UTF-8 -*-

import numpy as np

class Ant(object):
    def __init__(self, net, node_num, ant_num, p_max, p_min, route_source, route_destination, Rho):
        self.node_num = node_num
        self.netikeru_table = ((net - 100) * net).astype(bool)
        self.src = route_source
        self.des = route_destination
        self.net = net
        self.p_max = p_max
        self.p_min = p_min
        self.ant_num = ant_num
        self.pheromone_table = self.p_max * self.netikeru_table
        self.rho = Rho
        self.q = node_num * p_max
        
    def adapter(self, GA_route):
        self.pheromone_table = self.pheromone_table * 0.75
        for i in range(len(GA_route) - 1):
            self.pheromone_table[GA_route[i]][GA_route[i+1]] = self.pheromone_table[GA_route[i]][GA_route[i+1]] * 1.33333333
    
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
        
    def update_pheromone(self):
        self.pheromone_table = self.pheromone_table * self.rho
        d_pheromone = self.q/self.path_lenth
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
            self.update_pheromone()
    
    def route(self, N_GENERATIONS):
        for generation in range(N_GENERATIONS):
            self.sys_work()
        
        return list(self.path)
