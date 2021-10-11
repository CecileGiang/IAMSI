(define (domain chasseAuxBananes)
    (:requirements :strips :typing)
    (:types animal - entite objet - entite position hauteur)
    (:predicates (situe ?x - entite ?y - position)
                 (niveau ?x - entite ?y - hauteur)
                 (possede ?x - animal ?y - objet)
                 (mainsVides)
    )
    (:constants singe - animal
                bananes - objet
                caisse - objet
                haut - hauteur
                bas - hauteur
                a - position
                b - position
                c - position
    )
    (:action seDeplace
        ;;; Le singe se déplace de l'emplacement ?x à l'emplacement ?y 
        :parameters (?x - position ?y - position)
        :precondition (and (situe singe ?x) (niveau singe bas))
        :effect (and (situe singe ?y)
                (not (situe singe ?x)))
    )
    (:action prend
        ;;; Le singe prend l'objet ?x (ne peut prendre qu'un objet à la fois)
        :parameters (?x - objet ?pos - position ?niv - hauteur)
        :precondition (and (situe singe ?pos) (situe ?x ?pos) (niveau singe ?niv) (niveau ?x ?niv) (mainsVides))
        :effect (and (possede singe ?x)
                (not (situe ?x ?pos))
                (not (niveau ?x ?niv))
                (not (mainsVides)))
    )
    (:action depose
        ;;; Le singe dépose l'objet ?x
        :parameters (?x - objet ?pos - position ?niv - hauteur)
        :precondition (and (possede singe ?x) (situe singe ?pos) (niveau singe ?niv))
        :effect (and (situe ?x ?pos)
                (niveau ?x ?niv)
                (mainsVides)
                (not (possede singe ?x)))
    )
    (:action monteCaisse
        ;;; Le singe monte sur la caisse
        :parameters (?pos - position)
        :precondition (and (situe singe ?pos) (situe caisse ?pos) (niveau singe bas) (niveau caisse bas))
        :effect (and (niveau singe haut)
                (not (niveau singe bas)))
    )
)