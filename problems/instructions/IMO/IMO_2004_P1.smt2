(param (A B C) acuteTri)
(assert (not (cong A B A C)))

(compute M point (interLC (line A B) (diam B C) (rsNeq B)))
(compute N point (interLC (line A C) (diam B C) (rsNeq C)))

(compute O point (midp B C))
(compute R point (interLL (ibisector B A C) (ibisector M O N)))

(confirm (onSeg (interCC (circumcircle B M R) (circumcircle C N R) (rsNeq R)) B C))