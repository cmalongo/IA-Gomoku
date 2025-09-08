import numpy as np
TAILLE_PLATEAU = 15
VIDE = 0
NOIR = 1
BLANC = 2
#bababababaababababah

# Indicateur pour gérer le premier coup noir
premier_coup_noir = True  # Variable globale pour restreindre le premier coup noir
deuxieme_coup_noir = False # Variable globale pour restreindre le deuxième coup noir

def init_plateau():
    """Initialise le plateau de jeu."""
    plateau = np.zeros((TAILLE_PLATEAU, TAILLE_PLATEAU), dtype=int)
    # Le premier coup est forcé au centre
    plateau[7][7] = NOIR
    return plateau

def afficher_plateau(plateau):
    """Affiche le plateau en mode texte, numéroté de 0 à 14, avec un alignement précis."""
    lettres = "ABCDEFGHIJKLMNO"
    print("  " + " ".join([str(i) for i in range(TAILLE_PLATEAU)]))  # Colonnes alignées
    for i, ligne in enumerate(plateau):
        print(lettres[i], " ".join(['.' if cell == VIDE else 'X' if cell == NOIR else 'O' for cell in ligne]))



def coup_valide(plateau, ligne, colonne, joueur):
    """Vérifie si un coup est valide, avec restriction pour le premier coup noir."""
    global premier_coup_noir  # Utilisation pour restreindre uniquement le premier coup noir
    if not (0 <= ligne < TAILLE_PLATEAU and 0 <= colonne < TAILLE_PLATEAU):
        return False
    if plateau[ligne, colonne] != VIDE:
        return False
    if joueur == NOIR and premier_coup_noir:
        # Restriction spécifique : le coup doit être en dehors du carré central 7x7
        if 4 <= ligne <= 10 and 4 <= colonne <= 10:
            return False
    return True

def detecter_alignement_4_adverse(plateau, joueur):
    """Détecte un alignement de 4 jetons adverses prêts à gagner."""
    adversaire = NOIR if joueur == BLANC else BLANC
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for ligne in range(TAILLE_PLATEAU):
        for colonne in range(TAILLE_PLATEAU):
            for dl, dc in directions:
                # Vérifie la séquence dans la direction normale
                cases = [(ligne + step * dl, colonne + step * dc) for step in range(4)]
                suivant = (ligne + 4 * dl, colonne + 4 * dc)

                if all(0 <= nl < TAILLE_PLATEAU and 0 <= nc < TAILLE_PLATEAU for nl, nc in cases + [suivant]):
                    valeurs = [plateau[nl, nc] for nl, nc in cases]
                    # Cas : 4 pions adverses + 1 espace
                    if valeurs.count(adversaire) == 4 and plateau[suivant] == VIDE:
                        return suivant

                # Vérifie la séquence inversée (1 espace + 4 pions adverses)
                precedent = (ligne - dl, colonne - dc)
                if all(0 <= nl < TAILLE_PLATEAU and 0 <= nc < TAILLE_PLATEAU for nl, nc in cases + [precedent]):
                    valeurs = [plateau[nl, nc] for nl, nc in cases]
                    # Cas : 1 espace + 4 pions adverses
                    if valeurs.count(adversaire) == 4 and plateau[precedent] == VIDE:
                        return precedent

    return None

def verifier_alignement(plateau, joueur):
    """Vérifie si un joueur a gagné en alignant 5 pions."""
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for ligne in range(TAILLE_PLATEAU):
        for colonne in range(TAILLE_PLATEAU):
            if plateau[ligne, colonne] == joueur:
                for d in directions:
                    count = 1
                    for step in range(1, 5):
                        nl, nc = ligne + step * d[0], colonne + step * d[1]
                        if 0 <= nl < TAILLE_PLATEAU and 0 <= nc < TAILLE_PLATEAU and plateau[nl, nc] == joueur:
                            count += 1
                        else:
                            break
                    if count == 5:
                        return True
    return False

def detecter_alignement_adverse(plateau, joueur):
    """Détecte un alignement de 3 jetons adverses pour le blocage, même avec un espace."""
    adversaire = NOIR if joueur == BLANC else BLANC
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Vertical, horizontal, diagonales
    for ligne in range(TAILLE_PLATEAU):
        for colonne in range(TAILLE_PLATEAU):
            if plateau[ligne, colonne] == adversaire:
                for d in directions:
                    # Vérifie les deux cas : alignement direct ou avec un espace
                    if alignement_3_avec_espace(plateau, ligne, colonne, d, adversaire):
                        return alignement_3_avec_espace(plateau, ligne, colonne, d, adversaire)
    return None

