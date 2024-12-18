#!/usr/local/bin python3

import numpy as np
import os
import csv

def export_nbody_to_file(filename, masses, positions, velocities, N):
    """
    Exports N-body data to a text file where each line contains:
    mass, x, y, z, vx, vy, vz
    """
    
    if filename == "solar_system_2023_01_01.csv":
        directory = os.path.join("..", "data")
    else:
        directory = os.path.join("..", "data", str(N))
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = os.path.join(directory, filename)

    N = len(masses)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write a header row (optional)
        writer.writerow(["mass", "x", "y", "z", "vx", "vy", "vz"])
        
        for i in range(N):
            row = [
                masses[i],
                positions[i,0], positions[i,1], positions[i,2],
                velocities[i,0], velocities[i,1], velocities[i,2]
            ]
            writer.writerow(row)
    print(f"Exported {N} bodies to {filename}")

def generate_random_nbody(N=100, box_size=100.0, v_max=1.0, 
                          mass_min=1.0, mass_max=10.0):
    """
    Generate initial conditions for an N-body system with randomized positions, velocities, and masses.
    """
    
    positions = np.random.uniform(-box_size, box_size, size=(N, 3))
    velocities = np.random.uniform(-v_max, v_max, size=(N, 3))
    masses = np.random.uniform(mass_min, mass_max, size=(N,))
    
    return positions, velocities, masses

def generate_stable_orbits(N=10, radius=50.0, central_mass=1e5):
    """
    Generate initial conditions for an N-body system in stable circular orbits 
    around a central massive body.
    """
    if N < 2:
        raise ValueError("N must be >= 2")
    
    G = 1.0
    positions = np.zeros((N, 3))
    velocities = np.zeros((N, 3))
    masses = np.zeros(N)
    
    masses[0] = central_mass
    positions[0] = np.array([0,0,0])
    velocities[0] = np.array([0,0,0])
    
    orbiting_bodies = N - 1
    for i in range(orbiting_bodies):        # Create velocities tangential to the orbit
        angle = 2.0 * np.pi * i / orbiting_bodies
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        z = 0.0
        
        positions[i+1] = np.array([x, y, z])
        masses[i+1] = 1.0
        
        v_circ = np.sqrt(G * central_mass / radius)
        vx = -v_circ * np.sin(angle)
        vy =  v_circ * np.cos(angle)
        vz = 0.0
        velocities[i+1] = np.array([vx, vy, vz])
    
    return positions, velocities, masses

def generate_binary_system_with_debris(N=50, star_mass1=5e4, star_mass2=5e4, 
                                       star_separation=100.0, debris_count=48, 
                                       debris_radius=300.0):
    """
    Generate a binary star system plus small debris bodies swirling around them.
    """
    if N != (2 + debris_count):
        raise ValueError("N must be 2 + debris_count.")
        
    G = 1.0
    positions = np.zeros((N, 3))
    velocities = np.zeros((N, 3))
    masses = np.zeros(N)
    
    total_mass = star_mass1 + star_mass2
    r1 = star_separation * (star_mass2 / total_mass)
    r2 = star_separation * (star_mass1 / total_mass)
    
    positions[0] = np.array([+r1, 0, 0])
    positions[1] = np.array([-r2, 0, 0])
    masses[0] = star_mass1
    masses[1] = star_mass2
    
    v_star1 = np.sqrt(G * star_mass2 / star_separation)
    v_star2 = np.sqrt(G * star_mass1 / star_separation)
    velocities[0] = np.array([0, +v_star1, 0])
    velocities[1] = np.array([0, -v_star2, 0])
    
    for i in range(debris_count):
        idx = i + 2
        radius = np.random.uniform(star_separation * 1.2, debris_radius)
        theta = np.random.uniform(0, 2*np.pi)
        phi = np.random.uniform(0, np.pi)
        
        x = radius * np.sin(phi) * np.cos(theta)
        y = radius * np.sin(phi) * np.sin(theta)
        z = radius * np.cos(phi)
        positions[idx] = np.array([x, y, z])
        
        masses[idx] = 1.0
        
        r_vec = positions[idx]
        r = np.linalg.norm(r_vec)
        v_debris = np.sqrt(G * total_mass / r)
        
        z_hat = np.array([0, 0, 1])
        tangential = np.cross(r_vec, z_hat)
        norm_tan = np.linalg.norm(tangential)
        if norm_tan < 1e-8:
            tangential = np.cross(r_vec, np.array([0,1,0]))
            norm_tan = np.linalg.norm(tangential)
        tangential /= norm_tan
        
        velocities[idx] = v_debris * tangential
    
    return positions, velocities, masses

