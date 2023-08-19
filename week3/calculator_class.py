#! /usr/bin/python3
import subprocess

### global variables ###
plus_minus = {"+":"PLUS", "-":"MINUS"}
mul_div = {"*":"MUL", "/":"DIV"}
ops = {**plus_minus, **mul_div}
parens = {"(":"LPAREN", ")":"RPAREN"}
arithmetic = {**ops, **parens}
functions = {"abs":"ABS", "int":"INT", "round":"ROUND"}

class Tokenizer:
    def __init__(self, line):
        self.line = line
        self.tokens = []

    def tokenize(self):
        self.line = self.line.replace(' ', '')
        self.tokens = []
        index = 0
        while index < len(self.line):
            if self.line[index].isdigit():
                (token, index) = self.read_number(index)
            elif self.line[index] in arithmetic:
                (token, index) = self.read_arithmetic(index)
            elif self.line[index:index + 3] in functions:
                (token, index) = self.read_abs_int(index)
            elif self.line[index:index + 5] in functions:
                (token, index) = self.read_round(index)
            else:
                print("  Invalid character %s found in %d" % (self.line[index], index+1))
                return None
            self.tokens.append(token)
        return self.tokens

    def read_number(self, index):
        number = 0
        while index < len(self.line) and self.line[index].isdigit():
            number = number * 10 + int(self.line[index])
            index += 1
        if index < len(self.line) and self.line[index] == ".":
            index += 1
            decimal = 0.1
            while index < len(self.line) and self.line[index].isdigit():
                number += int(self.line[index]) * decimal
                decimal /= 10
                index += 1
        token = {"type": "NUMBER", "number": number}
        return token, index

    def read_arithmetic(self, index):
        symbol = self.line[index]
        token = {"type": arithmetic[symbol]}
        return token, index + 1

    def read_abs_int(self, index):
        symbol = self.line[index:index + 3]
        token = {"type": functions[symbol]}
        return token, index + 3

    def read_round(self, index):
        symbol = self.line[index:index + 5]
        token = {"type": functions[symbol]}
        return token, index + 5

class Validator:
    def __init__(self, tokens):
        self.tokens = tokens

    def validate(self):
        if not self.is_first_token_valid():
            return None
        elif not self.is_paren_balanced():
            return None
        else:
            if len(self.tokens) >= 2 and not self.is_adjacent_valid():
                return None
            return self.tokens

    def is_first_token_valid(self):
        if len(self.tokens) == 1 and self.tokens[0]["type"] != "NUMBER":
            print("  Invalid 1st token: %s" % (self.tokens[0]["type"]))
            return False
        elif self.tokens[0]["type"] in ["NUMBER", "MINUS", "LPAREN"] or self.tokens[0]["type"] in functions.values():
            return True
        print("  Invalid 1st token: %s" % (self.tokens[0]["type"]))
        return False

    def is_adjacent_valid(self):
        prev_type = self.tokens[0]["type"]
        for token in self.tokens[1:]:
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

    def is_paren_balanced(self):
        paren_count = 0
        for token in self.tokens:
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

class Evaluator:
    def __init__(self, tokens):
        self.tokens = tokens

    def evaluate(self):
        if len(self.tokens) <= 2:
            do_base_cases_result = self.evaluate_base_cases()
            if do_base_cases_result is not None:
                return do_base_cases_result
        else:
            do_parens_result = self.do_parens()
            if do_parens_result is not None:
                return do_parens_result
            do_add_and_sub_result = self.do_add_and_sub()
            if do_add_and_sub_result is not None:
                return do_add_and_sub_result
            do_mul_and_div_result = self.do_mul_and_div()
            if do_mul_and_div_result is not None:
                return do_mul_and_div_result

    def evaluate_base_cases(self):
        if len(self.tokens) == 1:
            return self.tokens[0]["number"]
        elif len(self.tokens) == 2:
            if self.tokens[0]["type"] == "MINUS":
                return -self.tokens[1]["number"]
            elif self.tokens[0]["type"] == "ABS":
                return abs(self.tokens[1]["number"])
            elif self.tokens[0]["type"] == "INT":
                return int(self.tokens[1]["number"])
            elif self.tokens[0]["type"] == "ROUND":
                return round(self.tokens[1]["number"])
        return None

    def do_parens(self):
        for index in range(len(self.tokens)):
            if self.tokens[index]["type"] == "LPAREN":
                start = index
                end = self.find_matching_paren(start)
                new_tokens = self.tokens[:start] + [{"type": "NUMBER", "number": Evaluator(self.tokens[start + 1:end]).evaluate()}] + self.tokens[end + 1:]
                return Evaluator(new_tokens).evaluate()

    def do_add_and_sub(self):
        for index in reversed(range(len(self.tokens))):
            if self.tokens[index]["type"] in ["PLUS", "MINUS"] and index != 0:
                left = Evaluator(self.tokens[:index]).evaluate()
                right = Evaluator(self.tokens[index + 1:]).evaluate()
                if self.tokens[index]["type"] == "PLUS":
                    return left + right
                else:
                    return left - right

    def do_mul_and_div(self):
        for index in reversed(range(len(self.tokens))):
            if self.tokens[index]["type"] in ["MUL", "DIV"]:
                left = Evaluator(self.tokens[:index]).evaluate()
                right = Evaluator(self.tokens[index + 1:]).evaluate()
                if self.tokens[index]["type"] == "MUL":
                    return left * right
                else:
                    return left / right

    def find_matching_paren(self, start):
        paren_count = 0
        for index in range(start, len(self.tokens)):
            if self.tokens[index]["type"] == "LPAREN":
                paren_count += 1
            elif self.tokens[index]["type"] == "RPAREN":
                paren_count -= 1
            if paren_count == 0:
                return index


class Calculator:
    def __init__(self, line):
        self.line = line
        self.Tokenizer = Tokenizer
        self.Validator = Validator
        self.Evaluator = Evaluator

    def calculate(self):
        try:
            tokens = self.Tokenizer(self.line).tokenize()
            if not tokens:
                return None
            valid_tokens = self.Validator(tokens).validate()
            if not valid_tokens:
                return None
            answer = self.Evaluator(valid_tokens).evaluate()
            return answer
        except ZeroDivisionError:
            print("  Cannot divide by zero")


def print_help():
    print("\nyou can use +, -, *, /, (), abs(), int(), round()\n")
    print("            Press 'Ctrl - c' to exit")
    print("            Type 'test' to run test")
    print("            Type 'help' to see this again\n")
    print("==================================================\n")

def main():
        print("\n=========== Welcome to the calculator! ===========")
        print_help()
        try:
            while True:
                print("> ", end="")
                line = input()
                if line == "help":
                    print_help()
                    continue
                if line == "test":
                    subprocess.run("pipenv run pytest test_calculator_class.py", shell=True)
                    continue
                answer = Calculator(line).calculate()
                if answer is not None:
                    print("  %s" % answer)
                else:
                    continue
        except KeyboardInterrupt:
            print("\n\nBye!")
            exit(0)

if __name__ == "__main__":
    main()
