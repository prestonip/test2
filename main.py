import lexer
import RDA



f1_name = 'test1.txt'
f1 = open(f1_name)
ftext = f1.read()
result, error = lexer.run(f1_name, ftext)

if error: print(error.to_string())
else:print(result)


