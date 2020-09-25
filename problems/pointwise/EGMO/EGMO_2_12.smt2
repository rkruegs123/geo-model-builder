(declare-points A B C D E F H)

(assert (triangle A B C))
(assert (foot D A B C))
(assert (foot E B A C))
(assert (foot F C A B))

(assert (interLL H A D E B))
(prove (coll H F C))