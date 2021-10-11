# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 16:46:36 2021

@author: GIANG Cécile
"""

from championnat import *

# Récupération du nombre d'équipes
ne = int( input('\nNombre d\'équipes : ') )

# Récupéraion du nombre de jours
nj = int( input('Nombre de jours : ') )

# Récupéraion du nom du fichier contenant les noms des équipes
teams_file = input('Fichier contenant les noms des équipes (optionnel) : ')

# Génération du fichier cnf correspondant à la théorie
genere_cnf(ne,nj)
print('\n*** Le fichier \'championnat.cnf\' a été mis à jour ***')

# Affichage optionnel de la théorie
display = input('Afficher la théorie ? (y/n) ')
if display == 'y':
    print('\n', to_cnf('championnat.cnf'))
    
# Résolution par solveur SAT
input()
print('\n*** Résolution de la théorie SAT ***\n')

if teams_file == '':
    teams_file = None
    
planning = decoder('championnat.cnf', ne, nj, teams_file = teams_file)

# Bel affichage
affiche_planning(planning)