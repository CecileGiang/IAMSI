(define (domain blockWorld)
    (:requirements :strips :typing)
    (:types block - object support - object)
    (:predicates
        (on ?x - block ?y - object)
        (clear ?x - object)
    )
    (:constants table - support)
    (:action moveTo
        ;;; Action qui déplace un block ?x sur un autre block ?z depuis un objet ?y
        :parameters (?x - block ?y - object ?z - block)
        :precondition (and (clear ?x) (on ?x ?y) (clear ?z))
        :effect (and (on ?x ?z)
                (not (on ?x ?y))
                (clear ?y)
                (not (clear ?z)))
    )
    (:action moveToTable
        ;;; Action qui déplace un block ?x sue la table depuis un objet ?y
        :parameters (?x - block ?y - object)
        :precondition (and (clear ?x) (on ?x ?y))
        :effect (and (on ?x table)
                (not (on ?x ?y))
                (clear ?y))
    )
)