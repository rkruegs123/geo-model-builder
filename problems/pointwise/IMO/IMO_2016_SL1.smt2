;; Note: This problem has very minor differences with IMO 2016 P1

(declare-points A B C D E F M X Aux)

;; ABCDE is a convex pentagon
(assert (polygon A B C D E))

;; F is on AC s.t. <FBC = 90
(assert (onSeg F A C))
(assert (perp F B B C))

;; ABF, ACD, and ADE are similar isosceles triangles
(assert (simtri A B F A C D))
(assert (simtri A C D A D E))
(assert (cong F A F B))
(assert (cong D A D C))
(assert (cong E A E D))

;; M is the midpoint of CF
(assert (midp M C F))

;; Point X is chosen s.t. AMXE is a parallelogram
(assert (para A M X E))
(assert (para A E X M))

;; show that BD, EM, and FX are concurrent
(assert (interLL Aux B D E M))
(prove (coll Aux F X))
