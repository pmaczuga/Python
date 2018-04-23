import sys

infix_operators = ["<=>", "=>", "||", "&&", "xor"]
precedence = {"<=>": 1, "=>": 2, "||": 3, "&&": 4, "xor": 5}
associativity = {"<=>": "right", "=>": "right", "||": "left", "&&": "left", "xor": "left"}
prefix_operators = ["!"]
constants = ["0", "1"]
    
def is_variable(string):
    """Checks if string has only alfa-numeric charaachters and starts with letter"""
    if len(string) == 0:
        return False
    if not string.isalnum():
        return False
    if string[0].isdigit():
        return False
    if string in infix_operators or string in prefix_operators:
        return False
    return True
    
def finish_word(expr, i):
    """Returns index, where the word or operator ends"""
    if expr[i].isalnum():
        state = True
    elif expr[i] in "()":
        return i+1
    else:
        state = False
    i+=1

    if state:
        while i < len(expr) and expr[i].isalnum():
            i+=1
    else:
        while i < len(expr) and not expr[i].isalnum() and expr[i] not in "()" and expr[i] != " ":
            i+=1

    return i
   
def super_split(expr):
    """Converts string to list"""
    list = []
    i = 0
    while i < len(expr):
        if expr[i] ==  " ":
            i+=1
            continue
        j = finish_word(expr, i)
        list.append(expr[i:j])
        i = j
    return list 

def validate(expr):
    """Validates expression"""
    state = False
    bracket_count = 0
    
    for string in expr:
        if state:
            if string in infix_operators:
                state = False
            elif string == ")":
                bracket_count -= 1
            else:
                return False
        else:
            if is_variable(string) or string in constants:
                state = True
            elif string == "(":
                bracket_count += 1
            elif string == "!":
                pass
            else:
                return False
        if bracket_count < 0:
            return False
    return bracket_count == 0 and state
   
    
def to_rpn(expr):
    """Shunting-yard algorithm"""
    stack = []
    output = []
    
    def while_conditions(string, stack_top):
        if stack_top in prefix_operators:
            return True
        if stack_top in infix_operators:
            if precedence[stack_top] > precedence[string]:
                return True
            if precedence[stack_top] == precedence[string] and associativity[stack_top] == "left":
                return True
            return False
    
    for string in expr:
        if is_variable(string) or string in constants:
            output.append(string)
        elif string in prefix_operators:
            stack.append(string)
        elif string == "(":
            stack.append(string)
        elif string == ")":
            while stack[-1] != "(":
                output.append(stack.pop())
            stack.pop()
        else: # string is infix operator
            while len(stack) > 0 and while_conditions(string, stack[-1]):
                output.append(stack.pop())
            stack.append(string)
            
    while len(stack) > 0:
        output.append(stack.pop())

    return output
                
def get_variables(expr):
    """Returns list of all variables in expression"""
    not_variables = infix_operators + prefix_operators + ["(", ")"] + constants
    return list(sorted(set(expr) - set(not_variables)))
    
                
def eval_expression(expr, var_dict):
    """Evaluate expression"""
    def xor(a,b):
        return bool(a) != bool(b)
        
    def implicaton(a,b):
        if a and not b:
            return False
        return True
        
    def biconditional(a, b):
        return bool(a) == bool(b)
        
    def my_and(a, b):
        return bool(a) and bool(b)
        
    def my_or(a, b):
        return bool(a) or bool(b)
        
    def my_not(a):
        return not bool(a)
        
    function_dict = {
        "xor": xor,
        "=>": implicaton,
        "<=>": biconditional,
        "&&": my_and,
        "||": my_or,
        "!": my_not
        }
    
    stack = []
    for string in expr:
        if is_variable(string):
            stack.append(int(var_dict[string]))
        elif string in constants:
            stack.append(int(string))
        elif string in infix_operators:
            a = stack.pop()
            b = stack.pop()
            res = function_dict[string](b, a)
            stack.append(res)
        else: # prefix_operators (!)
            a = stack.pop()
            res = function_dict[string](a)
            stack.append(res)
    
    return stack.pop()
    
# get number of chars strings differ with
def get_difference_in_strings(string1, string2):
    """Returns number of chars, strings differ with"""
    i = 0
    for a, b in zip(string1, string2):
        if a != b:
            i += 1
            
    return i

def combine_bin_numbers(bin1, bin2):
    """Combines two bin numbers (strings) putting '-' where they differ"""
    output = ""
    for a, b in zip(bin1, bin2):
        if a != b:
            output += "-"
        else:
            output += a
        
    return output
            
    
def to_bin(number, length):
    return "{:0{}b}".format(number, length)
    
def generate_binary(length):
    """Generates list of binary numbers of specified length"""
    output = []
    for i in range(2 ** length):
        output.append(to_bin(i, length))
    return output
    
