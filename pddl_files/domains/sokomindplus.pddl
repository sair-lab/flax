(define (domain sokomindplus)
    (:requirements :strips :typing)
    (:types obj robot pos)
    (:predicates
        (rAt ?r - robot ?p - pos)
        (oAt ?o - obj ?p - pos)
        (upTo ?p1 - pos ?p2 - pos)
        (downTo ?p1 - pos ?p2 - pos)
        (leftTo ?p1 - pos ?p2 - pos)
        (rightTo ?p1 - pos ?p2 - pos)
        (isBox ?o - obj)
        (posEmpty ?p - pos)
    )

    ; Move forward
    (:action MoveForwardWhenUp
        :parameters (?r - robot ?p1 - pos ?p2 - pos)
        :precondition (and
            (rAt ?r ?p1)
            (upTo ?p2 ?p1)
            (posEmpty ?p2)
        )
        :effect (and
            (rAt ?r ?p2)
            (not (rAt ?r ?p1))
        )
    )
    (:action MoveForwardWhenDown
        :parameters (?r - robot ?p1 - pos ?p2 - pos)
        :precondition (and
            (rAt ?r ?p1)
            (downTo ?p2 ?p1)
            (posEmpty ?p2)
        )
        :effect (and
            (rAt ?r ?p2)
            (not (rAt ?r ?p1))
        )
    )
    (:action MoveForwardWhenLeft
        :parameters (?r - robot ?p1 - pos ?p2 - pos)
        :precondition (and
            (rAt ?r ?p1)
            (leftTo ?p2 ?p1)
            (posEmpty ?p2)
        )
        :effect (and
            (rAt ?r ?p2)
            (not (rAt ?r ?p1))
        )
    )
    (:action MoveForwardWhenRight
        :parameters (?r - robot ?p1 - pos ?p2 - pos)
        :precondition (and
            (rAt ?r ?p1)
            (rightTo ?p2 ?p1)
            (posEmpty ?p2)
        )
        :effect (and
            (rAt ?r ?p2)
            (not (rAt ?r ?p1))
        )
    )

    ; Push box
    (:action PushBoxWhenUp
        :parameters (?r - robot ?o - obj ?p1 - pos ?p2 - pos ?p3 - pos)
        :precondition (and
            (rAt ?r ?p1)
            (oAt ?o ?p2)
            (upTo ?p2 ?p1)
            (upTo ?p3 ?p2)
            (posEmpty ?p3)
            (isBox ?o)
        )
        :effect (and
            (oAt ?o ?p3)
            (not (oAt ?o ?p2))
            (posEmpty ?p2)
            (not (posEmpty ?p3))
            (rAt ?r ?p2)
            (not (rAt ?r ?p1))
        )
    )
    (:action PushBoxWhenDown
        :parameters (?r - robot ?o - obj ?p1 - pos ?p2 - pos ?p3 - pos)
        :precondition (and
            (rAt ?r ?p1)
            (oAt ?o ?p2)
            (downTo ?p2 ?p1)
            (downTo ?p3 ?p2)
            (posEmpty ?p3)
            (isBox ?o)
        )
        :effect (and
            (oAt ?o ?p3)
            (not (oAt ?o ?p2))
            (posEmpty ?p2)
            (not (posEmpty ?p3))
            (rAt ?r ?p2)
            (not (rAt ?r ?p1))
        )
    )
    (:action PushBoxWhenLeft
        :parameters (?r - robot ?o - obj ?p1 - pos ?p2 - pos ?p3 - pos)
        :precondition (and
            (rAt ?r ?p1)
            (oAt ?o ?p2)
            (leftTo ?p2 ?p1)
            (leftTo ?p3 ?p2)
            (posEmpty ?p3)
            (isBox ?o)
        )
        :effect (and
            (oAt ?o ?p3)
            (not (oAt ?o ?p2))
            (posEmpty ?p2)
            (not (posEmpty ?p3))
            (rAt ?r ?p2)
            (not (rAt ?r ?p1))
        )
    )
    (:action PushBoxWhenRight
        :parameters (?r - robot ?o - obj ?p1 - pos ?p2 - pos ?p3 - pos)
        :precondition (and
            (rAt ?r ?p1)
            (oAt ?o ?p2)
            (rightTo ?p2 ?p1)
            (rightTo ?p3 ?p2)
            (posEmpty ?p3)
            (isBox ?o)
        )
        :effect (and
            (oAt ?o ?p3)
            (not (oAt ?o ?p2))
            (posEmpty ?p2)
            (not (posEmpty ?p3))
            (rAt ?r ?p2)
            (not (rAt ?r ?p1))
        )
    )
)