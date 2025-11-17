from texttranslation import mod3_filetr as m3

if __name__ == "__main__":
    print("== Demo модуля 3 (deep_translator + langdetect) ==")
    print("CodeLang('english') ->", m3.CodeLang("english"))
    print("CodeLang('uk') ->", m3.CodeLang("uk"))
    print('LangDetect("Je t\'aime","all") ->', m3.LangDetect("Je t'aime", "all"))
    print("TransLate('Доброго вечора, ми з України','auto','en') ->", m3.TransLate("Доброго вечора, ми з України", "auto", "en"))
    print("LanguageList('screen','Добрий день') ->")
    print(m3.LanguageList("screen", "Добрий день"))
