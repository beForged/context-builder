def a():
    return ("o", "t")
def b(a, b):
    print(a)

c = a()
b(c[0], c[1])
