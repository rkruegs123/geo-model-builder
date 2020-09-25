(declare-points A B C Ia B1 C1)

(assert (triangle A B C))
(assert (excenter Ia A B C))

(assert (foot B1 Ia A B))
(assert (foot C1 Ia A C))

(prove (cong A B1 A C1))