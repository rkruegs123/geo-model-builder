(param (A1 A2 A3) acute-tri)

(compute K1 point (foot A1 (line A2 A3)))
(compute K2 point (foot A2 (line A1 A3)))
(compute K3 point (foot A3 (line A1 A2)))

(compute L1 point (inter-lc (line A2 A3) (incircle A1 A2 A3) rs-arbitrary))
(compute L2 point (inter-lc (line A1 A3) (incircle A1 A2 A3) rs-arbitrary))
(compute L3 point (inter-lc (line A1 A2) (incircle A1 A2 A3) rs-arbitrary))

;; Just named for convenience
(compute refl1 line (reflect-ll (line K1 K2) (line L1 L2)))
(compute refl2 line (reflect-ll (line K2 K3) (line L2 L3)))
(compute refl3 line (reflect-ll (line K3 K1) (line L3 L1)))

(confirm (on-circ (inter-ll refl1 refl2) (incircle A1 A2 A3)))
(confirm (on-circ (inter-ll refl1 refl3) (incircle A1 A2 A3)))
(confirm (on-circ (inter-ll refl2 refl3) (incircle A1 A2 A3)))
