USE [SalesPilotDW]
GO

/****** Object:  View [dbo].[vw_SaaS_KPI_Dashboard]    Script Date: 3/10/2026 5:04:17 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[vw_SaaS_KPI_Dashboard]
AS
SELECT dbo.DimDate.Year, dbo.DimDate.Month, dbo.DimDate.MonthName, SUM(dbo.FactSubscriptions.MRR_Amount) AS Total_MRR, CAST(ROUND(SUM(dbo.FactSubscriptions.MRR_Amount) * 12, 2) AS DECIMAL(10, 2)) 
                 AS Total_ARR, CAST(ROUND(SUM(CAST(dbo.FactSubscriptions.IsChurned AS INT)) * 1.0 / COUNT(dbo.FactSubscriptions.SubscriptionID), 2) AS DECIMAL(5, 2)) AS Churn_Rate, 
                 SUM(CASE WHEN dbo.FactSubscriptions.IsUpgrade = 1 THEN dbo.FactSubscriptions.MRR_Amount ELSE 0 END) AS Expansion_Revenue, 
                 SUM(CASE WHEN dbo.FactSubscriptions.IsDowngrade = 1 THEN (dbo.FactSubscriptions.MRR_Amount) * (- 1.0) ELSE 0 END) AS Contraction_Revenue, 
                 SUM(CASE WHEN dbo.FactSubscriptions.IsChurned = 1 THEN (dbo.FactSubscriptions.MRR_Amount) * (- 1.0) ELSE 0 END) AS Churned_Revenue, CAST(ROUND((SUM(dbo.FactSubscriptions.MRR_Amount) 
                 + SUM(CASE WHEN dbo.FactSubscriptions.IsUpgrade = 1 THEN dbo.FactSubscriptions.MRR_Amount ELSE 0 END) 
                 + SUM(CASE WHEN dbo.FactSubscriptions.IsDowngrade = 1 THEN (dbo.FactSubscriptions.MRR_Amount) * (- 1.0) ELSE 0 END) 
                 + SUM(CASE WHEN dbo.FactSubscriptions.IsChurned = 1 THEN (dbo.FactSubscriptions.MRR_Amount) * (- 1.0) ELSE 0 END)) / NULLIF (SUM(dbo.FactSubscriptions.MRR_Amount), 0), 2) AS DECIMAL(10, 2)) AS NRR
FROM    dbo.FactSubscriptions LEFT OUTER JOIN
                 dbo.DimDate ON dbo.DimDate.DateKey = dbo.FactSubscriptions.SnapshotDateKey
GROUP BY dbo.DimDate.Year, dbo.DimDate.MonthName, dbo.DimDate.Month
GO

