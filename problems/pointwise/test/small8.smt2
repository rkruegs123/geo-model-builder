(declare-points A B C D E F)
;; (assert (cong A B C D))
;; (assert (eq 4.0 (dist A B)))
(assert (concur (line A B) (line C D) (line E F)))