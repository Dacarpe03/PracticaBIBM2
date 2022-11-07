# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 15:37:24 2022

@author: Daniel
"""

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt



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


def set_interval(value):
    if 0 < value <= 5:
        return "[0,5]"
    if 5 < value <= 10:
        return "[05,10]"
    if 10 < value <= 15:
        return "[10,15]"
    if 15 < value <= 20:
        return "[15,20]"
    if 20 < value <= 25:
        return "[20,25]"
    if 25 < value <= 30:
        return "[25,30]"
    else:
        return ""
    
def main():
    
    initial_temperatures = [25, 100, 200, 500, 2500, 5000]
    neighborhood_radiuses = [1, 2, 5, 10]
    temperature_decrease = [0.8, 0.85, 0.9, 0.99]
    
    
    dataframe = pd.read_csv(FILENAME)
    dataframe.neighborhood_radius = dataframe.neighborhood_radius.astype(int)
    
    for temp in initial_temperatures:
        
        problem_dataframe = dataframe[dataframe.initial_temperature == temp]
        
        solutions_box_plot = problem_dataframe.boxplot(column=BEST_SOLUTION,
                                                       by=[NEIGHBOR_RADIUS, TEMP_DECREASE],
                                                       rot=45, 
                                                       showfliers=True)
        plt.suptitle('')
        solutions_box_plot.set_title(f"Solutions with T={temp}º")
        solutions_box_plot.set_xlabel("(Neighborhood radius, alpha)")
        solutions_box_plot.set_ylabel("Best solution")
        
    dataframe['interval'] = dataframe.initial_solution.apply(set_interval)
    
    for temp in initial_temperatures:
            
        problem_dataframe = dataframe[dataframe.initial_temperature == temp]
        print(problem_dataframe.initial_temperature)
        for radius in neighborhood_radiuses:
            subproblem_dataframe = problem_dataframe[problem_dataframe.neighborhood_radius == radius]
            solutions_box_plot = subproblem_dataframe.boxplot(column=BEST_SOLUTION,
                                                              by=['interval'],
                                                              rot=45, 
                                                              showfliers=True)
            plt.suptitle('')
            solutions_box_plot.set_title(f"Radius={radius} and T={temp}º")
            solutions_box_plot.set_xlabel("Interval")
            solutions_box_plot.set_ylabel("Best solution")

        
    
if __name__ == "__main__":
    main()