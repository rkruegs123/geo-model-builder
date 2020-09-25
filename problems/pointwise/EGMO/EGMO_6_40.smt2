(declare-points A B C I Oaib Haib Obic Hbic Ocia Hcia Oabc Habc X)

(assert (triangle A B C))
(assert (incenter I A B C))

;; Euler line of AIB
(assert (orthocenter Haib A I B))
(assert (circumcenter Oaib A I B))

;; Euler line of BIC
(assert (orthocenter Hbic B I C))
(assert (circumcenter Obic B I C))

;; Euler line of CIA
(assert (orthocenter Hcia C I A))
(assert (circumcenter Ocia C I A))

;; Euler line of ABC
(assert (orthocenter Habc A B C))
(assert (circumcenter Oabc A B C))

;; Prove that the Euler lines of AIB, BIC, CIA, and ABC are concurrent
(assert (interLL X Oaib Haib Obic Hbic))
(prove (interLL X Ocia Hcia Oabc Habc))