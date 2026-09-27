from translator import translate_to_hindi

text = "The current time is 4 PM."

result = translate_to_hindi(text)

print("English:", text)
print("Hindi:", result.encode("utf-8").decode("utf-8"))