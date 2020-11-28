(param (A B C) acute-tri)
(assert (not (cong A B A C)))

(let M point (inter-lc (line A B) (diam B C) (rs-neq B)))
(let N point (inter-lc (line A C) (diam B C) (rs-neq C)))

(let O point (midp B C))
(let R point (inter-ll (i-bisector B A C) (i-bisector M O N)))

(eval (on-seg (inter-cc (circumcircle B M R) (circumcircle C N R) (rs-neq R)) B C))