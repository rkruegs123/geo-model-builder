(declare-points A B C D A1 E F I K)

;; ABC is a triangle with AB = AC
(assert (triangle A B C))
(assert (cong A B A C))

;; D is the midpoint of AC
(assert (midp D A C))

;; (Auxiliary point) line(A1, A) is the internal bisector of <BAC
(assert (ibisector A1 B A C))

;; The angle bisector of <BAC intersects the circle through D, B, and C in a point E inside triangle ABC
(assert (coll A A1 E))
(assert (cycl D B C E))
(assert (insidePolygon E A B C))

;; The line BD intersects the circle through A, E, and B in two points B and F
(assert (coll B D F))
(assert (cycl A E B F))

;; The lines AF and BE meet at a point I
(assert (interLL I A F B E))

;; The lines C I and B D meet at a point K
(assert (interLL K C I B D))

;; Show that I is the incenter of triangle KAB
(prove (incenter I K A B))
