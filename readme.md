# ERP Daily Sales ETL Pipeline

This project automates the extraction of sales data from a PostgreSQL database and saves a transformed CSV to a local OneDrive-synced folder.

## Key Design Choices
* **Orchestration:** Used **Apache Airflow** to handle scheduling and retry logic.
* **Database:** **PostgreSQL** was chosen as the source to mimic a standard ERP transactional database.
* **Data Handling:** Used **Pandas** for transformation because it handles missing values and column calculations efficiently for medium-sized datasets.
* **Storage Strategy:** Instead of complex API calls, we use **Docker Volume Mounting** to write directly to a OneDrive-synced path on the host machine.

## Prerequisites
* Docker and Docker Desktop installed.
* Windows/Linux/Mac with a folder named `Bucket` in your OneDrive.

## Setup and Running
1. **Clone the repository:**
   `git clone <your-repo-link>`

2. **Initialize Docker:**
   Run `docker compose down -v` (to ensure a fresh start) then `docker compose up --build -d`.

3. **Configure Connection:**
   - Open Airflow at `localhost:8080` (default user: `airflow`, pass: `airflow`).
   - Go to **Admin > Connections** and create a connection with ID `postgres`.
   - **Host:** `postgres`, **Login:** `postgres`, **Password:** `postgres123`.

4. **Run the Pipeline:**
   Toggle the `daily_sales` DAG to **On** and click the **Trigger** button.