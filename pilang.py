import sys

class MissingVariableError(Exception):
    pass

class BraceExpressionMissesVariable(Exception):
    pass

class WrongTokenType(Exception):
    pass

class WrongNumberOfParenthesses(Exception):
    pass

class WrongArrayExpressionError(Exception):
    pass

class MissingArrayError(Exception):
    pass

class WrongBinaryOperatorError(Exception):
    pass

class WrongVariableNameError(Exception):
    pass

class NotEnoughArguments(Exception):
    pass

class InvalidFunction(Exception):
    def __init__(self, name):
        print("The function", name, "does not exist")

class ListIsEmpty(Exception):
    def __init__(self, name):
        print("The list", name, "is empty");


class Token:
    def __init__(self, typ, val, sons):
        self.typ = typ
        self.value = val
        self.sons = sons
    
    def evaluate(self, variables, inp, erase = False):
        if self.typ == "VAR":
            if self.value[0] == "'":
                if self.value[-1] != "'":
                    raise WrongVariableNameError()
                if erase:
                    try:
                        res = variables[self.value][0]
                        variables[self.value].remove(variables[self.value][0]);
                    except:
                        raise ListIsEmpty(self.value);
                    return res
                if type(variables[self.value]) == list:
                    return variables[self.value].copy()
                return variables[self.value]
            else:
                if erase:
                    res = global_var[self.value][0]
                    global_var[self.value].remove(global_var[self.value][0]);
                    return res
                if type(global_var[self.value]) == list:
                    return global_var[self.value].copy()
                return global_var[self.value]
        elif self.typ == "NUM":
            return int(self.value)
        elif self.typ == "ARR":
            arr = []
            for son in self.sons:
                arr.append(son.evaluate(variables, inp))
            return arr.copy()
        elif self.typ == "INP":
            if self.value == '&':
                s = input()
                if s.isnumeric():
                    return int(s)
                array = [ord(c) for c in s]
                array = [len(array)] + array;
                return array
            elif self.value == '#':
                try:
                    res = inp[0]
                    inp.remove(inp[0])
                    return res
                except:
                    raise NotEnoughArguments()
            elif self.value == '<':
                s = input()
                array = [ord(c) for c in s]
                array = [len(array)] + array
                return array
        elif self.typ == "UNO":
            if self.value == "#":
                res = self.sons[0].evaluate(variables, inp, True)
                return res
            exp = self.value + str(self.sons[0].evaluate(variables, inp))
            return eval(exp)
        elif self.typ == "BIN":
            exp = str(self.sons[0].evaluate(variables, inp)) + self.value + str(self.sons[1].evaluate(variables, inp))
            if self.value == "/":
                exp = str(self.sons[0].evaluate(variables, inp)) + "//" + str(self.sons[1].evaluate(variables, inp))
            return eval(exp)
        elif self.typ == "FUN":
            try:
                return func[self.value].compute({}, self.sons[0].evaluate(variables, inp))
            except:
                raise InvalidFunction(self.value)
        raise WrongTokenType()
    
    def print_token(self, k): # debug function
        if self.typ == "VAR" or self.typ == "NUM":
            print(k * " ", self.value)
        if self.typ == "ARR":
            print(k * " ", "[")
            for s in self.sons:
                s.print_token(k + 1)
            print(k * " ", "]")
        if self.typ == "INP":
            print(k * " ", self.value)
        if self.typ == "UNO":
            print(k * " ", self.value)
            self.sons[0].print_token(k + 1);
        if self.typ == "BIN":
            print(k * " ", self.value)
            self.sons[0].print_token(k + 1);
            self.sons[1].print_token(k + 1);
        if self.typ == "FUN":
            print(k * " ", self.value, "[")
            self.sons[0].print_token(k + 1);
            print(k * " ", "]")

