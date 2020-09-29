(declare-points A B C E F M Oaef A1)

(assert (triangle A B C))
(assert (acutes A B C))
(assert (foot E B A C))
(assert (foot F C A B))
(assert (midp M B C))

;; Prove that ME, MF, and the line through A parallel to BC are all tangents to (AEF)
(assert (circumcenter Oaef A E F))
(assert (para A A1 B C))
(confirm (perp Oaef A A A1))
(confirm (perp Oaef E E M))
(confirm (perp Oaef F F M))
