# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 14:09:09 2021

@author: GIANG Cécile
"""

######################## IMPORTATION DE LIBRAIRIES ###########################

import re
from pyparsing import OneOrMore, nestedExpr


############################### CLASSE PARSER ################################

class Parser:
    """ Classe permettant de parser deux fichiers PDDL (domain et problem) en
        une représentation ASP du problème STRIPS.
    """
    def __init__(self, domain_filename, problem_filename, asp_filename = 'asp.txt'):
        """ Constructeur de la classe Parser.
            @param domain_filename: str, chemin vers le fichier domain (.pddl)
            @param problem_filename: str, chemin vers le fichier problem (.pddl)
            @param asp_filename: str, chemin vers le fichier asp à créer (.txt)
        """
        # Stockage des fichiers domain et problem, suppression des commentaires
        self.domain_file = re.sub(r'(;;;.*\n)', ' ', open(domain_filename, 'r').read())
        self.problem_file = re.sub(r'(;;;.*\n)', ' ', open(problem_filename, 'r').read())
        
        # Ensemble des lignes à afficher dans le fichier asp
        self.to_write = {'types' : [], 'predicates' : [], 'actions' : [], 'objects' : [], 'constants' : [], 'init' : [], 'goal' : []}
        
        # Liste des constantes
        self.constants = []
        
        # Pipeline
        print('\n*** Parsing du fichier {} en cours ***' . format(domain_filename))
        self.parse_domain()
        
        print('\n*** Parsing du fichier {} en cours ***' . format(problem_filename))
        self.parse_problem()
        
        print('\n*** Ecriture du fichier {} en cours ***' . format(asp_filename))
        self.write_asp(asp_filename)
        
        print('\n*** Fin de traitement ***')
        
        
    def parse_domain(self):
        """ Parsing du fichier domain.
        """
        # Structure à parcourir, qui conserve les relations d'imbrication
        domain = OneOrMore( nestedExpr() ).parseString( self.domain_file )
        
        # Parcours du fichier domain
        for object in domain[0]:
            
            if object[0] == ':types':
                
                self.to_write['types'].append('%Déclaration des types (domain)')
                object = list( object[1:] )
                
                # Indices des underscores
                index_underscores = [ i for i in range(len(object)) if object[i] == '-' ]
                
                for i in index_underscores:
                    self.to_write['types'].append('{}(X):-{}(X).'.format(object[i+1], object[i-1]))
                    
            elif object[0] == ':predicates':
                
                self.to_write['predicates'].append('%Déclaration des prédicats (domain)')
                
                for predicat in object[1:]:
                    # Cas d'un prédicat sans paramètres
                    if len(predicat) == 1:
                        self.to_write['predicates'].append('pred({}).'.format(predicat[0]))
                    # Cas d'un prédicat avec paramètres
                    else:
                        name = predicat[0]
                        predicat = list(filter(('-').__ne__, predicat[1:]))
                        vars = [ predicat[i].strip('?').upper() for i in range(len(predicat)) if i%2 == 0 ]
                        classes = [ '{}({})'.format(predicat[i], vars[(i-1)//2]) for i in range(len(predicat)) if i%2 != 0 ]
                        self.to_write['predicates'].append('pred({}({})):-{}.'.format(name, ','.join(vars), ','.join(classes)))
            
            elif object[0] == ':constants':
                
                self.to_write['constants'].append('%Déclaration des prédicats (domain)')
                
                # Indices des underscores
                index_underscores = [ i for i in range(len(object)) if object[i] == '-' ]
                
                for i in index_underscores:
                    self.to_write['constants'].append('{}({}).'.format(object[i+1], object[i-1].lower()))
                    self.constants.append(object[i-1])
            
            elif object[0] == ':action':
                
                action = list( object )
                name = object[1]
                parameters = list(filter(('-').__ne__, action[ action.index(':parameters') + 1 ]))
                precondition = action[ action.index(':precondition') + 1 ]
                effect = action[ action.index(':effect') + 1 ]
                self.to_write['actions'].append('%Déclaration de l\'action {}'.format(name))
                
                # Déclaration de l'action
                vars = [ parameters[i].strip('?') for i in range(len(parameters)) if i%2 == 0 ]
                vars = [ var.upper() if var not in self.constants else var for var in vars ]
                classes = [ '{}({})'.format(parameters[i], vars[(i-1)//2]) for i in range(len(parameters)) if i%2 != 0 ]
                self.to_write['actions'].append('action({}({})):-{}.'.format(name, ','.join(vars), ','.join(classes)))
                
                # Préconditions
                self.to_write['actions'].append('%Préconditions')
                
                if precondition[0] != 'and':
                    precondition = [precondition]
                else:
                    precondition = precondition[1:]
                
                action_ = '{}({})'.format(name, ','.join(vars))
                
                for element in precondition:
                    if len(element) == 1:
                        self.to_write['actions'].append('pre({},{}):-action({}).'.format(action_, element[0], action_))
                    else:
                        name_element = element[0]
                        vars_element = [ e.strip('?').upper() if e not in self.constants else e.strip('?') for e in element[1:] ]
                        self.to_write['actions'].append('pre({},{}({})):-action({}).'.format(action_, name_element, ','.join(vars_element), action_))
                    
                # Effets
                self.to_write['actions'].append('%Effets')
                
                if effect[0] != 'and':
                    effect = [effect]
                else:
                    effect = effect[1:]
                
                for element in effect:
                    # Récupération de la polarité
                    if element[0] == 'not':
                        operator = 'del'
                        element = element[1:][0]
                    else:
                        operator = 'add'
                    
                    if len(element) == 1:
                        self.to_write['actions'].append('{}({},{}):-action({}).'.format(operator, action_, element[0], action_))
                    else:
                        name_element = element[0]
                        vars_element = [ e.strip('?').upper() if e not in self.constants else e.strip('?') for e in element[1:] ]
                        self.to_write['actions'].append('{}({},{}({})):-action({}).'.format(operator, action_, name_element, ','.join(vars_element), action_))
    
    def parse_problem(self):
        """ Parsing du fichier problem.
        """
        # Structure à parcourir, qui conserve les relations d'imbrication
        problem = OneOrMore( nestedExpr() ).parseString( self.problem_file )
        
        # Parcours du fichier problem
        for object in problem[0]:
                    
            if object[0] == ':objects':
                
                self.to_write['objects'].append('%Déclaration des objets (problem)')
                object = list( object[1:] )
                
                if len(object) == 1:
                    self.to_write['objects'].append('{}.'.format(object[0]))
                
                else:
                    i = 0
                    vars = []
                    
                    while i < len(object):
                        if object[i] == '-':
                            i += 1
                            self.to_write['objects'].append('{}({}).'.format(object[i], ';'.join(vars)))
                            vars = []
                        else:
                            vars.append(object[i].lower())
                        i += 1
            
            if object[0] == ':init':
                
                self.to_write['init'].append('%Etat initial (problem)')
                object = list( object[1:] )
                
                for element in object:
                    if len(element) == 1:
                        self.to_write['init'].append('init({}).'.format(element[0]))
                    
                    else:
                        name = element[0]
                        vars = [ var.lower() for var in element[1:] ]
                        self.to_write['init'].append('init({}({})).'.format(name, ','.join(vars)))
            
            if object[0] == ':goal':
                
                self.to_write['goal'].append('%But (problem)')
                object = list( object[1:] )[0]
                
                if object[0] != 'and':
                    object = [object]
                else:
                    object = object[1:]
                
                for element in object:
                    # Cas d'un prédicat sans paramètre
                    if len(element) == 1:
                        self.to_write['goal'].append('but({}).'.format(element[0]))
                    
                    else:
                        name = element[0]
                        vars = [ var.lower() for var in element[1:] ]
                        self.to_write['goal'].append('but({}({})).'.format(name, ','.join(vars)))
    
    def write_asp(self, asp_filename):
        """ Ecrit dans un fichier .txt nommé asp_filename le problème STRIPS
            traduit en ASP.
            @param asp_filename: str, chemin vers le fichier asp à créer (.txt)
        """
        with open(asp_filename, 'w') as asp_file:
            
            asp_file.write('%%% PROBLEME ASP %%%\n')
            
            for all_lines in self.to_write.values():
                for line in all_lines:
                    asp_file.write(line + '\n')


################################ EXECUTION ###################################

def main(domain_filename, problem_filename, asp_filename):
    # Appel à la classe Parser
    parser = Parser(domain_filename, problem_filename, asp_filename)

#  main(domain_filename = 'exemples/blockWorld-domain.pddl', problem_filename = 'exemples/blockWorld-problem.pddl', asp_filename = 'exemples/asp_blockWorld.txt')
#  main(domain_filename = 'exemples/chasseAuxBananes-domain.pddl', problem_filename = 'exemples/chasseAuxBananes-problem.pddl', asp_filename = 'exemples/asp_chasseAuxBananes.txt')