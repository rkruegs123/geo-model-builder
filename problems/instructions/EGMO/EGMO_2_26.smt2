(sample (A B C) acuteTri)

(compute C1 (interLL (perpAt C A B) (line A B)))
(compute M (interLC (line C C1) (diam A B) (rsArbitrary)))
(compute N (interLC (line C C1) (diam A B) (rsNeq M)))

(compute B1 (interLL (perpAt B C A) (line C A)))
(compute P (interLC (line B B1) (diam A C) (rsArbitrary)))
(compute Q (interLC (line B B1) (diam A C) (rsNeq P)))

(confirm (cycl M N P Q))