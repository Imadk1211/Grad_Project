# tree
class Node:
    def __init__(self, symbol, left=None, right=None) -> None:
        self.symbol = symbol
        self.left = left
        self.right = right

# file input object, init one with every file read
class lexObject:
    def __init__(self, file) -> None:
        with open(file, "r") as f:
            self.expression = f.read()
        self.token_index = 0
        
    def get_next_token(self):
        self.token_index += 1
        return self.expression[self.token_index-1]

    def unconsumed_input(self):
        return self.expression[self.token_index:]

error = False
next_token = "%"

# function to update next token
def lex(fileReader: lexObject):
    global next_token
    next_token = fileReader.get_next_token()

def print_tree(tree: Node):
    if tree is None:
        return
    print_tree(tree.left)
    print_tree(tree.right)
    print(tree.symbol)

# compute the value of the expression
def evaluate(tree: Node):
    if tree.symbol == 1: return -1
    if tree.symbol == 'a': return 10
    if tree.symbol == 'b': return 20
    if tree.symbol == 'c': return 30
    if tree.symbol == 'd': return 40
    if tree.symbol in [0, 1, 2, 3]: return tree.symbol
    if tree.symbol == '+': return evaluate(tree.left) + evaluate(tree.right) 
    if tree.symbol == '*': return evaluate(tree.left) * evaluate(tree.right)
    if tree.symbol == '-': return evaluate(tree.left) - evaluate(tree.right)
    if tree.symbol == '/':
        right_value = evaluate(tree.right)
        if right_value == 0:
            raise ValueError("Division by zero")
        return evaluate(tree.left) / right_value


def G() -> Node:
    global error, next_token
    lex(lexObject)
    print ("G -> E"); 
    tree = E()
    if (next_token=='$'  and not error):
        print("success") 
        return tree; 
    else:
        print(f"failure: unconsumed input={lexObject.unconsumed_input()}"); 
        return None; 


def E() -> Node: 
    global error, next_token
    if (error): return None
    print ("E -> T R"); 
    temp = T()
    return R(temp)

def R(tree: Node) -> Node:
    global error, next_token
    if (error): return None; 
    if (next_token== '+'):
        print ("R -> + T R")
        lex(lexObject)
        temp1 = T()
        temp2 = R(temp1)
        return Node('+', tree, temp2)
    elif (next_token== '-'):
        print ("R -> - T R")
        lex(lexObject)
        temp1: Node = T()
        temp2: Node = R(temp1)
        return Node('-', tree, temp2)
        
    else:
        print ("R->e")
        return(tree)
 
def T()->Node: 
    global error, next_token
    if (error): return
    print (" T -> F S"); 
    temp: Node =  F() 
    return S(temp)
    
def S(tree: Node)-> Node: 
    global error, next_token
    if (error): return
    if (next_token =='*'):
        print ("S -> * F S")
        lex(lexObject) 
        temp1: Node = F()
        temp2: Node = S(temp1)    
        return Node('*', tree, temp2)
        
    elif (next_token=='/'):
        print("S -> / F S") 
        lex(lexObject)
        temp1: Node = F()
        temp2: Node = S(temp1)   
        return Node('/',tree,temp2)
    else:
        print("S -> e") 
        return(tree)   
    

def F() -> Node:
    global error, next_token
    temp: Node
    if (error): return None 
    if (next_token=='(' ):
        print("F->( E )") 
        lex(lexObject)
        temp = E() 
        if (next_token == ')'  ):
            lex(lexObject)
            return(temp)    
        else:
            error=True; 
            print("error: unexpected token ", next_token);       
            print("unconsumed_input ", lexObject.unconsumed_input()); 
            return None;  

    elif (next_token in ['a', 'b', 'c', 'd']):
        print ("F->M")
        return M()
      
    elif (next_token in ['0', '1', '2', '3']):
        print ("F->N"); 
        return N() 
    
    else: 
        error=True;   
        print("error: unexpected token ", next_token);     
        print("unconsumed_input ", lexObject.unconsumed_input()); 
        return(None); 
        

def M() -> Node: 
    global error, next_token
    prev_token = next_token
    if (error): return None 
    if  (next_token in ['a', 'b', 'c', 'd']):
        print ("M->", next_token)
        lex(lexObject)
        return Node(prev_token, None,None)
    else:
        error=True
        print("error: unexpected token ", next_token)    
        print("unconsumed_input ", lexObject.unconsumed_input())
        return None

