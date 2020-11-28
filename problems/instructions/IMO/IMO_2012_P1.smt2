(param (A B C) triangle)
(let J point (excenter A B C))

(let M point (foot J (line B C)))
(let K point (foot J (line A B)))
(let L point (foot J (line A C)))

(let F point (inter-ll (line L M) (line B J)))
(let G point (inter-ll (line K M) (line C J)))

(let S point (inter-ll (line A F) (line B C)))
(let T point (inter-ll (line A G) (line B C)))

(eval (midp M S T))