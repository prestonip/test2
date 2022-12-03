import lexer

f = open("test1.txt")
text = f.read()
result = lexer.run(text)
print(result)
