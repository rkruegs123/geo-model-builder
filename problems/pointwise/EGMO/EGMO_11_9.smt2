(declare-points A B C D M N Q R K)

(assert (polygon A B C D))
(assert (perp D A A B))
(assert (perp C D D A))

(assert (midp M A C))
(assert (midp N B D))

(assert (coll Q B C))
(assert (cycl Q A B N))
(assert (coll R B C))
(assert (cycl R C D M))

(assert (midp K M N))
(prove (cong K Q K R))