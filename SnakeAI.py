import random, math
import matplotlib.pyplot as plt
from PySnake import display_width, display_height, snake_block_size, generate_apple_position, main_game_loop

class AI():
    def __init__(self, genes):
        self.genes = genes
        self.fitness = 0

    def simulate_gameplay(self, apple_x, apple_y):  # Pass apple_x and apple_y as arguments
        # Reset game variables
        game_over_flag = False
        x, y = display_width / 2, display_height / 2
        snake_list = []
        length_of_snake = 1

        x_change, y_change = 0, 0  # Declare x_change and y_change as local variables

        # Simulate game with agent's genes
        while not game_over_flag:
            # Calculate distance to the apple
            snake_head_x, snake_head_y = x, y
            distance_to_apple = math.sqrt((snake_head_x - apple_x)**2 + (snake_head_y - apple_y)**2)

            snake_head = [x, y]
            snake_list.append(snake_head)

            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for segment in snake_list[:-1]:  # Use 'segment' as the loop variable
                if segment == snake_head:
                    game_over_flag = True
            
            # Determine agent's action based on current position and genes
            agent_action = self.genes[len(snake_list) % len(self.genes)]

            # Calculate the relative positions of the snake's head and the apple
            horizontal_distance = apple_x - snake_head_x
            vertical_distance = apple_y - snake_head_y
            
            # Prioritize actions based on the relative positions
            if abs(horizontal_distance) >= abs(vertical_distance):
                if horizontal_distance > 0:
                    agent_action = "right"
                else:
                    agent_action = "left"
            else:
                if vertical_distance > 0:
                    agent_action = "down"
                else:
                    agent_action = "up"

            # Translate agent_action into movement
            if agent_action == "up":
                y_change, x_change = -snake_block_size, 0
            elif agent_action == "down":
                y_change, x_change = snake_block_size, 0
            elif agent_action == "left":
                y_change, x_change = 0, -snake_block_size
            elif agent_action == "right":
                y_change, x_change = 0, snake_block_size

            # Move snake
            x += x_change
            y += y_change

            # Check for game over conditions
            if x >= display_width or x < 0 or y >= display_height or y < 0:
                game_over_flag = True

            # Check for apple collision and update length_of_snake
            if (x, y) == (apple_x, apple_y):
                apple_x, apple_y = generate_apple_position()
                length_of_snake += 1  # Increase snake's length when apple is collected

        # Return the length of the snake and the apple's position
        return length_of_snake - 1


# up, down, left, right
num_genes = 4
# initial population size
population_size = 200
# number of population that will be selected as parents
parent_selection_rate = 0.3
# number of generations 
num_generations = 100
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

    # Sort the population by fitness in descending order
    sorted_population = sorted(current_population, key=lambda agent: agent.fitness, reverse=True)

    # Select the top-performing parents for reproduction
    num_parents = int(len(current_population) * parent_selection_rate)
    num_parents -= num_parents % 2  # Make sure it's an even number
    num_parents = max(num_parents, 2)  # Ensure at least 2 parents
    parents = sorted_population[:num_parents]

    offspring = []

    # Perform crossover and mutation on selected parents
    while len(offspring) < len(current_population) - num_parents:
        parent1, parent2 = random.sample(parents, 2)  # Select two random parents from the top-performing parents
        child = crossover(parent1, parent2)
        mutate(child)
        offspring.append(child)

    # Combine parents and offspring to create the next generation
    next_generation = parents + offspring

    return next_generation


def evaluate_fitness(agent, num_games=10):
    total_score = 0
    for _ in range(num_games):
        # Generate initial apple position
        apple_x, apple_y = generate_apple_position()

        # Simulate gameplay and accumulate scores across games
        ai_action = agent.genes[0]  # Set AI action based on the first gene
        total_score += agent.simulate_gameplay(apple_x, apple_y)

    # Calculate average score across games
    average_score = total_score 

    return average_score


def selection(population):
    # Sort agents by fitness in descending order
    sorted_population = sorted(population, key=lambda agent: agent.fitness, reverse=True)
    
    # Select top agents as parents if there are enough agents
    num_parents = int(len(population) * parent_selection_rate)
    num_parents -= num_parents % 2  # Make sure it's an even number
    num_parents = max(num_parents, 2)  # Ensure at least 2 parents
    parents = sorted_population[:num_parents]

    return parents


best_fitness_scores = []  # Initialize an empty list to store fitness scores

def main():
    population = create_initial_population(population_size)
    best_agent = None

    # Evaluate fitness of initial population
    for agent in population:
        agent.fitness = evaluate_fitness(agent)

    for generation in range(num_generations):
        # Find the best agent in the current generation
        best_agent_in_generation = max(population, key=lambda agent: agent.fitness)

        # Update the best agent if needed
        if best_agent is None or best_agent_in_generation.fitness > best_agent.fitness:
            best_agent = best_agent_in_generation

        # Append the best fitness score of the current generation to the list
        best_fitness_scores.append(best_agent.fitness)

        # Display the progress and best fitness score
        print(f"Generation {generation+1}/{num_generations} - Best Fitness: {best_agent.fitness}")

        # Evolve the population using selection, crossover, and mutation
        population = evolve_population(population)

        

    # Extract the genes of the best agent
    best_genes = best_agent.genes

    create_fitness_progress_plot(best_fitness_scores)

    # Simulate multiple games using the best agent's genes
    num_games = 10 
    for _ in range(num_games):
        main_game_loop(1, num_games=num_games)

def create_fitness_progress_plot(best_fitness_scores):
    # Plot the best fitness scores for each generation
    plt.plot(range(1, len(best_fitness_scores) + 1), best_fitness_scores, marker='o')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness Score')
    plt.title('Fitness Progress Over Generations')
    plt.grid(True)
    plt.show()



if __name__ == "__main__":
    main()