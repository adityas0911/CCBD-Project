# CCBD-Project: Final Project for CCBD Course

This project aims to demonstrate the use of PySpark and Docker for scalable data processing. The repository contains a gravity simulator model implemented using PySpark and Docker.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Installation Instructions](#installation-instructions)

   - [Docker Setup](#docker-setup)
   - [Git Setup](#git-setup)

3. [Running the Project](#running-the-project)
4. [Project Directory Structure](#project-directory-structure)
5. [License](#license)

---

### Project Overview

This repository contains code to simulate gravity-based calculations using PySpark, packaged within a Docker environment. It is designed to show how to scale computations and run simulations efficiently in a distributed environment.

The main project consists of:

- Gravity simulation code (`Gravity Simulator.py`)
- Docker configuration for Spark-based computation (`docker-spark` folder)
- PySpark setup for handling large-scale data in a distributed environment

---

### Installation Instructions

Follow the steps below to set up your environment and run the project.

### 1. Docker Setup

First, you need to install Docker on your platform. Follow the official documentation for installation:

- [Install Docker](https://docs.docker.com/get-docker/)
- [Docker Desktop Installation Guide](https://www.docker.com/get-started/)

After installation, make sure Docker is running by verifying it with the following command:

```bash
docker --version
```

### 2. Git Setup

Ensure that Git is installed on your system:

- [Download Git](https://git-scm.com/downloads)

You can You can verify the installation with:

```bash
git --version
```

### 3. Clone the Repository

Navigate to the desired directory where you want to store the repository, then clone it using the following command:

```bash
git clone https://github.com/adityas0911/CCBD-Project.git
```

### 4. Navigate to the Docker-Spark Directory

Once cloned, navigate to the docker-spark directory to configure Docker:

```bash
cd CCBD-Project/docker-spark
```

### 5. Launch Docker Containers

Use Docker Compose to launch the Spark containers:

```bash
docker-compose up -d --remove-orphans
```

This will start the Spark master and worker containers in detached mode.

### 6. Running the Project

You will need to open two separate terminals to interact with the Spark containers. Here's how you can proceed:

1. Open a Terminal for the Worker Container
In the first terminal, access the worker container by running:

```bash
docker exec -it docker-spark-worker-1 bash
```

2. Open a Terminal for the Master Container
In the second terminal, access the master container by running:

```bash
docker exec -it docker-spark-master-1 bash
```

3. Running Gravity Simulator on PySpark

To run the Gravity Simulator code directly using PySpark, submit the job with:

```bash
spark-submit 'Gravity Simulator.py'
```

This will run the gravity simulation on the Spark cluster.

### 7. Project Directory Structure

The project directory structure is as follows:

```bash
CCBD-Project/
├── docker-spark/                  # Contains Docker setup for Spark
│   ├── docker-compose.yml         # Docker Compose configuration
│   ├── spark/                     # Spark-related configuration files
│   └── Dockerfile                 # Dockerfile for building the image
│
├── Gravity Simulator.py           # Gravity simulation code  
└── README.md                      # This file
```

### 8. License

This project is licensed under the MIT License - see the LICENSE file for details.

### 9. Additional Notes

Ensure that Docker is configured correctly on your system. If you're running on Windows, ensure that Docker Desktop is using Linux containers.
Make sure you have sufficient memory allocated to Docker (at least 4GB recommended) for Spark to run effectively.
