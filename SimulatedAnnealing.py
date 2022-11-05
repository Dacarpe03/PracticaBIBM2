# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 12:56:02 2022

@author: Daniel
"""
import random as rd
import math
import matplotlib.pyplot as plt
import pandas as pd

MIN_X = 0.001
MAX_X = 30
X_DOMAIN = [MIN_X, MAX_X]

FILENAME = "simulated_annealing_results_analysis.csv"
# .csv column names
INITIAL_TEMPERATURE = "initial_temperature"
INITIAL_SOLUTION = "initial_solution"
NEIGHBOR_RADIUS = "neighborhood_radius"
TEMP_DECREASE = "temperature_decrease"
BEST_SOLUTION = "best_solution"
FINAL_SOLUTION = "final_solution"

CSV_COLUMNS = {
    INITIAL_TEMPERATURE: [],
    TEMP_DECREASE: [],
    NEIGHBOR_RADIUS: [],
    INITIAL_SOLUTION: [],
    BEST_SOLUTION: [],
    FINAL_SOLUTION: []
    }

def f(x):
    return math.cos(x)/x



def discretize_real_interval(interval,
                             n_points):
    
    offset = (interval[1]-interval[0])/n_points
    discretized_interval = []
    current_point = interval[0]
    while current_point <= interval[1]:
        discretized_interval.append(current_point)
        current_point += offset
    return discretized_interval


def get_function_points(discretized_interval):
    function_points = []
    for point in discretized_interval:
        function_points.append(f(point))
    return function_points
    

def simulated_annealing(interval,
                        initial_temperature,
                        alpha,
                        neighborhood_radius,
                        animation,
                        statistics):
    
    initial_solution = get_random_point(X_DOMAIN)
    current_solution = initial_solution
    current_temperature = initial_temperature
    
    best_solution = initial_solution
    
    accepted_solutions = 0
    rejected_solutions = 0
    
    temperatures = []
    probabilities = []
    
    i=0
    while (current_temperature > 0.00001):
        current_neighborhood = get_neighborhood(current_solution, 
                                                neighborhood_radius)
        candidate_solution = get_random_point(current_neighborhood)
        
        
        if (animation):
            plot_solution(best_solution, 
                          current_solution, 
                          candidate_solution,
                          current_neighborhood)
        
        print(f"Iteration {i}:\n"
              f"    Best solution: {best_solution}\n"
              f"    Current_solution: {current_solution}\n"
              f"    Candidate_solution: {candidate_solution}\n"
              f"    Current_temperature: {current_temperature}\n"
              f"    Accepted solutions: {accepted_solutions}\n"
              f"    Rejected solutions: {rejected_solutions}")
        
        if (f(candidate_solution) < f(best_solution)):
            print("Acceptance probability: 1")
            current_solution = candidate_solution
            best_solution = candidate_solution
        else:
            r_value = rd.random()
            prob_to_accept = get_probability_to_accept(candidate_solution,
                                                       current_solution,
                                                       current_temperature)
            print(f"    Acceptance probability: {prob_to_accept}")
            temperatures.append(current_temperature)
            probabilities.append(prob_to_accept)
            
            if (prob_to_accept > r_value):
                current_solution = candidate_solution
                accepted_solutions += 1
            else:
                rejected_solutions += 1
            
        i+=1
        current_temperature *= alpha
        
    return temperatures, probabilities, initial_solution, best_solution, current_solution
            

def get_probability_to_accept(candidate_solution,
                              current_solution,
                              temperature):
    try:
        exponential_numerator = f(current_solution) - f(candidate_solution)
        exponential_denominator = temperature
        probability = math.exp(exponential_numerator/exponential_denominator)
        return min(1, probability)
    except OverflowError:
        return 1

def get_random_point(interval):
    return rd.uniform(interval[0], interval[1])


def get_neighborhood(point, radius):
    lower_bound = max(MIN_X, point-radius)
    upper_bound = min(MAX_X, point+radius)
    return [lower_bound, upper_bound] 


def plot_solution(best_solution, current_solution, candidate_solution, neighborhood):
    discretized_points = discretize_real_interval(X_DOMAIN, 400)
    function_points = get_function_points(discretized_points)
    
    discretized_neighborhood = discretize_real_interval(neighborhood, 40)
    neighborhood_points =  get_function_points(discretized_neighborhood)
    
    plt.scatter(best_solution,
                f(best_solution), 
                marker='o', 
                color='r', 
                label="Solution")
    
    plt.scatter(current_solution,
                f(current_solution), 
                marker='s', 
                color='m', 
                label="Current solution")
    
    plt.scatter(candidate_solution,
                f(candidate_solution), 
                marker='^', 
                color='y', 
                label="Candidate solution")
    
    plt.plot(discretized_points, 
             function_points, 
             'g-',
             label='f')
    
    plt.plot(discretized_neighborhood, 
             neighborhood_points, 
             'b-',
             label='Neighborhood')
    
    plt.ylabel("f(x)")
    plt.xlabel("x")
    plt.ylim(-1, 2)
    plt.xlim(0, 30)
    plt.legend()
    plt.show()
    
    
def plot_probs(temps, probs, lim):
    plt.title("Probability over temperature")
    plt.plot(temps, 
             probs, 
             'g-',
             label='f')
    plt.ylabel("Probability to accept")
    plt.xlabel("Temperature")
    plt.gca().invert_xaxis()
    plt.xlim(0,lim)
    

def create_csv():
    dataframe = pd.DataFrame(CSV_COLUMNS)
    dataframe.to_csv(FILENAME, index=False)
    
    
def main():
    analysis_dataframe  = pd.read_csv(FILENAME)


    animation = False
    statistics = True
    initial_temperatures = [25, 100, 200, 500, 2500, 5000]
    neighborhood_radiuses = [1, 2, 5, 10]
    temperature_decrease = [0.8, 0.85, 0.9, 0.99]
    
    for initial_temp in initial_temperatures:
        for neighbor_radius in neighborhood_radiuses:
            for temp_decrease in temperature_decrease:
                for i in range(50):
                    temps, probs, initial_sol, best_sol, final_sol = simulated_annealing(X_DOMAIN,
                                                                                         initial_temp,
                                                                                         temp_decrease,
                                                                                         neighbor_radius,
                                                                                         animation,
                                                                                         statistics)
                    if statistics:
                        analysis_dataframe.loc[len(analysis_dataframe)] = [initial_temp,
                                                                           temp_decrease,
                                                                           neighbor_radius,
                                                                           initial_sol,
                                                                           best_sol,
                                                                           final_sol]
                        
                        analysis_dataframe.to_csv(FILENAME, index=False)
                    if animation:
                        plot_probs(temps, probs, 5)
                        plot_probs(temps, probs, 25)
    
if __name__ == "__main__":
    main()