;; Importantly, for the scipy.optimize.minimize trust-constr method, if the xtol is set high, termination will be successful despite the problem being over-constrained

(declare-points A B C D)

(assert (polygon A B C D))
(assert (midp A B C))
