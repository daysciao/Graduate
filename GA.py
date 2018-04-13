import time
import numpy as np

toponet = np.array([[0,2,1,100,100,100],
            [2,0,2,3,4,100],
                [1,2,0,100,3,100],
            [100,3,100,0,2,5],
                [100,4,3,2,0,2],
            [100,100,100,5,2,0]])

CROSS_RATE = 0.2
MUTATE_RATE = 0.01
POP_SIZE = 50
N_GENERATIONS = 50
DNA_size = np.shape(toponet)[0]

    
class GA(object):
    def __init__(self, DNA_size, cross_rate, mutation_rate, pop_size, route_source, route_destination):
        self.DNA_size = DNA_size
        self.cross_rate = cross_rate
        self.mutate_rate = mutation_rate
        self.pop_size = pop_size
        self.pop = np.vstack([np.random.permutation(DNA_size) for _ in range(pop_size)])
        self.src = route_source
        self.des = route_destination
    
    def get_distance(self, net):
        distance = np.zeros(self.pop_size, dtype=np.int)
        jump = self.DNA_size - 1
        for i, route in enumerate(self.pop):
            for k in range(jump):
                distance[i] += net[route[k]][route[k+1]]
        return distance
    
    def get_fitness(self, distance):
        target = np.zeros(self.pop_size, dtype=np.int)
        for i, route in enumerate(self.pop):
            if route[0] == self.src and route[-1] == self.des:
                target[i] = 10
        fitness = (1000 - distance) * target
        return fitness
    
    def select(self):
        idx = np.random.choice(np.arange(self.pop_size), size=self.pop_size, replace=True, p=fitness/fitness.sum())
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
                child[point] = np.random.randint(self.DNA_size)
        return child

    def evolve(self):
        pop = self.select()
        pop_copy = pop.copy()
        for parent in pop:  # for every parent
            child = self.crossover(parent, pop_copy)
            child = self.mutate(child)
            parent[:] = child
        self.pop = pop
        


if __name__ == '__main__':
    start = time.clock()
    
    ga = GA(DNA_size=DNA_size, cross_rate=CROSS_RATE, mutation_rate=MUTATE_RATE, pop_size=POP_SIZE, route_source=0, route_destination=5)

    for generation in range(N_GENERATIONS):
        distance = ga.get_distance(toponet)
        fitness = ga.get_fitness(distance)
        idx = np.argmax(fitness)
        best_path = ga.pop[idx]
        shortest_path = distance[idx]
        print('Gen', generation, ': ', best_path, 'Shortest Distance: ',shortest_path)
        ga.evolve()

    end = time.clock()
    print(end - start)
