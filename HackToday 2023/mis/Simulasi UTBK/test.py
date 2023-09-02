from deep_translator import GoogleTranslator

to_translate = "I want to translate this text"
translated = GoogleTranslator(source="en", target="id").translate(to_translate)

print(translated)
