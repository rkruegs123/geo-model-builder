(declare-points A B C D Ha Hb Hc Hd X)

(assert (polygon A B C D))
(assert (cycl A B C D))

(assert (orthocenter Ha B C D))
(assert (orthocenter Hb C D A))
(assert (orthocenter Hc D A B))
(assert (orthocenter Hd A B C))

(assert (interLL X A Ha B Hb))
(prove (interLL X C Hc D Hd))