(define (domain difficultlogistics)
  (:requirements :strips)

  (:predicates
    ;; Type-like predicates
    (OBJ ?obj)
    (TRUCK ?truck)
    (AIRPLANE ?airplane)
    (LOCATION ?loc)
    (CITY ?city)
    (AIRPORT ?airport)

    ;; Spatial & containment
    (at ?thing ?loc)          ; thing (object or vehicle) at location
    (in ?obj ?veh)            ; object is inside vehicle (truck/airplane)
    (in-city ?loc ?city)      ; location belongs to a city

    ;; Connectivity
    (road ?from ?to)          ; directed road edge for trucks
    (air-link ?from ?to)      ; directed air-link edge for airplanes

    ;; Stacking
    (on-ground ?obj)          ; obj is on the ground (bottom of its stack)
    (on ?obj ?below)          ; obj is directly on top of ?below
    (clear ?obj)              ; nothing on top of obj

    ;; Emptiness for ground unloading:
    ;;  - true initially only at locations with no packages
    ;;  - once a package is ground-unloaded there, it becomes false forever
    (loc-empty ?loc)

    ;; Capacity: single slot per vehicle
    (slot-free ?veh)          ; vehicle currently carries no package

    ;; Locked hubs & keys
    (locked ?loc)             ; trucks cannot drive into this location while locked
    (switch-for ?panel ?loc)  ; panel location controls locked location
    (key-package ?obj)        ; special package that can unlock locations
  )

  ;; ============================================================
  ;; LOADING INTO TRUCKS (single slot)
  ;; ============================================================

  ;; Load a clear package from the ground (bottom of stack)
  (:action LOAD-TRUCK-FROM-GROUND
    :parameters (?obj ?truck ?loc)
    :precondition
      (and (OBJ ?obj) (TRUCK ?truck) (LOCATION ?loc)
           (at ?truck ?loc)
           (at ?obj ?loc)
           (on-ground ?obj)
           (clear ?obj)
           (slot-free ?truck))
    :effect
      (and (not (at ?obj ?loc))
           (not (on-ground ?obj))
           (in ?obj ?truck)
           (not (slot-free ?truck)))
  )

  ;; Load a clear package from the top of a stack
  (:action LOAD-TRUCK-FROM-STACK
    :parameters (?obj ?below ?truck ?loc)
    :precondition
      (and (OBJ ?obj) (OBJ ?below)
           (TRUCK ?truck) (LOCATION ?loc)
           (at ?truck ?loc)
           (at ?obj ?loc)
           (at ?below ?loc)
           (on ?obj ?below)
           (clear ?obj)
           (slot-free ?truck))
    :effect
      (and (not (at ?obj ?loc))
           (not (on ?obj ?below))
           (clear ?below)
           (in ?obj ?truck)
           (not (slot-free ?truck)))
  )

  ;; ============================================================
  ;; UNLOADING FROM TRUCKS
  ;; ============================================================

  ;; To ground: ONLY when location is marked loc-empty (no package has ever been ground-unloaded there).
  ;; Once you place the first package, loc-empty becomes false forever.
  (:action UNLOAD-TRUCK-TO-GROUND
    :parameters (?obj ?truck ?loc)
    :precondition
      (and (OBJ ?obj) (TRUCK ?truck) (LOCATION ?loc)
           (at ?truck ?loc)
           (in ?obj ?truck)
           (loc-empty ?loc))
    :effect
      (and (not (in ?obj ?truck))
           (slot-free ?truck)
           (at ?obj ?loc)
           (on-ground ?obj)
           (clear ?obj)
           (not (loc-empty ?loc)))
  )

  ;; Onto another package: allowed only if there is a clear package at loc.
  ;; This is how we build multi-package stacks at non-empty locations.
  (:action UNLOAD-TRUCK-ONTO
    :parameters (?obj ?below ?truck ?loc)
    :precondition
      (and (OBJ ?obj) (OBJ ?below)
           (TRUCK ?truck) (LOCATION ?loc)
           (at ?truck ?loc)
           (in ?obj ?truck)
           (at ?below ?loc)
           (clear ?below))
    :effect
      (and (not (in ?obj ?truck))
           (slot-free ?truck)
           (at ?obj ?loc)
           (on ?obj ?below)
           (clear ?obj)
           (not (clear ?below)))
  )

  ;; ============================================================
  ;; LOADING INTO AIRPLANES
  ;; ============================================================

  (:action LOAD-AIRPLANE-FROM-GROUND
    :parameters (?obj ?airplane ?loc)
    :precondition
      (and (OBJ ?obj) (AIRPLANE ?airplane) (LOCATION ?loc)
           (at ?airplane ?loc)
           (at ?obj ?loc)
           (on-ground ?obj)
           (clear ?obj)
           (slot-free ?airplane))
    :effect
      (and (not (at ?obj ?loc))
           (not (on-ground ?obj))
           (in ?obj ?airplane)
           (not (slot-free ?airplane)))
  )

  (:action LOAD-AIRPLANE-FROM-STACK
    :parameters (?obj ?below ?airplane ?loc)
    :precondition
      (and (OBJ ?obj) (OBJ ?below)
           (AIRPLANE ?airplane) (LOCATION ?loc)
           (at ?airplane ?loc)
           (at ?obj ?loc)
           (at ?below ?loc)
           (on ?obj ?below)
           (clear ?obj)
           (slot-free ?airplane))
    :effect
      (and (not (at ?obj ?loc))
           (not (on ?obj ?below))
           (clear ?below)
           (in ?obj ?airplane)
           (not (slot-free ?airplane)))
  )

  ;; ============================================================
  ;; UNLOADING FROM AIRPLANES
  ;; ============================================================

  ;; To ground: ONLY when location is loc-empty.
  (:action UNLOAD-AIRPLANE-TO-GROUND
    :parameters (?obj ?airplane ?loc)
    :precondition
      (and (OBJ ?obj) (AIRPLANE ?airplane) (LOCATION ?loc)
           (at ?airplane ?loc)
           (in ?obj ?airplane)
           (loc-empty ?loc))
    :effect
      (and (not (in ?obj ?airplane))
           (slot-free ?airplane)
           (at ?obj ?loc)
           (on-ground ?obj)
           (clear ?obj)
           (not (loc-empty ?loc)))
  )

  ;; Onto a package
  (:action UNLOAD-AIRPLANE-ONTO
    :parameters (?obj ?below ?airplane ?loc)
    :precondition
      (and (OBJ ?obj) (OBJ ?below)
           (AIRPLANE ?airplane) (LOCATION ?loc)
           (at ?airplane ?loc)
           (in ?obj ?airplane)
           (at ?below ?loc)
           (clear ?below))
    :effect
      (and (not (in ?obj ?airplane))
           (slot-free ?airplane)
           (at ?obj ?loc)
           (on ?obj ?below)
           (clear ?obj)
           (not (clear ?below)))
  )

  ;; ============================================================
  ;; LOCKED HUBS & SWITCHES (for trucks)
  ;; ============================================================

  ;; Activate a switch: use a key-package inside a truck at a panel location
  ;; to unlock some locked location.
  (:action ACTIVATE-SWITCH
    :parameters (?key ?truck ?panel ?loc)
    :precondition
      (and (OBJ ?key) (key-package ?key)
           (TRUCK ?truck)
           (LOCATION ?panel) (LOCATION ?loc)
           (at ?truck ?panel)
           (in ?key ?truck)
           (switch-for ?panel ?loc)
           (locked ?loc))
    :effect
      (and (not (locked ?loc)))
  )

  ;; ============================================================
  ;; MOVEMENT
  ;; ============================================================

  ;; Trucks cannot drive into a location that is still locked
  (:action DRIVE-TRUCK
    :parameters (?truck ?loc-from ?loc-to ?city)
    :precondition
      (and (TRUCK ?truck)
           (LOCATION ?loc-from) (LOCATION ?loc-to)
           (CITY ?city)
           (at ?truck ?loc-from)
           (in-city ?loc-from ?city)
           (in-city ?loc-to ?city)
           (road ?loc-from ?loc-to)
           (not (locked ?loc-to)))
    :effect
      (and (not (at ?truck ?loc-from))
           (at ?truck ?loc-to)))

  ;; Planes unaffected by lock
  (:action FLY-AIRPLANE
    :parameters (?airplane ?loc-from ?loc-to)
    :precondition
      (and (AIRPLANE ?airplane)
           (AIRPORT ?loc-from) (AIRPORT ?loc-to)
           (at ?airplane ?loc-from)
           (air-link ?loc-from ?loc-to))
    :effect
      (and (not (at ?airplane ?loc-from))
           (at ?airplane ?loc-to)))
)
