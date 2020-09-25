(declare-points A B C I Ia Ib Ic)

(assert (triangle A B C))
(assert (incenter I A B C))
(assert (excenter Ia A B C))
(assert (excenter Ib B C A))
(assert (excenter Ic C A B))

;; Prove that ABC is the orthic triangle of IaIbIc
;(prove (foot A Ia Ib Ic))
;(prove (foot B Ib Ia Ic))
;(prove (foot C Ic Ia Ib))

;; Prove that the orthocenter of IaIbIc is I
(prove (orthocenter I Ia Ib Ic))
