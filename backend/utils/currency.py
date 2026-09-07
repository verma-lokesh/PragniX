DEFAULT_FX = {"USD": 1.0, "INR": 83.5}


def convert(amount: float, from_ccy: str, to_ccy: str, fx_table: dict | None = None) -> float:
    table = fx_table or DEFAULT_FX
    if from_ccy == to_ccy:
        return round(amount, 2)
    usd_amount = amount / table.get(from_ccy, 1.0)
    return round(usd_amount * table.get(to_ccy, 1.0), 2)
