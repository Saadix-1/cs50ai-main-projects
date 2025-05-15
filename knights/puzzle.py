from logic import *

# Define symbols for each person's possible roles
AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says: "I am both a knight and a knave."
knowledge0 = And(
    # A can only be one: a knight or a knave, not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # If A is a knight, then the statement must be true (which is a contradiction)
    Implication(AKnight, And(AKnight, AKnave)),

    # If A is a knave, then the statement is false (which is consistent)
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says: "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Basic assumptions: each person is either a knight or a knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # If A is a knight, then the statement is true → both are knaves
    Implication(AKnight, And(AKnave, BKnave)),

    # If A is a knave, the statement is false → not both are knaves
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says: "We are the same kind."
# B says: "We are of different kinds."
same_type = Or(And(AKnight, BKnight), And(AKnave, BKnave))
different_type = Or(And(AKnight, BKnave), And(AKnave, BKnight))

knowledge2 = And(
    # Each person is either a knight or a knave, not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # If A is a knight, then they are the same type
    Implication(AKnight, same_type),
    # If A is a knave, then the statement is false → they are different
    Implication(AKnave, Not(same_type)),

    # If B is a knight, then they are different types
    Implication(BKnight, different_type),
    # If B is a knave, then they are not different → same type
    Implication(BKnave, Not(different_type))
)

# Puzzle 3
# A says either: "I am a knight." or "I am a knave." (but we don't know which)
# B says: "A said 'I am a knave'" and also "C is a knave"
# C says: "A is a knight"
knowledge3 = And(
    # Basic constraints
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # If B is telling the truth, then A said "I am a knave."
    # If A is a knight, saying "I am a knave" would be false → contradiction
    # So we encode what it would mean if A had said "I am a knave"
    Implication(BKnight, And(
        Implication(AKnight, AKnave),
        Implication(AKnave, Not(AKnave))
    )),

    # If B is lying, then A did not say "I am a knave"
    Implication(BKnave, Not(And(
        Implication(AKnight, AKnave),
        Implication(AKnave, Not(AKnave))
    ))),

    # B says: "C is a knave"
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),

    # C says: "A is a knight"
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
