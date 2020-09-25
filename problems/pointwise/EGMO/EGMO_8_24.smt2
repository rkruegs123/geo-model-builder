;; TODO: Read proof to see if diagram must be further constrained to match Figure 8.9B (EGMO pg. 166)

(declare-points A O1 B O2 C O3 D O4)

(assert (cong O1 A O1 B))
(assert (cong O2 B O2 C))
(assert (coll O1 B O2))
(assert (cong O3 C O3 D))
(assert (coll O2 C O3))
(assert (cong O4 D O4 A))
(assert (coll O3 D O4))
(assert (coll O4 A O1))

(prove (cycl A B C D))