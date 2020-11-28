(param (B C F) (right-tri B))
(let A point (inter-lc (line C F) (coa F B) (rs-opp-sides C (line F B))))

;; D is chosen s.t. DA = DC and AC is the bisector of <DAB
(param D point)
(assert (cong D A D C))
(assert (i-bisector C D A B))

;; E is chosen s.t. EA = ED and AD is the bisector of EAC
(param E point)
(assert (cong E A E D))
(assert (i-bisector D E A C))

(let M point (midp C F))

;; X is s.t. AMXE is a parallelogram
(let X point (inter-ll (para-at E (line M A)) (para-at M (line A E))))

(eval (concur (line B D) (line F X) (line M E)))