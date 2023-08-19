## calculator.py and calculator_class.py

### usage

`$ python3 calculator.py` or `$ python3 calculator_class.py`

- in each program,
- first, you will enter the interactive mode
- in the interactive mode, you can input a formula using the following expressions
  - `+`: addition
  - `-`: subtraction
  - `*`: multiplication
  - `/`: division
  - `()`: parenthesis
  - `abs()`: absolute
  - `int()`: integer
  - `round()`: round
- if you want to exit the interactive mode, press `Ctrl + C`
- if you want to run test, you can input `test`
- if you want to see the help message, you can input `help`

### calculator.py

- calculator is mainly composed of 3 functions
- `tokenize(str)`: tokenize the input string and return a list of tokens
- `validate(list[dict])`: make sure that the input string can be evaluated and return a (tokens, bool) tuple
- `evaluate(list[dict])`: evaluate the input string recursively and return the result

### calculator_class.py

- class Calculator has 4 variables
  - `line` is the input string
  - `tokenizer`: an instance of class Tokenizer
  - `validator`: an instance of class Validator
  - `evaluator`: an instance of class Evaluator

### Benefits of Class-based Implementation

The class-based implementation of the calculator improves:
- Code Modularity
- Code Reusability
- Code Readability
- Code Extensibility

### to use other functions

you can add other functions in `calculator.py` and `calculator_class.py`

1. add a function in global dictionary `functions`
2. modify `tokenize()` to tokenize the function name
   1. if the len(function_name) != 3 and len(function_name) != 5, you should define a new function like `read_round(index)` and `read_abs_int(index)`
   2. then change `tokenize()` to call the new function
3. modify `evaluate_base_cases()` to evaluate the function
