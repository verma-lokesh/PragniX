NM_PER_KM = 0.539957


def tons_to_kg(tons: float) -> float:
    return tons * 1000


def km_to_nm(km: float) -> float:
    return km * NM_PER_KM


def nm_to_km(nm: float) -> float:
    return nm / NM_PER_KM


def per_ton(total: float, quantity_tons: float) -> float:
    if quantity_tons <= 0:
        return 0.0
    return round(total / quantity_tons, 2)
