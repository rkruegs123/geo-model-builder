(declare-points A B C D E F CCa CCc CCe)

;; ABCDEF is a convex hexagon s.t. AB para DE, BC para EF, and CD para FA
(assert (polygon A B C D E F))
(assert (para A B D E))
(assert (para B C E F))
(assert (para C D F A))

;; Let Ra, Rc, Re denote the circumradii of triangles FAB, BCD, and DEF, respectively
;; Note: CCa, CCc, CCe are the circumcenters of triangles FAB, BCD, and DEF, respectively
(assert (circumcenter CCa F A B))
(assert (circumcenter CCc B C D))
(assert (circumcenter CCe D E F))

;; FIXME: Trivial placeholder goal
