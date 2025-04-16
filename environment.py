import math
import tsplib95
import networkx as nx

# Class representing the environment of the ant colony
"""
    rho: pheromone evaporation rate
    ant_population: number of ant population
"""
class Environment:
    def __init__(self, rho, ant_population):

        self.rho =rho
        self.ant_population = ant_population
        
        # Initialize the environment topology
        self.problem = tsplib95.load('att48-specs/att48.tsp')
        self.graph = self.problem.get_graph()

        # Initialize the pheromone map in the environment
        self.initialize_pheromone_map()

        print(self.graph[1][2])

    # Initialize the pheromone trails in the environment
    def initialize_pheromone_map(self):
        c_nn = self._calculate_nearest_neighbor_tour_length()

        # Initial pheromone level (τ₀) as per the Ant System algorithm
        initial_pheromone = self.ant_population / c_nn

        for u, v in self.graph.edges():
            self.graph[u][v]['pheromone'] = initial_pheromone

    def _calculate_nearest_neighbor_tour_length(self):
        """Calculate the length of a tour constructed using the nearest neighbor heuristic."""
        nodes = list(self.graph.nodes())
        start_node = nodes[0]  # Start from the first city
        visited = {start_node}
        current = start_node
        tour_length = 0

        while len(visited) < len(nodes):
            # Find nearest unvisited node
            next_node = min(
                (node for node in nodes if node not in visited),
                key=lambda node: self.graph[current][node]['weight']
            )
            tour_length += self.graph[current][next_node]['weight']
            current = next_node
            visited.add(current)

        # Return to starting node to complete the tour
        tour_length += self.graph[current][start_node]['weight']
        return tour_length

    # Update the pheromone trails in the environment
    def update_pheromone_map(self, ant_tours):
        # Step 1: Pheromone evaporation on all edges
        for u, v in self.graph.edges():
            self.graph[u][v]['pheromone'] = (1 - self.rho) * self.graph[u][v]['pheromone']

        # Step 2: Add pheromone based on ant tours
        for tour in ant_tours:
            # Calculate total cost of the tour
            tour_cost = 0
            for i in range(len(tour) - 1):
                u, v = tour[i], tour[i + 1]
                tour_cost += self.graph[u][v]['weight']
            # Add the return to starting point
            tour_cost += self.graph[tour[-1]][tour[0]]['weight']

            # Add pheromone to all edges in the tour
            for i in range(len(tour) - 1):
                u, v = tour[i], tour[i+1]
                self.graph[u][v]['pheromone'] += 1.0 / tour_cost

            # Complete the tour (return to start)
            u, v = tour[-1], tour[0]
            self.graph[u][v]['pheromone'] += 1.0 / tour_cost


    # Get the environment topology
    def get_possible_locations(self):
        pass

    
