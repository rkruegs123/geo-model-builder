(declare-points B C F A D E M X Aux)

;; Triangle BCF has a right angle at B
(assert (triangle B C F))
(assert (perp C B B F))

;; A is the point on CF s.t. FA = FB and F lies between A and C
(assert (cong F A F B))
(assert (onSeg F A C))

;; D is chosen s.t. DA = DC and AC is the bisector of <DAB
(assert (cong D A D C))
(assert (ibisector C D A B))

;; E is chosen s.t. EA = ED and AD is the bisector of EAC
(assert (cong E A E D))
(assert (ibisector D E A C))

;; M is the midpoint of CF
(assert (midp M C F))

;; X is s.t. AMXE is a parallelogram
(assert (para A M E X))
(assert (para A E M X))

;; Prove that BD, FX, and ME are concurrent
(assert (interLL Aux B D F X))
(prove (coll Aux M E))