def into_tree(tokens):
    if tokens[0] == '[':
        array = []
        cntin, last = 0, 0
        for i, token in enumerate(tokens[1:-1]):
            if token == ',' and cntin == 0:
                if i == 0 or i == len(tokens) - 2:
                    raise WrongArrayExpressionError()
                array.append(into_tree(tokens[last + 1:i + 1]))
                last = i + 1
            elif token == '[':
                cntin += 1
            elif token == ']':
                cntin -= 1
        if last != len(tokens) - 2:
            array.append(into_tree(tokens[last + 1:-1]))
        return Token("ARR", "", array)
    
    without_parenthesses = []
    cntin, last = 0, -1
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == '(':
            cntin += 1
            if cntin == 1:
                last = i
        elif token == ')':
            cntin -= 1
            if cntin == 0:
                without_parenthesses.append(into_tree(tokens[last + 1:i]))
        elif cntin == 0:
            if not token in "&#-*+/[(]),?<":
                if token.isnumeric():
                    without_parenthesses.append(Token("NUM", token, []))
                else:
                    if i == len(tokens) - 1 or tokens[i + 1] != "[":
                        without_parenthesses.append(Token("VAR", token, []))
                    else:
                        till = i + 2
                        count = 1
                        while count > 0:
                            if tokens[till] == ']':
                                count -= 1
                            elif tokens[till] == '[':
                                count += 1
                            till += 1
                        without_parenthesses.append(Token("FUN", token, [into_tree(tokens[i + 1:till])]))
                        i = till - 1
            elif token == '&':
                without_parenthesses.append(Token("INP", token, []))
            elif token == '<':
                without_parenthesses.append(Token("INP", token, []))
            else:
                without_parenthesses.append(token)
        i += 1
    
    without_unary = []
    last = None
    
    for i, token in enumerate(without_parenthesses):
        if type(token) == str and last == "#":
            without_unary.append(Token("INP", last, []))
            last = None
        if type(token) == str and token == '#':
            last = token
            if i == len(without_parenthesses) - 1:
                without_unary.append(Token("INP", token, []))
        elif type(token) == str and token == "-" and i == 0:
            if i == len(without_parenthesses) - 1:
                raise WrongBinaryOperatorError()
            last = token
        elif last != None:
            without_unary.append(Token("UNO", last, [token]))
            last = None
        else:
            without_unary.append(token)
    
    
    without_priority = []
    last = ""
    
    for i, token in enumerate(without_unary):
        if type(token) == str:
            last = token
            if i == len(without_unary) - 1:
                raise WrongBinaryOperatorError()
        else:
            if last == "*" or last == "/":
                without_priority[-1] = Token("BIN", last, [without_priority[-1], token])
            else:
                if last != "":
                    without_priority.append(last)
                without_priority.append(token)
    
    last = ""
    tree = None
    
    for i, token in enumerate(without_priority):
        if type(token) == str:
            last = token
            if i == len(without_priority):
                raise WrongBinaryOperatorError()
        else:
            if last == "":
                tree = token
            else:
                tree = Token("BIN", last, [tree, token])
    return tree


class Expression:
    def __init__(self, expression):
        tokens = []
        cur = ""
        for c in expression:
            if c in "&#-*+/[(]),?":
                if cur != "":
                    tokens.append(cur)
                    cur = ""
                tokens.append(c)
            else:
                cur += c
        if(cur != ""):
            tokens.append(cur)
        self.expression = into_tree(tokens)
    
    def compute(self, variables, inp):
        return self.expression.evaluate(variables, inp)

class BraceExpression:
    def __init__(self, target, expressions):
        self.expressions = expressions
        self.var_target = target
    def compute(self, variables, inp):
        my_vars = dict(variables.copy())
        for expression in self.expressions:
            name = expression[0]
            result = expression[1].compute(my_vars, inp)
            if name == "!":
                print(result)
            if name == '%':
                if type(result) == int:
                       print(result)
                else:
                    output = "".join([chr(c) for c in result[1:]])
                    print(output)
            if name[0] == "'":
                if name[-1] != "'":
                    raise WrongVariableNameError()
                my_vars[name] = result
            else:
                global_var[name] = result
        for var, val in my_vars.items():
            if var in variables:
                variables[var] = val
        return my_vars["'" + self.var_target + "'"]

