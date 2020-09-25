(declare-points A B C H D E OA A1 A2 OB B1 B2 OC C1 C2)

;; ABC is an acute triangle
(assert (triangle A B C))
(assert (acutes A B C))

;; H is the orthocenter of ABC, and D and E are the feet of the altitudes from A and B, respectively
(assert (orthocenter H A B C))
(assert (foot D A B C))
(assert (foot E B A C))

;; The circle GammaA is centered at the midpoint of BC, passes through H, and intersects BC at A1 and A2
(assert (midp OA B C))
(assert (coll A1 B C))
(assert (cong OA A1 OA H))
(assert (coll A2 B C))
(assert (cong OA A2 OA H))

;; The circle GammaB is centered at the midpoint of AC, passes through H, and intersects AC at B1 and B2
(assert (midp OB C A))
(assert (coll B1 C A))
(assert (cong OB B1 OB H))
(assert (coll B2 C A))
(assert (cong OB B2 OB H))

;; The circle GammaC is centered at the midpoint of AB, passes through H, and intersects AB at C1 and C2
(assert (midp OC A B))
(assert (coll C1 A B))
(assert (cong OC C1 OC H))
(assert (coll C2 A B))
(assert (cong OC C2 OC H))

;; A1, A2, B1, B2, C1, and C2 are concyclic
(prove (cycl A1 A2 B1 B2 C1 C2))
