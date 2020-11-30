(param (A1 A2 A3) acute-tri)

(define K1 point (foot A1 (line A2 A3)))
(define K2 point (foot A2 (line A1 A3)))
(define K3 point (foot A3 (line A1 A2)))

(define L1 point (inter-lc (line A2 A3) (incircle A1 A2 A3) rs-arbitrary))
(define L2 point (inter-lc (line A1 A3) (incircle A1 A2 A3) rs-arbitrary))
(define L3 point (inter-lc (line A1 A2) (incircle A1 A2 A3) rs-arbitrary))

;; Just named for convenience
(define refl1 line (reflect-ll (line K1 K2) (line L1 L2)))
(define refl2 line (reflect-ll (line K2 K3) (line L2 L3)))
(define refl3 line (reflect-ll (line K3 K1) (line L3 L1)))

(eval (on-circ (inter-ll refl1 refl2) (incircle A1 A2 A3)))
(eval (on-circ (inter-ll refl1 refl3) (incircle A1 A2 A3)))
(eval (on-circ (inter-ll refl2 refl3) (incircle A1 A2 A3)))
