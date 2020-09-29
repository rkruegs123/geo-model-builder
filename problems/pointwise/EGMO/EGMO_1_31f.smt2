(declare-points A B C O P)

(assert (triangle A B C))
(assert (circumcenter O A B C))

;; If OA is perp to AP, then <PAB = <ACB
(assert (perp O A A P))
(confirm (eqangle P A A B A C C B))