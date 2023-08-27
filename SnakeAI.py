import random
from PySnake import display_width, display_height, snake_block_size, current_score

class AI(P):
    def __init__(self, genes):
        self.genes = genes
        self.fitness = 0

    def simulate_gameplay(self):
        # Reset game variables
        game_over_flag = False
        x, y = display_width / 2, display_height / 2
        snake_list = []
        length_of_snake = 1

        # Simulate game with agent's genes
        while not game_over_flag:
            # Determine agent's action based on current position and genes
            agent_action = self.genes[len(snake_list) % len(self.genes)]

            # Translate agent_action into movement
            if agent_action == "up":
                y_change, x_change = -snake_block_size, 0
            # ... Similar cases for other actions ...

            # Move snake
            x += x_change
            y += y_change

            # Check for game over conditions
            if x >= display_width or x < 0 or y >= display_height or y < 0:
                game_over_flag = True
            # ... Check for collisions and update snake_list ...

        # Return the score achieved
        return current_score

# up, down, left, right
num_genes = 4
# initial population size
population_size = 100
# number of population that will be selected as parents
parent_selection_rate = 0.3
# number of generations 
num_generations = 50
# the rate of which mutations will occur in the population
mutation_rate = 0.1


def create_initial_population(population_size):
    initial_population = []
    for _ in range(population_size):
        genes = [random.choice(["up", "down", "left", "right"]) for _ in range(num_genes)]
        initial_population.append(AI(genes))
    return initial_population

def mutate(agent):
    # Iterate through each gene in the agent's genes
    for i in range(len(agent.genes)):
        if random.random() < mutation_rate:
            # Mutate the gene with some probability
            agent.genes[i] = random.choice(["up", "down", "left", "right"])

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1.genes) - 1)
    offspring_genes = parent1.genes[:crossover_point] + parent2.genes[crossover_point:]
    return AI(offspring_genes)  # Create a new agent with the combined genes

def evolve_population(current_population):
    # Calculate fitness for each AI agent
    for agent in current_population:
        agent.fitness = evaluate_fitness(agent)

    # Select parents and perform crossover/mutation
    parents = selection(current_population)
    offspring = []
    for i in range(0, len(parents), 2):
        child = crossover(parents[i], parents[i + 1])
        mutate(child)
        offspring.append(child)

    # Combine parents and offspring to create the next generation
    next_generation = parents + offspring

    return next_generation


def evaluate_fitness(agent):
    # Simulate gameplay and return score achieved by the agent
    return agent.simulate_gameplay()


def selection(population):
    # Sort agents by fitness in descending order
    sorted_population = sorted(population, key=lambda agent: agent.fitness, reverse=True)
    
    # Select top agents as parents
    num_parents = int(len(population) * parent_selection_rate)
    parents = sorted_population[:num_parents]

    return parents


def main():
    population = create_initial_population(population_size)
    best_agent = None

    for generation in range(num_generations):
        # Evaluate fitness and evolve population
        for agent in population:
            agent.fitness = evaluate_fitness(agent)

        # Find the best agent in the current generation
        best_agent_in_generation = max(population, key=lambda agent: agent.fitness)

        # Update the best agent if needed
        if best_agent is None or best_agent_in_generation.fitness > best_agent.fitness:
            best_agent = best_agent_in_generation

        # Evolve the population using selection, crossover, and mutation
        population = evolve_population(population)

    # Extract the genes of the best agent
    best_genes = best_agent.genes

    # Use best_genes in your game loop

