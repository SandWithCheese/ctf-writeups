#!/usr/local/bin/python3 -S

restricted_globals = {
    "__builtins__": None,
    "flag": "CJ{REDACTED}",
}

expression = input()

if len(expression) <= 50 and "flag" not in expression:
    try:
        eval(expression, restricted_globals)
    except Exception as e:
        print("Invalid")