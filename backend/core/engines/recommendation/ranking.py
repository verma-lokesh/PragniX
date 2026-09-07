def rank_options(options: list[dict]) -> list[dict]:
    ranked = sorted(options, key=lambda o: o["score"], reverse=True)
    rank = 1
    for o in ranked:
        if o["is_feasible"]:
            o["rank"] = rank
            rank += 1
        else:
            o["rank"] = 999
    ranked.sort(key=lambda o: o["rank"])
    return ranked
