# CCBD-Project

This project aims to demonstrate the use of PySpark and Docker for scalable data processing. The repository contains a gravity simulator model implemented using PySpark and Docker.
This repository contains the [final project](https://rutgers.instructure.com/courses/295164/assignments/3370507) for the course [16:332:516:01 CLOUD COMP BIG DATA](https://rutgers.instructure.com/courses/295164) Fall 2024.

---

## Table of Contents

1. [Course Information](#course-information)
2. [Due Date](#due-date)
3. [Contributors](#contributors)
4. [Project Overview](#project-overview)
5. [Installation Instructions](#installation-instructions)
6. [Running the Project](#running-the-project)
7. [Project Directory Structure](#project-directory-structure)
8. [License](#license)
9. [Additional Notes](#additional-notes)

---

## Course Information

- **Course:** [16:332:516:01 CLOUD COMP BIG DATA](https://rutgers.instructure.com/courses/295164)
- **Professor:** [Maria Striki](mailto:maria.striki@rutgers.edu)

---

## Due Date

- **December 02, 2024 @ 11:59 PM EST**

---

## Contributors

- **Aditya Sharma**

  - **RUID:** 219008361
  - **NetID:** as4108
  - **Email:** [as4108@scarletmail.rutgers.edu](mailto:as4108@scarletmail.rutgers.edu)

- **Pranav Angiya Janarthanan**

  - **RUID:** _
  - **NetID:** pa446
  - **Email:** [pa446@scarletmail.rutgers.edu](mailto:pa446@scarletmail.rutgers.edu)

---

## Project Overview

This repository contains code to simulate gravity-based calculations using PySpark, packaged within a Docker environment. It is designed to show how to scale computations and run simulations efficiently in a distributed environment.

The main parts of the project consist of:

- Gravity simulation code (`Gravity Simulator.py`)
- Docker configuration for Spark-based computation (`docker-spark` folder)
- PySpark setup for handling large-scale data in a distributed environment

---

## Installation Instructions

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

## Running the Project

### 1. Navigate to the Docker-Spark Directory

Once cloned, navigate to the docker-spark directory to configure Docker:

```bash
cd CCBD-Project/docker-spark
```

### 2. Launch Docker Containers

Use Docker Compose to launch the Spark containers:

```bash
docker-compose up -d --remove-orphans
```

This will start the Spark master and worker containers in detached mode.

### 3. Access the Spark Containers

You will need to open two separate terminals to interact with the Spark containers. Here's how you can proceed:

### 1. Open a Terminal for the Worker Container

In the first terminal, access the worker container by running:

```bash
docker exec -it docker-spark-worker-1 bash
```

### 2. Open a Terminal for the Master Container

In the second terminal, access the master container by running:

```bash
docker exec -it docker-spark-master-1 bash
```

### 3. Running Gravity Simulator on PySpark

To run the Gravity Simulator code directly using PySpark, submit the job with:

```bash
spark-submit 'Gravity Simulator.py'
```

This will run the gravity simulation on the Spark cluster.

## Project Directory Structure

The project directory structure is as follows:

```bash
CCBD-Project/
├── Description/
│   ├── F24_Final_Project_ECE494-516_Rubric_Grades_Template_Final.doc
│   ├── Final_Project_Ideas_F24.pdf
│   └── Project_Labs_Setup_F24.docx
├── docker-spark/
│   ├── conf/
│   │   ├── master/
│   │   │   └── spark-defaults.conf
│   │   └── worker/
│   │       └── spark-defaults.conf
│   ├── data/
│   │   └── .gitkeep
│   ├── gitignore
│   ├── cloudbuild.yaml
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── LICENSE
│   └── README.md
├── Resources/
│   ├── Docker-Spark_setup_for_Windows_11.pdf
│   └── docker-spark-hadoop-containers-howto_F24.pdf
├── .gitattributes
├── CCBD Final Project Proposal.pdf
├── Gravity Simulator.py
└── README.md
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Additional Notes

Ensure that Docker is configured correctly on your system. If you're running on Windows, ensure that Docker Desktop is using Linux containers.
Make sure you have sufficient memory allocated to Docker (at least 4GB recommended) for Spark to run effectively.
