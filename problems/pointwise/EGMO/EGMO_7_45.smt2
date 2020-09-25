(declare-points A B C D Oabc P Q R E)

(assert (polygon A B C D))
(assert (cycl A B C D))
(assert (circumcenter Oabc A B C))

(assert (coll P A C))
(assert (perp P B B Oabc))
(assert (perp P D D Oabc))

(assert (perp C Q C Oabc))
(assert (coll Q P D))
(assert (coll R C Q))
(assert (coll R A D))

(assert (coll E A Q))
(assert (cycl E A B C))

(prove (coll B E R))