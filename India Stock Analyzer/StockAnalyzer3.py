"""
Fundamental Stock Analyzer v5.0 (Part 1 + Part 2)
Requires:
    pip install yfinance requests
"""

#+------------------------------------------------------+
#| Imports section                                      
#+------------------------------------------------------+

import requests
import yfinance as yf


#+------------------------------------------------------+
#| Utility Functions definitions                        
#+------------------------------------------------------+
def format_number(v):
    if v is None:
        return "N/A"
    if isinstance(v,(int,float)):
        return f"{v:.2f}" if isinstance(v,float) else f"{v:,}"
    return str(v)

def format_market_cap(v):
    if v is None: return "N/A"
    return f"₹{v/10000000:,.2f} Cr"

def format_crore(value):
    """
    Convert a number to Indian Crores.
    Example:
    278450000000 -> ₹27,845.00 Cr
    """
    if value is None:
        return "N/A"

    crore = value / 10000000
    return f"₹{crore:,.2f} Cr"

#+------------------------------------------------------+
#| Search Functions                                     |
#+------------------------------------------------------+

def search_company(query):
    url="https://query2.finance.yahoo.com/v1/finance/search"
    r=requests.get(url,params={"q":query,"quotesCount":10,"newsCount":0},
                   headers={"User-Agent":"Mozilla/5.0"},timeout=10)
    r.raise_for_status()
    quotes=r.json().get("quotes",[])
    res=[]
    for q in quotes:
        sym=q.get("symbol","")
        if sym.endswith(".NS"):
            res.append({"symbol":sym,
                        "name":q.get("shortname") or q.get("longname") or sym})
    return res

def select_symbol():
    while True:
        q=input("Enter Company Name / NSE Symbol : ").strip()
        res=search_company(q)
        if not res:
            print("No NSE companies found. Try again.\n")
            continue
        if len(res)==1:
            print(f"Selected : {res[0]['name']} ({res[0]['symbol']})\n")
            return res[0]["symbol"]
        print("\nMultiple companies found:\n")
        for i,r in enumerate(res,1):
            print(f"{i}. {r['name']} ({r['symbol']})")
        while True:
            try:
                c=int(input(f"\nSelect Company (1-{len(res)}): "))
                if 1<=c<=len(res):
                    return res[c-1]["symbol"]
            except:
                pass
            print("Invalid selection.")

def score(metric,val):
    if val is None: return ("N/A",0)
    if metric=="Current Ratio":
        return ("Excellent",10) if 1<=val<=2.5 else ("Good",8) if .8<=val<1 else ("Poor",0)
    if metric=="Quick Ratio":
        return ("Excellent",10) if val>=1.5 else ("Good",8) if val>=1 else ("Poor",0)
    if metric=="Debt/Equity":
        return ("Excellent",10) if val<=0.25 else ("Good",8) if val<=0.5 else ("Average",5) if val<=1 else ("Poor",0)
    if metric=="ROE":
        return ("Excellent",10) if val>=20 else ("Good",8) if val>=15 else ("Average",5) if val>=10 else ("Poor",0)
    if metric=="ROA":
        return ("Excellent",10) if val>=10 else ("Good",8) if val>=5 else ("Average",5) if val>=2 else ("Poor",0)
    if metric=="Price/Book":
        return ("Excellent",10) if val<=2 else ("Good",8) if val<=3 else ("Average",5) if val<=5 else ("Poor",0)
    if metric=="Dividend Yield":
        return ("Excellent",10) if 2<=val<=5 else ("Good",8) if 1<=val<2 else ("Average",5) if val>5 else ("Poor",0)
    return ("N/A",0)

#+------------------------------------------------------+
#| Financial Functions                                  |
#+------------------------------------------------------+

def print_financial_table(title, data):
    """
    Displays a financial metric for the last 3 financial years.
    """

    print()
    print("=" * 70)
    print(title.center(70))
    print("=" * 70)

    if not data:
        print("Data not available.")
        return

    print(f"{'Financial Year':<20}{'Value':>25}")
    print("-" * 45)

    for year, value in data:
        print(f"{year:<20}{format_crore(value):>25}")

    print("-" * 45)
    
    
