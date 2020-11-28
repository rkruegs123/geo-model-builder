(sample (A B C) acuteTri)

(let C1 (interLL (perpAt C A B) (line A B)))
(let M (interLC (line C C1) (diam A B) (rsArbitrary)))
(let N (interLC (line C C1) (diam A B) (rsNeq M)))

(let B1 (interLL (perpAt B C A) (line C A)))
(let P (interLC (line B B1) (diam A C) (rsArbitrary)))
(let Q (interLC (line B B1) (diam A C) (rsNeq P)))

(confirm (cycl M N P Q))