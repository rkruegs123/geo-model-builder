(declare-points A B C Oabc B0 C0 D G X Oo)

;; ABC is an acute triangle
(assert (triangle A B C))
(assert (acutes A B C))

(assert (circumcenter Oabc A B C))

;; B0 is the midpoint of AC and C0 is the midpoint of AB
(assert (midp B0 A C))
(assert (midp C0 A B))

;; D is the foot of the altitude from A
(assert (foot D A B C))

;; G is the centroid of the triangle ABC
(assert (centroid G A B C))

;; omega is a circle through B0 and C0 that is tangent to the circumcircle of ABC at X /= A
(assert (cycl X A B C))
(assert (circumcenter Oo X B0 C0))
(assert (onSeg Oo Oabc X))

;; Prove that D, G, and X are collinear
(prove (coll D G X))
