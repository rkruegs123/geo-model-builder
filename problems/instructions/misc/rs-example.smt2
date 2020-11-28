(param Gamma circle)
(param l line)

;; Intersection points of l and Gamma
(let A point (inter-lc l Gamma rs-arbitrary))
(let B point (inter-lc l Gamma (rs-neq A)))

;; Intersection points of l and Omega
(param Omega circle)
(let C point (inter-lc l Omega (rs-closer-to-p A)))
(let D point (inter-lc l Omega (rs-neq C)))

;; Intersection points of Gamma and Omega
(let E point (inter-cc Gamma Omega (rs-closer-to-l l)))
(let F point (inter-cc Gamma Omega (rs-neq E)))