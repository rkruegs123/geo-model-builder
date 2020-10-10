(param (A B C) triangle)
(compute J point (excenter A B C))

(compute M point (foot J B C))
(compute K point (foot J A B))
(compute L point (foot J A C))

(compute F point (interLL L M B J))
(compute G point (interLL K M C J))

(compute S point (interLL A F B C))
(compute T point (interLL A G B C))

(confirm (midp M S T))