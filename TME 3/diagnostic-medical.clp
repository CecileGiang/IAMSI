;;; IAMSI 2020 : séance TME 3
;;; diagnostic-medical.clp


(defrule my_init
	(initial-fact)
=>
	(watch facts)
	(watch rules)

	(assert (taches_rouges patient))
	(assert (peu_boutons patient))
	(assert (sensation_froid patient))
	(assert (forte_fievre patient))
	(assert (yeux_douloureux patient))
	(assert (amygdales_rouges patient))
	(assert (peau_pele patient))
	(assert (peau_seche patient))
)

; Eruption cutanée
(defrule eruption_cutanee
	(or (peu_boutons ?patient)
	    (beaucoup_boutons ?patient))
=>
	(assert (eruption_cutanee ?patient))
)

; Exanthème
(defrule exantheme
	(or (eruption_cutanee ?patient)
	    (rougeurs ?patient))
=>
	(assert (exantheme ?patient))
)

; Etat fébrile
(defrule etat_febrile
	(or (forte_fievre ?patient)
	    (sensation_froid ?patient))
=>
	(assert (etat_febrile ?patient))
)

; Signe suspect
(defrule signe_suspect
	(amygdales_rouges ?patient)
	(taches_rouges ?patient)
	(peau_pele ?patient)
=>
	(assert (signe_suspect ?patient))
)

; Rougeole
(defrule rougeole
	(or (and (etat_febrile ?patient)
		 (yeux_douloureux ?patient)
		 (exantheme ?patient))
	    (and (signe_suspect ?patient)
		 (forte_fievre ?patient)))
=>
	(assert (rougeole ?patient))
)

; Non rougeole
(defrule non_rougeole
	(peu_fievre ?patient)
	(peu_boutons ?patient)
	?a_rougeole <- (rougeole ?patient)
=>
	(retract ?a_rougeole)
	(assert (non_rougeole ?patient))
)

; Douleur
(defrule douleur
	(or (yeux_douloureux ?patient)
	    (dos_douloureux ?patient))
=>
	(assert (douleur ?patient))
)

; Grippe
(defrule grippe
	(dos_douloureux ?patient)
	(etat_febrile ?patient)
=>
	(assert (grippe ?patient))
)

; Diagnostic
(defrule diagnostic
	(non_rougeole ?patient)
=>
	(assert (rubeole ?patient))
	(assert (varicelle ?patient))
)

; Varicelle
(defrule varicelle
	(fortes_demangeaisons ?patient)
	(pustules ?patient)
=>
	(assert (varicelle ?patient))
)

? Rubéole
(defrule rubeole
	(peau_seche ?patient)
	(inflammation_ganglions ?patient)
	(not (pustules ?patient))
	(not (sensation_froid ?patient))
=>
	(assert (rubeole ?patient))
)


; ----- fin fichier diagnostic-medical.clp
