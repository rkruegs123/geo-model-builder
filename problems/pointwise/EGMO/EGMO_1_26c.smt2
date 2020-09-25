(declare-points A B C H D E F)

(assert (triangle A B C))
(assert (orthocenter H A B C))
(assert (foot D A B C))
(assert (foot E B A C))
(assert (foot F C A B))

(prove (cycl C D H E))
