(param (A B C) acute-tri)
(define H point (orthocenter A B C))
(param W point (on-seg B C))
(define M point (foot B (line C A)))
(define N point (foot C (line A B)))

(define omega_1 circle (circumcircle B W N))
(define X point (inter-lc (line W (origin omega_1)) omega_1 (rs-neq W)))

(define omega_2 circle (circumcircle C W M))
(define Y point (inter-lc (line W (origin omega_2)) omega_2 (rs-neq W)))

(eval (coll X Y H))