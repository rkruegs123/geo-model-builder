(param (A B C) (right-tri C))
(define D point (foot C (line A B)))
(param X point (on-seg C D))
(param K point (on-seg A X))
(assert (cong B K B C))
(param L point (on-seg B X))
(assert (cong A L A C))
(define M point (inter-ll (line A L) (line B K)))
(eval (cong M K M L))