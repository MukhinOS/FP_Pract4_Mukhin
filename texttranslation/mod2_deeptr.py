"""
Модуль 2 — deep_translator (п.5)
Без langdetect. Додається перевірка Python >= 3.13.
"""

import sys
from typing import Dict

# Перевірка версії Python
if sys.version_info >= (3, 13):
    raise RuntimeError("Python 3.13+ не підтримує deep_translator!")

try:
    from deep_translator import GoogleTranslator
except Exception as e:
    GoogleTranslator = None
    _tr_err = e
else:
    _tr_err = None


def _ensure_ok():
    if _tr_err:
        raise RuntimeError(f"deep_translator error: {_tr_err}")


# Мінімальний набір мов (стабільно працює)
def _langs_dict() -> Dict[str, str]:
    return {
        "english": "en",
        "ukrainian": "uk",
        "french": "fr",
        "german": "de",
        "spanish": "es"
    }


def CodeLang(lang: str) -> str:
    _ensure_ok()
    l = lang.lower().strip()
    d = _langs_dict()

    # Назва → код
    if l in d:
        return d[l]

    # Код → назва
    for name, code in d.items():
        if code == l:
            return name

    return "Error: unknown language"


def TransLate(text: str, scr: str, dest: str) -> str:
    _ensure_ok()
    try:
        src = None if scr.lower() == "auto" else scr
        if src is None:
            src = "auto"
        return GoogleTranslator(source=src, target=dest).translate(text)
    except Exception as e:
        return f"Error: {e}"


def LanguageList(out="screen", text=""):
    _ensure_ok()
    d = _langs_dict()

    print(f"{'language':12} {'code':6} translated")
    print("-" * 40)

    for name, code in d.items():
        try:
            translated = GoogleTranslator(source="auto", target=code).translate(text) if text else ""
        except:
            translated = "(error)"
        print(f"{name:12} {code:6} {translated}")

    return "Ok"
