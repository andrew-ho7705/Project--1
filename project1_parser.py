# Lexer
import re
class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0

    # move the lexer position and identify next possible tokens.
    def get_token(self):
        while self.position < len(self.code) and self.code[self.position] in (" ", "\n"):
            self.position += 1
            
        if self.position == len(self.code):
            return None
        
        if self.code[self.position].isdigit():
            start_pos = self.position
            while self.code[self.position].isdigit():
                self.position += 1
            return int(self.code[start_pos:self.position]) # returns number (w/ multiple digits)
        
        if self.code[self.position].isalpha():
            start_pos = self.position
            while self.code[self.position].isalnum():
                self.position += 1
            return self.code[start_pos:self.position] # returns variable name, if, while, then, else, and do
        
        special_chars = re.compile(r"(=|!=|<|>|<=|>=|\+|\-|\*|\/|\(|\))")
        match = special_chars.match(self.code, self.position)
        if match:
            self.position = match.end()
            return match.group(1) # returns special characters mentioned in grammar.txt

# Parser
# Input : lexer object
# Output: AST program representation.


# First and foremost, to successfully complete this project you have to understand
# the grammar of the language correctly.

# We advise(not forcing you to stick to it) you to complete the following function 
# declarations.

# Basic idea is to walk over the program by each statement and emit a AST representation
# in list. And the test_utility expects parse function to return a AST representation in list.
# Return empty list for ill-formed programs.

# A minimal(basic) working parser must have working implementation for all functions except:
# if_statment, while_loop, condition.

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_token()
        
    # function to parse the entire program
    def parse(self):
        return self.program()
        
    # move to the next token.
    def advance(self):
        self.current_token = self.lexer.get_token()

    # parse the one or multiple statements
    def program(self):
        ast = []
        while self.current_token is not None:
            ast.append(self.statement())
        return ast
        
    
    # parse if, while, assignment statement.
    def statement(self):
        match self.current_token:
            # for if statements
            case "if": 
                self.advance()
                return self.if_statement()
            case "then" | "else":
                self.advance()
                if(self.current_token == "if"):
                    self.advance()
                    return self.if_statement()
                return self.assignment()
            # for while statements
            case "while": 
                self.advance()
                return self.while_loop()
            case "do":
                self.advance()
                return self.program()
        # for basic assignments
        return self.assignment()


    # parse assignment statements
    def assignment(self):
        variable = self.current_token
        self.advance()
        if self.current_token == "=":
            self.advance()
            expr = self.arithmetic_expression()
            return ("=", variable, expr)

    # parse arithmetic experssions
    def arithmetic_expression(self):
        term = self.term()
        while self.current_token in ("+", "-"):
            operand = self.current_token
            self.advance()
            term = (operand, term, self.term())
        return term
        
    def term(self):
        factor = self.factor()
        while self.current_token in ("*", "/"):
            operand = self.current_token
            self.advance()
            factor = (operand, factor, self.factor())
        return factor

    def factor(self):
        if type(self.current_token) == int:
            value = self.current_token
            self.advance()
            return value
        elif self.current_token.isalnum():
            variable = self.current_token
            self.advance()
            return variable
        elif self.current_token == "(":
            self.advance()
            expression = self.arithmetic_expression()
            self.advance()
            return expression

    # parse if statement, you can handle then and else part here.
    # you also have to check for condition.
    def if_statement(self):
        condition = self.condition()
        thenStatement = self.statement()
        elseStatement = self.statement()
        return (
            ("if", condition, thenStatement, elseStatement) 
            if elseStatement 
            else ("if", condition, thenStatement)
            )
    
    # implement while statment, check for condition
    # possibly make a call to statement?
    def while_loop(self):
        condition = self.condition()
        return ("while", condition, self.statement())

    def condition(self):
        expr1 = self.arithmetic_expression()
        if self.current_token in ("<", ">", "<=", ">=", "=="):
            operand = self.current_token
            self.advance()
            expr2 = self.arithmetic_expression()
            return (operand, expr1, expr2)