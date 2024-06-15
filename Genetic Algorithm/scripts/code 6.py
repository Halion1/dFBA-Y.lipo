# Import necessary packages
import numpy as np
import cobra.test
import cobra.flux_analysis
import pygad

# Load a metabolic model
model = cobra.test.create_test_model("textbook")

# Define the objective function
def objective_function(solution, solution_idx):
    model.reactions.get_by_id("Biomass_Ecoli_core").upper_bound = solution[0]
    model.reactions.get_by_id("Biomass_Ecoli_core").lower_bound = solution[0]
    solution = model.optimize()
    fitness = -solution.objective_value
    return fitness

# Define the bounds for the biomass reaction
bounds = [{"lower_bound": 0, "upper_bound": 1000}]

# Define the GA parameters
num_generations = 100
mutation_rate = 0.1
num_parents_mating = 4

# Initialize the GA
ga_instance = pygad.GA(num_generations=num_generations, num_parents_mating=num_parents_mating, 
                       fitness_func=objective_function, sol_per_pop=50, num_genes=1, 
                       gene_type=float, gene_space=bounds, mutation_percent_genes=mutation_rate)

# Run the GA
ga_instance.run()

# Print the best solution
best_solution = ga_instance.best_solution()
best_fitness = -ga_instance.best_solution()[1]
print("Best biomass flux: ", best_solution[0])

# Set the biomass reaction flux to the optimal value
model.reactions.get_by_id("Biomass_Ecoli_core").upper_bound = best_solution[0]
model.reactions.get_by_id("Biomass_Ecoli_core").lower_bound = best_solution[0]

# Run FBA with the optimal biomass flux
solution = cobra.flux_analysis.parsimonious.optimize_minimal_flux(model)
print("Optimal objective value: ", -solution.objective_value)
