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
                        alpha,
                        neighborhood_radius,
                        animation):
    
    initial_solution = 30
    current_solution = initial_solution
    current_temperature = initial_temperature
    
    best_solution = initial_solution
    
    accepted_solutions = 0
    rejected_solutions = 0
    
    i=0
    while (current_temperature > 0.00001):
        current_neighborhood = get_neighborhood(current_solution, 
                                                neighborhood_radius)
        candidate_solution = get_random_point(current_neighborhood)
        
        
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
            current_solution = candidate_solution
            best_solution = candidate_solution
        else:
            r_value = rd.random()
            prob_to_accept = get_probability_to_accept(candidate_solution,
                                                       current_solution,
                                                       current_temperature)
            print(r_value)
            print(prob_to_accept)
            if (prob_to_accept > r_value):
                current_solution = candidate_solution
                accepted_solutions += 1
            else:
                rejected_solutions += 1
            
        i+=1
        current_temperature *= alpha
        
            

def get_probability_to_accept(candidate_solution,
                              current_solution,
                              temperature):
    exponential_numerator = f(current_solution) - f(candidate_solution)
    exponential_denominator = temperature
    probability = math.exp(exponential_numerator/exponential_denominator)
    return probability
    

def get_random_point(interval):
    return rd.uniform(interval[0], interval[1])


def get_neighborhood(point, radius):
    lower_bound = max(MIN_X, point-radius)
    upper_bound = min(MAX_X, point+radius)
    return [lower_bound, upper_bound] 


def plot_solution(best_solution, current_solution, candidate_solution, neighborhood):
    discretized_points = discretize_real_interval(X_DOMAIN, 400)
    function_points = get_function_points(discretized_points)
    
    discretized_neighborhood = discretize_real_interval(neighborhood, 25)
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
    
    
def main():
    animation = True
    if (animation):
        initial_temperature = 5000
        iterations = 1000
        neighborhood_radius = 10
        temperature_decrease = 0.97
        simulated_annealing(X_DOMAIN,
                            iterations,
                            initial_temperature,
                            temperature_decrease,
                            neighborhood_radius,
                            animation)
        
    
    
if __name__ == "__main__":
    main()