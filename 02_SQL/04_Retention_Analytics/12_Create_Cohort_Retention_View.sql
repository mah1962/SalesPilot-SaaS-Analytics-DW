USE SalesPilotDW;
GO
drop view dbo.vw_Retention_Rate
CREATE VIEW dbo.vw_Retention_Rate
AS 
WITH CohortData AS
(
SELECT
	c.CompanyID,
	DATEFROMPARTS(YEAR(fs.SnapshotDateKey),MONTH(fs.SnapshotDateKey),1)AS CohortMonth,
	DATEFROMPARTS(YEAR(d.FullDate),MONTH(d.FullDate),1)AS ActivityMonth
FROM FactSubscriptions fs
JOIN DimCompany c
ON fs.CompanyID=c.CompanyID
JOIN DimDate d
ON fs.SnapshotDateKey=d.DateKey
JOIN DimDate ds
ON ds.DateKey=c.SignupDateKey
),
MonthIndexCalc AS
(
SELECT
	CompanyID,
	CohortMonth,
	ActivityMonth,
	DATEDIFF(MONTH,CohortMonth,ActivityMonth)AS MonthIndex
FROM CohortData
),
CustomersCounts AS
(
SELECT
	CohortMonth,
	MonthIndex,
	COUNT(DISTINCT CompanyID)AS ActiveCompanies
FROM MonthIndexCalc
GROUP BY
	CohortMonth,
	MonthIndex
),
BaseCustomers AS
(
SELECT
	CohortMonth,
	ActiveCompanies AS CohortSize
FROM CustomersCounts
WHERE MonthIndex=0
)
SELECT
	c.CohortMonth,
	c.MonthIndex,
	c.ActiveCompanies,
	CAST(1.0*c.ActiveCompanies/b.CohortSize AS DECIMAL(5,2))AS Retention_Rate
FROM CustomersCounts c 
JOIN BaseCustomers b
ON c.CohortMonth=b.CohortMonth;


