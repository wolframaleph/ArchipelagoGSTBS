from typing import Optional


class Node:
    def __init__(self, symbol: int = None, frequency: int = None):
        self.symbol : Optional[int] = symbol
        self.frequency : Optional[int] = frequency
        self.left : Optional[Node] = None
        self.right : Optional[Node] = None

    def __lt__(self, other) -> bool:
        return self.frequency < other.frequency


def generate_huffman_codes(node: Node, code: str, huffman_codes: dict[int, str]) -> dict[int, str]:
    if node is not None:
        if node.symbol is not None:
            huffman_codes[node.symbol] = code
        generate_huffman_codes(node.left, code + "0", huffman_codes)
        generate_huffman_codes(node.right, code + "1", huffman_codes)
    return huffman_codes


class GSHuffmanTree:
    def __init__(self, root: Optional[Node] = None):
        self.codes : Optional[dict[int, str]] = None
        self.root: Optional[Node] = root

    def flatten(self) -> None:
        self.codes = generate_huffman_codes(self.root, '', dict())


class GSHuffmanForest:
    def __init__(self):
        self.trees: dict[int, GSHuffmanTree] = dict()

    def __getitem__(self, char) -> GSHuffmanTree:
        return self.trees[char]

    def __setitem__(self, key, value) -> None:
        self.trees[key] = value

    def flatten_trees(self) -> None:
        for tree in self.trees.values(): tree.flatten()