def alignement_3_avec_espace(plateau, ligne, colonne, direction, adversaire):
    """Vérifie s'il y a un alignement de 3 adverses avec un espace et retourne la position du blocage."""
    dl, dc = direction
    cases = []

    # Collecte les positions des 4 cases potentiellement alignées
    for step in range(4):
        nl, nc = ligne + step * dl, colonne + step * dc
        if 0 <= nl < TAILLE_PLATEAU and 0 <= nc < TAILLE_PLATEAU:
            cases.append((nl, nc))
        else:
            break

    if len(cases) == 4:
        valeurs = [plateau[nl, nc] for nl, nc in cases]

        # Cas 1 : Trois adversaires consécutifs avec une case vide au début ou à la fin
        if valeurs[:3] == [adversaire, adversaire, adversaire] and valeurs[3] == VIDE:
            return cases[3]
        if valeurs[1:] == [adversaire, adversaire, adversaire] and valeurs[0] == VIDE:
            return cases[0]

        # Cas 2 : Deux adversaires avec une case vide entre eux
        if valeurs[0] == adversaire and valeurs[1] == VIDE and valeurs[2] == adversaire and valeurs[3] == adversaire:
            return cases[1]
        if valeurs[0] == adversaire and valeurs[1] == adversaire and valeurs[2] == VIDE and valeurs[3] == adversaire:
            return cases[2]

    return None

def evaluer_plateau(plateau, joueur):
    """Retourne une évaluation heuristique du plateau."""
    adversaire = NOIR if joueur == BLANC else BLANC
    score_joueur = compter_alignements(plateau, joueur)
    score_adversaire = compter_alignements(plateau, adversaire)

    # L'évaluation globale combine alignements et proximité
    return score_joueur - score_adversaire


def compter_alignements(plateau, joueur):
    """Compte les alignements pour un joueur."""
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    score = 0
    for ligne in range(TAILLE_PLATEAU):
        for colonne in range(TAILLE_PLATEAU):
            if plateau[ligne, colonne] == joueur:
                for d in directions:
                    count = 0
                    for step in range(5):
                        nl, nc = ligne + step * d[0], colonne + step * d[1]
                        if 0 <= nl < TAILLE_PLATEAU and 0 <= nc < TAILLE_PLATEAU and plateau[nl, nc] == joueur:
                            count += 1
                        else:
                            break
                    if count == 5:
                        score += 10000  # Victoire garantie
                    elif count == 4:
                        score += 1000  # Menace majeure
                    elif count == 3:
                        score += 10   # Alignement utile
    return score

def generer_coups(plateau, joueur):
    """Génère une liste de coups possibles autour des pions existants, avec restriction pour le premier coup noir."""
    global premier_coup_noir
    coups = set()
    for ligne in range(TAILLE_PLATEAU):
        for colonne in range(TAILLE_PLATEAU):
            if plateau[ligne, colonne] != VIDE:
                for dl in range(-2, 3):
                    for dc in range(-2, 3):
                        nl, nc = ligne + dl, colonne + dc
                        # Vérifie si le coup est valide en fonction des règles
                        if coup_valide(plateau, nl, nc, joueur):
                            # Restriction pour le premier coup noir
                            if joueur == NOIR and premier_coup_noir:
                                if 5 <= nl <= 11 and 5 <= nc <= 11:  # Exclut le carré de taille 7
                                    continue
                            coups.add((nl, nc))
    return list(coups)


def minimax(plateau, profondeur, alpha, beta, maximisant, joueur, cache):
    """Implémente le minimax avec élagage alpha-bêta et cache."""
    adversaire = NOIR if joueur == BLANC else BLANC
    plateau_tuple = tuple(map(tuple, plateau))
    if plateau_tuple in cache:
        return cache[plateau_tuple]

    if profondeur == 0 or verifier_alignement(plateau, NOIR) or verifier_alignement(plateau, BLANC):
        score = evaluer_plateau(plateau, joueur)
        cache[plateau_tuple] = (score, None)
        return score, None

    meilleur_coup = None
    coups = generer_coups(plateau,joueur)
    if maximisant:
        max_eval = -float('inf')
        for (ligne, colonne) in coups:
            plateau[ligne, colonne] = joueur
            evaluation, _ = minimax(plateau, profondeur - 1, alpha, beta, False, joueur, cache)
            plateau[ligne, colonne] = VIDE
            if evaluation > max_eval:
                max_eval = evaluation
                meilleur_coup = (ligne, colonne)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        cache[plateau_tuple] = (max_eval, meilleur_coup)
        return max_eval, meilleur_coup
    else:
        min_eval = float('inf')
        for (ligne, colonne) in coups:
            plateau[ligne, colonne] = adversaire
            evaluation, _ = minimax(plateau, profondeur - 1, alpha, beta, True, joueur, cache)
            plateau[ligne, colonne] = VIDE
            if evaluation < min_eval:
                min_eval = evaluation
                meilleur_coup = (ligne, colonne)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        cache[plateau_tuple] = (min_eval, meilleur_coup)
        return min_eval, meilleur_coup

