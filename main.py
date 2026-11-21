
from parser import Parser, tokenize, ParseError
from solver import Solver


# =========================
# DISPLAY HELPERS
# =========================

def tf(value):
    return "T" if value else "F"


def role(value):
    return "a knight" if value else "a knave"


# =========================
# DISPLAY TRUTH TABLE
# =========================

def show_table(solver):

    headers = ["p", "q"]

    if solver.a_statement is not None:
        headers.append("A's statement")

    if solver.b_statement is not None:
        headers.append("B's statement")

    headers.append("Consistent")

    rows = solver.rows()

    data = []

    for row in rows:
        cells = [tf(row.p), tf(row.q)]

        if solver.a_statement is not None:
            cells.append(tf(row.a))

        if solver.b_statement is not None:
            cells.append(tf(row.b))

        cells.append("Yes" if row.consistent else "No")

        data.append(cells)

    widths = []

    for i, header in enumerate(headers):
        width = len(header)

        for row in data:
            width = max(width, len(row[i]))

        widths.append(width + 2)

    print()

    print(
        "".join(
            headers[i].ljust(widths[i])
            for i in range(len(headers))
        )
    )

    for row, cells in zip(rows, data):

        line = "".join(
            cells[i].ljust(widths[i])
            for i in range(len(cells))
        )

        if row.consistent:
            line += "<== solution"

        print(line)


# =========================
# DISPLAY ANSWER
# =========================

def show_answer(solutions):

    count = len(solutions)

    if count == 0:
        print("\nNo solution: no assignment of knights and knaves fits these statements.")
        return

    if count == 1:
        print("\nSolution:")
    else:
        print(f"\n{count} solutions:")

    for i, row in enumerate(solutions, start=1):

        answer = (
            f"A is {role(row.p)} and "
            f"B is {role(row.q)}."
        )

        if count > 1:
            print(f"{i}. {answer}")
        else:
            print(answer)


# =========================
# INPUT HANDLING
# =========================

def read_statement(label):

    while True:

        text = input(
            f"{label}'s statement (leave blank if silent): "
        ).strip()

        if text == "":
            return None

        try:
            tokens = tokenize(text)
            return Parser(tokens).parse()

        except ParseError as error:
            print(f"Invalid statement: {error}")
            print("Please try again.\n")


def read_puzzle():

    while True:

        print("\nEnter the statements using:")
        print("p, q, ¬, ∧, ∨, →, ↔")
        print("You can also use: not, and, or, ->, <->\n")

        a_node = read_statement("A")
        b_node = read_statement("B")

        if a_node is None and b_node is None:
            print("At least one of A and B must make a statement.\n")
            continue

        return a_node, b_node


# =========================
# MAIN PROGRAM
# =========================

def main():

    print("=" * 45)
    print("       KNIGHTS AND KNAVES SOLVER")
    print("=" * 45)

    print("\nLogical variables:")
    print("p = A is a knight")
    print("q = B is a knight")

    while True:

        a_node, b_node = read_puzzle()

        solver = Solver(a_node, b_node)

        print("\nTRUTH TABLE")
        print("-" * 45)

        show_table(solver)

        print("\nRESULT")
        print("-" * 45)

        show_answer(solver.solutions())

        again = input(
            "\nWould you like to solve another puzzle? (y/n): "
        ).strip().lower()

        if again != "y":
            print("\nThank you for using the solver!")
            break


if __name__ == "__main__":
    main()