def N() -> Node: 
    global error, next_token
    prev_token = next_token
    if (error): return None 
    if  (next_token in ['0', '1', '2', '3']):
        print ("N->", next_token) 
        lex(lexObject) 
        return Node(prev_token, None
# tree
class Node:
    def __init__(self, symbol, left=None, right=None) -> None:
        self.symbol = symbol
        self.left = left
        self.right = right

# file input object, init one with every file read
class lexObject:
    def __init__(self, file) -> None:
        with open(file, "r") as f:
            self.expression = f.read
        self.token_index = 0
        
    def get_next_token(self):
        self.token_index += 1
        return self.expression[self.token_index-1]

    def unconsumed_input(self):
        return self.expression[self.token_index:]

error = False
next_token = "%"

# function to update next token
def lex(fileReader: lexObject):
    global next_token
    next_token = lexObject.get_next_token()

def print_tree(tree: Node):
    if tree is None:
        return
    print(tree.left)
    print(tree.right)
    print(tree.symbol)

# compute the value of the expression
def evaluate(tree: Node):
    if tree.symbol == 1: return -1
    if tree.symbol == 'a': return 10
    if tree.symbol == 'b': return 20
    if tree.symbol == 'c': return 30
    if tree.symbol == 'd': return 40
    if tree.symbol in [0, 1, 2, 3]: return tree.symbol
    if tree.symbol == '+': return evaluate(tree.left) + evaluate(tree.right) 
    if tree.symbol == '*': return evaluate(tree.left) * evaluate(tree.right)
    if tree.symbol == '-': return evaluate(tree.left) - evaluate(tree.right)
    if tree.symbol == '/': return evaluate(tree.left) / evaluate(tree.right)


def G() -> Node:
    global error, next_token
    lex()
    print ("G -> E"); 
    tree = E()
    if (next_token=='$'  and not error):
        print("success") 
        return tree; 
    else:
        print(f"failure: unconsumed input={lexObject.unconsumed_input()}"); 
        return None; 


def E() -> Node: 
    global error, next_token
    if (error): return None
    print ("E -> T R"); 
    temp = T()
    return R(temp)

def R(tree: Node) -> Node:
    global error, next_token
    if (error): return None; 
    if (next_token== '+'):
        print ("R -> + T R")
        lex()
        temp1 = T()
        temp2 = R(temp1)
        return Node('+', tree, temp2)
    elif (next_token== '-'):
        print ("R -> - T R")
        lex()
        temp1: Node = T()
        temp2: Node = R(temp1)
        return Node('-', tree, temp2)
        
    else:
        print ("R->e")
        return(tree)
 
def T()->Node: 
    global error, next_token
    if (error): return
    print (" T -> F S"); 
    temp: Node =  F() 
    return S(temp)
    
def S(tree: Node)-> Node: 
    global error, next_token
    if (error): return
    if (next_token =='*'):
        print ("S -> * F S")
        lex() 
        temp1: Node = F()
        temp2: Node = S(temp1)    
        return Node('*', tree, temp2)
        
    elif (next_token=='/'):
        print("S -> / F S") 
        lex()
        temp1: Node = F()
        temp2: Node = S(temp1)   
        return Node('/',tree,temp2)
    else:
        print("S -> e") 
        return(tree)   
    

def F() -> Node:
    global error, next_token
    temp: Node
    if (error): return None 
    if (next_token=='(' ):
        print("F->( E )") 
        lex()
        temp = E() 
        if (next_token == ')'  ):
            lex()
            return(temp)    
        else:
            error=True; 
            print("error: unexpected token ", next_token);       
            print("unconsumed_input ", lexObject.unconsumed_input()); 
            return None;  

    elif (next_token in ['a', 'b', 'c', 'd']):
        print ("F->M")
        return M()
      
    elif (next_token in ['0', '1', '2', '3']):
        print ("F->N"); 
        return N() 
    
    else: 
        error=True;   
        print("error: unexpected token ", next_token);     
        print("unconsumed_input ", lexObject.unconsumed_input()); 
        return(None); 
        

def M() -> Node: 
    global error, next_token
    prev_token = next_token
    if (error): return None 
    if  (next_token in ['a', 'b', 'c', 'd']):
        print ("M->", next_token)
        lex()
        return Node(prev_token, None,None)
    else:
        error=True
        print("error: unexpected token ", next_token)    
        print("unconsumed_input ", lexObject.unconsumed_input())
        return None

def N() -> Node: 
    global error, next_token
    prev_token = next_token
    if (error): return None 
    if  (next_token in ['0', '1', '2', '3']):
        print ("N->", next_token) 
        lex() 
        return Node(prev_token, None,None) 
    else:
        error=True;   
        print("error: unexpected token ", next_token);      
        print("unconsumed_input ", lexObject.unconsumed_input()); 
        return None 





def lex(file):
    global next_token
    next_token = '%'
    while True:
        next_token = file.read(1)  # Read the next character from the file
        if next_token == '\t' or next_token == '\n' or next_token == ' ':
            pass  # Skip whitespace characters
        else:
            break  # Exit the loop when a non-whitespace character is found

def unconsumed_input(file):
    # Return the remaining input in the file
    return file.read()

def G(file):
    global next_token
    global error
    tree = None
    lex(file)
    print("G -> E")
    tree = E(file)
    if next_token == '$' and not error:
        print("Success")
        return tree
    else:
        print("Failure: unconsumed input=%s" % unconsumed_input(file))
        error = True
        return None

def E(file):
    global error
    if error:
        return None
    print("E -> T R")
    temp = T(file)
    return R(file, temp)

def R(file, tree):
    global next_token
    global error
    if error:
        return None
    if next_token == '+':
        print("R -> + T R")
        lex(file)
        temp1 = T(file)
        temp2 = R(file, temp1)
        return Node('+', tree, temp2)
    elif next_token == '-':
        print("R -> - T R")
        lex(file)
        temp1 = T(file)
        temp2 = R(file, temp1)
        return Node('-', tree, temp2)
    else:
        print("R -> e")
        return tree

def T(file):
    global error
    if error:
        return None
    print("T -> F S")
    temp = F(file)
    return S(file, temp)

def S(file, tree):
    global next_token
    global error
    if error:
        return None
    if next_token == '*':
        print("S -> * F S")
        lex(file)
        temp1 = F(file)
        temp2 = S(file, temp1)
        return Node('*', tree, temp2)
    elif next_token == '/':
        print("S -> / F S")
        lex(file)
        temp1 = F(file)
        temp2 = S(file, temp1)
        return Node('/', tree, temp2)
    else:
        print("S -> e")
        return tree

def F(file):
    global next_token
    global error
    if error:
        return None
    if next_token == '(':
        print("F -> ( E )")
        lex(file)
        temp = E(file)
        if next_token == ')':
            lex(file)
            return temp
        else:
            error = True
            print("Error: unexpected token ", next_token)
            print("Unconsumed input ", unconsumed_input(file))
            return None
    elif next_token in ['a', 'b', 'c', 'd']:
        print("F -> M")
        return M(file)
    elif next_token in ['0', '1', '2', '3']:
        print("F -> N")
        return N(file)
    else:
        error = True
        print("Error: unexpected token ", next_token)
        print("Unconsumed input ", unconsumed_input(file))
        return None

def M(file):
    global next_token
    global error
    prev_token = next_token
    if error:
        return None
    if next_token in ['a', 'b', 'c', 'd']:
        print("M ->", next_token)
        lex(file)
        return Node(prev_token)
    else:
        error = True
        print("Error: unexpected token ", next_token)
        print("Unconsumed input ", unconsumed_input(file))
        return None

def N(file):
    global next_token
    global error
    prev_token = next_token
    if error:
        return None
    if next_token in ['0', '1', '2', '3']:
        print("N ->", next_token)
        lex(file)
        return Node(prev_token)
    else:
        error = True
        print("Error: unexpected token ", next_token)
        print("Unconsumed input ", unconsumed_input(file))
        return None

def printTree(tree):
    if tree is None:
        return
    printTree(tree.leftChild)
    printTree(tree.rightChild)
    print(tree.symbol)

def evaluate(tree):
    if tree is None:
        return -1
    if tree.symbol == 'a':
        return 10
    if tree.symbol == 'b':
        return 20
    if tree.symbol == 'c':
        return 30
    if tree.symbol == 'd':
        return 40
    if tree.symbol in ['0', '1', '2', '3']:
        return int(tree.symbol)
    if tree.symbol == '+':
        return evaluate(tree.leftChild) + evaluate(tree.rightChild)
    if tree.symbol == '-':
        return evaluate(tree.leftChild) - evaluate(tree.rightChild)
    if tree.symbol == '*':
        return evaluate(tree.leftChild) * evaluate(tree.rightChild)
    if tree.symbol == '/':
        return evaluate(tree.leftChild) / evaluate(tree.rightChild)
if __name__ == '__main__':
    main()