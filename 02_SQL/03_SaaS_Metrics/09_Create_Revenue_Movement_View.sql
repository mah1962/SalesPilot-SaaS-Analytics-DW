USE [SalesPilotDW]
GO

/****** Object:  View [dbo].[vw_Revenue_Movement]    Script Date: 3/8/2026 5:40:57 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[vw_Revenue_Movement]
AS
SELECT dbo.DimDate.Year, dbo.DimDate.Month, dbo.DimDate.MonthName, SUM(CASE
WHEN dbo.FactSubscriptions.IsUpgrade = 1
THEN dbo.FactSubscriptions.MRR_Amount
ELSE 0
END) AS Expansion_Revenue,
SUM(CASE
WHEN dbo.FactSubscriptions.IsDowngrade = 1
THEN (dbo.FactSubscriptions.MRR_Amount)*(-1.0)
ELSE 0
END) AS Contraction_Revenue
FROM    dbo.FactSubscriptions LEFT OUTER JOIN
                 dbo.DimDate ON dbo.DimDate.DateKey = dbo.FactSubscriptions.SnapshotDateKey
GROUP BY dbo.DimDate.Year, dbo.DimDate.Month, dbo.DimDate.MonthName
GO


