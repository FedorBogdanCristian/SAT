def find_unit_clause(clauses):
    """
    Găsește clauza unitate din mulțimea de clauze (dacă există).
    Returnează literalul din clauza unitate sau None dacă nu există.
    """
    for clause in clauses:
        if len(clause) == 1:
            return clause[0]
    return None

def find_pure_literal(clauses):
    """
    Găsește un literal pur în mulțimea de clauze (dacă există).
    Un literal este pur dacă apare cu o singură polaritate în toate clauzele.
    """
    all_literals = []
    for clause in clauses:
        all_literals.extend(clause)
    
    literals = set(abs(lit) for lit in all_literals)
    
    for lit in literals:
        positive_exists = lit in all_literals
        negative_exists = -lit in all_literals
        
        if positive_exists and not negative_exists:
            return lit
        if negative_exists and not positive_exists:
            return -lit
    
    return None

def simplify_clauses(clauses, literal):
    """
    Simplifică mulțimea de clauze eliminând clauzele satisfăcute de literal
    și eliminând -literal din celelalte clauze.
    """
    new_clauses = []
    for clause in clauses:
        # Dacă literal este în clauză, clauza devine adevărată și o eliminăm
        if literal in clause:
            continue
        
        # Dacă negația literalului este în clauză, o eliminăm din clauză
        if -literal in clause:
            new_clause = [lit for lit in clause if lit != -literal]
            if not new_clause:  # Dacă clauza devine vidă, formula nu este satisfiabilă
                return None
            new_clauses.append(new_clause)
        else:
            new_clauses.append(clause)
    
    return new_clauses

def choose_variable(clauses):
    """
    Alege o variabilă pentru divizare.
    Strategie simplă: ia prima variabilă din prima clauză.
    În implementările avansate, aici s-ar putea folosi euristici precum VSIDS, JW, etc.
    """
    all_vars = set()
    for clause in clauses:
        for lit in clause:
            all_vars.add(abs(lit))
    
    if all_vars:
        return min(all_vars)  # Returnează variabila cu cel mai mic indice
    return None

def dpll(clauses, assignment=None):
    """
    Algoritmul DPLL pentru verificarea satisfiabilității.
    Returnează un model (asignare de valori) dacă formula este satisfiabilă, None în caz contrar.
    """
    if assignment is None:
        assignment = {}
    
    # Dacă nu mai sunt clauze, formula este satisfiabilă
    if not clauses:
        return assignment
    
    # Dacă există o clauză vidă, formula nu este satisfiabilă pe această ramură
    if [] in clauses:
        return None
    
    # Aplică regula clauzei unitate
    unit_literal = find_unit_clause(clauses)
    if unit_literal:
        var = abs(unit_literal)
        value = unit_literal > 0
        assignment[var] = value
        new_clauses = simplify_clauses(clauses, unit_literal)
        if new_clauses is None:
            return None
        return dpll(new_clauses, assignment)
    
    # Aplică regula literalului pur
    pure_literal = find_pure_literal(clauses)
    if pure_literal:
        var = abs(pure_literal)
        value = pure_literal > 0
        assignment[var] = value
        new_clauses = simplify_clauses(clauses, pure_literal)
        if new_clauses is None:
            return None
        return dpll(new_clauses, assignment)
    
    # Alege o variabilă pentru divizare
    var = choose_variable(clauses)
    if var is None:
        return assignment  # Toate variabilele sunt atribuite, formula este satisfiabilă
    
    # Încearcă cu valoarea True
    assignment_copy = assignment.copy()
    assignment_copy[var] = True
    new_clauses = simplify_clauses(clauses, var)
    if new_clauses is not None:
        result = dpll(new_clauses, assignment_copy)
        if result is not None:
            return result
    
    # Încearcă cu valoarea False
    assignment_copy = assignment.copy()
    assignment_copy[var] = False
    new_clauses = simplify_clauses(clauses, -var)
    if new_clauses is not None:
        result = dpll(new_clauses, assignment_copy)
        if result is not None:
            return result
    
    # Nicio asignare nu duce la o soluție
    return None

def solve_dpll(cnf_formula):
    """
    Rezolvă problema SAT folosind algoritmul DPLL.
    
    Args:
        cnf_formula: O formulă în forma normală conjunctivă reprezentată ca o listă de clauze,
                    unde fiecare clauză este o listă de literali (numere întregi).
                    Un literal pozitiv x este reprezentat ca x, iar negația sa ca -x.
    
    Returns:
        Un dicționar cu asignarea variabilelor dacă formula este satisfiabilă, None altfel.
    """
    return dpll(cnf_formula)

def is_satisfiable_dpll(cnf_formula):
    """
    Verifică dacă o formulă CNF este satisfiabilă folosind DPLL.
    
    Returns:
        True dacă formula este satisfiabilă, False altfel.
    """
    result = solve_dpll(cnf_formula)
    return result is not None

# Exemplu de utilizare
if __name__ == "__main__":
    # Exemplu de formulă CNF: (a ∨ b) ∧ (¬a ∨ c) ∧ (¬b ∨ ¬c)
    # Reprezentată ca: [[1, 2], [-1, 3], [-2, -3]]
    cnf_example = [[1, 2], [-1, 3], [-2, -3]]
    result = solve_dpll(cnf_example)
    if result:
        print(f"Formula este satisfiabilă cu asignarea: {result}")
    else:
        print("Formula nu este satisfiabilă")
    
    # Exemplu de formulă nesatisfiabilă: (a) ∧ (¬a)
    # Reprezentată ca: [[1], [-1]]
    unsat_example = [[1], [-1]]
    result = solve_dpll(unsat_example)
    if result:
        print(f"Formula este satisfiabilă cu asignarea: {result}")
    else:
        print("Formula nu este satisfiabilă")