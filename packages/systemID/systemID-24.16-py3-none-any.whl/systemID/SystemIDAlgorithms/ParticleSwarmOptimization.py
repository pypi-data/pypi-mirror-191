import numpy as np
from random import uniform, random


class Particle:
    def __init__(self, dim, bounds):
        self.position = np.zeros(dim)  # particle position
        self.velocity = np.zeros(dim)  # particle velocity
        self.fitness = float('inf')  # particle fitness

        self.pbest_pos = np.zeros(dim)  # position of best individual
        self.pbest_fitness = float('inf')  # fitness of best individual

        self.dim = dim
        self.pbounds = np.array(bounds)
        self.vbounds = np.zeros(np.shape(bounds))
        for i in range(0, self.dim):
            self.vbounds[i][1] = self.pbounds[i][1] - self.pbounds[i][0]  # set the upper bounds of velocity
            self.vbounds[i][0] = -self.vbounds[i][1]  # set the lower bounds of velocity

        # Randomly initialize the particle swarm position
        for i in range(0, self.dim):
            self.position[i] = uniform(self.pbounds[i][0], self.pbounds[i][1])

    # evaluate current fitness
    def evaluate(self, costFunc):
        self.fitness = costFunc(self.position)

        # check to see if the current position is an individual best
        if self.fitness < self.pbest_fitness:
            self.pbest_pos = np.copy(self.position)
            self.pbest_fitness = self.fitness

    # update new particle velocity
    def update_velocity(self, gbest_pos):

        c1 = 1.49445  # cognative constant
        c2 = 1.49445  # social constant

        for i in range(0, self.dim):
            r1 = random()
            r2 = random()
            r3 = random()

            v_i = (1 + r1) / 2 * self.velocity[i]
            v_c = c1 * r2 * (self.pbest_pos[i] - self.position[i])
            v_s = c2 * r3 * (gbest_pos[i] - self.position[i])

            self.velocity[i] = v_i + v_c + v_s

            # here should have a velocity bound applied here
            if self.velocity[i] > self.vbounds[i][1]:
                self.velocity[i] = self.vbounds[i][1]
            # adjust minimum position if neseccary
            if self.velocity[i] < self.vbounds[i][0]:
                self.velocity[i] = self.vbounds[i][0]

    # update the particle position based off new velocity updates
    def update_position(self):
        for i in range(0, self.dim):
            self.position[i] = self.position[i] + self.velocity[i]

            # adjust maximum position if necessary
            if self.position[i] > self.pbounds[i][1]:
                self.position[i] = uniform(self.pbounds[i][0], self.pbounds[i][1])
                self.velocity[i] = 0
            # adjust minimum position if neseccary
            if self.position[i] < self.pbounds[i][0]:
                self.position[i] = uniform(self.pbounds[i][0], self.pbounds[i][1])
                self.velocity[i] = 0





class PSO:
    # Constructor of PSO, with initial guess###########################
    def __init__(self, costFunc, bounds, Num_dimension, Num_particles, Num_iteration):

        self.Num_particles = Num_particles  # Number of particle
        self.Num_dimension = Num_dimension  # Number of dimension
        self.Num_iteration = Num_iteration  # Number of max iteration
        self.costFunc = costFunc  # Cost Function waiting for evaluate
        self.bounds = bounds  # Upper bound and Lower bound for each dimension

        self.gbest_pos = np.zeros(Num_dimension)  # position of Global best particle
        self.gbest_fitness = float('inf')  # fitness of Global best particle

        # establish the swarm
        self.swarm = []
        for i in range(0, self.Num_particles):
            self.swarm.append(Particle(self.Num_dimension, self.bounds))

        for iterCount in range(0, self.Num_iteration):
            print('Iteration:', iterCount)
            print('Best Fitness:', self.gbest_fitness)
            print('Position:', self.gbest_pos)
            for j in range(0, self.Num_particles):
                self.swarm[j].evaluate(self.costFunc)
                # determine if current particle is the best (globally)
                if self.swarm[j].fitness < self.gbest_fitness:
                    self.gbest_pos = np.copy(self.swarm[j].position)
                    self.gbest_fitness = self.swarm[j].fitness
            # cycle through swarm and update velocities and position
            for j in range(0, self.Num_particles):
                self.swarm[j].update_velocity(self.gbest_pos)
                self.swarm[j].update_position()

    # print final results###################################################
    def __repr__(self):
        print('FINAL:')
        print("The Global Best location is: " + str(self.gbest_pos))
        print("The Global Best fitness is: " + str(self.gbest_fitness))
        return 'DONE'



