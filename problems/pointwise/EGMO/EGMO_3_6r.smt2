(declare-points A B C M E X F)

(assert (triangle A B C))

;; AM, BE, CF are concurrent cevians of ABC
(assert (onSeg M B C))
(assert (onSeg E C A))
(assert (onSeg F A B))
(assert (interLL X A M B E))
(assert (coll X C F))

;; Show that BM = MC if EF || BC
(assert (para E F B C))
(prove (cong B M M C))
