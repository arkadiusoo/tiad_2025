from deep_translator import GoogleTranslator

def translate_words(words, src='auto', dest='en'):
    translated = []
    for word in words:
        try:
            t = GoogleTranslator(source=src, target=dest).translate(word)
            translated.append(t.lower())
        except Exception as e:
            print(f"Nie udało się przetłumaczyć '{word}': {e}")
            translated.append(word)
    return translated