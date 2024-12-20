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
def calculate_gravity(b_1,
                      b_2):
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
  updated_bodies = []

  for i, body_1 in enumerate(bodies):
    ax, ay, az = 0.0, 0.0, 0.0

    for j, body_2 in enumerate(bodies):
      if i != j:
        dx = body_2["x"] - body_1["x"]
        dy = body_2["y"] - body_1["y"]
        dz = body_2["z"] - body_1["z"]
        dist_sqr = dx**2 + dy**2 + dz**2 + 1e-9
        inv_dist = 1.0 / math.sqrt(dist_sqr)
        inv_dist3 = inv_dist * inv_dist * inv_dist
        f = UPDATED_GRAVITY_CONSTANT * body_2["mass"] * inv_dist3
        ax += dx * f
        ay += dy * f
        az += dz * f

    ax /= body_1["mass"]
    ay /= body_1["mass"]
    az /= body_1["mass"]
    vx_new = body_1["vx"] + ax
    vy_new = body_1["vy"] + ay
    vz_new = body_1["vz"] + az
    x_new = body_1["x"] + vx_new
    y_new = body_1["y"] + vy_new
    z_new = body_1["z"] + vz_new

    updated_bodies.append(Row(mass=body_1["mass"],
                              x=x_new,
                              y=y_new,
                              z=z_new,
                              vx=vx_new,
                              vy=vy_new,
                              vz=vz_new))

  return iter(updated_bodies)

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
  time_taken = time.time() - start_time
  simulated_df = spark.createDataFrame(simulated_data,
                                       schema=schema)

  logging.info("Simulation with {} threads completed in {:.2f} seconds".format(threads,
                                                                               time_taken))

  output_file = "{}_threads_{}.csv".format(OUTPUT_FILE_NAME,
                                           threads)

  simulated_df.write.csv(output_file,
                         header=True)
  logging.info("Results saved to {}".format(output_file))

  spark.stop()
