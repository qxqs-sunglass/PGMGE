a1 = {1}
a2 = {4}
a3 = {5}


a = [
    [a1, "a1"],
    [a2, "a2"],
    [a3, "a3"]
]

b = {
    "a1": {0, 1, 2},
    "a2": {3, 4, 5},
    "a3": {6, 7, 8}
}

for data, tag in a:
    print(data, tag)
    data = b[tag]
    print(data)
print(a)
print(a1)
print(a2)
print(a3)



