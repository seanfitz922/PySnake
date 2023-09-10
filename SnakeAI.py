import random, math, json
import matplotlib.pyplot as plt
from PySnake import display_width, display_height, snake_block_size, generate_apple_position

best_fitness_scores = []

class AI:
    def __init__(self, genes):
        self.genes = genes
        self.fitness = 0

    def bearing(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1

        angle = math.atan2(dy, dx)
        if angle < 0:
            # Ensure angle is in the range [0, 2*pi]
            angle += 2 * math.pi  

        return angle

    def determine_action(self, snake_x, snake_y, apple_x, apple_y, x_change, y_change, snake_list):
        # Calculate the bearing between snake head and apple
        bearing_to_apple = self.bearing(snake_x, snake_y, apple_x, apple_y)

        # Initialize a list of valid actions
        valid_actions = []

        # Determine the current direction the snake is moving
        if x_change == snake_block_size:
            current_direction = "right"
        elif x_change == -snake_block_size:
            current_direction = "left"
        elif y_change == snake_block_size:
            current_direction = "down"
        elif y_change == -snake_block_size:
            current_direction = "up"
        else:
            current_direction = None  # Snake is not moving

        # Add actions that do not lead to running into itself
        if current_direction != "left":
            valid_actions.append("right")
        if current_direction != "right":
            valid_actions.append("left")
        if current_direction != "up":
            valid_actions.append("down")
        if current_direction != "down":
            valid_actions.append("up")

        # Check for potential self-collision and remove invalid actions
        for action in valid_actions[:]:
            if self.will_collide(snake_x, snake_y, action, snake_list):
                valid_actions.remove(action)

        # Choose the action based on the bearing
        if 0 <= bearing_to_apple < math.pi / 4:
            action = "right"
        elif math.pi / 4 <= bearing_to_apple < 3 * math.pi / 4:
            action = "down"
        elif 3 * math.pi / 4 <= bearing_to_apple < 5 * math.pi / 4:
            action = "left"
        else:
            action = "up"

        # If the chosen action is valid, use. Else, choose a random valid action
        if action in valid_actions:
            return action
        else:
            return random.choice(valid_actions)

    def will_collide(self, snake_x, snake_y, action, snake_list):
        # Simulate the move before making it
        if action == "up":
            new_x, new_y = snake_x, snake_y - snake_block_size
        elif action == "down":
            new_x, new_y = snake_x, snake_y + snake_block_size
        elif action == "left":
            new_x, new_y = snake_x - snake_block_size, snake_y
        elif action == "right":
            new_x, new_y = snake_x + snake_block_size, snake_y

        # Check if the new position would collide with the snake's body
        # Exclude the snake's head
        for segment in snake_list[:-1]:  
            if (new_x, new_y) == segment:
                return True

        return False
    def simulate_gameplay(self, apple_x, apple_y):
        game_over_flag = False
        x, y = display_width / 2, display_height / 2
        snake_list = []
        length_of_snake = 1
        x_change, y_change = 0, 0

        while not game_over_flag:
            snake_head = [x, y]
            snake_list.append(snake_head)

            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for segment in snake_list[:-1]:
                if segment == snake_head:
                    game_over_flag = True

            # Use the determine_action method to select action
            agent_action = self.determine_action(x, y, apple_x, apple_y, x_change, y_change, snake_list)

            if agent_action == "up":
                y_change, x_change = -snake_block_size, 0
            elif agent_action == "down":
                y_change, x_change = snake_block_size, 0
            elif agent_action == "left":
                y_change, x_change = 0, -snake_block_size
            elif agent_action == "right":
                y_change, x_change = 0, snake_block_size

            x += x_change
            y += y_change

            if x >= display_width or x < 0 or y >= display_height or y < 0:
                game_over_flag = True

            if (x, y) == (apple_x, apple_y):
                apple_x, apple_y = generate_apple_position()
                length_of_snake += 1

        return length_of_snake - 1

# Constants
num_genes = 4
population_size = 50
parent_selection_rate = 0.3
num_generations = 100
mutation_rate = 0.1

def create_initial_population(population_size):
    # Create an initial population of AI agents with random genes
    initial_population = []
    for _ in range(population_size):
        genes = [random.choice(["up", "down", "left", "right"]) for _ in range(num_genes)]
        initial_population.append(AI(genes))
    return initial_population

def mutate(agent):
    # Mutate an agent's genes with a certain probability
    for i in range(len(agent.genes)):
        if random.random() < mutation_rate:
            agent.genes[i] = random.choice(["up", "down", "left", "right"])

def crossover(parent1, parent2):
    # Perform crossover between two parents' genes to create a new agent
    crossover_point = random.randint(1, len(parent1.genes) - 1)
    offspring_genes = parent1.genes[:crossover_point] + parent2.genes[crossover_point:]
    return AI(offspring_genes)

def evolve_population(current_population):
    # Evaluate fitness for each AI agent in the population
    for agent in current_population:
        agent.fitness = evaluate_fitness(agent)

    # Sort the population by fitness in descending order
    sorted_population = sorted(current_population, key=lambda agent: agent.fitness, reverse=True)

    # Select the top-performing parents for reproduction
    num_parents = int(len(current_population) * parent_selection_rate)
    num_parents -= num_parents % 2
    num_parents = max(num_parents, 2)
    parents = sorted_population[:num_parents]

    offspring = []

    # Perform crossover and mutation on selected parents to create offspring
    while len(offspring) < len(current_population) - num_parents:
        parent1, parent2 = random.sample(parents, 2)
        child = crossover(parent1, parent2)
        mutate(child)
        offspring.append(child)

    # Combine parents and offspring to create the next generation
    next_generation = parents + offspring

    return next_generation

def evaluate_fitness(agent, num_games=10):
    # Evaluate the fitness of an AI agent by simulating gameplay
    total_score = 0
    for _ in range(num_games):
        apple_x, apple_y = generate_apple_position()
        total_score += agent.simulate_gameplay(apple_x, apple_y)

    average_score = total_score 

    return average_score

def main():
    # Create an initial population
    population = create_initial_population(population_size)
    best_agent = None

    # Evaluate fitness for the initial population
    for agent in population:
        agent.fitness = evaluate_fitness(agent)

    # Main evolution loop
    for generation in range(num_generations):
        # Find the best agent in the current generation
        best_agent_in_generation = max(population, key=lambda agent: agent.fitness)

        # Update the best agent if needed
        if best_agent is None or best_agent_in_generation.fitness > best_agent.fitness:
            best_agent = best_agent_in_generation

        # Append the best fitness score of the current generation to the list
        best_fitness_scores.append(best_agent.fitness)

        # Display progress and best fitness score
        print(f"Generation {generation+1}/{num_generations} - Best Fitness: {best_agent.fitness}")

        # Evolve the population using selection, crossover, and mutation
        population = evolve_population(population)

    # Extract the genes of the best agent
    best_genes = best_agent.genes

    # Save the best genes to a JSON file
    with open('best_genes.json', 'w') as file:
        json.dump(best_genes, file)

    # Create a fitness progress plot
    create_fitness_progress_plot(best_fitness_scores)

    # Simulate multiple games using the best agent's genes
    num_games_to_simulate = 10 
    for i in range(num_games_to_simulate):
        apple_x, apple_y = generate_apple_position()
        score = best_agent.simulate_gameplay(apple_x, apple_y)
        print(f"Game {i+1}/{num_games_to_simulate} - Score: {score}")


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

