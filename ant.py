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
        self.initial_location = initial_location
        self.current_location = initial_location
        self.traveled_distance = 0

        self.tour = [initial_location]
        self.visited = {initial_location}

    # The ant runs to visit all the possible locations of the environment 
    def run(self):
        self.tour = [self.initial_location]      # Start tour at the initial location
        self.visited = {self.initial_location}
        self.traveled_distance = 0
        self.current_location = self.initial_location

        while len(self.visited) < len(self.environment.graph.nodes):
            next_city = self.select_path()

            if next_city is None:
                break

            # Update distance
            distance = self.get_distance(self.current_location, next_city)
            self.traveled_distance += distance

            # Move ant
            self.tour.append(next_city)
            self.visited.add(next_city)
            self.current_location = next_city

        # Complete tour by returning to start
        start = self.initial_location
        self.traveled_distance += self.get_distance(self.current_location, start)
        self.tour.append(start)

        return self.tour, self.traveled_distance

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
