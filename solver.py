
# =========================
# ROW
# =========================

class Row:
    def __init__(self, p, q, a, b, consistent):
        self.p = p
        self.q = q
        self.a = a
        self.b = b
        self.consistent = consistent


# =========================
# SOLVER
# =========================

class Solver:
    def __init__(self, a_node, b_node):
        self.a_statement = a_node
        self.b_statement = b_node

    def rows(self):
        results = []

        for p in (True, False):
            for q in (True, False):

                env = {
                    "p": p,
                    "q": q
                }

                a = (
                    self.a_statement.evaluate(env)
                    if self.a_statement is not None
                    else None
                )

                b = (
                    self.b_statement.evaluate(env)
                    if self.b_statement is not None
                    else None
                )

                consistent = (
                    (a is None or p == a)
                    and
                    (b is None or q == b)
                )

                row = Row(p, q, a, b, consistent)

                results.append(row)

        return results

    def solutions(self):
        return [
            row for row in self.rows()
            if row.consistent
        ]
