(declare-points A B C I D E M)

(assert (triangle A B C))
(assert (incenter I A B C))
(assert (foot D I B C))

(assert (cong I E I D))
(assert (coll E I D))

;; M is the midpoint of BC
(assert (midp M B C))

;; Prove that AE || IM
(prove (para A E I M))
