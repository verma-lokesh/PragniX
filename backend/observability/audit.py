"""Helpers for constructing DecisionAudit-friendly summaries (used by
the orchestrator's persistence step). Never logs secrets/credentials."""


def summarize_input(decision_request) -> str:
    return (
        f"{decision_request.commodity} {decision_request.cargo_quantity}t "
        f"{decision_request.origin}->{decision_request.destination}"
    )
