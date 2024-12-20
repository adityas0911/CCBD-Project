#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <chrono>

struct Body {
    float x, y, z;
    float vx, vy, vz;
    float mass;
};

__global__ void compute_accelerations(Body *bodies, float3 *acc, int n, float G, float eps2) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n && i != 0) {
        float xi = bodies[i].x;
        float yi = bodies[i].y;
        float zi = bodies[i].z;
        float ax = 0.0f, ay = 0.0f, az = 0.0f;

        for (int j = 0; j < n; j++) {
            if (j != i) {
                float dx = bodies[j].x - xi;
                float dy = bodies[j].y - yi;
                float dz = bodies[j].z - zi;
                float distSqr = dx*dx + dy*dy + dz*dz + eps2;
                float invDist = rsqrtf(distSqr);
                float invDist3 = invDist * invDist * invDist;
                float f = G * bodies[j].mass * invDist3;
                ax += dx * f;
                ay += dy * f;
                az += dz * f;
            }
        }

        acc[i].x = ax;
        acc[i].y = ay;
        acc[i].z = az;
    }
}

__global__ void update_bodies(Body *bodies, float3 *acc, int n, float dt) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n && i != 0) {
        bodies[i].vx += acc[i].x * dt;
        bodies[i].vy += acc[i].y * dt;
        bodies[i].vz += acc[i].z * dt;

        bodies[i].x += bodies[i].vx * dt;
        bodies[i].y += bodies[i].vy * dt;
        bodies[i].z += bodies[i].vz * dt;
    }
}

// Updated to assume CSV lines in the format:
// mass,x,y,z,vx,vy,vz
std::vector<Body> readBodiesFromCSV(const std::string& filename) {
    std::ifstream file(filename);
    std::vector<Body> bodies_host;

    if (!file.is_open()) {
        std::cerr << "Error: Could not open file " << filename << std::endl;
        return bodies_host; // empty
    }

    std::string line;
    bool first_line = true;
    while (std::getline(file, line)) {
        // Trim trailing whitespace
        while(!line.empty() && (line.back() == ' ' || line.back() == '\r' || line.back() == '\n'))
            line.pop_back();
        if (line.empty()) continue;

        // Check for header line (if present)
        if (first_line && (line.find('x') != std::string::npos ||
                   line.find('X') != std::string::npos || 
                   line.find("mass") != std::string::npos)) {
              // Likely a header line
              first_line = false;
              continue;
          }
          first_line = false;

        std::stringstream ss(line);
        std::string val;
        std::vector<std::string> tokens;
        while (std::getline(ss, val, ',')) {
            // Trim whitespace
            while(!val.empty() && (val.back() == ' ' || val.back() == '\r' || val.back() == '\n'))
                val.pop_back();
            while(!val.empty() && (val.front() == ' '))
                val.erase(val.begin());
            tokens.push_back(val);
        }

        if (tokens.size() != 7) {
            std::cerr << "Warning: Skipping malformed line (expected 7 fields): " << line << std::endl;
            continue;
        }

        try {
            // tokens: mass, x, y, z, vx, vy, vz
            Body b;
            b.mass = std::stof(tokens[0]);
            b.x    = std::stof(tokens[1]);
            b.y    = std::stof(tokens[2]);
            b.z    = std::stof(tokens[3]);
            b.vx   = std::stof(tokens[4]);
            b.vy   = std::stof(tokens[5]);
            b.vz   = std::stof(tokens[6]);
            bodies_host.push_back(b);
        } catch (const std::invalid_argument &e) {
            std::cerr << "Conversion error for line (non-numeric value): " << line << std::endl;
        } catch (const std::out_of_range &e) {
            std::cerr << "Conversion error for line (value out of range): " << line << std::endl;
        }
    }

    file.close();
    return bodies_host;
}

int main() {
    // Simulation parameters
    float dt = 1.0f;     // Time step
    int steps = 1 * 1/dt;      // Number of simulation steps
    float G = 4.9823e-10f;      // Adjusted gravitational constant for km, kg, days
    float eps2 = 0;   // Softening factor

    std::string filename = "/content/solar_system_2023_01_01.csv";
    std::vector<Body> bodies_host = readBodiesFromCSV(filename);

    int n = (int)bodies_host.size();
    if (n == 0) {
        std::cerr << "Error: No valid bodies found in the CSV file." << std::endl;
        return 1;
    }

    // Allocate host memory
    Body* h_bodies = (Body*)malloc(n*sizeof(Body));
    for (int i = 0; i < n; i++) {
        h_bodies[i] = bodies_host[i];
    }

    Body *d_bodies;
    float3 *d_acc;
    cudaMalloc(&d_bodies, n*sizeof(Body));
    cudaMalloc(&d_acc, n*sizeof(float3));

    cudaMemcpy(d_bodies, h_bodies, n*sizeof(Body), cudaMemcpyHostToDevice);

    // Setup CUDA launch parameters
    int blockSize = 256;
    int gridSize = (n + blockSize - 1) / blockSize;

    // Benchmark simulation
    auto start_sim = std::chrono::high_resolution_clock::now();
    for (int s = 0; s < steps; s++) {
        compute_accelerations<<<gridSize, blockSize>>>(d_bodies, d_acc, n, G, eps2);
        update_bodies<<<gridSize, blockSize>>>(d_bodies, d_acc, n, dt);
        cudaDeviceSynchronize();
    }
    auto end_sim = std::chrono::high_resolution_clock::now();
    double sim_time = std::chrono::duration<double>(end_sim - start_sim).count();

    // Benchmark copying results back
    cudaMemcpy(h_bodies, d_bodies, n*sizeof(Body), cudaMemcpyDeviceToHost);

    // Print out a few sample results
    int printCount = (n < 9) ? n : 9;
    printf("First %d bodies after %d steps:\n", printCount, steps);
    for (int i = 0; i < printCount; i++) {
        printf("Body %d: mass=%.3e, pos=(%.3f, %.3f, %.3f), vel=(%.3f, %.3f, %.3f)\n",
               i, h_bodies[i].mass,
               h_bodies[i].x, h_bodies[i].y, h_bodies[i].z,
               h_bodies[i].vx, h_bodies[i].vy, h_bodies[i].vz);
    }

    // Print benchmarking information
    printf("\n--- Benchmarking Information ---\n");
    printf("Simulation Time (GPU):      %.6f s\n", sim_time);
    printf("--------------------------------\n");

    // Cleanup
    free(h_bodies);
    cudaFree(d_bodies);
    cudaFree(d_acc);

    return 0;
}
