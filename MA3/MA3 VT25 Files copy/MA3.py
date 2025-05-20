""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc

def approximate_pi(n): # Ex1
    #n is the number of points
    # Write your code here
    n_in = 0
    plt.figure(figsize=(7, 7))
    for _ in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if (x**2+y**2) <= 1:
            plt.plot(x, y, 'r.')
            n_in += 1
        else:
            plt.plot(x, y, 'b.')
    plt.show()
    return  4*n_in/n

def sphere_volume(n, d): #Ex2, approximation
    #n is the number of points
    # d is the number of dimensions of the sphere 
    points = [[random.uniform(-1, 1) for _ in range(d)] for _ in range(n)]

    points_sq = map(lambda x: sum(map(lambda x:x**2, x)), points)

    n_in = len(list(filter(lambda x: x<1, points_sq)))

    return n_in/n * 2**d

def hypersphere_exact(n,d): #Ex2, real value
     #n is the number of points
    # d is the number of dimensions of the sphere 
    return m.pi**(d/2)/(m.gamma(d/2+1))

#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n,d,np=10):
    # n is the number of points
    # d is the number of dimensions of the sphere
    # np is the number of processes
    with future.ProcessPoolExecutor() as executor:
        futures = [executor.submit(sphere_volume, n, d) for _ in range(np)]
        results = [f.result() for f in future.as_completed(futures)]
    volume = sum(results) / len(results)
    return volume
    

#Ex4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n,d,np=10):
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    partition = n // np
    with future.ProcessPoolExecutor() as ex:
        results = [ex.submit(sphere_volume, partition, d) for _ in range(np)]

        vol = []
        for r in results:
            vol += [r.result()]
    
    return sum(vol)/np
    
def main():
    #Ex1
    """dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)"""
    #Ex2
    n = 100000
    d = 2
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)} vs approximated = {sphere_volume(n,d)}")

    n = 100000
    d = 11
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)} vs approximated = {sphere_volume(n,d)}")

    #Ex3
    n = 100000
    d = 11
    vol = []
    np = 2
    start = pc()
    for y in range (np):
        vol.append(sphere_volume(n,d))
    stop = pc()
    print(f"Ex3: Sequential time of {d}-dim and {n} points: {stop-start}")
    print(f'with average volume {sum(vol)/len(vol)}')
    print("What is parallel time?")
    start = pc()
    vol = sphere_volume_parallel1(n, d, np)
    stop = pc()
    print(f"Ex3: Parallel time of {d}-dim and {n} points: {stop-start}")
    print(f'with average volume {vol}')
    print()

    #Ex4
    n = 100000
    d = 11
    np = 2
    start = pc()
    vol = sphere_volume(n,d)
    stop = pc()
    print(f"Ex3: Sequential time of {d} and {n}: {stop-start}")
    print(f'with average volume {vol}')

    print("What is parallel time?")
    start = pc()
    vol = sphere_volume_parallel2(n, d, np)
    stop = pc()
    print(f"Ex3: Parallel time of {d} and {n}: {stop-start}")
    print(f'with average volume {vol}')
    

if __name__ == '__main__':
	main()
