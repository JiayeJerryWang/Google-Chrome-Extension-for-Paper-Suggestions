import sys, json

# print("Hello, this is the test Py file.")
# print("Sys.argv: ", sys.argv)

# dictionary
j = {
    "papers":
            [
                { "paperTitle":"Paper1", "abstract":"One algorithm1", "link":"https://acm.com/doi/12345" },
                { "paperTitle":"Paper2", "abstract":"One algorithm2", "link":"https://acm.com/doi/12345" },
                { "paperTitle":"Paper3", "abstract":"One algorithm3", "link":"https://acm.com/doi/12345" }
            ]
}

# print out json
print(json.dumps(j))