def get_financial_data(statement, row_name):
    """
    Returns last 3 financial years.

    Example:
    get_financial_data(income_stmt,"Net Income")
    """

    output = []

    try:

        if row_name in statement.index:

            values = statement.loc[row_name]

            for year, value in values.items():

                output.append((year.year, value))

            return output[:3]

    except Exception:
        pass

    return []
#+------------------------------------------------------+
#| Main Program                              
#+------------------------------------------------------+

while True:
    print("="*70)
    print("               FUNDAMENTAL STOCK ANALYZER")
    print("="*70)
    symbol=select_symbol()
    stock = yf.Ticker(symbol)

    info = stock.info

    income_stmt = stock.income_stmt
    cashflow = stock.cashflow
    f={
    "Company":info.get("longName"),
    "Sector":info.get("sector"),
    "Industry":info.get("industry"),
    "Current Price":info.get("currentPrice"),
    "Market Cap":info.get("marketCap"),
    "Current Ratio":info.get("currentRatio"),
    "Quick Ratio":info.get("quickRatio"),
    "Debt/Equity":(info.get("debtToEquity")/100 if info.get("debtToEquity") is not None else None),
    "ROE":(info.get("returnOnEquity") or 0)*100,
    "ROA":(info.get("returnOnAssets") or 0)*100,
    "Price/Book":info.get("priceToBook"),
    "Dividend Yield":info.get("dividendYield"),
    "stock_pe": info.get("trailingPE"),
    "face_value": info.get("faceValue")
    }
    print("="*70)
    print("COMPANY DETAILS")
    print("="*70)
    print(f"Company       : {f['Company']}")
    print(f"Symbol        : {symbol}")
    print(f"Sector        : {f['Sector']}")
    print(f"Industry      : {f['Industry']}")
    print(f"Current Price : ₹{format_number(f['Current Price'])}")
    print(f"Market Cap    : {format_market_cap(f['Market Cap'])}")
    print(f"Stock P/E          : {format_number(f['stock_pe'])}")
    #print(f"Face Value         : ₹{format_number(f['face_value'])}")
    print("\n"+"="*70)
    print("FUNDAMENTAL ANALYSIS")
    print("="*70)
    print(f"{'Metric':20}{'Value':12}{'Rating':15}{'Score'}")
    print("-"*70)
    metrics=["Current Ratio","Quick Ratio","Debt/Equity","ROE","ROA","Price/Book","Dividend Yield"]
    total=0
    for m in metrics:
        v=f[m]
        rating,s=score(m,v)
        total+=s
        disp=format_number(v)
        if m in ("ROE","ROA","Dividend Yield"):
            disp+=" %"
        print(f"{m:20}{disp:12}{rating:15}{s}/10")
    print("-"*70)
    norm=round(total/70*100)
    if norm>=90: rec=("EXCELLENT","STRONG BUY")
    elif norm>=80: rec=("VERY GOOD","BUY")
    elif norm>=70: rec=("GOOD","ACCUMULATE")
    elif norm>=60: rec=("AVERAGE","HOLD")
    else: rec=("POOR","AVOID")
    print(f"Overall Score : {total} / 70 ({norm}/100)")
    print(f"Overall Rating: {rec[0]}")
    print(f"Recommendation: {rec[1]}")
    #input("\nPress Enter to exit...")
    print("=" * 70)
    
    
#    +------------------------------------------------------+
#    | Display Functions                                    |
#    +------------------------------------------------------+
    pat_data = get_financial_data(
        income_stmt,
        "Net Income"
    )

    print_financial_table(
        "LAST 3 YEARS PROFIT AFTER TAX (PAT)",
        pat_data
    )
        
        
    ebitda_data = get_financial_data(
        income_stmt,
        "EBITDA"
    )

    print_financial_table(
        "LAST 3 YEARS EBITDA",
        ebitda_data
    )  


    fcf_data = get_financial_data(
        cashflow,
        "Free Cash Flow"
    )

    print_financial_table(
        "LAST 3 YEARS FREE CASH FLOW",
        fcf_data
    )  

    choice = input(
        "\nPress ENTER to analyze another stock or type EXIT to quit: "
    ).strip().upper()

    if choice == "EXIT":
        print("\nThank you for using Fundamental Stock Analyzer.")
        break