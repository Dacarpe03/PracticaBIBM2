# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 12:56:02 2022

@author: Daniel
"""
import math
import matplotlib.pyplot as plt

def f(x):
    return math.cos(x)/x


def discretize_real_interval(interval, n_points):
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
    
    
def main():
    discretized_points = discretize_real_interval([0.1, 30], 500)
    function_points = get_function_points(discretized_points)
    plt.plot(discretized_points, function_points, 'g-')
    plt.ylabel("f(x)")
    plt.xlabel("x")
    plt.show()
    
    
if __name__ == "__main__":
    main()