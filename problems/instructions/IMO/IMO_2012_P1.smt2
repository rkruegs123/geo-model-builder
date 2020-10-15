(param (A B C) triangle)
(compute J point (excenter A B C))

(compute M point (foot J (line B C)))
(compute K point (foot J (line A B)))
(compute L point (foot J (line A C)))

(compute F point (interLL (line L M) (line B J)))
(compute G point (interLL (line K M) (line C J)))

(compute S point (interLL (line A F) (line B C)))
(compute T point (interLL (line A G) (line B C)))

(confirm (midp M S T))