(declare-points A B C A1 B1 C1 A2 B2 C2 Mbc Mca Mab A3 B3 C3)

;; A1, B1, C1 are chosen on the sides BC, CA, AB of a triangle ABC
(assert (triangle A B C))
(assert (onSeg A1 B C))
(assert (onSeg B1 C A))
(assert (onSeg C1 A B))

;; The circumcircles of triangles AB1C1, BC1A1, CA1B1 intersect the circumcircle of ABC again at points A2, B2, C2, respectively
(assert (cycl A2 A B1 C1))
(assert (cycl A2 A B C))

(assert (cycl B2 B C1 A1))
(assert (cycl B2 A B C))

(assert (cycl C2 C A1 B1))
(assert (cycl C2 A B C))

;; A3, B3, C3 are symmetric to A1, B1, C1 w.r.t. the midpoints of the sides BC, CA, AB
(assert (midp Mbc B C))
(assert (midp Mca C A))
(assert (midp Mab A B))

(assert (midp Mbc A1 A3))
(assert (midp Mca B1 B3))
(assert (midp Mab C1 C3))

;; Prove that the triangles A2B2C2 and A3B3C3 are similar
(prove (simtri A2 B2 C2 A3 B3 C3))