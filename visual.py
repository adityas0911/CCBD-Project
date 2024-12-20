import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Simulation Parameters
G = 4.9823e-10  # Gravitational constant
dt = 1.0  # Time step (days)
steps = 365  # Number of steps
softening = 1e-18  # Softening factor to prevent singularities

# Load bodies from a CSV file
def load_bodies_from_csv(filename):
    data = np.genfromtxt(filename, delimiter=',', skip_header=1)
    masses = data[:, 0]
    positions = data[:, 1:4]
    velocities = data[:, 4:7]
    return masses, positions, velocities

# Compute accelerations
def compute_accelerations(masses, positions):
    n = len(masses)
    accelerations = np.zeros_like(positions)

    for i in range(n):
        for j in range(n):
            if i != j:
                diff = positions[j] - positions[i]
                dist_sqr = np.dot(diff, diff) + softening
                dist = np.sqrt(dist_sqr)
                force = G * masses[j] / dist_sqr
                accelerations[i] += force * diff / dist
    return accelerations

# Update positions and velocities
def update_bodies(masses, positions, velocities):
    accelerations = compute_accelerations(masses, positions)
    velocities += accelerations * dt
    positions += velocities * dt
    return positions, velocities

# Initialize simulation
masses, positions, velocities = load_bodies_from_csv('./data/solar_system_2023_01_01.csv')
simulation_data = [positions.copy()]

# Run simulation
for _ in range(steps):
    positions, velocities = update_bodies(masses, positions, velocities)
    simulation_data.append(positions.copy())

# Plot animation
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter([], [], [])

# Set plot limits (adjust based on your data)
ax.set_xlim(-1e11, 1e11)
ax.set_ylim(-1e11, 1e11)
ax.set_zlim(-1e11, 1e11)
# ax.set_xlim(-6000, 6000)
# ax.set_ylim(-6000, 6000)
# ax.set_zlim(-6000, 6000)

# Set labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Update function for animation
def update(frame):
    positions = simulation_data[frame]
    scatter._offsets3d = (
        positions[:, 0],  # X-coordinates
        positions[:, 1],  # Y-coordinates
        positions[:, 2],  # Z-coordinates
    )
    ax.set_title(f"Time Step: {frame}")
    return scatter,

# Create the animation
ani = FuncAnimation(fig, update, frames=len(simulation_data), interval=10, blit=False)

# Show the animation
plt.show()
