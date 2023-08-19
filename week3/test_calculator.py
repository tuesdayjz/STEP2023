import pytest

from calculator import tokenize, validate, evaluate

# tokenize just returns a list of tokens
@pytest.mark.parametrize("input_ok", [
  "1", "9.2", "+", "-", "*", "/", "(", ")", "abs", "int", "round", "1 +2*abs (rou nd(6.2 *(9.2 3 4-4  /3/2+ 5-4* 2) ))/in t(3 .5)", "absint", "roundabs", "roundabsint****/////((()))))))", "roundabs+int-*1)/(123"])
def test_tokenize_ok(input_ok):
  assert tokenize(input_ok)[1] == True

@pytest.mark.parametrize("input_ng", [
  "hello", "abs_int", ".9", "0x100001523638"])
def test_tokenize_ng(input_ng):
  assert tokenize(input_ng)[1] == False

# validate ensures that the tokens are valid
@pytest.mark.parametrize("input_ok", [
  "1", "9.2", "-0.2+3.5", "1+2*abs(3.5)-2", "int(abs(-0.054))*2.25/4", "round(1.5)"])
def test_validate_ok(input_ok):
  tokens = tokenize(input_ok)[0]
  assert validate(tokens)[1] == True

@pytest.mark.parametrize("input_ng", [
  "-", "+", "*", "/", "(", ")", "abs -1", "int2.9999", "round9.9999", "absint", "roundabs", "roundabsint****/////((()))))))", "roundabs+int-*1)/(123"
])
def test_validate_ng(input_ng):
  tokens = tokenize(input_ng)[0]
  assert validate(tokens)[1] == False

@pytest.mark.parametrize(("input"), [
  # integer
  "1",
  # float negative
  "9.2", "-54322365.16287642",
  # addition subtraction
  "1+2", "0.00876+2356.35", "-16451216.12345671+24341256.98765432", "1-2","1-2.3", "-16451216.12345671-24341256.98765432", "1+2.3-4-5.6+7+8.9-10.11-12.13-14.15-123456+7654+3.3335432+8.23-5.234-1+2.3-4-5.6+7+8.9-12345.011-12.13-14.15-123456+7654+3.33332+8.23-5.234+14.15-123456+7654+3.3335432+8.23-5.234-1+2.3-4-5.6",
  # multiplication division
  "1*2", "-1*2.3", "-1616.1231*2456.9432", "1/2", "-1/2.3", "16112346.1239*8761/24765656.94323432","2/3/5*4*3/2-1-3/4/5*6*7/8/9/2.876*8765*165.4567",
  # mix of addition subtraction multiplication division
  "-34.561+54.2*0.0003-4/5*6+7-8/9*10.765+11.8765-12.98765/13.1234/14.125+15.123456-34.561+54.2*0.003-4/5*6+7-8/9*10.765+11.65-12.98765/13.1234/14.345+15.123456/34.561+54.2*0.003-4/5*6",
  # parentheses
  "((((((((((((((((((((((((((((((((((((-1))))))))))))))))))))))))))))))))))))", "((1+(2+(-(4+(-(-1))*3)+(-(-(0.08765+((((0.2345))/2.345)*6-2))/(2.083+((-(0.03*(((((2.179)))))*(99.2456+2+2*4/2))))))*(-34.561+54.2*0.0003-4/5*6+7-8/9*10.765+11.8765-12.98765/13.1234/14.12345+15.123456))))))",
  # functions
  "abs(-56.7654)", "int(56.7654)", "round(56.7654)",
  "abs((1+(2+(-(4+(-(-1)))+(-(-(0.08765+((((0.2345)))))/(2.083+((-(0.03*(((((2.179)))))*(99.2456+2+2*4/2))))))*(-34.561+54.2*0.0003-4/5*6+7-8/9*10.765+11.8765-12.98765/13.1234/14.12345+15.123456))))))",
  "round((1+(2+(-(4+(-(-1)))+(-(-(0.08765+((((0.2345)))))/(2.083+((-(0.03*(((((2.179)))))*(99.2456+2+2*4/2))))))*(-34.561+54.2*0.0003-4/5*6+7-8/9*10.765+11.8765-12.98765/13.1234/14.12345+15.123456))))))",
  "int((1+(2+(-(4+(-(-1)))+(-(-(0.08765+((((0.2345)))))/(2.083+((-(0.03*(((((2.179)))))*(99.2456+2+2*4/2))))))*(-34.561+54.2*0.0003-4/5*6+7-8/9*10.765+11.8765-12.98765/13.1234/14.12345+15.123456))))))",
  # mix of all
  "12.43+abs(-56.7654)+23/456.3431*round(0.2345)+int(56.7654)+round(int(56.7654))+abs(round(576.5454))*int(abs(round(236.7654)))+round(int(abs(round(31.7654))))/abs(round(int(abs(round(31.7654)))))+int(abs(round(int(abs(round(31.7654))))))+round(int(abs(round(int(abs(round(31.765*0.123)))*0.003))*0.002))+abs(round(int(abs(round(int(abs(round(31.7654))))+2.3))*2934)/6.3)/135.3"
  ])
def test_evaluate_ok(input):
  tokens = tokenize(input)[0]
  assert evaluate(tokens) - eval(input) < 1e-8
