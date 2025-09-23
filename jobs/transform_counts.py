import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, date_trunc, sum as s, coalesce, when, lit, regexp_replace, split, size

# Usage: spark-submit transform_counts.py /data/raw/file.csv /data/curated

if __name__ == "__main__":
    src = sys.argv[1]
    out_dir = sys.argv[2]

    spark = SparkSession.builder.appName("cph-traffic-transform").getOrCreate()
    df = spark.read.option("header", True).csv(src)

    print(f"Input columns: {df.columns}")
    print(f"Sample data:")
    df.show(5, truncate=False)

    cols = [c.lower() for c in df.columns]
    def pick(*opts):
        for o in opts:
            if o in cols: return o
        return None

    # More flexible column detection for Copenhagen traffic data
    ts = pick("timestamp","datetime","time","date_time","dato","tidspunkt","date","created_at")
    cnt = pick("count","counts","value","passes","antal","trafik","bike","cykler","bicycle","vehicle","køretøj")
    cid = pick("counter_id","counterid","sensor_id","site_id","id","lokation_id","location_id")
    name = pick("counter_name","name","sensor_name","site_name","lokation","location","sted","place")
    
    # For AADT data, look for specific columns
    aadt_bike = pick("aadt_bike","aadt_cykler","bike_aadt","cykler_aadt")
    aadt_car = pick("aadt_car","aadt_bil","car_aadt","bil_aadt")
    aadt_total = pick("aadt_total","aadt_total","total_aadt")

    print(f"Detected columns - timestamp: {ts}, count: {cnt}, counter_id: {cid}, name: {name}")
    print(f"AADT columns - bike: {aadt_bike}, car: {aadt_car}, total: {aadt_total}")

    # Handle different data formats
    if aadt_bike or aadt_car or aadt_total:
        # This is AADT (Annual Average Daily Traffic) data
        print("Processing AADT data...")
        
        # Create a unified count column from AADT data
        count_col = None
        if aadt_bike:
            count_col = col(aadt_bike)
        elif aadt_car:
            count_col = col(aadt_car)
        elif aadt_total:
            count_col = col(aadt_total)
        else:
            # Try to find any numeric column that could be counts
            numeric_cols = [c for c in df.columns if df.select(c).dtypes[0][1] in ['int', 'bigint', 'double', 'float']]
            if numeric_cols:
                count_col = col(numeric_cols[0])
                print(f"Using numeric column as count: {numeric_cols[0]}")
        
        if count_col is None:
            raise RuntimeError(f"Could not find count column in AADT data. Available columns: {df.columns}")
        
        # For AADT data, we'll treat each record as a daily average
        # Create a synthetic timestamp (use current date or a default)
        norm = (df
            .withColumn("timestamp", lit("2024-01-01 00:00:00"))  # Default timestamp for AADT data
            .withColumn("count", count_col.cast("int"))
            .select(
                # Use street name (vejnavn) as counter_id, fallback to t_nr, then unknown
                coalesce(col("vejnavn"), col("t_nr"), lit("unknown")).alias("counter_id"),
                # Use description (beskrivelse) as counter_name, fallback to street name
                coalesce(col("beskrivelse"), col("vejnavn"), lit("unknown")).alias("counter_name"),
                col("timestamp"), col("count"))
            .where(col("count").isNotNull()))
            
    else:
        # Traditional time-series data
        if not ts or not cnt:
            raise RuntimeError(f"Could not infer timestamp/count columns from: {df.columns}")

        norm = (df
            .withColumn("timestamp", to_timestamp(col(ts)))
            .withColumn("count", col(cnt).cast("int"))
            .select(
                (col(cid) if cid else lit("unknown")).alias("counter_id"),
                (col(name) if name else lit("unknown")).alias("counter_name"),
                col("timestamp"), col("count"))
            .where(col("timestamp").isNotNull() & col("count").isNotNull()))

    print(f"Normalized data sample:")
    norm.show(5, truncate=False)

    daily = (norm
        .withColumn("day", date_trunc("day", col("timestamp")))
        .groupBy("day", coalesce(col("counter_id"), col("counter_name")).alias("counter_key"))
        .agg(s("count").alias("total")))

    print(f"Daily aggregated data sample:")
    daily.show(5, truncate=False)

    (daily
        .repartition(1)
        .write
        .mode("overwrite")
        .parquet(f"{out_dir}/daily_counts.parquet"))

    spark.stop()
    print("Wrote parquet to", f"{out_dir}/daily_counts.parquet")