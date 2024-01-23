import datetime


class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3 
    WHITE = 4  


def latest_financial_index(data: dict):
    for index, financial in enumerate(data.get("financials", [])):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0



def total_revenue(data: dict, financial_index):  
    return data["financials"][financial_index]["pnl"]["lineItems"]["net_revenue"]


def total_borrowing(data: dict, financial_index):
    long_term_borrowings = data["financials"][financial_index]["bs"]["liabilities"]["long_term_borrowings"]
    short_term_borrowings = data["financials"][financial_index]["bs"]["liabilities"]["short_term_borrowings"]
    
    total_borrowings = long_term_borrowings + short_term_borrowings
    
    total_revenue_value = total_revenue(data, financial_index)
    
    ratio = total_borrowings / total_revenue_value
    
    return ratio


def iscr_flag(data: dict, financial_index):
    iscr_value = iscr(data, financial_index)
    
    if iscr_value >= 2:
        return FLAGS.GREEN
    else:
        return FLAGS.RED


def total_revenue_5cr_flag(data: dict, financial_index):
    total_revenue_value = total_revenue(data, financial_index)
    
    if total_revenue_value >= 50000000:  # Assuming 50 million as the threshold
        return FLAGS.GREEN
    else:
        return FLAGS.RED


def iscr(data: dict, financial_index):
   
    interest_expenses = data["financials"][financial_index]["pnl"]["lineItems"]["total_employee_benefit_expense"]
    profit_before_tax = data["financials"][financial_index]["pnl"]["lineItems"]["profit_before_tax"]
    depreciation = data["financials"][financial_index]["pnl"]["lineItems"]["depreciation"]
    
    iscr_value = (profit_before_tax + depreciation + 1) / (interest_expenses + 1)
    
    return iscr_value


def borrowing_to_revenue_flag(data: dict, financial_index):
   
    ratio = total_borrowing(data, financial_index)
    
    if ratio <= 0.25:
        return FLAGS.GREEN
    else:
        return FLAGS.AMBER
