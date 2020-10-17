(param (A B C) acute-tri)
(assert (not (cong A B A C)))

(compute M point (inter-lc (line A B) (diam B C) (rs-neq B)))
(compute N point (inter-lc (line A C) (diam B C) (rs-neq C)))

(compute O point (midp B C))
(compute R point (inter-ll (i-bisector B A C) (i-bisector M O N)))

(confirm (on-seg (inter-cc (circumcircle B M R) (circumcircle C N R) (rs-neq R)) B C))