def print_minterms(minterm_list):
    for number_of_1s in minterm_list:
        print(minterm_list.index(number_of_1s), ": ", number_of_1s)
        
    print()
    
def max_elements_in_minterm(minterm_list):
    """Returns element in list with the most numbers combined"""
    maximum = minterm_list[0]
    for minterm in minterm_list:
        if(len(minterm[0])) > len(maximum[0]):
            maximum = minterm
            
    return maximum
    
def simplify(expr):
    """Quine–McCluskey algorithm"""
    vars = get_variables(expr)
    bin_numbers = generate_binary(len(vars))
    
    output_is_1 = []
    
    for bin_num in bin_numbers:
        if eval_expression(expr, dict(zip(vars, bin_num))) == True:
            output_is_1.append(int(bin_num, 2))
    
    if len(output_is_1) == 2 ** len(vars):
        return "1"
    if len(output_is_1) == 0:
        return "0"
    
    if print_steps:
        print("Output is 1 for: ")
        print(output_is_1)
        print()
    
    prime_implicants = []
    
    last_minterms = [ set() for i in range(len(vars) + 1) ]
    next_minterms = [ set() for i in range(len(vars) + 1) ]
    
    for minterm in output_is_1:
        bin_minterm = to_bin(minterm, len(vars))
        last_minterms[bin_minterm.count("1")].update([((minterm, ), bin_minterm)])
        
        
    cant_combine_more = False
    
    while not cant_combine_more:
        
        if print_steps:
            print_minterms(last_minterms)
        
        cant_combine_more = True
        next_minterms = [ set() for i in range(len(vars) + 1) ]
        for i in range(len(last_minterms) - 1):
            for minterm_1, bin_minterm_1 in last_minterms[i]:
                cant_combine_minterm_1 = True
                for minterm_2, bin_minterm_2 in last_minterms[i + 1]:
                    if get_difference_in_strings(bin_minterm_1, bin_minterm_2) == 1:
                        cant_combine_minterm_1 = False
                        cant_combine_more = False
                        combined_bin = combine_bin_numbers(bin_minterm_1, bin_minterm_2)
                        combined_num = tuple(sorted(minterm_1 + minterm_2))
                        next_minterms[i].update([(combined_num, combined_bin)])
                if cant_combine_minterm_1:
                    prime_implicants.append((minterm_1, bin_minterm_1))
                        
        
        last_minterms = next_minterms
           
    if print_steps:
        print("Prime implicants: ")
        print(prime_implicants)
        print()
    
    chosen_prime_implicants = []
    covered_ouptut = set()
    
    # choose essential prime implicants
    for case in output_is_1:
        how_many_minterms = 0
        for minterm, bin_minterm in prime_implicants:
            if case in minterm:
                how_many_minterms += 1
                chosen_minterm = (minterm, bin_minterm)
        if how_many_minterms == 1:
            covered_ouptut.update(chosen_minterm[0])
            chosen_prime_implicants.append(chosen_minterm)
            
    # choose remaining
    for case in output_is_1:
        if case not in covered_ouptut:
            chosen_minterms = []
            for minterm, bin_minterm in prime_implicants:
                if (minterm, bin_minterm) not in chosen_prime_implicants:
                    if case in minterm:
                        chosen_minterms.append((minterm, bin_minterm))
            if chosen_minterms:
                biggest_minterm = max_elements_in_minterm(chosen_minterms)
                covered_ouptut.update(biggest_minterm[0])
                chosen_prime_implicants.append(biggest_minterm)  
      
    if print_steps:
        print("Chosen prime implicants")
        print(chosen_prime_implicants)
        print()
    
    simplified_expression = []
    for minterm, bin_minterm in chosen_prime_implicants:
        one_component = []
        for var, val in zip(vars, bin_minterm):
            if val == "0":
                one_component.append("!" + var)
            elif val == "1": 
                one_component.append(var)
        simplified_expression.append(" && ".join(one_component))
    
    return " || ".join(simplified_expression)
    
    
def main():
    if len(sys.argv) < 2:
        print("Not enough arguments")
        return
        
    global print_steps
    if len(sys.argv) == 3 and sys.argv[2] == "-p":
        print_steps = True
    else:
        print_steps = False
    
    expr = super_split(sys.argv[1])
    if print_steps:
        print("Splitted expression: ")
        print(expr)
        print()
    
    if not validate(expr):
        return

    expr = to_rpn(expr)
    if print_steps:
        print("Expression in RPN: ")
        print(expr)
        print()
    
    vars = get_variables(expr)
    if print_steps:
        print("Variables: ")
        print(vars)
        print()
    
    result = simplify(expr)
    if print_steps:
        print("RESULT:")
    print(result)

if __name__ == "__main__":
    main()
    
