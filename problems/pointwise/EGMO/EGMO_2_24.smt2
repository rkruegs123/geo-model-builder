(declare-points A B C I Ia Ib Ic)

(assert (triangle A B C))
(assert (excenter Ia A B C))
(assert (excenter Ib B A C))
(assert (excenter Ic C B A))
(assert (incenter I A B C))

;; Prove that triangle IaIbIc has orthocenter I...
(prove (orthocenter I Ia Ib Ic))

;; .. and that triangle ABC is its orthic triangle
(prove (foot A Ia Ib Ic))
(prove (foot B Ib Ic Ia))
(prove (foot C Ic Ia Ib))