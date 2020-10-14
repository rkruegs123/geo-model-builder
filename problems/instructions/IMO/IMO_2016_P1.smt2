(param (B C F) (rightTri B))
(compute A point (interLC (line C F) (coa F B) (rsOppSides C (line F B))))

;; D is chosen s.t. DA = DC and AC is the bisector of <DAB
(param D point)
(assert (cong D A D C))
(assert (ibisector C D A B))

;; E is chosen s.t. EA = ED and AD is the bisector of EAC
(param E point)
(assert (cong E A E D))
(assert (ibisector D E A C))

(compute M point (midp C F))

;; X is s.t. AMXE is a parallelogram
(compute X point (interLL (paraAt E (line M A)) (paraAt M (line A E))))

(confirm (concur (line B D) (line F X) (line M E)))