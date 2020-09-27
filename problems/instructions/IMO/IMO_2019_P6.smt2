(sample (A B C) acuteTri))
(assert (not (cong A B A C)))

(compute I (incenter A B C))
(compute D (interLL (perpAt I B C) (line B C)))
(compute E (interLL (perpAt I A C) (line A C)))
(compute F (interLL (perpAt I A B) (line A B)))

(compute R (interLC (perpAt D E F) (circ D E F) (rsNeq D)))
(compute P (interLC (line A R) (circ D E F) (rsNeq R)))
(compute Q (interCC (circ P C E) (circ P B F) (rsNeq P)))

(confirm (onL (interLL (line D I) (line P Q)) (perpAt A A I)))