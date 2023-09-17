import random
import math
import json
import matplotlib.pyplot as plt
from PySnake import display_width, display_height, snake_block_size, generate_apple_position
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

best_fitness_scores = []

# Constants
num_genes = 3  # Change the number of genes to 3
population_size = 50
parent_selection_rate = 0.3
num_generations = 100
mutation_rate = 0.1

class AI:
    def __init__(self, genes):
        self.genes = {
            'apple_attraction': genes[0],
            'wall_repulsion': genes[1],
            'snake_repulsion': genes[2]
        }
        self.fitness = 0

        # Initialize the MLP model
        self.model = self.initialize_mlp()

    def initialize_mlp(self):
        # Create and configure the MLP model
        model = MLPClassifier(
            hidden_layer_sizes=(16, 16),  # Adjust the number of layers and neurons as needed
            activation='relu',  # You can choose different activation functions
            max_iter=1000,  # You can adjust the number of training iterations
        )

        # Fit the model to the training data
        model.fit(x_train, y_train)

        return model

    def determine_action(self, x1, y1, apple_x, apple_y, x1_change, y1_change, snake_list):
        # Extract features based on current state and genes
        features = [
            x1, y1, apple_x, apple_y, x1_change, y1_change,
            self.genes['apple_attraction'], self.genes['wall_repulsion'], self.genes['snake_repulsion']
        ]

        # Standardize the features (scaling)
        scaler = StandardScaler()
        scaled_features = scaler.transform([features])

        # Predict the best action using the fitted MLP model
        action_probabilities = self.model.predict_proba(scaled_features)[0]

        # Map predicted probabilities to actions
        actions = ["up", "down", "left", "right"]
        action = actions[action_probabilities.argmax()]

        return action

    
    def simulate_gameplay(self, apple_x, apple_y):
        # Initialize the game variables
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

def create_initial_population(population_size):
    initial_population = []
    for _ in range(population_size):
        # Initialize genes randomly within a specific range
        genes = [random.uniform(0.0, 1.0) for _ in range(num_genes)]
        initial_population.append(AI(genes))
    return initial_population

def mutate(agent):
    # Mutate an agent's genes with a certain probability
    for i in range(len(agent.genes)):
        if random.random() < mutation_rate:
            # Mutate the gene to a random value within a specific range
            agent.genes[i] = random.uniform(0.0, 1.0)  # Adjust the range as needed

def crossover(parent1, parent2):
    # Perform crossover between two parents' genes to create a new agent
    crossover_point = random.randint(1, len(parent1.genes) - 1)
    offspring_genes = parent1.genes[:crossover_point] + parent2.genes[crossover_point:]
    child = AI(offspring_genes)
    return child


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

    average_score = total_score / num_games

    return average_score

def main():
    # Create an initial population
    population = create_initial_population(population_size)
    best_agent = None

    # Main evolution loop
    for generation in range(num_generations):
        # Evaluate fitness for the initial population
        for agent in population:
            agent.fitness = evaluate_fitness(agent)

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
