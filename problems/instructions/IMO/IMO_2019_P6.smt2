(param (A B C) acuteTri))
(assert (not (cong A B A C)))

(compute I point (incenter A B C))

(compute omega circle (incircle A B C))
(compute D point (interLC (line B C) omega rsArbitrary))
(compute E point (interLC (line C A) omega rsArbitrary))
(compute F point (interLC (line A B) omega rsArbitrary))

(compute R point (interLC (perpAt D (line E F)) omega (rsNeq D)))
(compute P point (interLC (line A R) omega (rsNeq R)))
(compute Q point (interCC (circ P C E) (circ P B F) (rsNeq P)))

(confirm (concur (line D I) (line P Q) (perpAt A (line A I))))
