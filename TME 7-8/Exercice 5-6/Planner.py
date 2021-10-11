# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 11:05:11 2021

@author: GIANG Cécile
"""

######################## IMPORTATION DE LIBRAIRIES ###########################

from Parser import *


############################### CLASSE PLANNER ###############################

class Planner:
    """ Classe se comportant comme un plannificateur STRIPS en ASP.
    """
    def __init__(self, domain_filename, problem_filename, asp_filename, plan_filename, n):
        """ Constructeur de la classe Parser.
            @param domain_filename: str, chemin vers le fichier domain (.pddl)
            @param problem_filename: str, chemin vers le fichier problem (.pddl)
            @param asp_filename: str, chemin vers le fichier asp à créer (.txt)
            @param plan_filename: str, chemin vers le fichier du plan à créer
            @param n: int, horizon
        """
        # Création du fichier .txt correspondant à la traduction du problème 
        # PDDL en problème ASP
        self.parser = Parser(domain_filename, problem_filename, asp_filename)
        
        # Ensemble des lignes à ajouter dans le plan
        self.to_write = []
        
        # Définition du plan
        self.plan(plan_filename, n)
        
        # Ecriture du plan dans le fichier plan_filename
        self.write_plan()
        
    def plan(self, plan_filename, n):
        """ Pour rajouter les commandes correspondant à la plannification.
            @param plan_filename: str, chemin vers le fichier du plan à créer
            @param n: int, horizon
        """
        self.plan_filename = plan_filename
        
        self.to_write.append('\n\n%%% PLANIFICATION STRIPS %%%')
        
        # Stockage de l'horizon n, déclaration de l'horloge discrète
        self.to_write.append('#const n={}.'.format(n))
        self.to_write.append('time(0..n).\n')
        
        # Etat initial
        self.to_write.append('% Etat initial: si quelquechose est initialement vrai, il est vrai au temps 0')
        self.to_write.append('holds(P,0) :- init(P).\n')
        
        self.to_write.append('1 { perform(A,T) : action(A) } 1 :- time(T), T != n.\n')
        
        # Pré-conditions
        self.to_write.append('% Préconditions: une action ne peut se produire que si toutes les conditions sont vérifiées')
        self.to_write.append('% Autrement dit, si une action s\'effectue alors qu\'une condition n\'est pas vérifiée, on a contradiction.')
        self.to_write.append(':- perform(A,T), not holds(P,T), pre(A,P), action(A), pred(P), time(T).\n')
        
        # Effets positifs
        self.to_write.append('% Effets positifs: si une action s\'effectue au temps T, tous ses effets sont vrais au temps T+1')
        self.to_write.append('holds(P,T+1):- perform(A,T), add(A,P), action(A), pred(P), time(T).\n')
        
        # Inertie et effets négatifs
        self.to_write.append('% Inertie et effets positifs; ce qui est vrai au temps T est vrai au temps T+1, sauf si une action y a mis fin')
        self.to_write.append('% Autrement dit, un prédicat reste vrai sauf si une action effectuée au temps T l\'annule.')
        self.to_write.append('holds(P,T+1) :- holds(P,T), not del(A,P), perform(A,T), action(A), pred(P), time(T).\n')
        
        # Choix d'action
        self.to_write.append('% Choix d\'action: une seule action est effectuée à chaque pas de temps (sauf le dernier)')
        self.to_write.append(':- perform(A1,T), perform(A2,T), action(A1), action(A2), A1 != A2, time(T).\n')
        
        # Spécification du but
        self.to_write.append('% Spécification du but: le but doit être atteint au temps n.')
        self.to_write.append('% Autrement dit: on a contradiction s\'il ne l\'est pas au temps n.')
        self.to_write.append(':- not holds(P,n), but(P), pred(P).\n')
        
        # Affichage de prédicats: on affiche seulement perform
        self.to_write.append('#show perform/2.')
    
    def write_plan(self):
        """ Ecrit dans un fichier .txt nommé plan_filename le plan de résolution
            du problème STRIPS traduit en ASP.
            @param plan_filename: str, chemin vers le fichier plan à créer (.txt)
        """
        # On écrit déjà ce qu'il y a dans le fichier asp
        self.parser.write_asp(self.plan_filename)
        
        # Puis on ajoute les lignes correspondant au planificateur
        with open(self.plan_filename, 'a') as plan_file:
            
            for line in self.to_write:
                    plan_file.write(line + '\n')


################################ EXECUTION ###################################

def main(domain_filename, problem_filename, asp_filename, plan_filename, n):
    # Appel à la classe Planner
    planner = Planner(domain_filename, problem_filename, asp_filename, plan_filename, n)

#  main(domain_filename = 'exemples/blockWorld-domain.pddl', problem_filename = 'exemples/blockWorld-problem.pddl', asp_filename = 'exemples/asp_blockWorld.txt', plan_filename = 'exemples/plan_blockWorld.txt', n=4)
#  main(domain_filename = 'exemples/chasseAuxBananes-domain.pddl', problem_filename = 'exemples/chasseAuxBananes-problem.pddl', asp_filename = 'exemples/asp_chasseAuxBananes.txt', plan_filename = 'exemples/plan_chasseAuxBananes.txt', n=6)