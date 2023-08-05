

class A:
    def __init__(self):
        self.a = "a"

class B(A):
    def __init__(self):
        super().__init__()
        self.b = "b"

class C:
    def __init__(self):
        self.c = "c"

class D(B, C):
    def __init__(self):
        self.d = "d"
        B.__init__(self)

if __name__ == "__main__":
    d = D()
    for attr_name, attr_value in d.__dict__.items():
        print(attr_name, ": ", attr_value)
