(declare-points A B C I X Y Z)

(assert (triangle A B C))
(assert (incenter I A B C))

(assert (amidpOpp X B C A))
(assert (amidpOpp Y A C B))
(assert (amidpOpp Z A B C))

(prove (orthocenter I X Y Z))

;; (watch (coll A I X))