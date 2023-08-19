#! /usr/bin/python3
import subprocess


### global variables ###
plus_minus = {"+":"PLUS", "-":"MINUS"}
mul_div = {"*":"MUL", "/":"DIV"}
ops = {**plus_minus, **mul_div}
parens = {"(":"LPAREN", ")":"RPAREN"}
arithmetic = {**ops, **parens}
functions = {"abs":"ABS", "int":"INT", "round":"ROUND"}


### tokenizer ###
def tokenize(line):
    line = line.replace(' ', '')
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] in arithmetic:
            (token, index) = read_arithmetic(line, index)
        elif line[index:index + 3] in functions:
            (token, index) = read_abs_int(line, index)
        elif line[index:index + 5] in functions:
            (token, index) = read_round(line, index)
        else:
            print("  Invalid character %s found in %d" % (line[index], index+1))
            return (None, False)
        tokens.append(token)
    return (tokens, True)


def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == ".":
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {"type": "NUMBER", "number": number}
    return token, index


def read_arithmetic(line, index):
    symbol = line[index]
    token = {"type": arithmetic[symbol]}
    return token, index + 1


def read_abs_int(line, index):
    symbol = line[index:index + 3]
    token = {"type": functions[symbol]}
    return token, index + 3


def read_round(line, index):
    symbol = line[index:index + 5]
    token = {"type": functions[symbol]}
    return token, index + 5


### validator ###
def validate(tokens):
    if not is_first_token_valid(tokens):
        return (None, False)
    elif not is_paren_balanced(tokens, 0, len(tokens)):
        return (None, False)
    else:
        if len(tokens) >= 2 and not is_adjacent_valid(tokens):
            return (None, False)
        return (tokens, True)


def is_first_token_valid(tokens):
    if len(tokens) == 1 and tokens[0]["type"] != "NUMBER":
        print("  Invalid 1st token: %s" % (tokens[0]["type"]))
        return False
    elif tokens[0]["type"] in ["NUMBER", "MINUS", "LPAREN"] or tokens[0]["type"] in functions.values():
        return True
    print("  Invalid 1st token: %s" % (tokens[0]["type"]))
    return False


def is_adjacent_valid(tokens):
    prev_type = tokens[0]["type"]
    for token in tokens[1:]:
        this_type = token["type"]
        if prev_type == "NUMBER" and (this_type in ops.values() or this_type == "RPAREN"):
            pass
        elif prev_type in ops.values() and (this_type in functions.values() or this_type in ["LPAREN", "NUMBER"]):
            pass
        elif prev_type in functions.values() and this_type == "LPAREN":
            pass
        elif prev_type == "LPAREN" and (this_type in ["NUMBER", "MINUS", "LPAREN"] or this_type in functions.values()):
            pass
        elif prev_type == "RPAREN" and (this_type in ops.values() or this_type == "RPAREN"):
            pass
        else:
            print("  Invalid syntax: %s %s" % (prev_type, this_type))
            return False
        prev_type = this_type
    return True


def is_paren_balanced(tokens, start, end):
    paren_count = 0
    for token in tokens[start:end]:
        if token["type"] == "LPAREN":
            paren_count += 1
        elif token["type"] == "RPAREN":
            paren_count -= 1
        if paren_count < 0:
            print("  Invalid syntax, unbalanced parentheses")
            return False
    if paren_count > 0:
        print("  Invalid syntax, unbalanced parentheses")
        return False
    return True


### evaluator ###
def evaluate(tokens):
    if len(tokens) <= 2:
        do_base_cases_result = evaluate_base_cases(tokens)
        if do_base_cases_result is not None:
            return do_base_cases_result
    else:
        do_parens_result = do_parens(tokens)
        if do_parens_result is not None:
            return do_parens_result
        do_add_and_sub_result = do_add_and_sub(tokens)
        if do_add_and_sub_result is not None:
            return do_add_and_sub_result
        do_mul_and_div_result = do_mul_and_div(tokens)
        if do_mul_and_div_result is not None:
            return do_mul_and_div_result


def evaluate_base_cases(tokens):
    if len(tokens) == 1:
        return tokens[0]["number"]
    elif len(tokens) == 2:
        if tokens[0]["type"] == "MINUS":
            return -tokens[1]["number"]
        elif tokens[0]["type"] == "ABS":
            return abs(tokens[1]["number"])
        elif tokens[0]["type"] == "INT":
            return int(tokens[1]["number"])
        elif tokens[0]["type"] == "ROUND":
            return round(tokens[1]["number"])
    return None


def do_parens(tokens):
    for index in range(len(tokens)):
        if tokens[index]["type"] == "LPAREN":
            start = index
            end = find_matching_paren(tokens, start)
            tokens = tokens[:start] + [{"type": "NUMBER", "number": evaluate(tokens[start + 1:end])}] + tokens[end + 1:]
            return evaluate(tokens)

def do_add_and_sub(tokens):
    for index in reversed(range(len(tokens))):
        if tokens[index]["type"] in ["PLUS", "MINUS"] and index != 0:
            left = evaluate(tokens[:index])
            right = evaluate(tokens[index + 1:])
            if tokens[index]["type"] == "PLUS":
                return left + right
            else:
                return left - right

def do_mul_and_div(tokens):
    for index in reversed(range(len(tokens))):
        if tokens[index]["type"] in ["MUL", "DIV"]:
            left = evaluate(tokens[:index])
            right = evaluate(tokens[index + 1:])
            if tokens[index]["type"] == "MUL":
                return left * right
            else:
                return left / right


def find_matching_paren(tokens, start):
    for index in range(start+1, len(tokens)):
        if tokens[index]["type"] == "RPAREN" and is_paren_balanced(tokens, start, index + 1):
            return index


### caluculator ###
def calculator():
    print("\n=========== Welcome to the calculator! ===========")
    print_help()
    while True:
        try:
            print("> ", end="")
            line = input()
            if line == "help":
                print_help()
                continue
            if line == "test":
                subprocess.run("pipenv run pytest test_calculator.py", shell=True)
                continue
            tokens = tokenize(line)[0]
            if not tokens:
                continue
            valid_tokens = validate(tokens)[0]
            if not valid_tokens:
                continue
            answer = evaluate(valid_tokens)
            print("  answer = %f\n" % answer)
        except ZeroDivisionError:
            print("  Cannot divide by zero")
        except KeyboardInterrupt:
            print("\n\nBye!")
            exit(0)


def print_help():
    print("\nyou can use +, -, *, /, (), abs(), int(), round()\n")
    print("            Press 'Ctrl - c' to exit")
    print("            Type 'test' to run test")
    print("            Type 'help' to see this again\n")
    print("==================================================\n")


def main():
    calculator()


if __name__ == "__main__":
    main()
