"""
Genetic algorithm to identify the solution that generates the flattest parabola
of the equation: y = ax^2 + bx + c

Source: https://www.datacamp.com/tutorial/genetic-algorithm-python
"""
import numpy as np
import matplotlib.pyplot as plt
import random
from prettytable import PrettyTable

# Quadratic equation being optimized
def quad_equation(x, a, b, c):
    return a*(x**2) + b*x + c


def fitness_function(params):
    a, b, c = params

    # Heavily penalize downward-facing curves
    if a < 0:
        return -float('inf')
    
    vertex_x = -b / (2*a)
    vertex_y = quad_equation(vertex_x, a, b, c)
    y_left = quad_equation(-1, a, b, c)
    y_right = quad_equation(1, a, b, c)

    curviness = abs(y_left - vertex_y) + abs(y_right - vertex_y)

    # Negative sign for minimization
    return -curviness


def create_init_population(size, lbound, ubound):
    population = []

    for _ in range(size):
        individual = (random.uniform(lbound, ubound),
                      random.uniform(lbound, ubound),
                      random.uniform(lbound, ubound))

        population.append(individual)
    
    return population


def selection(population, fitnesses, tournament_size=3):
    """
    Selects individuals based on fitness values from a random pool
    using tournament selection. Default value is 3
    """

    selected = []

    for _ in range(len(population)):
        tournament = random.sample(list(zip(population, fitnesses)), tournament_size)
        winner = max(tournament, key=lambda x: x[1])[0]
        selected.append(winner)
    
    return selected


def crossover(parent1, parent2):
    """
    Performs crossover/genetic recombination of two parents. Alpha is the 
    crossover probability between 0 and 1
    """

    alpha = random.random()

    child1 = tuple(alpha*p1 + (1-alpha)*p2 for p1, p2 in zip(parent1, parent2))
    child2 = tuple(alpha*p2 + (1-alpha)*p1 for p1, p2 in zip(parent1, parent2))

    return child1, child2


def mutation(individual, mutation_rate, lbound, ubound):
    individual = list(individual)

    for i in range(len(individual)):
        if random.random() < mutation_rate:
            mutation_amount = random.uniform(-1, 1)
            individual[i] += mutation_amount
            individual[i] = max(min(individual[i], ubound), lbound)

    return tuple(individual)


def genetic_algorithm(population_size, lbound, ubound, generations, mutation_rate, tournament_size):
    population = create_init_population(population_size, lbound, ubound)

    best_performers = []
    all_populations = []

    # Prepare for table
    table = PrettyTable()
    table.field_names = ["Generation", "a", "b", "c", "Fitness"]

    for generation in range(generations):
        fitnesses = [fitness_function(ind) for ind in population]

        # Store the best performer of the current generation
        best_individual = max(population, key=fitness_function)
        best_fitness = fitness_function(best_individual)
        best_performers.append((best_individual, best_fitness))
        all_populations.append(population[:])
        table.add_row([generation + 1, best_individual[0], best_individual[1], best_individual[2], best_fitness])

        population = selection(population, fitnesses, tournament_size)

        next_population = []
        for i in range(0, len(population), 2):
            parent1 = population[i]
            parent2 = population[i + 1]

            child1, child2 = crossover(parent1, parent2)

            next_population.append(mutation(child1, mutation_rate, lbound, ubound))
            next_population.append(mutation(child2, mutation_rate, lbound, ubound))

        # Replace the old population with the new one, preserving the best individual
        next_population[0] = best_individual
        population = next_population

    # Plot the population of one generation (last generation)
    final_population = all_populations[-1]
    final_fitnesses = [fitness_function(ind) for ind in final_population]

    return max(population, key=fitness_function), final_population, best_individual, best_performers, table


def main():
    population_size = 100
    lbound = -50
    ubound = 50
    generations = 20
    mutation_rate = 1
    tournament_size = 3

    best_solution = genetic_algorithm(population_size, lbound, ubound, generations, mutation_rate, tournament_size)
    print(f"Best solution found: a = {best_solution[0]}, b = {best_solution[1]}, c = {best_solution[2]}")


if __name__ == "__main__":
    main()