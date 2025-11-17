import os, re, sys, importlib, configparser
from texttranslation import mod3_filetr as detect_mod

def count_stats(s: str):
    chars = len(s)
    words = len(re.findall(r"\b\w+\b", s, flags=re.UNICODE))
    sentences = len(re.findall(r"[.!?]+", s, flags=re.UNICODE))
    return chars, words, sentences

def read_limited(path: str, max_c: int, max_w: int, max_s: int) -> str:
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            out.append(line)
            text = "".join(out)
            chars, words, sentences = count_stats(text)
            if (max_c and chars >= max_c) or (max_w and words >= max_w) or (max_s and sentences >= max_s):
                break
    return "".join(out)

if __name__ == "__main__":
    cfg = configparser.ConfigParser()
    cfg.read("config.ini", encoding="utf-8")
    if "run" not in cfg:
        print("Error: config [run] section missing")
        sys.exit(1)
    run = cfg["run"]
    text_file = run.get("text_file", "text.txt")
    dest = run.get("dest_lang", "en")
    module_name = run.get("module", "mod3_filetr")
    output = run.get("output", "screen").lower()
    limit_chars = run.getint("limit_chars", 0)
    limit_words = run.getint("limit_words", 0)
    limit_sentences = run.getint("limit_sentences", 0)
    try:
        if not os.path.exists(text_file):
            print(f"Error: file not found: {text_file}")
            sys.exit(1)
        size = os.path.getsize(text_file)
        with open(text_file, "r", encoding="utf-8") as f:
            full_text = f.read()
        chars, words, sentences = count_stats(full_text)
        file_lang = detect_mod.LangDetect(full_text, "lang")
        print(f"File: {text_file}")
        print(f"Size: {size} bytes")
        print(f"Chars: {chars}")
        print(f"Words: {words}")
        print(f"Sentences: {sentences}")
        print(f"Detected language: {file_lang}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    chunk = read_limited(text_file, limit_chars, limit_words, limit_sentences)
    try:
        m = importlib.import_module(f"texttranslation.{module_name}")
    except Exception as e:
        print(f"Error: cannot import module '{module_name}': {e}")
        sys.exit(1)
    translated = m.TransLate(chunk, "auto", dest)
    if output == "screen":
        print(f"Target language: {dest}")
        print(f"Module used: {module_name}")
        print("Translated text:")
        print(translated)
    else:
        base, ext = os.path.splitext(text_file)
        if not ext:
            ext = ".txt"
        out_path = f"{base}_{dest}{ext}"
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(translated)
            print("Ok")
        except Exception as e:
            print(f"Error: {e}")
