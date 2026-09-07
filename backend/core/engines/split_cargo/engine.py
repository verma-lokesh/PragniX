from core.interfaces.engine import Engine
from core.engines.split_cargo.optimizer import build_single_vessel_option, build_multi_vessel_option


class SplitCargoEngine(Engine):
    name = "SplitCargoEngine"

    def execute(self, context) -> None:
        dr = context.decision_request
        recs = context.recommendation_result or []
        feasible_recs = [r for r in recs if r["is_feasible"]]
        if not feasible_recs:
            context.split_cargo_result = {"options": [], "recommended_option": "NONE"}
            return

        top = feasible_recs[0]
        single_cost_per_ton = top["landed_cost"]["cost_per_ton"] if top.get("landed_cost") else 0
        smaller_class = "Supramax" if top["vessel_class"] in ("Panamax", "Capesize") else "Handysize"
        smaller_rec = next((r for r in feasible_recs if r["vessel_class"] == smaller_class), None)
        multi_cost_per_ton = smaller_rec["landed_cost"]["cost_per_ton"] if smaller_rec and smaller_rec.get("landed_cost") else single_cost_per_ton * 1.08

        option_a = build_single_vessel_option(top["vessel_class"], dr.cargo_quantity, single_cost_per_ton)
        option_b = build_multi_vessel_option(smaller_class, dr.cargo_quantity, multi_cost_per_ton)

        recommended = "Option A - Single Vessel" if option_a["total_cost"] <= option_b["total_cost"] else "Option B - Split Cargo"

        option_a["is_recommended"] = recommended == option_a["option_label"]
        option_b["is_recommended"] = recommended == option_b["option_label"]

        context.split_cargo_result = {
            "options": [option_a, option_b],
            "recommended_option": recommended,
        }
