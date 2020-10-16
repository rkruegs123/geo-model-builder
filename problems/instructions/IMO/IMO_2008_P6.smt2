(param (A B C D) polygon)
(assert (not (cong B A B C)))

(compute omega_1 circle (incircle A B C))
(compute omega_2 circle (incircle A D C))

(param omega circle (tangentCL (line B A)))
(assert (onRay (interLC (line B A) omega rsArbitrary) B A))
(assert (not (onSeg (interLC (line B A) omega rsArbitrary) B A)))

(assert (tangentLC (line B C) omega))
(assert (onRay (interLC (line B C) omega rsArbitrary) B C))

(assert (tangentLC (line A D) omega))
(assert (tangentLC (line C D) omega))