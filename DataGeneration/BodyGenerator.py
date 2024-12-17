#!/usr/bin/env python3

import numpy as np

def export_nbody_to_file(filename, masses, positions, velocities):
    """
    Exports N-body data to a text file where each line contains:
    mass, x, y, z, vx, vy, vz
    """
    with open(filename, 'w') as f:
        f.write("# mass x y z vx vy vz\n")
        for i in range(len(masses)):
            mass = masses[i]
            x, y, z = positions[i]
            vx, vy, vz = velocities[i]
            line = f"{mass:.9e} {x:.9e} {y:.9e} {z:.9e} {vx:.9e} {vy:.9e} {vz:.9e}\n"
            f.write(line)
    print(f"Exported N-body data to {filename}")

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
    Returns names, positions (AU), velocities (AU/day), and masses (kg) 
    for the Sun + 8 major planets on Jan 1, 2023 (heliocentric frame).
    """
    names = [
        "Sun", "Mercury", "Venus", "Earth", 
        "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"
    ]
    
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
    
    # Approx Jan 1, 2023 positions in AU and velocities in AU/day 
    # Data from an approximate ephemeris (NASA JPL Horizons).
    initial_data = np.array([
        # Sun
        [  0.0,          0.0,          0.0,           0.0,         0.0,         0.0       ],
        # Mercury
        [  1.2697e-01,   2.5334e-01,   1.2217e-01,   -3.1264e-02,  1.0078e-02,  8.6239e-03],        #FIXED
        # Venus
        [  4.4553e-02,  -7.2519e-01,  -1.0596e-02,    2.0053e-02,  1.3797e-03, -1.1440e-03],
        # Earth
        [ -1.7283e-01,   9.6613e-01,   4.0910e-05,   -1.7231e-02, -3.0671e-03, -8.5525e-07],
        # Mars
        [  1.3948e+00,  -2.4861e-01,  -4.0429e-02,    3.9098e-03,  1.4138e-02,  2.7986e-04],
        # Jupiter
        [  3.9820e+00,  -3.1462e+00,  -6.6743e-02,    4.4883e-03,  5.7381e-03, -1.0581e-04],
        # Saturn
        [  6.4487e+00,  -7.6007e+00,  -1.8828e-01,    3.8546e-03,  3.4029e-03, -2.1316e-04],
        # Uranus
        [  1.4046e+01,   1.2824e+01,  -1.2851e-01,   -2.5057e-03,  2.6807e-03,  4.6748e-05],
        # Neptune
        [  2.9754e+01,  -4.5290e-01,  -5.5911e-01,    4.4692e-04,  3.1026e-03, -8.0777e-05]
    ])
    
    positions = initial_data[:, 0:3]
    velocities = initial_data[:, 3:6]
    
    return names, positions, velocities, masses_kg

def main():

    AllN = [100, 1000, 10000, 100000]

    for N in AllN: 
        # 1) Random N-body
        rand_pos, rand_vel, rand_m = generate_random_nbody(
            N=N, box_size=100.0, v_max=20.0, mass_min=1.0, mass_max=100.0
        )
        filestring = f"random_{N}_body.txt"
        export_nbody_to_file(filestring, rand_m, rand_pos, rand_vel)

        # 2) Stable Orbits
        stable_pos, stable_vel, stable_m = generate_stable_orbits(
            N=N, radius=500.0, central_mass=1e7
        )
        filestring = f"stable_orbits_{N}_body.txt"
        export_nbody_to_file(filestring, stable_m, stable_pos, stable_vel)

        # 3) Binary System + Debris
        binary_pos, binary_vel, binary_m = generate_binary_system_with_debris(
            N=N, star_mass1=2e4, star_mass2=3e4, star_separation=80.0, debris_count=N-2, debris_radius=200.0
        )
        filestring = f"binary_debris_{N}_body.txt"
        export_nbody_to_file(filestring, binary_m, binary_pos, binary_vel)

    # 4) Solar System (Jan 1, 2023)
    ss_names, ss_pos, ss_vel, ss_m = generate_solar_system_2023_01_01()
    export_nbody_to_file("solar_system_2023_01_01.txt", ss_m, ss_pos, ss_vel)
    

if __name__ == "__main__":
    main()
