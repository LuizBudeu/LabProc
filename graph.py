import networkx as nx
from _parser import BinOp, Num, Parser, Lexer


# def ast_to_graph(ast):
#     graph = nx.DiGraph()

#     def dfs(node, parent=None):
#         if isinstance(node, BinOp):
#             graph.add_node(node, label=node.op)
#             if parent:
#                 graph.add_edge(parent, node)
#             dfs(node.left, node)
#             dfs(node.right, node)
#         elif isinstance(node, Num):
#             graph.add_node(node, label=str(node.value))
#             if parent:
#                 graph.add_edge(parent, node)

#     dfs(ast)
#     return graph


# import matplotlib.pyplot as plt

# def visualize_ast(graph):
#     pos = nx.nx_pydot.graphviz_layout(graph, prog="dot")
#     labels = nx.get_node_attributes(graph, "label")

#     plt.figure(figsize=(10, 6))
#     nx.draw(graph, pos, with_labels=True, labels=labels, node_size=1500, font_size=12, font_weight="bold", node_color="lightblue", arrowsize=20)
#     plt.show()



# text = '3 + 4 * (10 - 5 / (1*2 - 4))'
# lexer = Lexer(text)
# parser = Parser(lexer)
# ast = parser.parse()
# ast_graph = ast_to_graph(ast)
# print(ast_graph)
# visualize_ast(ast_graph)



import networkx as nx
import matplotlib.pyplot as plt

def build_graph(node, graph):
    if isinstance(node, Num):
        graph.add_node(id(node), label=node.as_string())
    elif isinstance(node, BinOp):
        graph.add_node(id(node), label=node.as_string())
        build_graph(node.left, graph)
        build_graph(node.right, graph)
        graph.add_edge(id(node), id(node.left))
        graph.add_edge(id(node), id(node.right))
        
text = '3 + 4 * (10 - 5)'
lexer = Lexer(text)
parser = Parser(lexer)
ast = parser.parse()

G = nx.DiGraph()
build_graph(ast, G)

pos = nx.drawing.nx_agraph.graphviz_layout(G, prog='dot')
nx.draw(G, pos, with_labels=True, node_size=1500, node_color="skyblue", font_size=10, font_weight="bold", arrowsize=20)
plt.show()