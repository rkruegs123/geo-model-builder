(param (A B C) acute-tri)

(let Gamma circle (circumcircle A B C))

(param D point (on-seg A B))
(param E point (on-seg A C))
(assert (cong A D A E))

(let F point (inter-lc (perp-bis B D) Gamma (rs-opp-sides C (line A B))))
(let G point (inter-lc (perp-bis C E) Gamma (rs-opp-sides B (line A C))))

(eval (para (line D E) (line F G)))
