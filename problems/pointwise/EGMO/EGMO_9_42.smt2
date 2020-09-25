(declare-points A B C A1 B1 C1 A2 B2 C2 D E F D1 E1 F1 X)

;; ABC is a scalene triangle
(assert (triangle A B C))
(assert (not (cong A B A C)))
(assert (not (cong A B B C)))
(assert (not (cong B C A C)))

;; The feet of the perpendiculars from A to BC, B to CA, and C to AB be A1, B1, C1
(assert (foot A1 A B C))
(assert (foot B1 B C A))
(assert (foot C1 C A B))

;; A2 is the intersection of lines BC and B1C1
(assert (interLL A2 B C B1 C1))

;; Define B2 and C2 analogously
(assert (interLL B2 C A C1 A1))
(assert (interLL C2 A B A1 B1))

;; Let D, E, F be the respective midpoints of sides BC, CA AB
(assert (midp D B C))
(assert (midp E C A))
(assert (midp F A B))

;; Show that the perpendiculars from D to (A, A2), E to (B, B2), and F to (C, C2) are concurrent lines
(assert (foot D1 D A A2))
(assert (foot E1 E B B2))
(assert (foot F1 F C C2))
(assert (interLL X D D1 E E1))
(prove (coll X F F1))