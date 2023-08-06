from enum import Enum


class OrderState(Enum):
    """Order State"""

    Active = "active"
    Consummated = "consummated"
    Inactive = "inactive"
    Withdrawn = "withdrawn"


class OrderType(Enum):
    """Order Type"""

    Bid = "bid"
    Offer = "offer"
    RFBid = "rf bid"
    RFOffer = "rf offer"


class CurveType(Enum):
    """Curve Type"""

    Relative = "relative forward curve"
    Absolute = "absolute forward curve"


class MatFrequency(Enum):
    """Derivative Maturity Frequency"""

    Week = "week"
    Month = "month"
    Quarter = "quarter"
    Season = "season"
    Year = "year"
    GasYear = "gas year"


class ContractType(Enum):
    """Contract Type"""

    Spot = "spot"
    Forward = "forward"
    Future = "future"
    Swap = "swap"
    Strip = "strip"
    CFD = "cfd"
    Index = "index"
    OfficialSellingPrice = "official selling price"
    Yield = "yield"
    Contract = "contract"
    ESS = "ess"
    Prompt = "prompt"
    Statistic = "statistic"
    EFP = "efp"
    Netback = "netback"
    EFS = "efs"
    Rack = "rack"


class AssessmentFrequency(Enum):
    """Asessment Frequency"""

    Intraday = "Intraday"
    Daily = "Daily (7 day)"
    DailyWeekday = "Daily (weekday)"
    DailyBidweekOnly = "Daily (bidweek only)"
    SemiWeekly = "Semi-weekly"
    Weekly = "Weekly"
    SemiMonthly = "Semi-monthly"
    Monthly = "Monthly"
    EveryOtherMonth = "Every other month"
    Quarterly = "Quarterly"
    SemiAnnual = "Semi-annual"
    Yearly = "Yearly"
