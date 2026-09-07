from core.guardrails.validators import (
    validate_commodity, validate_origin_destination, validate_dates,
    validate_quantity, validate_contract_preference,
)
from core.exceptions import GuardrailViolation


def run_input_guardrail(decision_request) -> None:
    errors: list[str] = []
    errors += validate_commodity(decision_request.commodity)
    errors += validate_origin_destination(decision_request.origin, decision_request.destination)
    errors += validate_dates(decision_request.earliest_loading_date, decision_request.latest_delivery_date)
    errors += validate_quantity(decision_request.cargo_quantity)
    errors += validate_contract_preference(decision_request.contract_preference)

    if errors:
        raise GuardrailViolation("; ".join(errors))
