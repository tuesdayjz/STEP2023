class User:
    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password
        self.left: User = None
        self.right: User = None
        self.height = 0


class UserTree:
    def __init__(self):
        self.root = None

    def get_height(self, user: User) -> int:
        # bottom node's height is 0
        if not user:
            return -1
        return user.height

    def diff_height(self, user: User) -> int:
        # get diff of left.height and right.height
        if not user:
            return 0
        return self.get_height(user.left) - self.get_height(user.right)

    def register(self, user: User) -> User:
        # start from root
        self.root = self._register(user, self.root)
        return self.root

    def _register(self, user: User, node: User) -> User:
        # if node is empty, set user as node
        if not node:
            node = user
        # if name is smaller than node's name, go left
        if user.name < node.name:
            node.left = self._register(user, node.left)
        # if name is bigger than node's name, go right
        elif user.name > node.name:
            node.right = self._register(user, node.right)
        # if name is same, update password
        else:
            node.password = user.password
        # update height
        node.height = max(self.get_height(node.left),
                          self.get_height(node.right)) + 1
        # balance tree
        return self.balance(user, node)

    def balance(self, user: User, node: User) -> User:
        # get diff of left.height and right.height
        diff = self.diff_height(node)
        # if diff is 2 or -2, rotate
        if diff > 1 and user.name < node.left.name:
            return self.rotate_right(node)
        if diff < -1 and user.name > node.right.name:
            return self.rotate_left(node)
        if diff > 1 and user.name > node.left.name:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if diff < -1 and user.name < node.right.name:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    def rotate_left(self, user: User) -> User:
        # first, see user as root
        # set right as root
        # connect right's left child to user's right child
        right = user.right
        right_left = right.left
        right.left = user
        user.right = right_left
        # update height, return new root
        user.height = max(self.get_height(user.left),
                          self.get_height(user.right)) + 1
        right.height = max(self.get_height(right.left),
                           self.get_height(right.right)) + 1
        return right

    def rotate_right(self, user: User) -> User:
        # first, see user as root
        # set left as root
        # connect left's right child to user's left child
        left = user.left
        left_right = left.right
        left.right = user
        user.left = left_right
        # update height, return new root
        user.height = max(self.get_height(user.left),
                          self.get_height(user.right)) + 1
        left.height = max(self.get_height(left.left),
                          self.get_height(left.right)) + 1
        return left

    def login(self, name: str, password: str) -> bool:
        # start from root
        node = self.root
        while node:
            # if name and password are correct, return True
            if node.name == name:
                if node.password == password:
                    return True
                else:
                    return False
            # if name is smaller, go right
            elif node.name < name:
                node = node.right
            # if name is bigger, go left
            else:
                node = node.left
        return False

    def delete(self, user: User) -> None:
        ########################
        # TODO: implement here #
        ########################
        pass

    def draw(self) -> None:
        # draw tree, start from root
        self._draw(self.root)

    def _draw(self, node: User) -> None:
        # if node is empty, return
        if not node:
            return None
        # draw left child
        self._draw(node.left)
        # draw node
        print(" " * self.get_length(node) + node.name + " " + node.password)
        # draw right child
        self._draw(node.right)

    def get_length(self, node: User) -> int:
        # get max sum of left and right child's name + password length
        if not node.left and not node.right:
            return 0
        elif not node.left and node.right:
            return len(node.right.name) + len(node.right.password) + 1
        elif not node.right and node.left:
            return len(node.left.name) + len(node.left.password) + 1
        else:
            return max(self.get_length(node.left) + len(node.left.name) + len(node.left.password) + 1,
                       self.get_length(node.right) + len(node.right.name) + len(node.right.password) + 1)


def functional_test() -> UserTree:
    user_tree = UserTree()
    assert user_tree.register(User("m", "passwd")).name == "m"
    assert user_tree.login("m", "passwd") == True
    assert user_tree.login("m", "n") == False
    assert user_tree.login("n", "passwd") == False
    assert user_tree.root.left == None
    assert user_tree.root.right == None

    assert user_tree.register(User("n", "mon")).name == "m"
    assert user_tree.register(User("l", "tue")).name == "m"
    assert user_tree.login("n", "mon") == True
    assert user_tree.login("l", "tue") == True
    assert user_tree.login("l", "mon") == False
    assert user_tree.login("n", "tue") == False
    assert user_tree.root.left.name == "l"
    assert user_tree.root.right.name == "n"

    assert user_tree.register(User("a", "passwd")).name == "m"
    assert user_tree.register(User("b", "b")).name == "m"
    assert user_tree.register(User("c", "c")).name == "l"
    assert user_tree.login("a", "passwd") == True
    assert user_tree.login("b", "b") == True
    assert user_tree.login("c", "c") == True
    assert user_tree.root.left.name == "b"
    assert user_tree.root.right.name == "m"
    assert user_tree.root.left.left.name == "a"
    assert user_tree.root.left.right.name == "c"
    assert user_tree.root.right.right.name == "n"

    assert user_tree.register(User("o", "o")).name == "l"
    assert user_tree.login("o", "o") == True
    assert user_tree.root.right.name == "n"
    assert user_tree.root.right.left.name == "m"
    assert user_tree.root.right.right.name == "o"

    print("Functional test passed!\n=======================\n")
    return user_tree


if __name__ == "__main__":
    functional_test().draw()
