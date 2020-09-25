(declare-points A B C D E F H)

(assert (polygon A B C))
(assert (foot D A B C))
(assert (foot E B C A))
(assert (foot F C A B))
(assert (coll H A D))
(assert (coll H B E))

(watch (cycl A F E H))
(watch (cycl A B E D))

(watch (cycl C E H D))
(watch (cycl C A F D))

(watch (cycl B F H D))
(watch (cycl B C F E))

(prove (coll H C F))
