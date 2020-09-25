(declare-points A B C Mab Mac C1 M N B1 P Q)

(assert (triangle A B C))


;; The circle with diameter AB intersects altitude (C, C1) and its extension at points M and N
(assert (foot C1 C A B))
(assert (midp Mab A B))
(assert (coll M C C1))
(assert (coll N C C1))
(assert (cong Mab A Mab M))
(assert (cong Mab A Mab N))

;; The circle with diameter AC intersects altitude (B, B1) and its extensionat P and Q
(assert (foot B1 B C A))
(assert (midp Mac A C))
(assert (coll P B B1))
(assert (coll Q B B1))
(assert (cong Mac A Mac P))
(assert (cong Mac A Mac Q))

;; Prove that M, N, P, Q lie on a common circle
(prove (cycl M N P Q))