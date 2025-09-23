# 🚴‍♂️ Copenhagen Bike Data Pipeline

A comprehensive data pipeline for analyzing Copenhagen cycling patterns with real-time processing, orchestration, and interactive visualization.

## 🎯 **Project Overview**

This project demonstrates a complete data engineering pipeline using modern tools:
- **Apache Airflow** for workflow orchestration
- **Apache Spark** for distributed data processing  
- **Streamlit** for interactive data visualization
- **Docker** for containerized deployment
- **Real Copenhagen cycling data** from Kaggle (2005-2014)

## 🏗️ **Architecture**

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

## 🚀 **Quick Start**

### Prerequisites
- Docker & Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
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

## 📊 **Data Pipeline**

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

## 🔧 **Services**

### **Apache Airflow**
- **Purpose**: Workflow orchestration and scheduling
- **Port**: 8080
- **Features**: DAG monitoring, task scheduling, retry logic
- **Credentials**: admin/admin

### **Apache Spark**
- **Purpose**: Distributed data processing
- **Components**: Master + Worker nodes
- **Port**: 8081 (Master UI)
- **Features**: PySpark jobs, data transformations

### **Streamlit**
- **Purpose**: Interactive data visualization
- **Port**: 8501
- **Features**: Real-time dashboard, interactive charts, data exploration

### **PostgreSQL**
- **Purpose**: Airflow metadata storage
- **Features**: Task history, DAG runs, user management

## 📈 **Dashboard Features**

### **Key Metrics**
- Total rides across all time periods
- Average daily rides by month/season
- Peak usage patterns and trends

### **Interactive Analysis**
- **Monthly Selector**: Drill down into specific months
- **Location Analysis**: Top cycling locations and patterns
- **Weather Impact**: Temperature and precipitation effects
- **Seasonal Trends**: Year-over-year comparisons

### **Visualizations**
- Time series charts with seasonal patterns
- Weather correlation scatter plots
- Location-based heat maps
- Interactive filtering and exploration

## 🔄 **Data Flow**

1. **Ingestion**: Kaggle API → Raw CSV files
2. **Processing**: PySpark → Aggregated Parquet files
3. **Orchestration**: Airflow → Scheduled workflows
4. **Visualization**: Streamlit → Interactive dashboard

## 📊 **Data Sources**

- **Cycling Data**: [Kaggle - Bike Traffic Counts in Copenhagen](https://www.kaggle.com/datasets/emilhvitfeldt/bike-traffic-counts-in-copenhagen)
- **Weather Data**: [Open-Meteo API](https://open-meteo.com/) - Historical weather for Copenhagen
- **Time Period**: 2005-2014 (10 years of real data)

## 🛠️ **Development**

### **Adding New Features**
1. Create new Airflow tasks in `dags/cph_bikes_daily.py`
2. Add PySpark jobs in `jobs/` directory
3. Extend Streamlit dashboard in `app/streamlit_app.py`

### **Data Processing**
- Raw data stored in `data/raw/`
- Processed data in `data/curated/`
- Parquet format for efficient storage

### **Monitoring**
- Airflow UI for workflow monitoring
- Spark UI for job performance
- Streamlit logs for dashboard issues

## 🚀 **Production Deployment**

### **Scaling**
- Add more Spark workers in `docker-compose.yml`
- Configure Airflow for high availability
- Use external databases for production

### **Security**
- Change default Airflow credentials
- Configure SSL/TLS for production
- Set up proper authentication

## 📝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `docker-compose up`
5. Submit a pull request

## 📄 **License**

This project is open source and available under the MIT License.

## 🙏 **Acknowledgments**

- **Copenhagen Municipality** for open data initiatives
- **Kaggle** for hosting the cycling dataset
- **Open-Meteo** for historical weather data
- **Apache Foundation** for excellent open-source tools

---

**Built with ❤️ for Copenhagen's cycling community** 🚴‍♂️✨