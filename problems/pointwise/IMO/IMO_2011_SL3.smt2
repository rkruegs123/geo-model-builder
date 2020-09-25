(declare-points A B C D Oab Ocd E F OE1 OE2 OE3 OF1 OF2 OF3 Mef X1ef X2ef)

;; ABCD is a convex quadrilateral whose sides AD and BC are not parallel
(assert (polygon A B C D))
(assert (not (para A D B C)))

;; Circles with diameters AB and CD...
(assert (midp Oab A B))
(assert (midp Ocd C D))

;; ... meet at points E and F inside the quadrilateral ABCD
(assert (cong Oab A Oab E))
(assert (cycl A B E F))
(assert (cong Ocd C Ocd E))
(assert (cycl C D E F))
(assert (insidePolygon E A B C D))
(assert (insidePolygon F A B C D))

;; OmegaE is the circle through the feet of the perpendiculars from E to the lines AB, BC, and CD
(assert (foot OE1 E A B))
(assert (foot OE2 E B C))
(assert (foot OE3 E C D))

;; OmegaF is the circle through the feet of the perpendiculars from F to the liens CD, DA, and AB
(assert (foot OF1 F C D))
(assert (foot OF2 F D A))
(assert (foot OF3 F A B))

;; Prove that the midpoint of the segment EF lies on the line through the two intersection points of OmegaE and OmegaF
(assert (midp Mef E F))
(assert (cycl OE1 OE2 OE3 X1ef))
(assert (cycl OE1 OE2 OE3 X2ef))
(assert (cycl OF1 OF2 OF3 X1ef))
(assert (cycl OF1 OF2 OF3 X2ef))
(prove (coll Mef X1ef X2ef))