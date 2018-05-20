# -*- coding: utf-8 -*-

import numpy as np
    
class GA(object):
    def __init__(self, net, DNA_size, cross_rate, mutation_rate, pop_size, route_source, route_destination):
        self.net = net
        self.DNA_size = DNA_size
        self.cross_rate = cross_rate
        self.mutate_rate = mutation_rate
        self.pop_size = pop_size
        bound = np.arange(DNA_size + 2)
        bound = bound[bound != route_source]
        bound = bound[bound != route_destination]
        self.bound = bound
        self.pop = np.vstack([np.random.permutation(bound) for _ in range(pop_size)])
        self.src = route_source
        self.des = route_destination
        
    def get_fitness(self):
        s = np.ones(self.pop_size, np.int).reshape(self.pop_size, 1) * self.src
        d = np.ones(self.pop_size, np.int).reshape(self.pop_size, 1) * self.des
        fitness = np.zeros(self.pop_size, dtype=np.int)
        routes = np.c_[s, self.pop, d]
        jump = self.DNA_size + 1
        for i, route in enumerate(routes):
            for k in range(jump):
                #if self.net[route[k]][route[k+1]] == 100:
                #    fitness[i] += 2000
                fitness[i] += self.net[route[k]][route[k+1]]
        return fitness
    
    def select(self,fitness):
        team = np.random.choice(np.arange(self.pop_size), size=4*self.pop_size, replace=True).reshape(4, -1)
        game = fitness[team]
        compete = np.argmin(game, axis=0)
        idx = np.choose(compete, team)
        return self.pop[idx]
        
        
    def crossover(self, parent, pop):
        if np.random.rand() < self.cross_rate:
            i_ = np.random.randint(0, self.pop_size, size=1)                        # select another individual from pop
            cross_points = np.random.randint(0, 2, self.DNA_size).astype(np.bool)   # choose crossover points
            parent[cross_points] = pop[i_, cross_points]                            # mating and produce one child
        return parent

    def mutate(self, child):
        for point in range(self.DNA_size):
            if np.random.rand() < self.mutate_rate:
                child[point] = np.random.randint(self.DNA_size + 2)
        return child

    def evolve(self,fitness):
        pop = self.select(fitness)
        pop_copy = pop.copy()
        for parent in pop:  # for every parent
            child = self.crossover(parent, pop_copy)
            child = self.mutate(child)
            parent[:] = child
        self.pop = pop
        
    def decircle(self,path):
        path = [self.src] + list(path) + [self.des]
        i = 0
        while (i!=len(path)):
            i = i+1
            for k in range(i,len(path)):
                if path[k] == path[i-1]:
                    path = path[:i] + path[(k+1):]
                    i = 0
                    break
        return path
    
    def route(self,N_GENERATIONS):
        for generation in range(N_GENERATIONS):
            fitness = self.get_fitness()
            idx = np.argmin(fitness)
            best_path = self.pop[idx]
            shortest_path = fitness[idx]
            self.evolve(fitness)
        return self.decircle(best_path)