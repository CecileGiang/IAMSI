(define (domain blockWorld)
    (:requirements :strips :typing)
    (:types block)
    (:predicates
        (on ?x - block ?y - block)
        (ontable ?x - block)
        (clear ?x - block)
        (handempty)
        (holding ?x - block)
    )
    (:action pick-up
        ;;; Action qui ramasse un bloc posé sur la table
        :parameters (?x - block)
        :precondition (and (clear ?x) (ontable ?x) (handempty))
        :effect (and (not (ontable ?x))
                (not (clear ?x))
                (not (handempty))
                (holding ?x))
    )
    (:action put-down
        ;;; Action qui pose un block ?x sur la table
        :parameters (?x - block)
        :precondition (holding ?x)
        :effect (and (ontable ?x)
                (clear ?x)
                (handempty)
                (not (holding ?x)))
    )
    (:action stack
        ;;; Action qui empile un block ?x sur un autre block ?y
        :parameters (?x - block ?y - block)
        :precondition (and (clear ?y) (holding ?x))
        :effect (and (on ?x ?y)
                (clear ?x)
                (handempty)
                (not (clear ?y))
                (not (holding ?x)))
    )
    (:action unstack
        ;;; Action qui dépile un block ?x d'un autre block ?y
        :parameters (?x - block ?y - block)
        :precondition (and (on ?x ?y) (clear ?x) (handempty))
        :effect (and (holding ?x)
                (clear ?y)
                (not (on ?x ?y))
                (not (clear ?x))
                (not (handempty)))
    )
)