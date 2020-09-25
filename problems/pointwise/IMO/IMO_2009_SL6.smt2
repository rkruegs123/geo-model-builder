(declare-points A B C D P O1 O2 H1 H2 E1 E2 Fe1cd Fe2ab Aux)

;; AB is not parallel to CD in the quadrilateral ABCD
(assert (polygon A B C D))
(assert (not (para A B C D)))

;; AD and BC intersect at P
(assert (interLL P A D B C))

;; O1 and O2 are the circumcenters of ABP and DCP
(assert (circumcenter O1 A B P))
(assert (circumcenter O2 D C P))

;; H1 and H2 are the orthocenters of ABP and DCP
(assert (orthocenter H1 A B P))
(assert (orthocenter H2 D C P))

;; The midpoints of segments O1H1 and O2H2 are E1 and E2, respectively
(assert (midp E1 O1 H1))
(assert (midp E2 O2 H2))

;; Prove that the perpendicular from E1 on CD, the perpendicular from E2 on AB, and the line H1H2 are concurrent
(assert (foot Fe1cd E1 C D))
(assert (foot Fe2ab E2 A B))
(assert (interLL Aux Fe1cd E1 Fe2ab E2))
(prove (coll Aux H1 H2))