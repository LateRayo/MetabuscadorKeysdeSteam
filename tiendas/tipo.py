import re

_ACCOUNT_PATTERNS = [
    r"\baccount\b",
    r"\bcuenta\b",
    r"\bsteam\s*account\b",
    r"\bsteam\s*cuenta\b",
    r"\bsteam[-_ ]?acc(?:ount)?\b",
]


def inferir_tipo(titulo, extra_texts=None):
    partes = []
    if titulo:
        partes.append(str(titulo))
    if extra_texts:
        for t in extra_texts:
            if t:
                partes.append(str(t))

    texto = " ".join(partes).lower()
    for patron in _ACCOUNT_PATTERNS:
        if re.search(patron, texto):
            return "account"

    return "game-key"
