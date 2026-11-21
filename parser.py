
import re


# =========================
# EXPRESSION TREE NODES
# =========================

class Var:
    def __init__(self, name):
        self.name = name

    def evaluate(self, env):
        return env[self.name]


class Not:
    def __init__(self, operand):
        self.operand = operand

    def evaluate(self, env):
        return not self.operand.evaluate(env)


class Binary:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class And(Binary):
    def evaluate(self, env):
        return self.left.evaluate(env) and self.right.evaluate(env)


class Or(Binary):
    def evaluate(self, env):
        return self.left.evaluate(env) or self.right.evaluate(env)


class Implies(Binary):
    def evaluate(self, env):
        return (not self.left.evaluate(env)) or self.right.evaluate(env)


class Iff(Binary):
    def evaluate(self, env):
        return self.left.evaluate(env) == self.right.evaluate(env)


# =========================
# PARSE ERROR
# =========================

class ParseError(Exception):
    pass


# =========================
# TOKENIZER
# =========================

def tokenize(text):
    text = text.lower()

    text = text.replace("<->", "↔")
    text = text.replace("->", "→")

    text = re.sub(r"\bnot\b", "¬", text)
    text = re.sub(r"\band\b", "∧", text)
    text = re.sub(r"\bor\b", "∨", text)

    tokens = []

    for char in text:
        if char.isspace():
            continue

        if char in "pq()¬∧∨→↔":
            tokens.append(char)
        else:
            raise ParseError(f"unknown symbol '{char}'")

    return tokens


# =========================
# PARSER
# =========================

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]

        return None

    def take(self):
        token = self.peek()
        self.pos += 1
        return token

    def parse(self):
        if not self.tokens:
            raise ParseError("statement is empty")

        node = self.iff()

        if self.peek() is not None:
            if self.peek() == ")":
                raise ParseError("unbalanced parentheses")

            raise ParseError(
                f"missing operator before '{self.peek()}'"
            )

        return node

    # Lowest precedence
    def iff(self):
        left = self.implies()

        while self.peek() == "↔":
            self.take()
            left = Iff(left, self.implies())

        return left

    def implies(self):
        left = self.disjunction()

        if self.peek() == "→":
            self.take()
            return Implies(left, self.implies())

        return left

    def disjunction(self):
        left = self.conjunction()

        while self.peek() == "∨":
            self.take()
            left = Or(left, self.conjunction())

        return left

    def conjunction(self):
        left = self.negation()

        while self.peek() == "∧":
            self.take()
            left = And(left, self.negation())

        return left

    def negation(self):
        if self.peek() == "¬":
            self.take()
            return Not(self.negation())

        return self.atom()

    def atom(self):
        token = self.take()

        if token == "p" or token == "q":
            return Var(token)

        if token == "(":
            node = self.iff()

            if self.take() != ")":
                raise ParseError("unbalanced parentheses")

            return node

        if token is None:
            raise ParseError("statement ends too early")

        raise ParseError(f"unexpected '{token}'")
