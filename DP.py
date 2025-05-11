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
    Alege o variabilă pentru eliminare.
    Strategie simplă: ia primul literal din prima clauză.
    """
    if not clauses:
        return None
    if not clauses[0]:
        return None
    return abs(clauses[0][0])

def dp_resolution(clauses, var):
    """
    Aplică eliminarea prin rezoluție a unei variabile.
    """
    result_clauses = []
    clauses_with_pos = [c for c in clauses if var in c]
    clauses_with_neg = [c for c in clauses if -var in c]
    clauses_without_var = [c for c in clauses if var not in c and -var not in c]
    
    # Aplicăm rezoluția între toate perechile posibile de clauze
    for pos_clause in clauses_with_pos:
        for neg_clause in clauses_with_neg:
            # Creăm clauza de rezolvare
            resolvent = [lit for lit in pos_clause if lit != var] + [lit for lit in neg_clause if lit != -var]
            # Eliminăm duplicatele
            resolvent = list(set(resolvent))
            
            # Verificăm dacă rezolventa conține un literal și negația sa (tauto)
            is_tautology = False
            for lit in resolvent:
                if -lit in resolvent:
                    is_tautology = True
                    break
            
            if not is_tautology and resolvent not in result_clauses:
                result_clauses.append(resolvent)
    
    # Adăugăm clauzele care nu conțin variabila
    result_clauses.extend(clauses_without_var)
    
    return result_clauses

def dp_sat(clauses):
    """
    Algoritmul Davis-Putnam pentru verificarea satisfiabilității.
    Returnează True dacă formula este satisfiabilă, False în caz contrar.
    """
    # Dacă nu mai sunt clauze, formula este satisfiabilă
    if not clauses:
        return True
    
    # Dacă există o clauză vidă, formula nu este satisfiabilă
    if [] in clauses:
        return False
    
    # Aplică regula clauzei unitate
    unit_literal = find_unit_clause(clauses)
    if unit_literal:
        new_clauses = simplify_clauses(clauses, unit_literal)
        if new_clauses is None:
            return False
        return dp_sat(new_clauses)
    
    # Aplică regula literalului pur
    pure_literal = find_pure_literal(clauses)
    if pure_literal:
        new_clauses = simplify_clauses(clauses, pure_literal)
        if new_clauses is None:
            return False
        return dp_sat(new_clauses)
    
    # Alege o variabilă pentru eliminare prin rezoluție
    var = choose_variable(clauses)
    if var is None:
        return True  # Toate variabilele sunt eliminate, formula este satisfiabilă
    
    # Aplică eliminarea prin rezoluție
    new_clauses = dp_resolution(clauses, var)
    
    return dp_sat(new_clauses)

def solve_dp(cnf_formula):
    """
    Rezolvă problema SAT folosind algoritmul Davis-Putnam.
    
    Args:
        cnf_formula: O formulă în forma normală conjunctivă reprezentată ca o listă de clauze,
                    unde fiecare clauză este o listă de literali (numere întregi).
                    Un literal pozitiv x este reprezentat ca x, iar negația sa ca -x.
    
    Returns:
        True dacă formula este satisfiabilă, False altfel.
    """
    return dp_sat(cnf_formula)

# Exemplu de utilizare
if __name__ == "__main__":
    # Exemplu de formulă CNF: (a ∨ b) ∧ (¬a ∨ c) ∧ (¬b ∨ ¬c)
    # Reprezentată ca: [[1, 2], [-1, 3], [-2, -3]]
    cnf_example = [[1, 2], [-1, 3], [-2, -3]]
    result = solve_dp(cnf_example)
    print(f"Formula este {'satisfiabilă' if result else 'nesatisfiabilă'}")
    
    # Exemplu de formulă nesatisfiabilă: (a) ∧ (¬a)
    # Reprezentată ca: [[1], [-1]]
    unsat_example = [[1], [-1]]
    result = solve_dp(unsat_example)
    print(f"Formula este {'satisfiabilă' if result else 'nesatisfiabilă'}")