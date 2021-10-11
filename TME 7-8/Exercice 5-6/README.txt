%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ----------------- GUIDE D'UTILISATION DU PLANIFICATEUR STRIPS ----------------- %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% I. Les classes ..................................................................

Notre librairie de planification STRIPS est composée de 3 classes principales, 
chacune implémentée dans un fichier .py:
	(1) classe Parser: permet de parser deux fichiers PDDL (domain et problem) 
	    et de créer une représentation ASP du problème STRIPS.
	(2) classe Planner: permet de générer un plan STRIPS d'horizon n
	(3) classe ASPPLAN: classe principale qui, à partir des deux classes précé-
	    -dentes, génère un plan minimal et l'affiche s'il existe. On fixera un
	    horizon maximal nmax.

% II. Les commandes ...............................................................

Chaque fichier python propose une fonction main, mais l'on pourra se contenter d'
appeler celle de la classe ASPPLAN qui fait elle-même appel aux autres classes.

Le dossier /exemples contient les traductions STRIPS de deux exercices vus en TD
(problème du monde des blocs et le problème du singe et des bananes).
Les appels à la fonction main tels qu'écrits ci-dessous génèrent de nouveaux fichiers:
	(1) asp_blockWorld.txt          # traduction du problème en ASP
	(2) asp_chasseAuxBananes.txt    # traduction du problème en ASP
	(3) plan_blockWorld.txt   	# plan minimal généré
	(4) plan_chasseAuxBananes.txt  	# plan minimal généré

***************************** Commandes sur un IDE ********************************

# Pour le problème du monde des blocs: plan minimal pour un horizon n=4
main(domain_filename = 'exemples/blockWorld-domain.pddl', problem_filename = 'exemples/blockWorld-problem.pddl', asp_filename = 'exemples/asp_blockWorld.txt', plan_filename = 'exemples/plan_blockWorld.txt', nmax=50)

# Pour le problème du singe et des bananes: plan minimal pour un horizon n=6
main(domain_filename = 'exemples/chasseAuxBananes-domain.pddl', problem_filename = 'exemples/chasseAuxBananes-problem.pddl', asp_filename = 'exemples/asp_chasseAuxBananes.txt', plan_filename = 'exemples/plan_chasseAuxBananes.txt', nmax=50)