(declare-points A B C O P)

(assert (triangle A B C))
(assert (circumcenter O A B C))

;; If <PAB = <ACB, then OA is perp to AP
(assert (eqangle P A A B A C C B))
(prove (perp O A A P))
