USE [SalesPilotDW]
GO

/****** Object:  Index [PK_FactSubscriptions]    Script Date: 3/7/2026 11:26:10 PM ******/
ALTER TABLE [dbo].[FactSubscriptions] ADD  CONSTRAINT [PK_FactSubscriptions] PRIMARY KEY CLUSTERED 
(
	[SubscriptionID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO

ALTER TABLE [dbo].[FactSubscriptions]  WITH CHECK ADD  CONSTRAINT [FK_FactSubscriptions_DimCompany] FOREIGN KEY([CompanyID])
REFERENCES [dbo].[DimCompany] ([CompanyID])
GO

ALTER TABLE [dbo].[FactSubscriptions] CHECK CONSTRAINT [FK_FactSubscriptions_DimCompany]
GO

ALTER TABLE [dbo].[FactSubscriptions]  WITH CHECK ADD  CONSTRAINT [FK_FactSubscriptions_DimDate] FOREIGN KEY([SnapshotDateKey])
REFERENCES [dbo].[DimDate] ([DateKey])
GO

ALTER TABLE [dbo].[FactSubscriptions] CHECK CONSTRAINT [FK_FactSubscriptions_DimDate]
GO

ALTER TABLE [dbo].[FactSubscriptions]  WITH CHECK ADD  CONSTRAINT [FK_FactSubscriptions_DimPlan] FOREIGN KEY([PlanID])
REFERENCES [dbo].[DimPlan] ([PlanID])
GO

ALTER TABLE [dbo].[FactSubscriptions] CHECK CONSTRAINT [FK_FactSubscriptions_DimPlan]
GO




