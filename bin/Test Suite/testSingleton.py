#!/usr/bin/env python3

from Singleton import *

print(type(TestSingle))
a = TestSingle(thing1=3, thing2=4)
b = TestSingle(thing1=2, thing2=4)
print(a is b)
print(a.thing1, a.thing2)
print(b.thing1, b.thing2)
