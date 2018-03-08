import argparse

class TapeInterpreter:
    ''' Inspired by Williams College's Breph language, this is an 
    interpreter for a simple programming language with only a simple tape of one byte values, a data pointer 
    that can move left and right, an instruction pointer to move through input code, and 8 operations:
    + : increase the the data value on the array
    - : decrement the data value on the array
    ( : begin a loop if the data pointer is nonzero
    ) : end of a loop
    l : move data pointer the left one position, if at the end of the data array stay put
    r : move the data pointer to the right one position, if at the end of the data stay put
    I : take one character of input
    p : print the character corresponding to the ascii value at the data pointer
    '''
    def __init__(self, code, inputs, array_size=1024, max_iterations=1024, verbose=False):
        self.verbose = verbose
        self._max_iterations = max_iterations
        self._instruction_pointer = 0
        self._data_pointer = 0
        self._iteration = 0
        self._data = [0]*array_size
        self.input = inputs
        self.output = ""
        self.code = code
        if len(self.code) == 0:
            raise Exception("Code is empty")
        if not self._check_parentheses():
            raise Exception("Code has unmatching parentheses")
        self._paren_matching = self._find_parentheses()
        if self.verbose:
            print("Passed parentheses matching:")
            print(self._paren_matching)

    def interpret(self):
        ''' runs the code up to the maximum iterations 
        returns true if program terminated'''
        if self.verbose:
            print("Beginning run with maximum iterations as {}".format(self._max_iterations))
        while self._iteration < self._max_iterations:
            self._iteration += 1
            if self._step():
                if self.verbose:
                    print("Finished successfully")
                return True
        if self.verbose:
            print("Did not finish in iterations")
        return False # did not finish in iterations

    def _step(self):
        ''' Execute the next command of the program 
        returns true if the program is finished running naturally'''
        mapping = {'+':self._oper_plus,
                   '-':self._oper_minus,
                   'l':self._oper_left,
                   'r':self._oper_right,
                   'i':self._oper_input,
                   'p':self._oper_print,
                   "(":self._oper_lparen,
                   ")":self._oper_rparen
                   }

        current_instruction = self.code[self._instruction_pointer]
        if self.verbose:
            print("iter={}, Performing {}".format(self._iteration, current_instruction))
        if current_instruction in mapping:
            mapping[current_instruction]() # execute command
        else:
            self._oper_ignore()
        return self._instruction_pointer >= len(self.code)                   
        
    def _oper_ignore(self):
        ''' ignore whatever character is under the instruction pointer '''
        self._instruction_pointer += 1

    def _oper_lparen(self):
        ''' operation definition for ('''
        if self._data[self._data_pointer] == 0:
            self._instruction_pointer = self._paren_matching[self._instruction_pointer] + 1
        else:
            self._instruction_pointer += 1

    def _oper_rparen(self):
        ''' operation definition for ) '''
        if self._data[self._data_pointer] != 0:
            self._instruction_pointer = self._paren_matching[self._instruction_pointer] + 1
        else:
            self._instruction_pointer += 1

    def _oper_plus(self):
        ''' operation definition for + '''
        self._data[self._data_pointer] += 1
        self._instruction_pointer += 1

    def _oper_minus(self):
        ''' operation definition for -'''
        self._data[self._data_pointer] -= 1
        self._instruction_pointer += 1

    def _oper_left(self):
        ''' operation definition for l'''
        self._data_pointer -= 1
        if self._data_pointer < 0:
            self._data_pointer = 0
        self._instruction_pointer += 1

    def _oper_right(self):
        ''' operation definition for r'''
        self._data_pointer += 1
        if self._data_pointer >= len(self._data):
            self._data_pointer = len(self._data) - 1
        self._instruction_pointer += 1

    def _oper_print(self):
        ''' operation definition for p,
        if number is outside ascii definition adds null to output'''
        try:
            c = chr(self._data[self._data_pointer])
        except:
            c = '\0'
        self.output += c
        self._instruction_pointer += 1

    def _oper_input(self):
        ''' operation definition for I,
        if no input remains places a null character '''
        if len(self.input) > 0:
            self._data[self._data_pointer] = self.input.pop(0)
        else:
            self._data[self._data_pointer] = '\0'
        self._instruction_pointer += 1
        
    def _check_parentheses(self):
        """ Return True if the parentheses in code match, otherwise False. 
        Modified from https://scipython.com/blog/parenthesis-matching-in-python/
        """
        j = 0
        for c in self.code:
            if c == ')':
                j -= 1
                if j < 0:
                    return False
            elif c == '(':
                j += 1
        return j == 0
                
    def _find_parentheses(self):
        """ Find and return the location of the matching parentheses pairs in code.
        Given code as a string return a dictionary of start: end pairs giving the
        indexes of the matching parentheses. Suitable exceptions are
        raised if code contains unbalanced parentheses.
        Modified from https://scipython.com/blog/parenthesis-matching-in-python/
        """
        
        # The indexes of the open parentheses are stored in a stack, implemented
        # as a list
        
        stack = []
        parentheses_locs = {}
        for i, c in enumerate(self.code):
            if c == '(':
                stack.append(i)
            elif c == ')':
                try:
                    parentheses_locs[stack.pop()] = i
                except IndexError:
                    raise IndexError('Too many close parentheses at index {}'.format(i))
        if stack:
            raise IndexError('No matching close parenthesis to open parenthesis at index {}'.format(stack.pop()))

        full_parentheses_locs = dict()
        for i,j in parentheses_locs.items():
                full_parentheses_locs[i] = j
                full_parentheses_locs[j] = i
        return full_parentheses_locs
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("program", help="path for program")
    parser.add_argument("--verbose","-v", action='store_true', help="provides helpful feedback")
    args = vars(parser.parse_args())

    with open(args['program']) as f:
        lines = f.readlines()
    inputs = [ord(c) for c in list(lines[0][:-1]) + ['\0']]
    code = "".join(lines[1:])
    interpreter = TapeInterpreter(code, inputs, verbose=args['verbose'])
    if interpreter.interpret():
        print("output:",interpreter.output)
    else:
        print("***PROGRAM FAILED***")
    if args['verbose']:
        print("Full data array:")
        print(interpreter._data)
        print("Data pointer at {}".format(interpreter._data_pointer))
