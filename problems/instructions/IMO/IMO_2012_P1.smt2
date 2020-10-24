(param (A B C) triangle)
(compute J point (excenter A B C))

(compute M point (foot J (line B C)))
(compute K point (foot J (line A B)))
(compute L point (foot J (line A C)))

(compute F point (inter-ll (line L M) (line B J)))
(compute G point (inter-ll (line K M) (line C J)))

(compute S point (inter-ll (line A F) (line B C)))
(compute T point (inter-ll (line A G) (line B C)))

(eval (midp M S T))