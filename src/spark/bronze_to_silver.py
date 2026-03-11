from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("BronzeToSilverPipeline") \
    .getOrCreate()

products_df = spark.read.option("multiline","true").json("/opt/project/src/data/raw/products/*.json")
users_df = spark.read.option("multiline","true").json("/opt/project/src/data/raw/users/*.json")
carts_df = spark.read.option("multiline","true").json("/opt/project/src/data/raw/carts/*.json")

products_clean = products_df.select(
    col("id").alias("product_id"),
    col("title"),
    col("price"),
    col("category")
)

users_clean = users_df.select(
    col("id").alias("user_id"),
    col("email"),
    col("username")
)

products_clean.write.mode("overwrite").parquet(
    "/opt/project/src/data/silver/products"
)

users_clean.write.mode("overwrite").parquet(
    "/opt/project/src/data/silver/users"
)

print("Pipeline Bronze → Silver executado com sucesso")