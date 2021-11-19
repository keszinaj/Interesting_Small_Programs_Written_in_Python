#made by keszinaj
''' 
    Simple well-formed formula checker
    How to use it?(p, q - formula or variable)
    Or(p, q) - or 
    And(p, q) - and
    Neg(p) - neg 
    Conditional(p, q) - => 
    Eq(p, q) <=> 
    Variable(p) define propositional variable
    LogicalValue(True/False)
    (formula).calculate(variables_value_dict) to solve formula
    (formula).isTautology(env) to check if formula is Tautology
    More complex formulas are created by composition.
'''
from logical_operators import And , Neg, Or, Conditional, Eq, Variable, LogicalValue

'''
    Tests
'''
#variables
p = Variable("p")
q = Variable("q")
r = Variable("r")

# test calculation
val_1 = Or(p, Or(Neg(p), Eq(p, r)))
print(str(val_1) + " let p be False and r be True: " + str(val_1.calculate({"p": False, "r": True})))
val_2 = Conditional(p, Conditional(Neg(p), Eq(p, r)))
print(str(val_2) + " let p be False and r be False: " + str(val_2.calculate({"p": False, "r": False})))
val_3 = val_1 + val_2 * val_1
print(str(val_3))

#testy simplify foo: 
simplify_1 = Or(And(p, Neg(p)), p).simplify(["p"])
print(str(simplify_1))
simplify_2 = And(LogicalValue(False), p).simplify(["p"])
print(str(simplify_2))

#tautology test
#prawo wyłaczonego rodka
tautology_1 = Or(p, Neg(p))
print(str(tautology_1) + " is tautology: " + str(tautology_1.isTautology(["p"])))

#drugie prawo definiowania implikacji
tautology_2 = Eq(Conditional(p, q), Neg(And(p, Neg(q))))
print(str(tautology_2) + " is tautology: " + str(tautology_2.isTautology(["p", "q"])))

#drugie prawo ekstensjonalnoci
tautology_3 = Conditional(Eq(p, q), Eq(Or(p, r), Or(q, r)))
print(str(tautology_3) + " is tautology: " + str(tautology_3.isTautology(["p", "q", "r"])))

# prawo rozdzielania nastpnika
tautology_4  = Conditional(Conditional(p, And(q,r)), And(Conditional(p, q), Conditional(p, r)))
print(str(tautology_4) + " is tautology: " + str(tautology_3.isTautology(["p", "q", "r"])))

not_tautology_1 = And(p, Neg(p))
print(str(not_tautology_1) + " is tautology: " + str(not_tautology_1.isTautology(["p"])))

not_tautology_2 = Or(And(p, And(p, q)), p)
print(str(not_tautology_2) + " is tautology: " + str(not_tautology_2.isTautology(["p", "q"])))

not_tautology_3 = Conditional(Eq(p, q), Eq(Or(p, r), And(Eq(q, p), r)))
print(str(not_tautology_3) + " is tautology: " + str(not_tautology_3.isTautology(["p", "q", "r"])))

not_tautology_4 = And(Conditional(p, Or(q,r)), Eq(Conditional(p, q), Conditional(p, r)))
print(str(not_tautology_4) + " is tautology: " + str(not_tautology_4.isTautology(["p", "q", "r"])))
