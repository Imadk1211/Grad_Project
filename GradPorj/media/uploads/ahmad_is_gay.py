class Node:
    def __init__(self, symbol, left=None, right=None):
        self.symbol = symbol
        self.leftChild = left
        self.rightChild = right

error = False
next_token = '%'  # Initializing next_token with a placeholder character

def lex(file):
    global next_token
    next_char = file.read(1)  # Read the next character from the file
    while next_char == ' ' or next_char == '\n':
        next_char = file.read(1)  # Skip whitespace characters
    if next_char:
        next_token = next_char  # Update next_token with the next valid token
    else:
        next_token = '$'  # Set next_token to '$' if end of file is reached

def G(file):
    global error, next_token
    tree = E(file)  # Parse E non-terminal
    if next_token == '$' and not error:  # If end of file and no error occurred
        print("Success")
        return tree
    else:
        error = True
        print(f"Failure: Unconsumed input: {unconsumed_input(file)}")
        return None

def E(file):
    global error
    temp = T(file)  # Parse T non-terminal
    return R(file, temp)  # Parse R non-terminal with the parsed T subtree

def R(file, tree):
    global error, next_token
    if next_token == '+':
        lex(file)
        temp1 = T(file)
        temp2 = R(file, temp1)
        return Node('+', tree, temp2)  # Create an AST node for addition
    elif next_token == '-':
        lex(file)
        temp1 = T(file)
        temp2 = R(file, temp1)
        return Node('-', tree, temp2)  # Create an AST node for subtraction
    else:
        return tree

def T(file):
    temp = F(file)  # Parse F non-terminal
    return S(file, temp)  # Parse S non-terminal with the parsed F subtree

def S(file, tree):
    global next_token
    if next_token == '*':
        lex(file)
        temp1 = F(file)
        temp2 = S(file, temp1)
        return Node('*', tree, temp2)  # Create an AST node for multiplication
    elif next_token == '/':
        lex(file)
        temp1 = F(file)
        temp2 = S(file, temp1)
        return Node('/', tree, temp2)  # Create an AST node for division
    else:
        return tree

def F(file):
    global error, next_token
    if next_token == '(':
        lex(file)
        temp = E(file)  # Parse expression inside parentheses
        if next_token == ')':
            lex(file)
            return temp  # Return the parsed subtree within parentheses
        else:
            error = True
            print(f"Error: Unexpected token {next_token}")
            print(f"Unconsumed input: {unconsumed_input(file)}")
            return None
    elif next_token in 'abcd':
        symbol = next_token
        lex(file)
        return Node(symbol)  # Create a leaf node for variables
    elif next_token in '0123':
        symbol = next_token
        lex(file)
        return Node(symbol)  # Create a leaf node for constants
    else:
        error = True
        print(f"Error: Unexpected token {next_token}")
        print(f"Unconsumed input: {unconsumed_input(file)}")
        return None

def unconsumed_input(file):
    current_pos = file.tell()  # Get the current file position
    file.seek(0, 2)  # Move the file pointer to the end of file
    file_size = file.tell()  # Get the file size
    file.seek(current_pos)  # Restore the file position
    remaining = file.read(file_size - current_pos)  # Read the remaining input
    return remaining

def printTree(tree):
    if tree is None:
        return
    printTree(tree.leftChild)  # Print left subtree
    printTree(tree.rightChild)  # Print right subtree
    print(tree.symbol, end=' ')  # Print the node symbol

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
    if tree.symbol in '0123':
        return int(tree.symbol)
    if tree.symbol == '+':
        return evaluate(tree.leftChild) + evaluate(tree.rightChild)
    if tree.symbol == '-':
        return evaluate(tree.leftChild) - evaluate(tree.rightChild)
    if tree.symbol == '*':
        return evaluate(tree.leftChild) * evaluate(tree.rightChild)
    if tree.symbol == '/':
        return evaluate(tree.leftChild) // evaluate(tree.rightChild)

def main():
    global error
    error = False
    next_token = '%'  # Reset next_token
    with open('input.txt', 'r') as file:  # Open input file for reading
        lex(file)  # Perform lexical analysis
        theTree = G(file)  # Start parsing with G non-terminal
        if not error:
            print("Abstract Syntax Tree (Postfix Notation):")
            printTree(theTree)  # Print AST in postfix notation
            print("\n")
            value = evaluate(theTree)  # Evaluate the expression from AST
            print(f"The value is {value}")
        else:
            print("Input not parsed correctly")

if __name__ == "__main__":
    main()
