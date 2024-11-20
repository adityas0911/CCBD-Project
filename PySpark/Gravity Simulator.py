from pyspark.sql import SparkSession

# Initialize SparkSession
spark = SparkSession.builder.appName("GravitySimulator").getOrCreate()

# Create a simple DataFrame for testing
data = [("Earth", 5.972e24), ("Moon", 7.342e22), ("Mars", 6.417e23)]
columns = ["Planet", "Mass"]

# Create a DataFrame from the sample data
df = spark.createDataFrame(data, columns)

# Show the DataFrame
df.show()

# Perform a simple transformation: add a new column for gravity force (assuming some simplified calculation)
# Formula for gravity force: F = G * (m1 * m2) / r^2, but for simplicity, we'll just multiply mass by a constant for now

gravity_constant = 6.67430e-11  # Newtonian gravity constant in m^3 kg^-1 s^-2
distance_from_sun = 1.496e11  # Average distance from the sun in meters (approx.)

df_with_gravity = df.withColumn("GravityForce", df["Mass"] * gravity_constant / (distance_from_sun ** 2))

# Show the transformed DataFrame
df_with_gravity.show()

# Stop the Spark session
spark.stop()
