from infero.inference_rules import (
    DisjunctiveSyllogism,
    HipoteticalSyllogism,
    ModusPonens,
    ModusTollens,
)
from infero.sentences import And, Implication, Not, Or, Sentence, Symbol


def solve(rules: list[Sentence], query: Sentence, symhash: dict[str, bool | None]):

    finded: bool | None = None
    path: list = []
    iterations: int = 0

    def calc_score(sentence):
        symbols = sentence.symbols()
        facts = sum(symhash[symbol] is not None for symbol in symbols)
        derive = isinstance(sentence, Implication) and sentence.consequent == query
        return len(symbols) - facts - 0.5 * derive

    score_list = list(
        sorted(
            [(sentence, calc_score(sentence)) for sentence in rules], key=lambda x: x[1]
        )
    )

    def process_sentence(sentence):
        if isinstance(sentence, Symbol):
            symhash[sentence.name] = True
        elif isinstance(sentence, Not):
            if isinstance(sentence.operand, Not):
                process_sentence(sentence.operand.operand)
            elif len(sentence.symbols()) == 1:
                symhash[sentence.operand.name] = False
            else:
                process_sentence(Sentence.apply_demorgan(sentence.operand))
        elif isinstance(sentence, And):
            process_sentence(sentence.conjuncts[0])
            process_sentence(sentence.conjuncts[1])
        else:
            # Implication or Or
            score_list.append((sentence, 0))

    def update_scores():
        return list(
            sorted(
                [(sentence, calc_score(sentence)) for sentence, _ in score_list],
                key=lambda x: x[1],
            )
        )

    while score_list and iterations < 100:
        iterations += 1
        s, score = score_list.pop(0)
        # Se implicação, uso modus ponens e tollens
        if isinstance(s, Implication):
            mp = ModusPonens(s)
            if mp.evaluate(symhash):
                path.append(mp)
                process_sentence(mp.conclusion)
                score_list = update_scores()
            mt = ModusTollens(s)
            if mt.evaluate(symhash):
                path.append(mt)
                process_sentence(mt.conclusion)
                score_list = update_scores()

            # Se nao for possivel avaliar ainda,
            # tento aplicar Silogismo Hipotético
            if mp.evaluate(symhash) is None and mt.evaluate(symhash) is None:
                # Silogismo Hipotetico
                for t, _ in score_list:
                    if isinstance(t, Implication):
                        if t.antecedent == s.consequent:
                            hs = HipoteticalSyllogism(s, t)
                            path.append(hs)
                            process_sentence(hs.apply())
                            score_list = update_scores()
                            break
                # se nao funcionar, volto a lista de regras
                else:
                    if not score_list:
                        break
                    score_list.append((s, score))

        # Se disjunção, aplico silogismo a esquerda e a direita
        elif isinstance(s, Or):
            ls = DisjunctiveSyllogism(s)
            if ls.evaluate(symhash):
                path.append(ls)
                process_sentence(ls.conclusion)
                score_list = update_scores()

            rs = DisjunctiveSyllogism(s, right=True)
            if rs.evaluate(symhash):
                path.append(rs)
                process_sentence(rs.conclusion)
                score_list = update_scores()

            # Se nao for possivel avaliar ainda, retorno regra a lista de regras
            if ls.evaluate(symhash) is None and rs.evaluate(symhash) is None:
                score_list.append((s, score))
        else:
            break

        querying = query.evaluate(symhash)
        if querying is True:
            finded = True
            break
        elif querying is False:
            finded = False
            break

    return finded, path
