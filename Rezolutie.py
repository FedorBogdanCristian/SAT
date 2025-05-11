def resolution_step(clauses):
    """
    Execută un pas de rezoluție, încercând să rezolve toate perechile de clauze posibile.
    Returnează noile clauze generate în acest pas.
    """
    new_clauses = []
    
    # Pentru fiecare pereche de clauze
    for i in range(len(clauses)):
        for j in range(i + 1, len(clauses)):
            # Găsim literalii complementari
            for lit in clauses[i]:
                if -lit in clauses[j]:
                    # Generăm clauza rezolvată
                    resolvent = [x for x in clauses[i] if x != lit] + [x for x in clauses[j] if x != -lit]
                    # Eliminăm duplicatele
                    resolvent = list(set(resolvent))
                    
                    # Verificăm dacă rezolventa conține un literal și negația sa (tautologie)
                    is_tautology = False
                    for lit in resolvent:
                        if -lit in resolvent:
                            is_tautology = True
                            break
                    
                    # Adăugăm rezolventa la noile clauze dacă nu este o tautologie și nu există deja
                    if not is_tautology and resolvent not in new_clauses and resolvent not in clauses:
                        new_clauses.append(resolvent)
    
    return new_clauses

def resolution(cnf_formula):
    """
    Aplică algoritmul Rezoluției pentru a verifica satisfiabilitatea formulei.
    
    Args:
        cnf_formula: O formulă în forma normală conjunctivă reprezentată ca o listă de clauze,
                    unde fiecare clauză este o listă de literali (numere întregi).
                    Un literal pozitiv x este reprezentat ca x, iar negația sa ca -x.
    
    Returns:
        True dacă formula este satisfiabilă, False dacă nesatisfiabilă.
    """
    # Inițializăm mulțimea de clauze cu formula inițială
    clauses = [sorted(list(set(clause))) for clause in cnf_formula]
    
    # Eliminăm clauzele care sunt tautologii
    clauses = [clause for clause in clauses if not any(lit in clause and -lit in clause for lit in clause)]
    
    # Algoritmul se oprește când nu mai putem genera noi clauze sau găsim clauza vidă
    while True:
        new_clauses = resolution_step(clauses)
        
        # Dacă am generat clauza vidă, formula este nesatisfiabilă
        if [] in new_clauses:
            return False
        
        # Dacă nu am generat nicio clauză nouă, formula este satisfiabilă
        if not new_clauses or all(clause in clauses for clause in new_clauses):
            return True
        
        # Adăugăm noile clauze la mulțimea existentă
        for clause in new_clauses:
            if clause not in clauses:
                clauses.append(clause)

def solve_resolution(cnf_formula):
    """
    Rezolvă problema SAT folosind algoritmul Rezoluției.
    
    Args:
        cnf_formula: O formulă în forma normală conjunctivă reprezentată ca o listă de clauze,
                    unde fiecare clauză este o listă de literali (numere întregi).
                    Un literal pozitiv x este reprezentat ca x, iar negația sa ca -x.
    
    Returns:
        True dacă formula este satisfiabilă, False dacă nesatisfiabilă.
    """
    return resolution(cnf_formula)

# Funcție auxiliară pentru a converti o formulă la forma normală negată (pentru rezoluție)
def negate_formula(cnf_formula):
    """
    Negează o formulă CNF pentru a o putea folosi în algoritmul rezoluției.
    
    Pentru a nega (A ∧ B ∧ C), obținem (¬A ∨ ¬B ∨ ¬C), unde A, B, C sunt clauze.
    În practică, aceasta înseamnă că vom aplica negarea fiecărei clauze și vom crea o clauză nouă pentru fiecare literal.
    """
    negated_clauses = []
    
    # Pentru fiecare clauză din formula originală
    for clause in cnf_formula:
        # Negăm fiecare literal din clauză
        negated_literals = [-lit for lit in clause]
        
        # Fiecare literal negat devine o clauză separată
        for lit in negated_literals:
            negated_clauses.append([lit])
    
    return negated_clauses

# Exemplu de utilizare
if __name__ == "__main__":
    # Exemplu de formulă CNF: (a ∨ b) ∧ (¬a ∨ c) ∧ (¬b ∨ ¬c)
    # Reprezentată ca: [[1, 2], [-1, 3], [-2, -3]]
    cnf_example = [[1, 2], [-1, 3], [-2, -3]]
    result = solve_resolution(cnf_example)
    print(f"Formula este {'satisfiabilă' if result else 'nesatisfiabilă'}")
    
    # Exemplu de formulă nesatisfiabilă: (a) ∧ (¬a)
    # Reprezentată ca: [[1], [-1]]
    unsat_example = [[1], [-1]]
    result = solve_resolution(unsat_example)
    print(f"Formula este {'satisfiabilă' if result else 'nesatisfiabilă'}")