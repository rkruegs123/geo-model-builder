(param B point)
(param C point)
(define O point (midp B C))

(param A point (on-circ (coa O B)))
(assert (gt (uangle A O C) (div pi 3)))

(define E point (inter-lc (perp-bis A O) (coa O B) rs-arbitrary))
(define F point (inter-lc (perp-bis A O) (coa O B) (rs-neq E)))

(define D point (amidp-opp A B C))
(define J point (inter-ll (para-at O (line A D)) (line A C)))

(eval (incenter J C E F))