class IfExpression:
    def __init__(self, expressions, brexes):
        self.braceExpression = brexes
        self.expressions = expressions
    
    def compute(self, variables, inp):
        for i, ex in enumerate(self.expressions):
            if ex.compute(variables, inp) > 0:
                return self.braceExpression[i].compute(variables, inp)
        return self.braceExpression[-1].compute(variables, inp)

class ForExpression:
    def __init__(self, expression, brex):
        self.braceExpression = brex
        self.expression = expression
    
    def compute(self, variables, inp):
        result = []
        while self.expression.compute(variables, inp) > 0:
            result.append(self.braceExpression.compute(variables, inp))
        return result

class Function:
    def __init__(self, brex):
        self.braceExpression = brex
    def compute(self, inp, variables):
        return self.braceExpression.compute(inp, variables)

# interpreting


program = sys.argv[1]
lines = []

with open(program) as F:
    for line in F:
        lines.append(line)

#special_chars = ["+", "-", "/", "*"]
global_var = {"!" : "", "%" : ""}
func = {}
# editing input
edited = []
for line in lines:
    new = ""
    for c in line:
        if c == '"':
            break
        if c != " " and c != "\t" and c != '\n':
            new += c
    if new != "":
        edited.append(new)

# dividing into expressions
stack = []
match = [-1 for l in edited]
var = ["" for l in edited]
expr = ["" for l in edited]
funcs = [False for l in edited]

for i, line in enumerate(edited):
    if line[0] == ")":
        match[stack[-1]] = i
        stack.remove(stack[-1])
        if len(line) > 1:
            if line[1:2] == ';':
                stack.append(i)
            elif line[1] == '?':
                stack.append(i)
                expr[i] = line[2:-1 - line[::-1].find('(')]
    else:
        poz = line.find(':')
        variable = line[:poz]
        var[i] = variable
        if line[poz + 1] == '?':
            stack.append(i)
            expr[i] = line[poz + 2:-1 - line[::-1].find('@') - 1]
        elif line[poz + 1:poz + 3] == "[]" and line.find('@') != -1:
            stack.append(i)
            funcs[i] = True
        elif line[poz + 1] == '[' and line.find('@') != -1:
            stack.append(i)
            expr[i] = line[poz + 2:-1 - line[::-1].find('@') - 1]
        else:
            expr[i] = line[poz + 1:]

def parse(s, e, target):
    this_scope = []
    while s != e:
        if match[s] == -1:
            this_scope.append((var[s], Expression(expr[s])))
            s += 1
        else:
            if match[match[s]] != -1:
                variable = var[s]
                exs, brexs = [], []
                while match[match[s]] != -1:
                    exs.append(Expression(expr[s][:]))
                    tar = edited[s][edited[s].find('@') + 1:]
                    brexs.append(parse(s + 1, match[s], tar))
                    s = match[s]
                tar = edited[s][edited[s].find('@') + 1:]
                brexs.append(parse(s + 1, match[s], tar))
                s = match[s] + 1
                this_scope.append((variable, IfExpression(exs, brexs)))
            elif funcs[s]:
                tar = edited[s][edited[s].find('@') + 1:]
                func[var[s]] = Function(parse(s + 1, match[s], tar))
                s = match[s] + 1
            else:
                tar = edited[s][edited[s].find('@') + 1:]
                this_scope.append((var[s], ForExpression(Expression(expr[s][:]), parse(s + 1, match[s], tar))))
                s = match[s] + 1
    return BraceExpression(target, this_scope)


code = parse(0, len(edited), "!")

varis = {"'!'" : ""}

code.compute(varis, [])
