(declare-points A B C D P X Mab)

(assert (polygon A B C D))
(assert (insidePolygon P A B C D))

(assert (eq (div (uangle P A D) (uangle P B A)) 0.5))
(assert (eq (div (uangle P A D) (uangle D P A)) (div 1 3)))

(assert (eq (div (uangle C B P) (uangle B A P)) 0.5))
(assert (eq (div (uangle C B P) (uangle B P C)) (div 1 3)))

(assert (ibisector X A D P))
(assert (ibisector X P C B))

(assert (midp Mab A B))
(confirm (perp X Mab A B))

;; FIXME - We have a problem with assertion_vals for triangle/acutes/poly, etc. HAve to clean up the trello