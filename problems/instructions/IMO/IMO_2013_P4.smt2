(param (A B C) acute-tri)
(let H point (orthocenter A B C))
(param W point (on-seg B C))
(let M point (foot B (line C A)))
(let N point (foot C (line A B)))

(let omega_1 circle (circumcircle B W N))
(let X point (inter-lc (line W (origin omega_1)) omega_1 (rs-neq W)))

(let omega_2 circle (circumcircle C W M))
(let Y point (inter-lc (line W (origin omega_2)) omega_2 (rs-neq W)))

(eval (coll X Y H))