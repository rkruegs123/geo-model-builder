(param Gamma circle)
(param l line)

;; Intersection points of l and Gamma
(define A point (inter-lc l Gamma rs-arbitrary))
(define B point (inter-lc l Gamma (rs-neq A)))

;; Intersection points of l and Omega
(param Omega circle)
(define C point (inter-lc l Omega (rs-closer-to-p A)))
(define D point (inter-lc l Omega (rs-neq C)))

;; Intersection points of Gamma and Omega
(define E point (inter-cc Gamma Omega (rs-closer-to-l l)))
(define F point (inter-cc Gamma Omega (rs-neq E)))