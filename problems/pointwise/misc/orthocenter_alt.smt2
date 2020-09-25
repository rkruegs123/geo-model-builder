(declare-points A B C D E F H)

(assert (triangle A B C))
(assert (foot D A B C))
(assert (foot E B C A))
(assert (coll H A D))
(assert (coll H B E))

(assert (coll H C F))
(assert (coll F A B))

(watch (cycl A F E H))
(watch (cycl A B E D))

(watch (cycl C E H D))
(watch (cycl C A F D))

(watch (cycl B F H D))
(watch (cycl B C F E))

(prove (perp H C A B))
