import time
import logging
import math

from pyspark.sql import SparkSession

INPUT_FILE = "solar_system_2023_01_01.csv"
OUTPUT_FILE = "GravitySimulatorResults.csv"
UPDATED_GRAVITY_CONSTANT = 6.67430e-11 * (86400**2) / (10**9)
DAYS_TO_SIMULATE = 365
THREAD_COUNTS = [1,
                 2,
                 4,
                 8]

logging.basicConfig(filename="GravitySimulatorResults.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def create_spark_session(threads):
  return SparkSession.builder \
         .appName("GravitySimulator") \
         .master(f"local[{threads}]") \
         .getOrCreate()
def load_data(spark):
  return spark.read.csv(INPUT_FILE,
                        header=True,
                        inferSchema=True)
def calculate_gravity(b1, b2):
  dx = b2["X"] - b1["X"]
  dy = b2["Y"] - b1["Y"]
  dz = b2["Z"] - b1["Z"]
  distance = math.sqrt(dx**2 + dy**2 + dz**2)

  if distance == 0:
    return (0,
            0,
            0)

  force = UPDATED_GRAVITY_CONSTANT * b1["Mass"] * b2["Mass"] / (distance**2)
  fx, fy, fz = force * dx / distance, force * dy / distance, force * dz / distance

  return (fx, 
          fy,
          fz)
def update_body_positions(partition):
  bodies = list(partition)

  for _ in range(DAYS_TO_SIMULATE):
    forces = {i: (0,
                  0,
                  0) for i in range(len(bodies))}

    for i, b1 in enumerate(bodies):
      for j, b2 in enumerate(bodies[i + 1:],
                             start=i + 1):
        fx, fy, fz = calculate_gravity(b1,
                                       b2)
        forces[i] = tuple(map(sum,
                              zip(forces[i],
                                  (fx,
                                   fy,
                                   fz))))
        forces[j] = tuple(map(sum,
                              zip(forces[j],
                                  (-fx,
                                   -fy,
                                   -fz))))
    for i, body in enumerate(bodies):
      fx, fy, fz = forces[i]
      ax, ay, az = fx / body["Mass"], fy / body["Mass"], fz / body["Mass"]
      body["VX"] += ax
      body["VY"] += ay
      body["VZ"] += az
      body["X"] += body["VX"]
      body["Y"] += body["VY"]
      body["Z"] += body["VZ"]

  return bodies

for threads in THREAD_COUNTS:
  logging.info(f"Starting simulation with {threads} threads")

  spark = create_spark_session(threads)
  data = load_data(spark)
  bodies = data.select("Mass",
                       "X",
                       "Y",
                       "Z",
                       "VX",
                       "VY",
                       "VZ")
  start_time = time.time()
  simulated_data = bodies.rdd.mapPartitions(update_body_positions)
  simulated_df = spark.createDataFrame(simulated_data)
  time_taken = time.time() - start_time

  logging.info(f"Simulation with {threads} threads completed in {time_taken:.2f} seconds")

  output_file = f"{OUTPUT_FILE}_threads_{threads}.csv"

  simulated_df.write.csv(output_file,
                         header=True)
  logging.info(f"Results saved to {output_file}")

  spark.stop()
