import cobra
import numpy as np
from scipy.optimize import minimize
from random import uniform, randint

# Load the metabolic model
model = cobra.io.read_sbml_model('model.xml')

# Define the objective function to maximize biomass production
def objective_function(fluxes):
    model.reactions.get_by_id('Biomass').upper_bound = fluxes[-1]
    solution = model.optimize()
    return -1 * solution.objective_value

# Define the bounds for the fluxes
bounds = []
for reaction in model.reactions:
    if reaction.id == 'Biomass':
        bounds.append((0, 1000))  # Set an upper bound for the biomass reaction
    else:
        bounds.append((reaction.lower_bound, reaction.upper_bound))

# Define the genetic algorithm
def genetic_algorithm(objective_function, bounds, generations=100, population_size=50, mutation_rate=0.1):
    best_solution = None
    best_fitness = np.inf
    population = np.zeros((population_size, len(bounds)))

    # Initialize the population with random fluxes within the bounds
    for i in range(population_size):
        for j in range(len(bounds)):
            population[i, j] = uniform(bounds[j][0], bounds[j][1])

    # Iterate over generations
    for generation in range(generations):
        # Evaluate the fitness of each individual in the population
        fitness = np.zeros(population_size)
        for i in range(population_size):
            fitness[i] = objective_function(population[i, :])

            # Check if the individual is the best solution so far
            if fitness[i] < best_fitness:
                best_solution = population[i, :]
                best_fitness = fitness[i]

        # Select the parents for the next generation
        parents = np.zeros((2, len(bounds)))
        for i in range(2):
            parent1 = population[randint(0, population_size - 1), :]
            parent2 = population[randint(0, population_size - 1), :]

            # Perform crossover
            crossover_point = randint(1, len(bounds) - 1)
            parents[i, :crossover_point] = parent1[:crossover_point]
            parents[i, crossover_point:] = parent2[crossover_point:]

            # Perform mutation
            for j in range(len(bounds)):
                if uniform(0, 1) < mutation_rate:
                    parents[i, j] = uniform(bounds[j][0], bounds[j][1])

        # Create the new generation by combining the parents
        population_new = np.zeros((population_size, len(bounds)))
        population_new[0, :] = best_solution
        for i in range(1, population_size):
            population_new[i, :] = parents[i % 2, :]

        population = population_new

    return best_solution, -1 * best_fitness

# Run the genetic algorithm to optimize biomass production
solution, objective_value = genetic_algorithm(objective_function, bounds)

# Print the optimal flux distribution and objective value
print('Optimal flux distribution:')
for i in range(len(model.reactions)):
    print(f'{model.reactions[i].id}: {solution[i]}')
print(f'Objective value: {objective_value}')
