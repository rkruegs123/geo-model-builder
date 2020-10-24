(param B point)
(param C point)
(compute O point (midp B C))

(param A point (on-circ (coa O B)))
(assert (gt (uangle A O C) (div pi 3)))

(compute E point (inter-lc (perp-bis A O) (coa O B) rs-arbitrary))
(compute F point (inter-lc (perp-bis A O) (coa O B) (rs-neq E)))

(compute D point (amidp-opp A B C))
(compute J point (inter-ll (para-at O (line A D)) (line A C)))

(eval (incenter J C E F))