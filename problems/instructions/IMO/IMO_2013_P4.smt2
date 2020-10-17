(param (A B C) acute-tri)
(compute H point (orthocenter A B C))
(param W point (on-seg B C))
(compute M point (foot B (line C A)))
(compute N point (foot C (line A B)))

(compute omega_1 circle (circumcircle B W N))
(compute X point (inter-lc (line W (origin omega_1)) omega_1 (rs-neq W)))

(compute omega_2 circle (circumcircle C W M))
(compute Y point (inter-lc (line W (origin omega_2)) omega_2 (rs-neq W)))

(confirm (coll X Y H))