from infero.sentences import Implication, Not, Or


class ModusPonens:

    def __init__(self, rule: Implication):
        self.premise1 = rule
        self.premise2 = rule.antecedent
        self.conclusion = rule.consequent

    def __repr__(self):
        return (
            f"Modus Ponens\n{self.premise1.formula()}\n"
            f"{self.premise2.formula()}\n"
            "------\n"
            f"{self.conclusion.formula()}\n"
        )

    def evaluate(self, symhash):
        return self.premise2.evaluate(symhash)


class ModusTollens:

    def __init__(self, rule: Implication):
        self.premise1 = rule
        self.premise2 = Not(rule.consequent)
        self.conclusion = Not(rule.antecedent)

    def __repr__(self):
        return (
            f"Modus Tollens\n{self.premise1.formula()}\n"
            f"{self.premise2.formula()}\n"
            "------\n"
            f"{self.conclusion.formula()}\n"
        )

    def evaluate(self, symhash):
        return self.premise2.evaluate(symhash)


class DisjunctiveSyllogism:

    def __init__(self, rule: Or, right: bool = False):
        self.premise1 = rule
        self.premise2 = Not(rule.disjuncts[int(right)])
        self.conclusion = rule.disjuncts[1 - int(right)]

    def __repr__(self):
        return (
            f"Disjunctive Syllogism\n{self.premise1.formula()}\n"
            f"{self.premise2.formula()}\n"
            "------\n"
            f"{self.conclusion.formula()}\n"
        )

    def evaluate(self, symhash):
        return self.premise2.evaluate(symhash)


class HipoteticalSyllogism:

    def __init__(self, premise1: Implication, premise2: Implication):
        self.premise1 = premise1
        self.premise2 = premise2

    def __repr__(self):
        return (
            f"Hipotetical Syllogism\n{self.premise1.formula()}\n"
            f"{self.premise2.formula()}\n"
            "------\n"
            f"{self.apply().formula()}\n"
        )

    def apply(self):
        return Implication(self.premise1.antecedent, self.premise2.consequent)
