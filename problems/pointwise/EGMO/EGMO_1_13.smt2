(declare-points A B C D E F H)

(assert (triangle A B C))
(assert (foot D A B C))
(assert (foot E B C A))
(assert (foot F C A B))
(assert (orthocenter H A B C))

(prove (incenter H D E F))
;;(watch (perp B F F H))
;; (prove (perp B F F H))
