USE [SalesPilotDW]
GO

/****** Object:  View [dbo].[vw_SaaS_Revenue_Analytics]    Script Date: 3/7/2026 11:40:01 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[vw_SaaS_Revenue_Analytics]
AS
SELECT dbo.FactSubscriptions.SubscriptionID, dbo.DimDate.Year, dbo.DimDate.Month, dbo.DimDate.MonthName, dbo.DimCompany.CompanyName, dbo.DimCompany.Industry, dbo.DimCompany.Country, 
                 dbo.DimCompany.CompanySize, dbo.FactSubscriptions.MRR_Amount, dbo.FactSubscriptions.MRR_Amount * 12 AS ARR, dbo.FactSubscriptions.IsActive, dbo.FactSubscriptions.IsChurned, 
                 dbo.FactSubscriptions.IsUpgrade, dbo.FactSubscriptions.IsDowngrade
FROM    dbo.FactSubscriptions INNER JOIN
                 dbo.DimDate ON dbo.DimDate.DateKey = dbo.FactSubscriptions.SnapshotDateKey INNER JOIN
                 dbo.DimCompany ON dbo.DimCompany.CompanyID = dbo.FactSubscriptions.CompanyID INNER JOIN
                 dbo.DimPlan ON dbo.DimPlan.PlanID = dbo.FactSubscriptions.PlanID
GO

EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPane1', @value=N'[0E232FF0-B466-11cf-A24F-00AA00A3EFFF, 1.00]
Begin DesignProperties = 
   Begin PaneConfigurations = 
      Begin PaneConfiguration = 0
         NumPanes = 4
         Configuration = "(H (1[40] 4[20] 2[20] 3) )"
      End
      Begin PaneConfiguration = 1
         NumPanes = 3
         Configuration = "(H (1 [50] 4 [25] 3))"
      End
      Begin PaneConfiguration = 2
         NumPanes = 3
         Configuration = "(H (1 [50] 2 [25] 3))"
      End
      Begin PaneConfiguration = 3
         NumPanes = 3
         Configuration = "(H (4 [30] 2 [40] 3))"
      End
      Begin PaneConfiguration = 4
         NumPanes = 2
         Configuration = "(H (1 [56] 3))"
      End
      Begin PaneConfiguration = 5
         NumPanes = 2
         Configuration = "(H (2 [66] 3))"
      End
      Begin PaneConfiguration = 6
         NumPanes = 2
         Configuration = "(H (4 [50] 3))"
      End
      Begin PaneConfiguration = 7
         NumPanes = 1
         Configuration = "(V (3))"
      End
      Begin PaneConfiguration = 8
         NumPanes = 3
         Configuration = "(H (1[56] 4[18] 2) )"
      End
      Begin PaneConfiguration = 9
         NumPanes = 2
         Configuration = "(H (1 [75] 4))"
      End
      Begin PaneConfiguration = 10
         NumPanes = 2
         Configuration = "(H (1[66] 2) )"
      End
      Begin PaneConfiguration = 11
         NumPanes = 2
         Configuration = "(H (4 [60] 2))"
      End
      Begin PaneConfiguration = 12
         NumPanes = 1
         Configuration = "(H (1) )"
      End
      Begin PaneConfiguration = 13
         NumPanes = 1
         Configuration = "(V (4))"
      End
      Begin PaneConfiguration = 14
         NumPanes = 1
         Configuration = "(V (2))"
      End
      ActivePaneConfig = 0
   End
   Begin DiagramPane = 
      Begin Origin = 
         Top = 0
         Left = 0
      End
      Begin Tables = 
         Begin Table = "DimDate"
            Begin Extent = 
               Top = 7
               Left = 303
               Bottom = 163
               Right = 488
            End
            DisplayFlags = 280
            TopColumn = 3
         End
         Begin Table = "FactSubscriptions"
            Begin Extent = 
               Top = 7
               Left = 765
               Bottom = 163
               Right = 967
            End
            DisplayFlags = 280
            TopColumn = 6
         End
         Begin Table = "DimCompany"
            Begin Extent = 
               Top = 7
               Left = 46
               Bottom = 163
               Right = 257
            End
            DisplayFlags = 280
            TopColumn = 0
         End
         Begin Table = "DimPlan"
            Begin Extent = 
               Top = 7
               Left = 534
               Bottom = 163
               Right = 719
            End
            DisplayFlags = 280
            TopColumn = 0
         End
      End
   End
   Begin SQLPane = 
   End
   Begin DataPane = 
      Begin ParameterDefaults = ""
      End
   End
   Begin CriteriaPane = 
      Begin ColumnWidths = 11
         Column = 4558
         Alias = 1615
         Table = 1170
         Output = 720
         Append = 1400
         NewValue = 1170
         SortType = 1350
         SortOrder = 1410
         GroupBy = 1350
         Filter = 1350
         Or = 1350
         Or = 1350
         Or = 1350
      End
   End
End
' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'vw_SaaS_Revenue_Analytics'
GO

EXEC sys.sp_addextendedproperty @name=N'MS_DiagramPaneCount', @value=1 , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'VIEW',@level1name=N'vw_SaaS_Revenue_Analytics'
GO

