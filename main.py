import lexer
import RDA



f1_name = 'test1.txt'
f2_name = 'test2.txt'
f1 = open(f1_name)
f2 = open(f2_name)
ftext = f2.read()

result, error = lexer.run(f2_name, ftext)

if error: print(error.to_string())
else:
    print(result)

 


