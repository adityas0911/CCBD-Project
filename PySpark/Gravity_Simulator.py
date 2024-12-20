import os
import time
import logging
import math
import csv

from pyspark.sql import SparkSession, Row
from pyspark.sql.types import StructType, StructField, DoubleType

INPUT_FILE = "../data/solar_system_2023_01_01.csv"
TERMINAL_LOG_FILE = "Terminal_Log.log"
PERFORMANCE_METRICS_FILE = "Performance_Metrics.csv"
OUTPUT_FILE_NAME = "Gravity_Simulator_Results_for"
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

logging.basicConfig(filename=TERMINAL_LOG_FILE,
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
def log_performance(threads,
                    partitions,
                    time_taken):
  with open(PERFORMANCE_METRICS_FILE,
            mode='a',
            newline='') as file:
    writer = csv.writer(file)
    writer.writerow([threads,
                     partitions,
                     time_taken])
def main():
  if not os.path.exists(PERFORMANCE_METRICS_FILE):
    with open(PERFORMANCE_METRICS_FILE,
              mode='w',
              newline='') as file:
      writer = csv.writer(file)
      writer.writerow(["Threads",
                       "Partitions",
                       "Time Taken (seconds)"])

  for threads in THREAD_COUNTS:
    logging.info("Current number of threads: {}".format(threads))

    spark = create_spark_session(threads)
    data = load_data(spark).repartition(threads)
    current_partitions = data.rdd.getNumPartitions()

    logging.info("Current number of partitions: {}".format(current_partitions))

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

    log_performance(threads,
                    current_partitions,
                    time_taken)

    simulated_df = spark.createDataFrame(simulated_data,
                                         schema=schema)

    if threads != 1:
      logging.info("Time taken with {} threads: {} seconds".format(threads,
                                                                   time_taken))

      output_file = "{}_{}_threads.csv".format(OUTPUT_FILE_NAME,
                                               threads)
    else:
      logging.info("Time taken with {} thread: {} seconds".format(threads,
                                                                  time_taken))

      output_file = "{}_{}_thread.csv".format(OUTPUT_FILE_NAME,
                                              threads)

    simulated_df.write.csv(output_file,
                           header=True)
    logging.info("Results saved to {}.".format(output_file))

    spark.stop()

if __name__ == "__main__":
  main()
