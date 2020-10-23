(param (A B C) acute-tri))
(assert (not (cong A B A C)))

(compute I point (incenter A B C))

(compute omega circle (incircle A B C))
(compute D point (inter-lc (line B C) omega rs-arbitrary))
(compute E point (inter-lc (line C A) omega rs-arbitrary))
(compute F point (inter-lc (line A B) omega rs-arbitrary))

(compute R point (inter-lc (perp-at D (line E F)) omega (rs-neq D)))
(compute P point (inter-lc (line A R) omega (rs-neq R)))
(compute Q point (inter-cc (circ P C E) (circ P B F) (rs-neq P)))

(eval (concur (line D I) (line P Q) (perp-at A (line A I))))
