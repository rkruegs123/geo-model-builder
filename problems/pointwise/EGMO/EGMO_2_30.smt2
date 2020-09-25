(declare-points A B C Mbc Mca Mab D E F A1 B1 C1 X)

(assert (triangle A B C))
(assert (midp Mbc B C))
(assert (midp Mca C A))
(assert (midp Mab A B))

(assert (perp D Mbc B C))
(assert (perp E Mca C A))
(assert (perp F Mab A B))

;; Show that the lines through A, B, C perpendicular to EF, FD, DE respectively are concurrent
(assert (perp A A1 E F))
(assert (perp B B1 F D))
(assert (perp C C1 D E))

(assert (interLL X A A1 B B1))
(prove (coll X C C1))