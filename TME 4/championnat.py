# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 09:31:28 2021

@author: GIANG Cécile
"""

############# PROGRAMMATION SAT - ORGANISATION D'UN CHAMPIONNAT ##############

import pycosat
import time


######################### EXERCICE 2 - MODELISATION ##########################

def codage(ne, nj, j, x, y):
    """ Retourne l'indice k de la variable propositionnelle vk correspondant.
        @param ne: int, nombre d'équipes participantes
        @param nj: int, nombre de jours de matchs maximum
        @param j: int, numéro du jour pour un match
        @param x: int, numéro de l'équipe à domicile
        @param y: int, numéro de l'équipe à l'extérieur
        @return k: int, indice de la variable vk correspondant
    """
    return j * ne**2 + x * ne + y + 1

def decodage(k, ne):
    """ Décode la valeur de l'indice k d'une variable vk et renvoie le jour j
        et les équipes x et y correspondant.
        @param k: int, indice de la variable vk
        @param ne: int, nombre d'équipes participantes
        @return j: int, numéro du jour du match
        @return x: int, numéro de l'équipe à domicile
        @return y: int, numéro de l'équipe à l'extérieur
    """
    j = ( k - 1 ) // ne**2
    x = ( ( k - 1 ) % ne**2 ) // ne
    y = ( k - 1 ) % ne
    return j, x, y


############## EXERCICE 3 - GENERATION D'UN PLANNING DE MATCHS ###############


# ----------------------  Contraintes de cardinalité ------------------------

def au_moins_un(vars):
    """ Renvoie une clause au format DIMACS traduisant la contrainte 'au moins
        une de ces variables est vraie'.
        @param vars: list(int), liste de variables
        @return clause: str, clause correspondant à la contrainte
    """
    return " " .join( str(i) for i in vars ) + " 0\n"

def au_plus_un(vars):
    """ Renvoie les clauses au format DIMACS traduisant la contrainte 'au plus
        une de ces variables est vraie' (encodage par paires).
        @param vars: list(int), liste de variables
        @return clause: str, clauses correspondant à la contrainte
    """
    clause = ""
    
    # Bouclage sur l'ensemble des couples de variables
    for i in range( len(vars) ):
        for j in range( i + 1, len(vars) ):
            clause += au_moins_un( [-vars[i], -vars[j]] )
            
    return clause


# ------------------------- Traduction du problème ---------------------------

def encoderC1(ne, nj):
    """ Contrainte 1: Chaque équipe ne peut jouer plus d'un match par jour.
        @param ne: int, nombre d'équipes participantes
        @param nj: int, nombre de jours de match maximum
        @return clause: str, clauses correspondant à la contrainte
    """
    clause = ""
    
    # Bouclage sur les équipes x et et les jours j
    for x in range(ne):
        for j in range(nj):
            # Liste des variables apparaissant dans la contrainte pour (x,j)
            vars = []
            for y in range(ne):
                if x != y:
                    vars.append(codage(ne, nj, j, x, y))
                    vars.append(codage(ne, nj, j, y, x))
            clause += au_plus_un(vars)
            
    return clause

def encoderC2(ne, nj):
    """ Contrainte 2: Sur le championnat, chaque équipe doit rencontrer l’
                      ensemble des autres équipes une fois exactement à
                      domicile et une fois exactement à l’extérieur.
        @param ne: int, nombre d'équipes participantes
        @param nj: int, nombre de jours de match maximum
        @return clause: str, clauses correspondant à la contrainte
    """
    clause = ""
    
    # Bouclage sur chaque paire d'équipes adverses (x,y)
    for x in range(ne):
        for y in range(ne):
            if x != y:
                # Liste des variables apparaissant dans la contrainte pour (x,y)
                vars = []
                for j in range(nj):
                    vars.append(codage(ne, nj, j, x, y))
                clause += au_plus_un(vars)
                clause += au_moins_un(vars)
    
    return clause

def encoder(ne, nj):
    """ Encode toutes les contraintes C1 et C2 pour ne et nj données.
        @param ne: int, nombre d'équipes participantes
        @param nj: int, nombre de jours de match maximum
        @return clause: str, clauses correspondant aux contraintes C1 et C2
    """
    clause = encoderC1(ne,nj) + encoderC2(ne,nj)
    nb_clauses = clause.count('\n')
    nb_vars = nj * ne**2
    
    return "p cnf {} {}\n".format(str(nb_vars),str(nb_clauses)) + clause

def genere_cnf(ne, nj):
    """ Génère un fichier cnf à partir de l'encodage avec ne et nj données.
        @param ne: int, nombre d'équipes participantes
        @param nj: int, nombre de jours de match maximum
    """
    with open('championnat.cnf', 'w') as file:
        file.write(encoder(ne,nj))

def to_cnf(filename):
    """ Lit un fichier cnf et renvoie une liste de sous listes, chaque sous-
        sous-liste correspondant à une clause.
        Exemple: [[1, -5, 4], [-1, 5, 3, 4], [-3, -4]]
        @param filename: str, nom du fichier .cnf
    """
    clause = []
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line[0] != 'c' and line[0] != 'p':
                if line.split()[:-1] != []:
                    clause.append([ int(i) for i in line.split()[:-1] ])
    return clause

def decoder(cnf_file, ne, nj, teams_file=None):
    """ Lit le fichier cnf_file correspondant la théorie et essaie de trouver
        une solution satisfiable.
        Si une solution est trouvée, l'affiche de manière lisible.
        @param cnf_file: str, nom du fichier contenant la théorie
        @param ne: int, nombre d'équipes participantes
        @param nj: int, nombre de jours de match maximum
        @param teams_file: str, fichier contenant le nom des équipes
    """
    solution = pycosat.solve( to_cnf(cnf_file) )
    
    # Cas UNSAT
    if solution == 'UNSAT':
        #print('UNSAT: aucun modèle ne satisfait la théorie')
        return None
    
    # Cas SAT : initialisation du planning sous forme de dictionnaire
    planning = { 'Jour ' + str(j + 1) : [] for j in range(nj) }
    
    # Récupération des noms des équipes
    if teams_file != None:
        teams_names = open(teams_file, 'r').read().splitlines()
    
    for s in solution:
        if s >= 0:
            j, x, y = decodage(s, ne)
            if teams_file != None:
                x = teams_names[x]
                y = teams_names[y]
            planning[ 'Jour ' + str(j + 1) ].append(( x , y ))
    
    return planning

def affiche_planning(planning):
    """ Affiche de manière plus lisible le planning retourné par la fonction
        decoder.
        @param planning: dict(str, list), planning retourné par decoder
    """
    for jour, matchs in planning.items():
        m_toString = ''
        for e1, e2 in matchs:
            m_toString += str(e1) + ' vs ' + str(e2) + '\n'
        print(jour, ':\n', m_toString)

def optimiser_nj(ne_min = 1, ne_max = 4):
    """ Cherche le nombre de jour nj minimal afin de pouvoir planifier tous
        les matchs du championnat. Tourne au plus 10s.
        @param ne_min: int
        @param ne_max: int
    """
    nj_opt = [0] * ( ne_max - ne_min + 1 )
    
    for ne in range( ne_min, ne_max + 1 ):
        t_start = time.time()
        nj = 1
        while time.time() - t_start < 10:
            genere_cnf(ne,nj)
            if decoder('championnat.cnf', ne, nj) != None:
                nj_opt[ ne - ne_min ] = nj
                print(nj_opt)
                break
            nj += 1
            
    return nj_opt
    