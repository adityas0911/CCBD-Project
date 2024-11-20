# CCBD-Project: Gravity Simulator

This [repository](https://github.com/adityas0911/CCBD-Project) contains the [final project](https://rutgers.instructure.com/courses/295164/assignments/3370507) for the course [16:332:516:01 CLOUD COMP BIG DATA](https://rutgers.instructure.com/courses/295164) Fall 2024. This project aims to demonstrate the use of PySpark and Docker for scalable data processing.

---

## Table of Contents

1. [Course Information](#course-information)
2. [Due Date](#due-date)
3. [Contributors](#contributors)
4. [Project Overview](#project-overview)
5. [Installation Instructions](#installation-instructions)
6. [Running the PySpark Portion](#running-the-pyspark-portion)
7. [Running the CUDA Portion](#running-the-cuda-portion)
8. [Project Directory Structure](#project-directory-structure)
9. [License](#license)
10. [Additional Notes](#additional-notes)

---

## Course Information

The course name is [16:332:516:01 CLOUD COMP BIG DATA](https://rutgers.instructure.com/courses/295164) and is taught by Professor [Maria Striki](mailto:maria.striki@rutgers.edu).

---

## Due Date

This [project](https://rutgers.instructure.com/courses/295164/assignments/3370507) is due on December 02, 2024 at 11:59 PM EST.

---

## Contributors

### 1. **Aditya Sharma**

- **RUID:** 219008361
- **NetID:** as4108
- **Email:** [as4108@scarletmail.rutgers.edu](mailto:as4108@scarletmail.rutgers.edu)

### 2. **Pranav Angiya Janarthanan**

- **RUID:** _________
- **NetID:** pa446
- **Email:** [pa446@scarletmail.rutgers.edu](mailto:pa446@scarletmail.rutgers.edu)

---

## Project Overview

This [repository](https://github.com/adityas0911/CCBD-Project) contains code to simulate gravity-based calculations using PySpark and CUDA. It is designed to show comparisions between PySpark and CUDA. The main parts of the project consists of:

### 1. README file for instruction on running the project ([README.md](README.md))

### 2. PySpark folder for the pyspark portion of the project ([PySpark](PySpark))

### 3. CUDA folder for the CUDA portion of the project ([CUDA](CUDA))

---

## Installation Instructions

Follow the steps below to set up your pyspark environment using docker and run the project:

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

- [Install Git](https://git-scm.com/downloads)

You can You can verify the installation with:

```bash
git --version
```

### 3. Navigate to the PySpark Directory

Navigate to the PySpark directory to configure Docker:

```bash
cd ./PySpark/
```

---

## Running the PySpark Portion

### 1. Navigate to the Docker-Spark Directory

Once cloned, navigate to the docker-spark directory to configure Docker:

```bash
cd ./docker-spark/
```

### 2. Launch Docker Containers

Launch the Docker Desktop software. Then, use Docker Compose to launch the Spark containers:

```bash
docker-compose up -d
```

This will start the Spark master and worker containers in detached mode.

### 3. Access the Spark Containers

You will need a total of two separate terminals to interact with the Spark containers. Here's how you can proceed:

- Use Terminal 1 for the Worker Container

In the first terminal, access the worker container by running:

```bash
docker exec -it docker-spark-worker-1 bash
```

- Use Terminal 2 for the Master Container

In the second terminal, access the master container by running:

```bash
docker exec -it docker-spark-master-1 bash
```

### 4. Running Gravity Simulator on PySpark

To run the Gravity Simulator code directly using PySpark, you will need to use Terminal 2 (the master container). Navigate to the project directory to access the project directory:

```bash
cd ./CCBD-Project
```

Submit the job with:

```bash
spark-submit 'Gravity Simulator.py'
```

This will run the gravity simulation file ```Gravity Simulator.py``` on the Spark cluster.

---

## Running the CUDA Portion

Follow the steps below to setup your CUDA environment and run the CUDA portion of the project:

---

## Project Directory Structure

The project directory structure is as follows:

```bash
CCBD-Project/
├── Description/
│   ├── F24_Final_Project_ECE494-516_Rubric_Grades_Template_Final.doc
│   ├── Final_Project_Ideas_F24.pdf
│   └── Project_Labs_Setup_F24.docx
├── Resources/
│   ├── Docker-Spark_setup_for_Windows_11.pdf
│   └── docker-spark-hadoop-containers-howto_F24.pdf
├── docker-spark/
│   ├── conf/
│   │   ├── master/
│   │   │   └── spark-defaults.conf
│   │   └── worker/
│   │       └── spark-defaults.conf
│   ├── data/
│   │   └── .gitkeep
│   ├── gitignore
│   ├── Dockerfile
│   ├── LICENSE
│   └── README.md
│   ├── cloudbuild.yaml
│   ├── docker-compose.yml
├── .gitattributes
├── CCBD Final Project Proposal.pdf
├── Gravity Simulator.py
└── README.md
```

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Additional Notes

Ensure that Docker is configured correctly on your system.
If you're running on Windows, ensure that Docker Desktop is using Linux containers.
Make sure you have sufficient memory allocated to Docker for Spark to run effectively.
