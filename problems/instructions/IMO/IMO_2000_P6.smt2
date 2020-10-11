(param (A1 A2 A3) acuteTri)

(compute K1 point (foot A1 A2 A3))
(compute K2 point (foot A2 A1 A3))
(compute K3 point (foot A3 A1 A2))

(compute L1 point (interLC (line A2 A3) (incircle A1 A2 A3) rsArbitrary))
(compute L2 point (interLC (line A1 A3) (incircle A1 A2 A3) rsArbitrary))
(compute L3 point (interLC (line A1 A2) (incircle A1 A2 A3) rsArbitrary))

;; Just named for convenience
(compute refl1 line (reflectLL (line K1 K2) (line L1 L2)))
(compute refl2 line (reflectLL (line K2 K3) (line L2 L3)))
(compute refl3 line (reflectLL (line K3 K1) (line L3 L1)))

(confirm (onCirc (interLL refl1 refl2) (incircle A1 A2 A3)))
(confirm (onCirc (interLL refl1 refl3) (incircle A1 A2 A3)))
(confirm (onCirc (interLL refl2 refl3) (incircle A1 A2 A3)))
