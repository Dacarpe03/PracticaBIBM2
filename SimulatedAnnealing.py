# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 12:56:02 2022

@author: Daniel
"""
import random as rd
import math
import matplotlib.pyplot as plt

MIN_X = 0.001
MAX_X = 30
X_DOMAIN = [MIN_X, MAX_X]

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
                        max_iterations, 
                        initial_temperature, 
                        neighborhood_radius):
    
    initial_solution = 30
    current_solution = initial_solution
    current_temperature = initial_temperature
    
    best_solution = initial_solution
    
    i=0
    while (current_temperature > 1):
        current_neighborhood = get_neighborhood(current_solution, 
                                                neighborhood_radius)
        print(current_neighborhood)
        candidate_solution = get_random_point(current_neighborhood)
        
        if (f(candidate_solution) < f(best_solution)):
            current_solution = candidate_solution
            best_solution = candidate_solution
        else:
            r_value = rd.random()
            prob_to_accept = get_probability_to_accept(candidate_solution,
                                                       current_solution,
                                                       current_temperature)
            if (prob_to_accept > r_value):
                current_solution = candidate_solution
            
        i+=1
        current_temperature *= 0.9
        print(best_solution)
        plot_solution(best_solution)
            

def get_probability_to_accept(candidate_solution,
                              best_solution,
                              temperature):
    exponential_numerator = f(best_solution) - f(candidate_solution)
    exponential_denominator = temperature
    probability = math.exp(-exponential_numerator/exponential_denominator)
    return probability
    

def get_random_point(interval):
    return rd.uniform(interval[0], interval[1])


def get_neighborhood(point, radius):
    lower_bound = max(MIN_X, point-radius)
    upper_bound = min(MAX_X, point+radius)
    return [lower_bound, upper_bound] 


def plot_solution(solution):
    discretized_points = discretize_real_interval(X_DOMAIN, 400)
    function_points = get_function_points(discretized_points)
    plt.plot(discretized_points, 
             function_points, 
             'g-')
    plt.scatter(solution, f(solution), marker='o', color='r', label="Solution")

    plt.ylabel("f(x)")
    plt.xlabel("x")
    plt.ylim(-1, 2)
    plt.xlim(0, 30)
    plt.show()
    
def main():
    initial_temperature = 5000
    iterations = 1000
    neighborhood_radius = 4
    simulated_annealing(X_DOMAIN,
                        iterations,
                        initial_temperature,
                        neighborhood_radius)
    
    
if __name__ == "__main__":
    main()