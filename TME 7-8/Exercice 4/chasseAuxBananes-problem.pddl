(define (problem chasseAuxBananesProblem)
    (:domain chasseAuxBananes)
    (:init  (situe singe a)
            (situe bananes b)
            (situe caisse c)
            (niveau singe bas)
            (niveau bananes haut)
            (niveau caisse bas)
            (mainsVides)
    )
    (:goal (possede singe bananes))
)