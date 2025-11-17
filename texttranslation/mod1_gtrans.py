from typing import Dict
"""
Модуль 1.
Реалізація функцій TransLate / LangDetect / CodeLang / LanguageList
з використанням googletrans 4.x (п.4).
"""
try:
    from googletrans import Translator, LANGUAGES
except Exception as e:
    Translator = None
    LANGUAGES = {}
    _import_error = e
else:
    _import_error = None

def _ensure_ok():
    if _import_error:
        raise RuntimeError(f"googletrans import error: {_import_error}")
    if Translator is None:
        raise RuntimeError("googletrans not available")

def CodeLang(lang: str) -> str:
    _ensure_ok()
    if not lang:
        return "Error: empty argument"
    l = lang.strip().lower()
    if l in LANGUAGES:
        return LANGUAGES[l]
    for code, name in LANGUAGES.items():
        if name.lower() == l:
            return code
    return "Error: unknown language"

def TransLate(text: str, scr: str, dest: str) -> str:
    _ensure_ok()
    if not isinstance(text, str) or not text.strip():
        return "Error: empty text"
    tr = Translator()

    def _norm_lang(value: str, allow_auto: bool = False):
        if not value:
            return "Error: bad language value"
        v = value.strip().lower()
        if allow_auto and v == "auto":
            return "auto"
        if v in LANGUAGES:
            return v
        for code, name in LANGUAGES.items():
            if name.lower() == v:
                return code
        return "Error: unknown language"

    src_code = _norm_lang(scr, allow_auto=True)
    if isinstance(src_code, str) and src_code.startswith("Error"):
        return src_code
    dest_code = _norm_lang(dest, allow_auto=False)
    if isinstance(dest_code, str) and dest_code.startswith("Error"):
        return dest_code
    try:
        res = tr.translate(text, src=src_code, dest=dest_code)
        return res.text
    except Exception as e:
        return f"Error: {e}"

def LangDetect(text: str, set: str = "all") -> str:
    _ensure_ok()
    if not isinstance(text, str) or not text.strip():
        return "Error: empty text"
    set = (set or "all").lower()
    try:
        tr = Translator()
        d = tr.detect(text)
        lang_code = d.lang
        conf = getattr(d, "confidence", None)
        conf_str = str(conf) if conf is not None else "N/A"
        if set == "lang":
            return lang_code
        elif set == "confidence":
            return conf_str
        else:
            return f"{lang_code} {conf_str}"
    except Exception as e:
        return f"Error: {e}"

def LanguageList(out: str = "screen", text: str = "") -> str:
    _ensure_ok()
    out = (out or "screen").lower()
    has_text = isinstance(text, str) and len(text) > 0
    tr = Translator() if has_text else None
    rows = []
    for code, name in sorted(LANGUAGES.items(), key=lambda kv: kv[1]):
        translated = ""
        if has_text and tr is not None:
            try:
                translated = tr.translate(text, src="auto", dest=code).text
            except Exception as e:
                translated = f"(err: {e})"
        rows.append((name, code, translated))
    if out == "file":
        import csv, os
        path = os.path.join(os.path.dirname(__file__), "..", "languages_gtrans.csv")
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
