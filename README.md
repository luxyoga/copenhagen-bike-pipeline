# Copenhagen Bike & Weather Data Pipeline

[Live Dashboard](https://copenhagen-bike-pipeline.streamlit.app) | [GitHub](https://github.com/luxyoga) | [LinkedIn](https://linkedin.com/in/luxyoga)

An end-to-end pipeline over 194.6 million bike rides and ten years of weather data, built to answer one question: what actually drives cycling volume in Copenhagen?

## The Findings

Location and season drive ridership. Weather does not.

Six of the 55 monitoring stations carry roughly a fifth of all cycling traffic in the city, and each of those six handles about twice the volume of the next tier down. Meanwhile temperature and precipitation show almost no measurable relationship with daily rides. Across four temperature bands, average daily rides vary by two rides out of 874. Across four precipitation bands, six rides out of 874.

If you're planning cycling infrastructure in Copenhagen, where and when matter enormously. Whether it rains barely registers.

## What I'd recommend

**Concentrate capacity investment in the six-station core.**<br>

Kongens Have, Østerbro Station, Kongens Nytorv, Vesterbro Station, Nørrebro Station and Rådhuspladsen each carry between 6.35M and 6.41M rides over the ten-year window. They're 11% of the monitoring network and 19.6% of total volume, and they run at almost exactly double the next tier of stations, which cluster tightly around 3.21M. That gap is stable rather than noisy, so it's a reliable basis for prioritising spend.

**Size for summer peaks, not for average days.**<br>

The busiest single day in the dataset hit 92,441 rides on 26 July 2010, which is 1.73 times the network's 53,293 daily average. Summer is the binding constraint on capacity, and infrastructure sized to the annual mean will be under pressure for a third of the year.

**Drop weather from the planning model.**<br>

There's no case for weather-contingent staffing, maintenance windows, or temporary capacity adjustment. The effect isn't just small, it's close to undetectable in two of the three ways I cut it. Planning effort spent here is effort not spent on the two variables that actually move volume.

## The evidence

### Weather has almost no effect

Average daily rides by temperature band:

| Temperature | Avg rides | Std dev |
|---|---|---|
| Cold (0-5°C) | 875 | 394 |
| Cool (5-15°C) | 874 | 396 |
| Warm (15-25°C) | 873 | 396 |
| Hot (25°C+) | 874 | 395 |

Average daily rides by precipitation level:

| Precipitation | Avg rides | Std dev |
|---|---|---|
| No rain (0-1mm) | 878 | 396 |
| Light rain (1-3mm) | 872 | 395 |
| Moderate rain (3-5mm) | 873 | 395 |
| Heavy rain (5mm+) | 873 | 395 |

Both tables are flat. The full spread across temperature is 0.23% and across precipitation is 0.69%, against a standard deviation of roughly 395 rides. There's no signal here.

Average daily rides by weather condition:

| Condition | Avg rides | Std dev |
|---|---|---|
| Sunny | 946 | 425 |
| Cloudy | 855 | 381 |
| Rainy | 812 | 362 |

This one shows a 16.5% gap between sunny and rainy days. Worth reading carefully though, because a 134-ride difference sits at about a third of one standard deviation. It's a small effect even taken at face value.

**A caveat I'd raise before anyone acts on that 16.5%.** These three cuts disagree with each other. If rainy days genuinely run 16.5% below sunny days, the precipitation table should show the same pattern, because rainy days are by definition days with precipitation. It doesn't. Heavy rain sits within six rides of no rain. Two of the three cuts say weather has no effect and one says it has a modest one, and the two using continuous measurements are the ones saying nothing. I'd want to reconcile how the categorical weather condition is derived before treating the 16.5% as firm. The headline conclusion holds either way, since 16.5% is small, but that specific number shouldn't be quoted without the check.

### Location is heavily concentrated

Top stations by total rides, 2005 to 2014:

| Station | Total rides | Avg daily | Max daily |
|---|---|---|---|
| Kongens Have | 6,410,464 | 1,755 | 4,160 |
| Østerbro Station | 6,384,679 | 1,748 | 3,903 |
| Kongens Nytorv | 6,371,710 | 1,744 | 4,073 |
| Vesterbro Station | 6,364,781 | 1,742 | 4,006 |
| Nørrebro Station | 6,352,665 | 1,739 | 3,906 |
| Rådhuspladsen | 6,349,454 | 1,738 | 4,066 |
| Nørrebrogade | 3,217,576 | 881 | 2,093 |
| Vester Søgade | 3,217,510 | 881 | 2,096 |
| Vesterport | 3,213,962 | 880 | 2,086 |
| Østerport | 3,213,491 | 879 | 2,094 |

The break between the sixth and seventh station is the structural feature here. It isn't a gradual decline, it's a cliff, and it holds across both total volume and peak daily load.

### Season swings volume far more than weather

Summer carries the highest total and highest average daily ridership of any season, winter the lowest, with spring and autumn between them. The seasonal swing dwarfs anything visible in the weather data.

### Headline figures

| Metric | Value |
|---|---|
| Total rides | 194,625,285 |
| Date range | 2005-01-01 to 2014-12-31 |
| Monitoring locations | 55 |
| Average daily rides | 53,293 |
| Peak daily usage | 92,441 on 26 July 2010 |
| Busiest station | Kongens Have, 6,410,464 rides |
| Most consistent station | Nørre Farimagsgade |

A note on vintage. This covers 2005 to 2014, so it describes a decade of mature cycling behaviour rather than current conditions. The structural findings about concentration and weather insensitivity should hold, but absolute volumes will have moved.

## How I built it

The pipeline ingests bike count data from Kaggle and historical weather from the Open-Meteo API, transforms and aggregates it with PySpark, stores results in PostgreSQL, and serves an interactive dashboard through Streamlit. Airflow handles scheduling and orchestration, and the whole stack runs in Docker for reproducible runs.

**Data flow**

1. **Ingestion:** Kaggle API and Open-Meteo into raw CSV
2. **Processing:** PySpark transformations into aggregated Parquet
3. **Orchestration:** Airflow scheduled workflows
4. **Storage:** PostgreSQL for modelled output and pipeline metadata
5. **Visualisation:** Streamlit dashboard

```
copenhagen-bike-pipeline/
├── app/
│   └── streamlit_app.py          # Interactive dashboard
├── dags/
│   ├── cph_bikes_daily.py        # Airflow DAG definition
│   └── scripts/
│       └── ingest_to_raw.py      # Data ingestion
├── jobs/
│   └── transform_counts.py       # PySpark transformation job
├── data/
│   ├── raw/                      # Raw data storage
│   └── curated/                  # Processed data storage
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Tech stack

Apache Airflow (orchestration and scheduling), Apache PySpark (distributed ETL), PostgreSQL (storage), Streamlit (visualisation), Docker (containerised deployment).

Data sources: Kaggle bike traffic counts for Copenhagen, Open-Meteo API for historical weather, 2005 to 2014.

## Run it locally

```bash
git clone https://github.com/luxyoga/copenhagen-bike-pipeline
cd copenhagen-bike-pipeline
docker-compose up -d
```
- Streamlit dashboard: http://localhost:8501
- Airflow UI: http://localhost:8080 (admin/admin)
- Spark Master: http://localhost:8081

## What I'd do next

Reconcile the three weather cuts so the condition-level figure can be trusted or discarded. Deploy to a cloud environment and add streaming ingestion with Kafka. Fit a seasonal forecast on daily counts to project when the six core stations hit capacity.