def alignement_4_pret_a_gagner(plateau, joueur):
    """Vérifie si le joueur a 4 jetons alignés avec une case vide pour compléter un alignement."""
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Vertical, horizontal, diagonales
    for ligne in range(TAILLE_PLATEAU):
        for colonne in range(TAILLE_PLATEAU):
            if plateau[ligne, colonne] == joueur:
                for d in directions:
                    dl, dc = d
                    cases = []
                    for step in range(5):  # Vérifie les 5 cases possibles dans cette direction
                        nl, nc = ligne + step * dl, colonne + step * dc
                        if 0 <= nl < TAILLE_PLATEAU and 0 <= nc < TAILLE_PLATEAU:
                            cases.append((nl, nc))
                        else:
                            break
                    if len(cases) == 5:
                        valeurs = [plateau[nl, nc] for nl, nc in cases]
                        # Vérifie s'il y a exactement 4 jetons et une case vide
                        if valeurs.count(joueur) == 4 and valeurs.count(VIDE) == 1:
                            return cases[valeurs.index(VIDE)]
    return None

def attaque(plateau, joueur):
    """Détecte un alignement de 3 jetons avec 2 espaces vides sur 5 cases."""
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for ligne in range(TAILLE_PLATEAU):
        for colonne in range(TAILLE_PLATEAU):
            for dl, dc in directions:
                cases = [(ligne + step * dl, colonne + step * dc) for step in range(5)]

                if all(0 <= nl < TAILLE_PLATEAU and 0 <= nc < TAILLE_PLATEAU for nl, nc in cases):
                    valeurs = [plateau[nl, nc] for nl, nc in cases]
                    # Condition : 3 pions IA + 2 espaces vides
                    if valeurs.count(joueur) == 3 and valeurs.count(VIDE) == 2:
                        return cases[valeurs.index(VIDE)]
    return None

def creer_menace_de_4(plateau, joueur):
    """Cherche à créer une double menace de 4 (deux alignements potentiels)."""
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Vertical, horizontal, diagonales
    menaces = []

    for ligne in range(TAILLE_PLATEAU):
        for colonne in range(TAILLE_PLATEAU):
            if plateau[ligne, colonne] == joueur:
                for d in directions:
                    dl, dc = d
                    cases = []
                    for step in range(4):  # Vérifie les 4 cases possibles dans cette direction
                        nl, nc = ligne + step * dl, colonne + step * dc
                        if 0 <= nl < TAILLE_PLATEAU and 0 <= nc < TAILLE_PLATEAU:
                            cases.append((nl, nc))
                        else:
                            break
                    if len(cases) == 4:
                        valeurs = [plateau[nl, nc] for nl, nc in cases]
                        # Vérifie 3 jetons alignés et 1 case vide aux extrémités
                        if valeurs.count(joueur) == 3 and valeurs.count(VIDE) == 1:
                            # Vérifie les extrémités pour une double menace
                            ext1 = (cases[0][0] - dl, cases[0][1] - dc)
                            ext2 = (cases[-1][0] + dl, cases[-1][1] + dc)
                            if (
                                0 <= ext1[0] < TAILLE_PLATEAU and 0 <= ext1[1] < TAILLE_PLATEAU
                                and plateau[ext1[0], ext1[1]] == VIDE
                                and 0 <= ext2[0] < TAILLE_PLATEAU and 0 <= ext2[1] < TAILLE_PLATEAU
                                and plateau[ext2[0], ext2[1]] == VIDE
                            ):
                                menaces.append(ext1)
                                menaces.append(ext2)

    # Priorise une double menace
    if len(menaces) >= 2:
        return menaces[0]  # Retourne l'une des positions menaçantes
    return None

def choisir_coup(plateau, joueur):
    """Choisit le meilleur coup pour l'IA, incluant des menaces de 4."""
    global premier_coup_noir
    global deuxieme_coup_noir

    if joueur == NOIR and deuxieme_coup_noir:
        deuxieme_coup_noir = False  # Marque que le premier coup a été joué
        return 7, 10  # Correspond à H10 (ligne 7, colonne 11 dans l'index 0-based)

    # Si c'est le premier coup des noirs, forcer H12
    if joueur == NOIR and premier_coup_noir:
        premier_coup_noir = False  # Marque que le premier coup a été joué
        deuxieme_coup_noir = True
        return 7, 11  # Correspond à H11 (ligne 7, colonne 12 dans l'index 0-based)

    # Vérifie si l'IA peut aligner un cinquième jeton pour gagner
    alignement_gagnant = alignement_4_pret_a_gagner(plateau, joueur)
    if alignement_gagnant:
        return alignement_gagnant

    # Bloquer en priorité un alignement de 4 de l'adversaire
    blocage_4 = detecter_alignement_4_adverse(plateau, joueur)
    if blocage_4:
        return blocage_4

    # Vérifie s'il y a un alignement adverse à bloquer
    if not attaque(plateau, joueur):  # Attaque prioritaire si 3 jetons alignés
      blocage = detecter_alignement_adverse(plateau, joueur)
      if blocage:
        return blocage

    # Vérifie si l'IA peut créer une menace de 4 (double ouverture)
    menace_4 = creer_menace_de_4(plateau, joueur)
    if menace_4:
        return menace_4


    # Utilise le minimax pour déterminer le meilleur coup
    cache = {}
    _, coup = minimax(plateau, 3, -float('inf'), float('inf'), True, joueur, cache)

    if coup is None:
        print("Erreur : Aucun coup valide trouvé pour l'IA.")
        return None

    return coup



