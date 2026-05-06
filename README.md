# Industrial Energy Intelligence Tracker (Germany)

An end-to-end Data Engineering pipeline that transforms raw European grid data into an actionable Industrial Intelligence System.

## Project Goal
To simulate an industrial energy management system that helps a factory manager optimize production based on real-time grid load, renewable availability, and market pricing in Germany.

## The Tech Stack
*   **Python (Pandas/SQLAlchemy):** For ETL automation and data transformation.
*   **SQLite:** As the centralized "Source of Truth" for processed time-series data.
*   **Jupyter Notebooks:** Used for initial Exploratory Data Analysis (EDA).
*   **Git/GitHub:** For version control and documentation.

## The ETL Pipeline
The pipeline handles a high-dimensional dataset (300+ columns) by:
1.  **Extraction:** Filtering for relevant German (DE) sensors to optimize memory.
2.  **Transformation:**
    *   **Unpivoting (Melt):** Converting "Wide" data into a "Long" format for better scalability in Power BI.
    *   **Smart Interpolation:** Filling minor sensor gaps (limit=2h) while preserving historical data gaps (e.g., the 2015-2018 price period).
3.  **Loading:** Automatically creating/updating a structured SQLite database.

## Key Insights from EDA
*   **Correlation:** Energy prices in the DE_LU zone strongly correlate with total load, but show significant crashes during high wind/solar generation periods.
*   **Peak Shaving Opportunity:** Identified an average price peak at 8:00 AM and 5:00 PM, suggesting a "Peak Shaving" strategy for heavy industrial operations.
