#!/usr/bin/env python
import cgi
import cgitb

cgitb.enable()

form = cgi.FieldStorage()
operands = form.getlist("operand")

try:
    total = sum(map(int, operands))
    body = "Your total is: {}".format(total)
except:
    body = "Unable to calculate sum. Please provide integer operands."
print("Content-type: text/plain")
print()
print(body)
