(declare-points A B C Ia I D X B1 C1 E)

(assert (triangle A B C))

(assert (excenter Ia A B C))
(assert (incenter I A B C))
(assert (foot D I B C))

;; The A-excircle is tangent to BC at X
(assert (foot X Ia B C))

;; B1 and C1 lie on AB and AC, and B1C1 is parallel to BC
(assert (onSeg B1 A B))
(assert (onSeg C1 A C))
(assert (para B1 C1 B C))

;; B1C1 is tangent to the incircle at E
(assert (foot E I B1 C1))
(assert (cong I E I D))

;; prove that A, E, and X are collinear
(prove (coll A E X))

;; prove that DE is a diameter of the incircle
(prove (coll D E I))