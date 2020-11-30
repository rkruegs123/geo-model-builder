(param (A B C) triangle)
(define J point (excenter A B C))

(define M point (foot J (line B C)))
(define K point (foot J (line A B)))
(define L point (foot J (line A C)))

(define F point (inter-ll (line L M) (line B J)))
(define G point (inter-ll (line K M) (line C J)))

(define S point (inter-ll (line A F) (line B C)))
(define T point (inter-ll (line A G) (line B C)))

(eval (midp M S T))