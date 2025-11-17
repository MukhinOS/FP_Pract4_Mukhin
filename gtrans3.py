from texttranslation import mod2_deeptr as m2

print("== Demo модуля 2 (deep_translator) ==")

# Перевірка CodeLang
print("CodeLang('english') ->", m2.CodeLang("english"))
print("CodeLang('uk') ->", m2.CodeLang("uk"))

print("LangDetect('Hello world','all') -> no langdetect in module 2")

# Демонстрація перекладу
print("TransLate('Добрий день','auto','en') ->",
      m2.TransLate("Добрий день", "auto", "en"))

# Демонстрація таблиці
print("\nLanguageList('screen','Привіт') ->")
m2.LanguageList("screen", "Привіт")
