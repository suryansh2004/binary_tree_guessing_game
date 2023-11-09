import os

class Node:
    def __init__(self, question, movie=None):
        self.question = question
        self.movie = movie
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def build_tree(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.root = self.build_tree_recursive(lines)

    def build_tree_recursive(self, lines):
        if not lines:
            return None

        line = lines.pop(0).strip()
        parts = line.split(" ", 1)
        address = int(parts[0])
        rest = parts[1]

        if rest.startswith("It's "):
            # It's a movie node
            movie = rest.replace("It's ", "")
            return Node(None, movie)

        question = rest
        left_child = self.build_tree_recursive(lines)
        right_child = self.build_tree_recursive(lines)
        node = Node(question)
        node.left = left_child
        node.right = right_child

        return node

    def play_game(self, node=None):
        if node is None:
            node = self.root

        print("Please answer a series of questions and I will tell you what movie you are thinking about:")
        while node.left or node.right:
            answer = input(node.question + " (Y/N)? ").strip().upper()
            if answer == 'Y':
                node = node.left
            elif answer == 'N':
                node = node.right
            else:
                print("Please answer with 'Y' or 'N'.")
        print(f"It’s '{node.movie}'.")

    def display(self, node=None, indent="", last='updown'):
        if node is not None:
            if last == 'updown':  # root
                print(indent + "Root -> " + (node.question if node.question else f"Movie: {node.movie}"))
                indent += "     "
            elif last == 'right':  # right child
                print(indent + "┌── " + (node.question if node.question else f"Movie: {node.movie}"))
                indent += "|    "
            elif last == 'left':  # left child
                print(indent + "└── " + (node.question if node.question else f"Movie: {node.movie}"))
                indent += "     "

            self.display(node.left, indent, 'left')
            self.display(node.right, indent, 'right')


def print_help():
    print("P Play the game")
    print("L Load another game file")
    print("D Display the binary tree")
    print("H Help information")
    print("X Exit the program")

if __name__ == "__main__":
    tree = BinaryTree()
    file_path = "game1.txt"  # Default game file
    tree.build_tree(file_path)

    print_help()  # Print help information at the start
    while True:
        print("…your choice: ", end='')
        choice = input().strip().upper()
        if choice == 'P':
            tree.play_game()
        elif choice == 'L':
            file_list = [f for f in os.listdir('.') if f.endswith('game.txt')]
            for fIndex in range(len(file_list)):
                print(f"{fIndex+1}: {file_list[fIndex]}")
            fileIndex = input("Enter the game file to load: ").strip()
            tree.build_tree(file_list[fIndex-1])
            print("Game file loaded successfully.")
        elif choice == 'D':
            tree.display(tree.root)
        elif choice == 'H':
            print_help()
        elif choice == 'X':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
