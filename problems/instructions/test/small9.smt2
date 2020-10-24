(param Gamma circle)
(param l line)

;; Intersection points of l and Gamma
(compute A point (inter-lc l Gamma rs-arbitrary))
(compute B point (inter-lc l Gamma (rs-neq A)))

;; Intersection points of l and Omega
(param Omega circle)
(compute C point (inter-lc l Omega (rs-closer-to-p A)))
(compute D point (inter-lc l Omega (rs-neq C)))

;; Intersection points of Gamma and Omega
(compute E point (inter-cc Gamma Omega (rs-closer-to-l l)))
(compute F point (inter-cc Gamma Omega (rs-neq E)))