def generate_solar_system_2023_01_01():
    """
    Returns names, positions (Km), velocities (Km/day), and masses (kg) 
    for the Sun + 8 major planets on Jan 1, 2023 (heliocentric frame).
    """
    
    masses_kg = np.array([
        1.98847e30,  # Sun
        3.3011e23,   # Mercury
        4.8675e24,   # Venus
        5.97237e24,  # Earth
        6.4171e23,   # Mars
        1.8982e27,   # Jupiter
        5.6834e26,   # Saturn
        8.6810e25,   # Uranus
        1.02409e26   # Neptune
    ])
    
    # Approx Jan 1, 2023 positions in Km and velocities in Km/day 
    # Data from an approximate ephemeris (NASA JPL Horizons).
    initial_data = np.array([
        # Sun
        [  0.0,          0.0,          0.0,           0.0,         0.0,         0.0       ],
        # Mercury
        [  1.89949e+07,   3.78989e+07,   1.82768e+07,   -4.67707e+06,  1.50758e+06,  1.29011e+06],
        # Venus
        [  8.39493e+07,  -6.11597e+07,  -3.28308e+07,    1.90494e+06,  2.16291e+06,  8.52698e+05],
        # Earth
        [ -2.54699e+07,   1.32931e+08,   5.76246e+07,   -2.57614e+06, -4.18553e+05, -1.81525e+05],
        # Mars
        [  9.10721e+06,   2.12633e+08,   9.72845e+07,   -2.01254e+06,  2.16137e+05,  1.53438e+05],
        # Jupiter
        [  7.23788e+08,   1.50162e+08,   4.67454e+07,   -2.51843e+05,  1.06185e+06,  4.61269e+05],
        # Saturn
        [  1.21883e+09,  -7.41999e+08,  -3.58956e+08,    4.20866e+05,  6.45417e+05,  2.48481e+05],
        # Uranus
        [  2.00008e+09,   1.98729e+09,   8.42074e+08,   -4.36135e+05,  3.40087e+05,  1.55103e+05],
        # Neptune
        [  4.45216e+09,  -3.66703e+08,  -2.60937e+08,    4.29981e+04,  4.36848e+05,  1.77795e+05]
    ])
    
    positions = initial_data[:, 0:3]
    velocities = initial_data[:, 3:6]
    
    return positions, velocities, masses_kg

def main():

    AllN = [100, 1000, 10000, 100000]
    # AllN = [100]

    for N in AllN: 
        # 1) Random N-body
        rand_pos, rand_vel, rand_m = generate_random_nbody(
            N=N, box_size=100.0, v_max=20.0, mass_min=1.0, mass_max=100.0
        )
        filestring = f"random_{N}_body.csv"
        export_nbody_to_file(filestring, rand_m, rand_pos, rand_vel, N)

        # 2) Stable Orbits
        stable_pos, stable_vel, stable_m = generate_stable_orbits(
            N=N, radius=500.0, central_mass=1e7
        )
        filestring = f"stable_orbits_{N}_body.csv"
        export_nbody_to_file(filestring, stable_m, stable_pos, stable_vel, N)

        # 3) Binary System + Debris
        binary_pos, binary_vel, binary_m = generate_binary_system_with_debris(
            N=N, star_mass1=2e4, star_mass2=3e4, star_separation=80.0, debris_count=N-2, debris_radius=200.0
        )
        filestring = f"binary_debris_{N}_body.csv"
        export_nbody_to_file(filestring, binary_m, binary_pos, binary_vel, N)

    # 4) Solar System (Jan 1, 2023)
    ss_pos, ss_vel, ss_m = generate_solar_system_2023_01_01()
    export_nbody_to_file("solar_system_2023_01_01.csv", ss_m, ss_pos, ss_vel, 9)
    

if __name__ == "__main__":
    main()
