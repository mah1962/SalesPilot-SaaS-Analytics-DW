USE [SalesPilotDW]
GO

/****** Object:  View [dbo].[vw_Net_Revenue_Retention]    Script Date: 3/8/2026 5:40:57 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW dbo.vw_Net_Revenue_Retention
AS

SELECT
    Revenue.Year,
    Revenue.Month,
    Revenue.MonthName,
    Revenue.Starting_Revenue,
    Revenue.Expansion_Revenue,
    Revenue.Contraction_Revenue,
    Revenue.Churned_Revenue,

(
    Revenue.Starting_Revenue
    + Revenue.Expansion_Revenue
    + Revenue.Contraction_Revenue
    + Revenue.Churned_Revenue
) / NULLIF(Revenue.Starting_Revenue,0) AS NRR

FROM
(

SELECT
    d.Year,
    d.Month,
    d.MonthName,

    SUM(f.MRR_Amount) AS Starting_Revenue,

    SUM(CASE
        WHEN f.IsUpgrade = 1
        THEN f.MRR_Amount
        ELSE 0
    END) AS Expansion_Revenue,

    SUM(CASE
        WHEN f.IsDowngrade = 1
        THEN f.MRR_Amount * (-1.0)
        ELSE 0
    END) AS Contraction_Revenue,

    SUM(CASE
        WHEN f.IsChurned = 1
        THEN f.MRR_Amount * (-1.0)
        ELSE 0
    END) AS Churned_Revenue

FROM dbo.FactSubscriptions f
LEFT JOIN dbo.DimDate d
ON d.DateKey = f.SnapshotDateKey

GROUP BY
    d.Year,
    d.Month,
    d.MonthName

) Revenue

