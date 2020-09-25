(declare-points A B C I Oa K L)

(assert (triangle A B C))
(assert (incenter I A B C))

(assert (mixtilinearIncenter Oa A B C))
(assert (foot K Oa A B))
(assert (foot L Oa A C))

(prove (midp I K L))