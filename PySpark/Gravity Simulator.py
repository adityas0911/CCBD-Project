import time
import logging

from pyspark.sql import SparkSession

logging.basicConfig(filename="GravitySimulatorResults.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

spark = SparkSession.builder \
        .appName("GravitySimulator") \
        .master("local[8]") \
        .getOrCreate()

logging.info("Spark version: {}".format(spark.version))
logging.info("Master URL: {}".format(spark.sparkContext.master))

gravity_constant = 6.67430e-11
planets_data = [("Earth",
                 5.972e24,
                 (0,
                  0)),
                ("Moon",
                 7.342e22,
                 (384400000,
                  0)),
                ("Mars",
                 6.417e23,
                 (227940000000,
                  0)),]
columns = ["Planet",
           "Mass",
           "Position"]

df = spark.createDataFrame(planets_data,
                           columns)

logging.info("Input Planet Data:")
df.show()

def distance_between_planets(planet_1,
                             planet_2):
  return ((planet_1[2][0] - planet_2[2][0])**2 + (planet_1[2][1] - planet_2[2][1])**2)**0.5
def calculate_gravity(planet_1,
                      planet_2):
  return gravity_constant * (planet_1[1] * planet_2[1]) / (distance_between_planets(planet_1,
                                                                                    planet_2)**2)

start_time = time.time()
gravity_results = []

for [i,
     planet_1] in enumerate(planets_data):
  for planet_2 in planets_data[i + 1:]:
    gravity_results.append((planet_1[0],
                            planet_2[0],
                            calculate_gravity(planet_1,
                                              planet_2)))

logging.info("Gravity Calculation Results:")

for result in gravity_results:
  logging.info("Gravity between {} and {}: {:.3e} N".format(result[0],
                                                            result[1],
                                                            result[2]))

time_taken = time.time() - start_time

logging.info("Time taken for gravity simulation: {} seconds".format(time_taken))

results_df = spark.createDataFrame(gravity_results,
                                   ["Planet_1",
                                    "Planet_2",
                                    "Gravitational_Force"])
results_df.write.csv("GravitySimulatorResults.csv",
                     header=True)

spark.stop()
