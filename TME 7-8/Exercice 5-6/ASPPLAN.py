# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 16:28:41 2021

@author: GIANG Cécile
"""

######################## IMPORTATION DE LIBRAIRIES ###########################

from Planner import *
import os

############################### CLASSE ASPPLAN ###############################

class ASPPLAN:
    """ Classe qui, à partir de deux fichiers définissant le domaine et le 
        problème d'un problème STRIPS, crée les problèmes ASP correspondant et
        génère le plan minimal.
    """
    def __init__(self, domain_filename, problem_filename, asp_filename, plan_filename, nmax=50):
        """ Constructeur de la classe Parser.
            @param domain_filename: str, chemin vers le fichier domain (.pddl)
            @param problem_filename: str, chemin vers le fichier problem (.pddl)
            @param asp_filename: str, chemin vers le fichier asp à créer (.txt)
            @param plan_filename: str, chemin vers le fichier du plan à créer
            @param nmax: int, horizon maximal à tester
        """
        # Initialisation de l'horizon, qui varie de 0 à nmax
        n = 0
        self.planner = Planner(domain_filename, problem_filename, asp_filename, plan_filename, 0)
        
        while n <= nmax and 'UNSATISFIABLE' in os.popen('clingo 0 {}'.format(plan_filename)).read().split('\n'):
            n += 1
            self.planner = Planner(domain_filename, problem_filename, asp_filename, plan_filename, n)
        
        output = os.popen('clingo 0 {}'.format(plan_filename)).read().split('\n')
        
        if 'SATISFIABLE' in output:
            print('\n*** Recherche d\'un plan minimal pour le domaine {} et le problème {}'.format(domain_filename, problem_filename))
            print('\nSATISFIABLE: Plan minimal trouvé pour n = %d' % n)
            print('\n\nPlan: \n', output[4])
        else:
            print('\nUNSATISFIABLE: Pas de plan trouvé pour nmax = %d' % nmax)


################################ EXECUTION ###################################

def main(domain_filename, problem_filename, asp_filename, plan_filename, nmax=50):
    # Appel à la classe Planner
    aspplan = ASPPLAN(domain_filename, problem_filename, asp_filename, plan_filename, nmax)

#  main(domain_filename = 'exemples/blockWorld-domain.pddl', problem_filename = 'exemples/blockWorld-problem.pddl', asp_filename = 'exemples/asp_blockWorld.txt', plan_filename = 'exemples/plan_blockWorld.txt', nmax=50)
#  main(domain_filename = 'exemples/chasseAuxBananes-domain.pddl', problem_filename = 'exemples/chasseAuxBananes-problem.pddl', asp_filename = 'exemples/asp_chasseAuxBananes.txt', plan_filename = 'exemples/plan_chasseAuxBananes.txt', nmax=50)