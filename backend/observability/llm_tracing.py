from config.logging import get_logger

logger = get_logger("navora.llm")


def log_llm_call(graph: str, node: str, tool: str | None, latency_ms: float, result_summary: str):
    logger.info(
        f"LLM/graph call: {graph}.{node}",
        extra={"engine": f"{graph}:{node}:{tool}", "duration_ms": latency_ms},
    )
