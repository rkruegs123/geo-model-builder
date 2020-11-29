(param (A B C) acute-tri)
(assert (not (cong A B A C)))

(let I point (incenter A B C))

(let omega circle (incircle A B C))
(let D point (inter-lc (line B C) omega rs-arbitrary))
(let E point (inter-lc (line C A) omega rs-arbitrary))
(let F point (inter-lc (line A B) omega rs-arbitrary))

(let R point (inter-lc (perp-at D (line E F)) omega (rs-neq D)))
(let P point (inter-lc (line A R) omega (rs-neq R)))
(let Q point (inter-cc (circ P C E) (circ P B F) (rs-neq P)))

(eval (concur (line D I) (line P Q) (perp-at A (line A I))))
