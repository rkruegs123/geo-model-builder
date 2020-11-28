(param B point)
(param C point)
(let O point (midp B C))

(param A point (on-circ (coa O B)))
(assert (gt (uangle A O C) (div pi 3)))

(let E point (inter-lc (perp-bis A O) (coa O B) rs-arbitrary))
(let F point (inter-lc (perp-bis A O) (coa O B) (rs-neq E)))

(let D point (amidp-opp A B C))
(let J point (inter-ll (para-at O (line A D)) (line A C)))

(eval (incenter J C E F))