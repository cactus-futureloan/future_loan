class Handler:
    a = 1
    b = 2

key = "a"
print(getattr(Handler,key,""))