def jouer_tour(plateau, joueur, ia_actif):
    """Gère le tour d’un joueur."""
    global premier_coup_noir
    global deuxieme_coup_noir
    if ia_actif:
        print(f"Tour de l'IA ({'Noir' if joueur == NOIR else 'Blanc'})")

        # Si l'IA joue Noir pour la deuxième fois, vérifier H10 et H4
        if joueur == NOIR and deuxieme_coup_noir == True and premier_coup_noir == False:
            # Vérifier si H11 (ligne 7, colonne 10) est vide
            if plateau[7, 10] == VIDE:
                ligne, colonne = 7, 10  # H10
                deuxieme_coup_noir = False
            # Si H11 n'est pas vide, jouer H3 (ligne 3, colonne 7)
            elif plateau[7,4] == VIDE:
                ligne, colonne = 7, 4  # H2
                deuxieme_coup_noir = False
            else:
                # Si ni H10 ni H4 ne sont vides, continuer avec l'IA normale
                ligne, colonne = choisir_coup(plateau, joueur)

        # Si l'IA joue Noir pour la première fois, vérifier H11 et H3
        elif joueur == NOIR and premier_coup_noir:
            # Vérifier si H11 (ligne 7, colonne 11) est vide
            if plateau[7, 11] == VIDE:
                ligne, colonne = 7, 11  # H11
                premier_coup_noir = False
                deuxieme_coup_noir = True
            elif plateau[7,3] == VIDE:
                ligne, colonne = 7, 3  # H3
                premier_coup_noir = False
                deuxieme_coup_noir = True
            else:
                # Si ni H11 ni H3 ne sont vides, continuer avec l'IA normale
                ligne, colonne = choisir_coup(plateau, joueur)
        else:
          ligne, colonne = choisir_coup(plateau, joueur)
    else:
        while True:
            coup = input("Entrez votre coup (ex: H0, H12): ").strip().upper()
            if len(coup) >= 2 and coup[0] in "ABCDEFGHIJKLMNO" and coup[1:].isdigit():
                ligne = "ABCDEFGHIJKLMNO".index(coup[0])
                colonne = int(coup[1:])  # Retirer le "-1" pour accepter "0" comme index
                if 0 <= colonne < TAILLE_PLATEAU:  # Vérifier que la colonne est bien dans les limites
                    if coup_valide(plateau, ligne, colonne, joueur):
                        break
                    else:
                        print("Coup invalide !")
                else:
                    print("Colonne hors limites (doit être entre 0 et 14).")
            else:
                print("Format invalide ! Veuillez entrer une lettre (A-O) suivie d'un chiffre (0-14).")

    plateau[ligne, colonne] = joueur

    # Marquer le premier coup noir comme terminé
    if joueur == NOIR and premier_coup_noir:
        premier_coup_noir = False

    afficher_plateau(plateau)
    return verifier_alignement(plateau, joueur)




def partie():
    """Lance une partie complète."""
    plateau = init_plateau()
    afficher_plateau(plateau)

    while True:
        choix = input("Voulez-vous jouer Noir (N) ou Blanc (B) ? ").strip().upper()
        if choix in ['N', 'B']:
            joueur_humain = choix == 'N'
            break
        else:
            print("Entrée invalide ! Veuillez choisir 'N' pour Noir ou 'B' pour Blanc.")

    joueur_actuel = BLANC  # Le premier joueur est toujours blanc

    while True:
        ia_actif = (joueur_actuel == NOIR and not joueur_humain) or (joueur_actuel == BLANC and joueur_humain)
        if jouer_tour(plateau, joueur_actuel, ia_actif):
            print(f"{'Noir' if joueur_actuel == NOIR else 'Blanc'} gagne !")
            break
        if np.all(plateau != VIDE):
            print("Match nul !")
            break
        joueur_actuel = NOIR if joueur_actuel == BLANC else BLANC

if __name__ == "__main__":
    partie()
