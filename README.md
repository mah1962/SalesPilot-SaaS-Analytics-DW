# 🚀 SalesPilotDW: The Next-Gen SaaS Sales Intelligence Hub

**Empowering Data-Driven Decisions through Advanced ETL Engineering and Predictive Analytics.**

---

## 🏗 High-Level Project Architecture
> This diagram illustrates the professional **Medallion Architecture** flow, from raw data ingestion to executive-level business intelligence.

```mermaid
graph LR
    subgraph "Data Sources"
        A[Sales Logs]
        B[Transaction CSVs]
        C[Operational Data]
    end

    subgraph "Data Warehouse (Medallion Architecture)"
        D[(01_Bronze: Raw)] -- "Extraction" --> E[(02_Silver: Cleaned)]
        E -- "Transformation & Star Schema" --> F[(03_Gold: Fact Tables)]
    end

    subgraph "Execution & Monitoring"
        G[06_ETL_Pipeline] -.-> E
        H[Logs] -.-> G
    end

    subgraph "Business Intelligence"
        F --> I[04_Power_BI Dashboards]
        I --> J{Decision Making}
    end

    style D fill:#cd7f32,stroke:#333,stroke-width:2px
    style E fill:#c0c0c0,stroke:#333,stroke-width:2px
    style F fill:#ffd700,stroke:#333,stroke-width:2px
    style G fill:#f96,stroke:#333,stroke-width:4px
    style I fill:#f9f,stroke:#333,stroke-width:2px