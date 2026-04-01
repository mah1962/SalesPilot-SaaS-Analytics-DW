USE [SalesPilotDW]
GO

/****** Object:  View [dbo].[vw_Churn_Analysis]    Script Date: 3/8/2026 3:16:45 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

ALTER VIEW [dbo].[vw_Churn_Analysis]
AS
SELECT dbo.DimDate.Year, dbo.DimDate.Month, dbo.DimDate.MonthName, COUNT(dbo.FactSubscriptions.SubscriptionID) AS Total_Customers, SUM(CAST(dbo.FactSubscriptions.IsChurned AS INT)) AS Churned_Customers,
CAST(ROUND(SUM(CAST(dbo.FactSubscriptions.IsChurned AS INT))*1.0/COUNT(dbo.FactSubscriptions.SubscriptionID),2) AS DECIMAL(5,2)) AS Churn_Rate
FROM    dbo.FactSubscriptions LEFT OUTER JOIN
                 dbo.DimDate ON dbo.DimDate.DateKey = dbo.FactSubscriptions.SnapshotDateKey
GROUP BY dbo.DimDate.Year, dbo.DimDate.Month, dbo.DimDate.MonthName

GO



