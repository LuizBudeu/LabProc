from _parser import BinOp, Num, Parser, Lexer


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def build_tree():
    # Create the nodes
    n1 = Node("+")
    n2 = Node(5)
    n3 = Node("x")
    n4 = Node(3)
    n5 = Node(4)

    # Connect the nodes to build the tree
    n1.left = n2
    n1.right = n3
    n3.left = n4
    n3.right = n5

    return n1


def ascii_visualize_tree(node, prefix="", is_left=None):
    if node is None:
        return

    if type(node) is BinOp:
        data = node.op.value
    else:
        data = node.value
    if isinstance(data, str):
        ascii_visualize_tree(node.left, prefix + "    ", True)
        print(prefix + ("|-- " if is_left is True else "\\-- ") + str(data))
        ascii_visualize_tree(node.right, prefix + "    ", False)
    else:
        print(prefix + ("|-- " if is_left is True else "\\-- ") + str(data))


# Build the tree
# root = build_tree()

text = '3 + 4 * (10 - 5 / (1*2 - 4))'
lexer = Lexer(text)
parser = Parser(lexer)
root = parser.parse()

# Visualize the tree
ascii_visualize_tree(root)
