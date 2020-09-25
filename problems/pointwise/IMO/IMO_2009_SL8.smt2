(declare-points A B C D I Tab Tbc Tcd Tda M N I1 I2 I3 H)

;; ABCD is a circumscribed quadrilateral
(assert (polygon A B C D))
(assert (insidePolygon I A B C D))
(assert (cong I Tab I Tbc))
(assert (cong I Tab I Tcd))
(assert (cong I Tab I Tda))
(assert (foot Tab I A B))
(assert (foot Tbc I B C))
(assert (foot Tcd I C D))
(assert (foot Tda I D A))

;; g is a line through A which meets segment BC in M and line CD in N
(assert (onSeg M B C))
(assert (interLL N A M C D))

;; I1, I2, and I3 are the incenters of ABM, MNC, and NDA, respectively
(assert (incenter I1 A B M))
(assert (incenter I2 M N C))
(assert (incenter I3 N D A))

;; Show that the orthocenter of I1I2I3 lies on g
(assert (orthocenter H I1 I2 I3))
(prove (coll H A M))
