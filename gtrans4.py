from texttranslation import mod1_gtrans as m1

if __name__ == "__main__":
    print("== Demo модуля 1 (googletrans 4.x) ==")
    print("CodeLang('english') ->", m1.CodeLang("english"))
    print("CodeLang('uk') ->", m1.CodeLang("uk"))
    print("LangDetect('Добрий день, як справи?','all') ->", m1.LangDetect("Добрий день, як справи?", "all"))
    print("TransLate('Привіт з Києва','auto','en') ->", m1.TransLate("Привіт з Києва", "auto", "en"))
    print("LanguageList('screen','Добрий день') ->")
    print(m1.LanguageList("screen", "Добрий день"))
