USE [SalesPilotDW]
GO

/****** Object:  View [dbo].[vw_Customer_LTV]    Script Date: 3/9/2026 11:03:46 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[vw_Customer_LTV]
AS
SELECT dbo.DimDate.Year, dbo.DimDate.Month, dbo.DimDate.MonthName, COUNT(DISTINCT dbo.FactSubscriptions.CompanyID) AS Customers, AVG(dbo.FactSubscriptions.MRR_Amount) AS ARPU, 
                 CAST(ROUND(COUNT(DISTINCT CASE WHEN dbo.FactSubscriptions.Ischurned = 1 THEN dbo.FactSubscriptions.CompanyID END)*1.0/
                 NULLIF(
        COUNT(DISTINCT CASE
            WHEN dbo.FactSubscriptions.IsActive = 1
            THEN dbo.FactSubscriptions.CompanyID
        END)
    ,0),2)AS DECIMAL(10,2)) AS Churn,
    CAST(
    ROUND(AVG(dbo.FactSubscriptions.MRR_Amount)/
    NULLIF(CAST(ROUND(COUNT(DISTINCT CASE WHEN dbo.FactSubscriptions.Ischurned = 1 THEN dbo.FactSubscriptions.CompanyID END)*1.0/
                 NULLIF(
        COUNT(DISTINCT CASE
            WHEN dbo.FactSubscriptions.IsActive = 1
            THEN dbo.FactSubscriptions.CompanyID
        END)
    ,0),2)AS DECIMAL(10,2)),0),2)AS DECIMAL(10,2))AS Customer_LTV
FROM    dbo.FactSubscriptions LEFT OUTER JOIN
                 dbo.DimDate ON dbo.DimDate.DateKey = dbo.FactSubscriptions.SnapshotDateKey
GROUP BY dbo.DimDate.Year, dbo.DimDate.Month, dbo.DimDate.MonthName
GO


