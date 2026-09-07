from core.engines.landed_cost.calculator import calculate_landed_cost


def test_landed_cost_components_sum_to_total():
    result = calculate_landed_cost(
        vessel_class="Panamax", freight_rate_usd_per_ton=13.0, cargo_quantity=80000,
        port_name="Vizag", distance_nm=4200, bunker_price=560, commodity_price_usd_per_ton=220,
    )
    component_sum = round(
        result["freight_cost"] + result["port_charges"] + result["insurance"] +
        result["levies"] + result["bunker_cost"] + result["other_costs"], 2
    )
    assert component_sum == result["total_cost"]
    assert result["cost_per_ton"] > 0
    assert result["total_cost"] > 0
