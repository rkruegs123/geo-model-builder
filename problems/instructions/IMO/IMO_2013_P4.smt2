(param (A B C) acuteTri)
(compute H point (orthocenter A B C))
(param W point (onSeg B C))
(compute M point (foot B (line C A)))
(compute N point (foot C (line A B)))

(compute omega_1 circle (circumcircle B W N))
(compute X point (interLC (line W (origin omega_1)) omega_1 (rsNeq W)))

(compute omega_2 circle (circumcircle C W M))
(compute Y point (interLC (line W (origin omega_2)) omega_2 (rsNeq W)))

(confirm (coll X Y H))