USE [SalesPilotDW]
GO

/****** Object:  Table [dbo].[FactSubscriptions]    Script Date: 3/7/2026 10:51:41 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[FactSubscriptions](
	[SubscriptionID] [int] NOT NULL,
	[CompanyID] [int] NOT NULL,
	[PlanID] [int] NOT NULL,
	[SnapshotDateKey] [int] NOT NULL,
	[ActiveUsers] [int] NOT NULL,
	[MRR_Amount] [decimal](10, 2) NOT NULL,
	[IsActive] [bit] NOT NULL,
	[IsChurned] [bit] NOT NULL,
	[IsUpgrade] [bit] NOT NULL,
	[IsDowngrade] [bit] NOT NULL,
 CONSTRAINT [PK_FactSubscriptions] PRIMARY KEY CLUSTERED 
(
	[SubscriptionID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[DimCompany]    Script Date: 3/7/2026 10:52:28 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[DimCompany](
	[CompanyID] [int] NOT NULL,
	[CompanyName] [nvarchar](200) NOT NULL,
	[Industry] [nvarchar](150) NOT NULL,
	[Country] [nvarchar](150) NOT NULL,
	[CompanySize] [nvarchar](50) NOT NULL,
	[AcquisitionChannel] [nvarchar](150) NOT NULL,
	[SignupDateKey] [int] NOT NULL,
 CONSTRAINT [PK_DimCompany] PRIMARY KEY CLUSTERED 
(
	[CompanyID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[DimDate]    Script Date: 3/7/2026 10:52:39 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[DimDate](
	[DateKey] [int] NOT NULL,
	[FullDate] [date] NOT NULL,
	[Day] [tinyint] NOT NULL,
	[Month] [tinyint] NOT NULL,
	[MonthName] [nvarchar](50) NOT NULL,
	[Quarter] [tinyint] NOT NULL,
	[Year] [smallint] NOT NULL,
	[WeekNumber] [tinyint] NOT NULL,
 CONSTRAINT [PK_DimDate] PRIMARY KEY CLUSTERED 
(
	[DateKey] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[DimPlan]    Script Date: 3/7/2026 10:52:53 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[DimPlan](
	[PlanID] [int] NOT NULL,
	[PlanName] [nvarchar](50) NOT NULL,
	[BasePrice] [decimal](10, 2) NOT NULL,
	[UserFee] [decimal](10, 2) NOT NULL,
	[BillingCycle] [nvarchar](50) NOT NULL,
	[TierLevel] [tinyint] NOT NULL,
 CONSTRAINT [PK_DimPlan] PRIMARY KEY CLUSTERED 
(
	[PlanID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


