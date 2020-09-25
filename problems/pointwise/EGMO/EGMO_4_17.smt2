(declare-points A B C I D E F M Aux)

(assert (triangle A B C))

;; I is the incenter of ABC
(assert (incenter I A B C))

;; DEF is the contact triangle of ABC
(assert (foot D I B C))
(assert (foot E I A C))
(assert (foot F I A B))

;; M is the midpoint of BC
(assert (midp M B C))

;; EF, AM and ray DI concur
(assert (interLL Aux E F A M))
(prove (onRay Aux D I))