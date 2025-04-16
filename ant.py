import random
# Class representing an artificial ant of the ant colony
"""
    alpha: a parameter controlling the influence of the amount of pheromone during ants' path selection process
    beta: a parameter controlling the influence of the distance to the next node during ants' path selection process
"""
class Ant():
    def __init__(self, alpha: float, beta: float, initial_location):
        self.environment = None
        self.alpha = alpha
        self.beta = beta
        self.current_location = initial_location
        self.traveled_distance = 0

        self.tour = [initial_location]
        self.visited = {initial_location}

    # The ant runs to visit all the possible locations of the environment 
    def run(self):
        pass

    # Select the next path based on the random proportional rule of the ACO algorithm
    def select_path(self):
        graph = self.environment.graph
        current = self.current_location

        # Only consider unvisited cities
        neighbors = [node for node in graph.nodes if node not in self.visited and node != current]

        if not neighbors:
            return None  # No unvisited neighbors left

        probs = []
        denominator = 0

        for j in neighbors:
            pheromone = graph[current][j]['pheromone']
            distance = self.get_distance(current, j)
            heuristic = 1.0 / distance if distance > 0 else float('inf')
            val = (pheromone ** self.alpha) * (heuristic ** self.beta)
            probs.append((j, val))
            denominator += val

        probabilities = [(city, val / denominator) for city, val in probs]

        # Roulette wheel selection
        r = random.random()
        cumulative = 0
        for city, prob in probabilities:
            cumulative += prob
            if r <= cumulative:
                return city

        return probabilities[-1][0]  # fallback

    # Position an ant in an environment
    def join(self, environment):
        self.environment = environment
    
    def get_distance(self, from_location, to_location):
        if from_location == to_location:
            return 0

        # Get the weight of the edge between from_location and to_location
        return self.environment.graph[from_location][to_location]['weight']
