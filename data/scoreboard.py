from json import load, dump

_SCORES_PATH = "data\scores.json"
TOP_N = 3


def _load() -> dict:
    try:
        with open(_SCORES_PATH, "r", encoding="utf-8") as f:
            return load(f)
    except Exception:
        print("Echec du chargement du fichier")
        return {}


def _save(data: dict) -> None:
    with open(_SCORES_PATH, "w", encoding="utf-8") as f:
        dump(data, f, indent=2)


def add_score(level_index: int, score: int, time: float, lives_remaining: int) -> None:
    """Ajoute un score pour un niveau et garde le top TOP_N."""
    data = _load()
    key = str(level_index + 1)
    entries = data.get(key, [])
    entries.append(
        {
            "score": score,
            "time": round(time, 1),
            "lives_remaining": lives_remaining,
        }
    )
    entries.sort(key=lambda e: e["score"], reverse=True)
    data[key] = entries[:TOP_N]
    _save(data)


def get_scores(level_index: int) -> list[dict]:
    """Retourne le top TOP_N pour un niveau (liste de dicts)"""
    data = _load()
    return data.get(str(level_index + 1), [])


def get_all_scores() -> dict:
    """Retourne tous les scores."""
    return _load()
