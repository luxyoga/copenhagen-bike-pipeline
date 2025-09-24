# Copenhagen Bike & Weather Data Pipeline

This project builds an end-to-end data engineering pipeline to analyze cycling traffic in Copenhagen and its relationship with weather conditions.

It demonstrates skills in data ingestion, ETL orchestration, distributed processing, and interactive dashboards — using real-world data from Kaggle (bike counts) and Open-Meteo (weather).

## **Tech Stack**

This project demonstrates a complete data engineering pipeline using modern tools:
- **Apache Airflow** for workflow orchestration & scheduling
- **Apache PySpark** for distributed ETL and aggregation
- **PostgreSQL** for storage for metadata & pipeline results
- **Streamlit** for interactive data visualization
- **Docker** for containerized deployment
- **Real Copenhagen cycling data** from Kaggle (2005-2014)
- **Weather data** from Open-Meteo (2005-2014)

## **Skills Demonstrated**

- Building reproducible ETL pipelines
- Writing PySpark transformations for big data
- Designing & deploying Dockerized services
- Visualizing results through Streamlit dashboards
- Integrating real APIs into pipelines

## **Insights**

From the processed data:
- Sunny weather shows only 16.6% higher ridership than rainy weather, suggesting Copenhagen cyclists are quite resilient to weather conditions! This indicates a strong cycling culture where people bike regardless of weather.
- 53,310 rides per day across all locations
- 194,686,937 bike rides across all locations
- Clear location-based differences in traffic volumes.
- Data Coverage: 55 monitoring locations
- 194,686,937 bike rides across all locations in 10 years.

## **Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │───▶│  Airflow DAGs   │───▶│  Spark Jobs     │
│                 │    │                 │    │                 │
│ • Kaggle API    │    │ • Scheduling    │    │ • Transform     │
│ • Open-Meteo    │    │ • Monitoring    │    │ • Aggregate     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │   Streamlit     │
│                 │    │                 │
│ • Metadata      │    │ • Dashboard     │
│ • Task History  │    │ • Analytics     │
└─────────────────┘    └─────────────────┘
```

## **Quick Start**

1. **Clone the repository**
   ```bash
   git clone <https://github.com/luxyoga/copenhagen-bike-pipeline>
   cd copenhagen-bike-pipeline
   ```

2. **Start the services**
   ```bash
   docker-compose up -d
   ```

3. **Access the applications**
   - **Streamlit Dashboard**: http://localhost:8501
   - **Airflow UI**: http://localhost:8080 (admin/admin)
   - **Spark Master**: http://localhost:8081

## **Data Pipeline**

### 1. **Data Ingestion**
- Downloads real Copenhagen cycling data from Kaggle
- Fetches historical weather data from Open-Meteo API
- Processes and cleans raw data

### 2. **Data Processing**
- **PySpark transformations** for distributed processing
- **Daily aggregation** of bike counts by location
- **Weather integration** with temperature, precipitation, and conditions
- **Seasonal analysis** and pattern detection

### 3. **Data Visualization**
- **Interactive dashboard** with monthly breakdowns
- **Weather impact analysis** with correlation charts
- **Location-based insights** and trends
- **Time series analysis** with seasonal patterns

## 🛠️ **Project Structure**

```
copenhagen-bike-pipeline/
├── app/
│   └── streamlit_app.py          # Interactive dashboard
├── dags/
│   ├── cph_bikes_daily.py        # Airflow DAG definition
│   └── scripts/
│       └── ingest_to_raw.py      # Data ingestion script
├── jobs/
│   └── transform_counts.py       # PySpark transformation job
├── data/
│   ├── raw/                      # Raw data storage
│   └── curated/                  # Processed data storage
├── docker-compose.yml            # Container orchestration
├── requirements.txt              # Python dependencies
└── README.md                    # Project documentation
```

## **Data Flow**

1. **Ingestion**: Kaggle API → Raw CSV files
2. **Processing**: PySpark → Aggregated Parquet files
3. **Orchestration**: Airflow → Scheduled workflows
4. **Visualization**: Streamlit → Interactive dashboard

## **Data Sources**

- **Cycling Data**: [Kaggle - Bike Traffic Counts in Copenhagen](https://www.kaggle.com/datasets/emilhvitfeldt/bike-traffic-counts-in-copenhagen)
- **Weather Data**: [Open-Meteo API](https://open-meteo.com/) - Historical weather for Copenhagen
- **Time Period**: 2005-2014 (10 years of real data)

## **Looking Ahead**

1. Deploy pipeline to cloud (AWS/GCP/Azure)
2. Add real-time streaming with Kafka
3. Extend dashboard with forecasting models for bike traffic

---
