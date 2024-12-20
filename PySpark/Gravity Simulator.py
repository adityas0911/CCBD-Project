import time
import logging
import math

from pyspark.sql import SparkSession, Row
from pyspark.sql.types import StructType, StructField, DoubleType

INPUT_FILE = "../data/solar_system_2023_01_01.csv"
OUTPUT_FILE_NAME = "GravitySimulatorResults"
UPDATED_GRAVITY_CONSTANT = 6.67430e-11 * (86400**2) / (10**9)
DAYS_TO_SIMULATE = 365
THREAD_COUNTS = [1,
                 2,
                 4,
                 8]
schema = StructType([StructField("mass",
                                 DoubleType(),
                                 True),
                     StructField("x",
                                 DoubleType(),
                                 True),
                     StructField("y",
                                 DoubleType(),
                                 True),
                     StructField("z",
                                 DoubleType(),
                                 True),
                     StructField("vx",
                                 DoubleType(),
                                 True),
                     StructField("vy",
                                 DoubleType(),
                                 True),
                     StructField("vz",
                                 DoubleType(),
                                 True)])

logging.basicConfig(filename="GravitySimulatorResults.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def create_spark_session(threads):
  return (SparkSession.builder
          .appName("GravitySimulator")
          .master("local[{}]".format(threads))
          .getOrCreate())
def load_data(spark):
  return spark.read.csv(INPUT_FILE,
                        header=True,
                        schema=schema)
def calculate_gravity(b_1, b_2):
  dx = b_2["x"] - b_1["x"]
  dy = b_2["y"] - b_1["y"]
  dz = b_2["z"] - b_1["z"]
  distance = math.sqrt(dx**2 + dy**2 + dz**2)

  if distance == 0:
    return (0,
            0,
            0)

  force = UPDATED_GRAVITY_CONSTANT * b_1["mass"] * b_2["mass"] / (distance**2)
  fx = force * dx / distance
  fy = force * dy / distance
  fz = force * dz / distance

  return (fx,
          fy,
          fz)
def update_body_positions(partition):
  bodies = list(partition)

  for _ in range(DAYS_TO_SIMULATE):
    forces = {i: (0,
                  0,
                  0) for i in range(len(bodies))}

    for i, b_1 in enumerate(bodies):
      for j, b_2 in enumerate(bodies[i + 1:],
                             start=i + 1):
        fx, fy, fz = calculate_gravity(b_1,
                                       b_2)
        forces[i] = (forces[i][0] + fx,
                     forces[i][1] + fy,
                     forces[i][2] + fz)
        forces[j] = (forces[j][0] - fx,
                     forces[j][1] - fy,
                     forces[j][2] - fz)
    for i, body in enumerate(bodies):
      fx, fy, fz = forces[i]
      ax, ay, az = fx / body["mass"], fy / body["mass"], fz / body["mass"]
      new_body = Row(mass=body["mass"],
                     x=body["x"] + body["vx"],
                     y=body["y"] + body["vy"],
                     z=body["z"] + body["vz"],
                     vx=body["vx"] + ax,
                     vy=body["vy"] + ay,
                     vz=body["vz"] + az)
      bodies[i] = new_body

  return bodies

for threads in THREAD_COUNTS:
  logging.info("Starting simulation with {} threads".format(threads))

  spark = create_spark_session(threads)
  data = load_data(spark)
  bodies = data.select("mass",
                       "x",
                       "y",
                       "z",
                       "vx",
                       "vy",
                       "vz")
  start_time = time.time()
  simulated_data = bodies.rdd.mapPartitions(update_body_positions)
  simulated_df = spark.createDataFrame(simulated_data,
                                       schema=schema)
  time_taken = time.time() - start_time

  logging.info("Simulation with {} threads completed in {:.2f} seconds".format(threads,
                                                                               time_taken))

  output_file = "{}_threads_{}.csv".format(OUTPUT_FILE_NAME,
                                           threads)

  simulated_df.write.csv(output_file,
                         header=True)
  logging.info("Results saved to {}".format(output_file))

  spark.stop()
