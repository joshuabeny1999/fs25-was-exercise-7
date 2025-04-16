import numpy as np
import argparse

from environment import Environment
from ant import Ant 

# Class representing the ant colony
"""
    ant_population: the number of ants in the ant colony
    iterations: the number of iterations 
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
    rho: pheromone evaporation rate
"""
class AntColony:
    def __init__(self, ant_population: int, iterations: int, alpha: float, beta: float, rho: float):
        self.ant_population = ant_population
        self.iterations = iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho 

        # Initialize the environment of the ant colony
        self.environment = Environment(self.rho, self.ant_population)

        # Initilize the list of ants of the ant colony
        self.ants = []

        # Initialize the ants of the ant colony
        for i in range(ant_population):
            
            # Initialize an ant on a random initial location
            random_start = np.random.choice(list(self.environment.graph.nodes))
            ant = Ant(self.alpha, self.beta, random_start)

            # Position the ant in the environment of the ant colony so that it can move around
            ant.join(self.environment)
        
            # Add the ant to the ant colony
            self.ants.append(ant)

    # Solve the ant colony optimization problem  
    def solve(self):
        best_solution = None
        shortest_distance = np.inf

        for iteration in range(self.iterations):
            ant_tours = []

            # Set a random start location for each ant, then run
            for ant in self.ants:
                # Pick a new random start city
                random_start = np.random.choice(list(self.environment.graph.nodes))
                ant.initial_location = random_start
                ant.current_location = random_start

                # Clear tour state
                ant.tour = [random_start]
                ant.visited = set([random_start])
                ant.traveled_distance = 0

                # Run the ant to complete a tour
                tour, distance = ant.run()
                ant_tours.append(tour)

                # Update best solution
                if distance < shortest_distance:
                    shortest_distance = distance
                    best_solution = tour

            # Update pheromones globally
            self.environment.update_pheromone_map(ant_tours)

            print(f"Iteration {iteration+1}/{self.iterations} — Best distance so far: {shortest_distance}")

        return best_solution, shortest_distance

def main():
    parser = argparse.ArgumentParser(description="Ant Colony Optimization Solver")
    parser.add_argument('--ants', type=int, default=48, help='Number of ants')
    parser.add_argument('--iterations', type=int, default=50, help='Number of iterations')
    parser.add_argument('--alpha', type=float, default=1.0, help='Pheromone influence')
    parser.add_argument('--beta', type=float, default=3.0, help='Distance influence')
    parser.add_argument('--rho', type=float, default=0.5, help='Evaporation rate')

    args = parser.parse_args()

    ant_colony = AntColony(
        ant_population=args.ants,
        iterations=args.iterations,
        alpha=args.alpha,
        beta=args.beta,
        rho=args.rho
    )

    # Solve the ant colony optimization problem
    solution, distance = ant_colony.solve()
    print("Solution: ", solution)
    print("Distance: ", distance)


if __name__ == '__main__':
    main()    