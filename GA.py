import random
import numpy as np
from deap import base, creator, tools, algorithms

# Constants for the problem
PROCESS_TIMES = {'Product 1': {'Assembly': 2, 'Testing': 1, 'Packaging': 1},  # Time slots required
                 'Product 2': {'Assembly': 3, 'Testing': 2, 'Packaging': 1}}
DEMAND = {'Product 1': 30, 'Product 2': 20}
MACHINES = {'Assembly': 2, 'Testing': 2, 'Packaging': 2}
TIME_SLOTS = 32  # Total time slots available per day

# Genetic Algorithm Parameters
POP_SIZE = 100
CXPB, MUTPB, NGEN = 0.7, 0.2, 50  # Crossover probability, mutation probability, and number of generations
# Define fitness and individual
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Individual generator
def create_individual():
    schedule = []
    for product in PROCESS_TIMES:
        for process in PROCESS_TIMES[product]:
            for _ in range(DEMAND[product]):
                machine = random.randint(1, MACHINES[process])
                time_slot = random.randint(0, TIME_SLOTS - PROCESS_TIMES[product][process])
                schedule.append((product, process, machine, time_slot))
    return schedule

toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
# Fitness function to minimize makespan
def evaluate(individual):
    end_times = [0] * (TIME_SLOTS + 1)
    for item in individual:
        product, process, machine, start_time = item
        duration = PROCESS_TIMES[product][process]
        end_time = start_time + duration
        end_times[end_time] = max(end_times[end_time], end_time)
    makespan = max(end_times)
    return (makespan,)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
def main():
    random.seed(42)
    pop = toolbox.population(n=POP_SIZE)
    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=CXPB, mutpb=MUTPB, ngen=NGEN,
                                   stats=stats, halloffame=hof, verbose=True)

    return pop, log, hof

if __name__ == "__main__":
    pop, log, hof = main()
    best_ind = hof.items[0]
    print("Best schedule found:")
    print(best_ind)
    print("With makespan:", evaluate(best_ind)[0])