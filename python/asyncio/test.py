class C:
    @classmethod
    def f(cls,s):
        print(s*2)
        return s*2
    @classmethod
    def g(cls,s):
        getattr(cls,"f")(s)
    
C.g("2")
    