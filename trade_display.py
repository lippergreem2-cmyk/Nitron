# ==========================================================
# NITRON TRADE DISPLAY
# Formats trading output into tables
# ==========================================================


def line():
    return "=" * 55



def show_analysis(report):

    print(line())
    print("             NITRON TRADE ANALYSIS")
    print(line())

    print()

    print(f"{'Symbol':15}: {report.get('symbol','N/A')}")
    print(f"{'Action':15}: {report.get('action','WAIT')}")
    print(f"{'Confidence':15}: {report.get('confidence','N/A')}%")

    print()

    print("-" * 55)
    print("PRICE PLAN")
    print("-" * 55)

    print(f"{'Entry':15}: {report.get('entry','N/A')}")
    print(f"{'Stop Loss':15}: {report.get('stop_loss','N/A')}")
    print(f"{'Take Profit':15}: {report.get('take_profit','N/A')}")

    print()

    print("-" * 55)
    print("RISK MANAGEMENT")
    print("-" * 55)

    print(f"{'Lot Size':15}: {report.get('lot_size','N/A')}")
    print(f"{'Risk Reward':15}: {report.get('risk_reward','N/A')}")

    print()

    print("-" * 55)
    print("MESSAGE")
    print("-" * 55)

    print(report.get(
        "message",
        "No message"
    ))

    print()
    print(line())



def show_open_trade(trade):

    print(line())
    print("              NITRON ACTIVE TRADE")
    print(line())

    print()

    print(f"{'Ticket':15}: {trade.get('ticket')}")
    print(f"{'Symbol':15}: {trade.get('symbol')}")
    print(f"{'Action':15}: {trade.get('action')}")
    print(f"{'Lot':15}: {trade.get('lot')}")
    print(f"{'Entry':15}: {trade.get('entry')}")
    print(f"{'Stop Loss':15}: {trade.get('stop_loss')}")
    print(f"{'Take Profit':15}: {trade.get('take_profit')}")
    print(f"{'Status':15}: {trade.get('status')}")
    print(f"{'Mode':15}: {trade.get('mode')}")

    print()
    print(line())
