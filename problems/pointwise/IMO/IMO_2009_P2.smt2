(declare-points A B C OABC P Q K L M OKLM)

(assert (triangle A B C))
(assert (circumcenter OABC A B C))

(assert (onSeg P C A))
(assert (onSeg Q A B))

(assert (midp K B P))
(assert (midp L C Q))
(assert (midp M P Q))

(assert (circumcenter OKLM K L M))
(assert (perp OKLM M P Q))

(prove (cong OABC P OABC Q))
