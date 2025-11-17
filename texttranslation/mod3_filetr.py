"""
Модуль 3 — deep_translator + langdetect (п.6, остаточна версія)
"""

from typing import Dict

try:
    from deep_translator import GoogleTranslator
except Exception as e:
    GoogleTranslator = None
    _tr_err = e
else:
    _tr_err = None

try:
    from langdetect import detect, detect_langs
except Exception as e:
    detect = None
    detect_langs = None
    _ld_err = e
else:
    _ld_err = None


def _ensure_ok():
    if _tr_err:
        raise RuntimeError(f"deep_translator import error: {_tr_err}")
    if _ld_err:
        raise RuntimeError(f"langdetect import error: {_ld_err}")


def _langs_dict() -> Dict[str, str]:
    """Отримує словник мов: назва → код."""
    try:
        langs = GoogleTranslator().get_supported_languages(as_dict=True)
        if isinstance(langs, dict):
            return {name.lower(): code for code, name in langs.items()}
        else:
            langs = GoogleTranslator().get_supported_languages()
            return {name.lower(): name[:2].lower() for name in langs}
    except Exception:
        # запасний список
        return {"english": "en", "ukrainian": "uk", "french": "fr", "german": "de", "spanish": "es"}


def CodeLang(lang: str) -> str:
    _ensure_ok()
    if not lang:
        return "Error: empty argument"
    l = lang.strip().lower()
    d = _langs_dict()
    if not d:
        return "Error: languages unavailable"
    # якщо назва
    if l in d:
        return d[l]
    # якщо код
    for name, code in d.items():
        if code.lower() == l:
            return name
    return "Error: unknown language"


def TransLate(text: str, scr: str, dest: str) -> str:
    _ensure_ok()
    if not text:
        return "Error: empty text"
    try:
        # мапа скорочень на повні назви
        lang_map = {
            "uk": "ukrainian",
            "en": "english",
            "fr": "french",
            "de": "german",
            "es": "spanish",
            "auto": "auto"
        }
        src = lang_map.get(scr.lower(), scr)
        dst = lang_map.get(dest.lower(), dest)
        return GoogleTranslator(source=src, target=dst).translate(text)
    except Exception as e:
        return f"Error: {e}"



def LangDetect(text: str, set: str = "all") -> str:
    _ensure_ok()
    if not text:
        return "Error: empty text"
    set = (set or "all").lower()
    try:
        lang_code = detect(text)
        conf = "N/A"
        if detect_langs:
            probs = detect_langs(text)
            if probs:
                for lp in probs:
                    s = str(lp)
                    if ':' in s:
                        code, sc = s.split(':', 1)
                        if code == lang_code:
                            conf = sc
                            break
        if set == "lang":
            return lang_code
        elif set == "confidence":
            return str(conf)
        else:
            return f"{lang_code} {conf}"
    except Exception as e:
        return f"Error: {e}"


def LanguageList(out: str = "screen", text: str = "") -> str:
    _ensure_ok()
    d = _langs_dict()
    if not d:
        return "Error: languages unavailable"
    pairs = sorted(d.items(), key=lambda kv: kv[0])
    has_text = isinstance(text, str) and len(text) > 0
    rows = []
    for name, code in pairs:
        translated = ""
        if has_text:
            try:
                translated = GoogleTranslator(source="auto", target=code).translate(text)
            except Exception as e:
                translated = f"(err: {e})"
        rows.append((name, code, translated))

    if (out or "screen").lower() == "file":
        import csv, os
        path = os.path.join(os.path.dirname(__file__), "..", "languages_file.csv")
        path = os.path.abspath(path)
        try:
            with open(path, "w", encoding="utf-8", newline="") as f:
                w = csv.writer(f, delimiter=";")
                header = ["language", "code"]
                if has_text:
                    header.append("translated_text")
                w.writerow(header)
                for name, code, translated in rows:
                    if has_text:
                        w.writerow([name, code, translated])
                    else:
                        w.writerow([name, code])
            return "Ok"
        except Exception as e:
            return f"Error: {e}"
    else:
        col1 = max(len("language"), *(len(r[0]) for r in rows))
        col2 = max(len("code"), *(len(r[1]) for r in rows))
        header = f"{'language'.ljust(col1)}  {'code'.ljust(col2)}"
        if has_text:
            header += "  translated_text"
        print(header)
        print("-" * len(header))
        for name, code, translated in rows:
            line = f"{name.ljust(col1)}  {code.ljust(col2)}"
            if has_text:
                line += "  " + translated
            print(line)
        return "Ok"
