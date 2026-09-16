def read_lines():
    with open("test.txt" , "r" , encoding = "utf-8") as file:
        for line in file:
            yield line.strip()

gen = read_lines()

print(next(gen))
print(next(gen))
print(next(gen))
