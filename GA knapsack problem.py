import random

# Data for the knapsack problem
items = [
    {'id': 1, 'weight': 12, 'value': 10},
    {'id': 2, 'weight': 5, 'value': 4},
    {'id': 3, 'weight': 4, 'value': 3},
    {'id': 4, 'weight': 9, 'value': 2},
    {'id': 5, 'weight': 7, 'value': 5},
    {'id': 6, 'weight': 11, 'value': 10},
    {'id': 7, 'weight': 15, 'value': 20},
    {'id': 8, 'weight': 6, 'value': 7},
    {'id': 9, 'weight': 3, 'value': 1},
    {'id': 10, 'weight': 2, 'value': 2},
]

# Problem constraints
max_weight = 25
population_size = 6
generations = 100
mutation_rate = 0.1

# Fitness function
def fitness(individual, items, max_weight):
    total_value = 0
    total_weight = 0
    for i in range(len(individual)):
        if individual[i] == 1:
            total_value += items[i]['value']
            total_weight += items[i]['weight']
    
    # Penalize if the total weight exceeds the capacity
    if total_weight > max_weight:
        return 0
    return total_value

# Create a random individual
def create_individual(n_items):
    return [random.randint(0, 1) for _ in range(n_items)]

# Create initial population
def create_population(pop_size, n_items):
    return [create_individual(n_items) for _ in range(pop_size)]

# Selection (tournament selection)
def selection(population, fitnesses):
    selected = random.choices(population, weights=fitnesses, k=2)
    return selected

# Crossover (single-point crossover)
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Mutation (flip bit with mutation rate)
def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = 1 - individual[i]  # Flip bit (0 -> 1 or 1 -> 0)
    return individual

# Evolve a population
def evolve_population(population, items, max_weight, mutation_rate):
    new_population = []
    fitnesses = [fitness(ind, items, max_weight) for ind in population]
    
    for _ in range(len(population) // 2):
        # Select two parents
        parent1, parent2 = selection(population, fitnesses)
        # Crossover to produce children
        child1, child2 = crossover(parent1, parent2)
        # Mutate the children
        child1 = mutate(child1, mutation_rate)
        child2 = mutate(child2, mutation_rate)
        # Add children to the new population
        new_population.extend([child1, child2])
    
    return new_population

# Run the genetic algorithm
def genetic_algorithm(items, max_weight, pop_size, generations, mutation_rate):
    n_items = len(items)
    population = create_population(pop_size, n_items)

    for generation in range(generations):
        population = evolve_population(population, items, max_weight, mutation_rate)
        # Calculate fitness of the best individual in the population
        best_individual = max(population, key=lambda ind: fitness(ind, items, max_weight))
        best_fitness = fitness(best_individual, items, max_weight)
        
        print(f"Generation {generation+1}: Best Fitness = {best_fitness}")
    
    return best_individual

# Execute the GA
best_solution = genetic_algorithm(items, max_weight, population_size, generations, mutation_rate)

# Display the best solution
print("\nBest Solution:")
print(f"Selected Items: {best_solution}")
total_weight = sum(items[i]['weight'] for i in range(len(best_solution)) if best_solution[i] == 1)
total_value = sum(items[i]['value'] for i in range(len(best_solution)) if best_solution[i] == 1)
print(f"Total Weight: {total_weight}, Total Value: {total_value}")
print("Hello, World!")