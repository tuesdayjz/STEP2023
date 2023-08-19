import sys


def store_input_to_list(input_file: str) -> list[str]:
    inputs: list = []
    with open(input_file, 'r') as file:
        for line in file:
            inputs.append(line.strip('\n'))
    return inputs


def write_output_to_file(solutions: list[str], output_file: str) -> None:
    with open(output_file, 'w') as file:
        for solution in solutions:
            file.write(solution + '\n')
    return None


def check_broccolies(input: str) -> bool:
    for char in input:
        if char != 'g' and char != 'w':
            return False
    return True


def solve(input: str) -> str:
    min_replace = len(input)
    for slice in range(len(input) + 1):
        replace = 0
        for char in input[slice:]:
            if char == 'g':
                replace += 1
        for char in input[:slice]:
            if char == 'w':
                replace += 1
        if replace < min_replace:
            min_replace = replace
    return str(min_replace)


def main(input_file: str, output_file: str) -> None:
    inputs: list[str] = store_input_to_list(input_file)
    solutions: list[str] = []
    for input in inputs:
        input = input.lower()
        if check_broccolies(input):
            solutions.append(str(solve(input)))
        else:
            solutions.append('non-broccoli-sequence')
    write_output_to_file(solutions, output_file)
    return None


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("usage: %s input_broccoli_file output_file" % sys.argv[0])
        exit(1)
    else:
        main(sys.argv[1], sys.argv[2])
        print("result is succesfully written to [%s]" % sys.argv[2])
        exit(0)
