#!/usr/bin/env python3

def singleton(cls):
    instances = {}

    def getinstance(thing1=1, thing2=2):
        print("GI: {} {}".format(thing1, thing2))
        if cls not in instances:
            instances[cls] = cls(thing1=thing1, thing2=thing2)
        return instances[cls]
    return getinstance

@singleton
class TestSingle:

    def __init__(self, thing1=1, thing2=2):
        self.count = 0
        print(thing1, thing2)
        self.thing1 = thing1
        self.thing2 = thing2
        print(self.thing1, self.thing2)
    def inc(self):
        self.count += 1

#print(type(TestSingle))
#a = TestSingle(thing1=3, thing2=4)
#b = TestSingle(thing1=2, thing2=4)
#print(a is b)
#print(a.thing1, a.thing2)
#print(b.thing1, b.thing2)
