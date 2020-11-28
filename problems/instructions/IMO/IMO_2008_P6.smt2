(param (A B C D) polygon)
(assert (not (cong B A B C)))

(let omega_1 circle (incircle A B C))
(let omega_2 circle (incircle A D C))

(param omega circle (tangent-cl (line B A)))
(assert (on-ray (inter-lc (line B A) omega rs-arbitrary) B A))
(assert (not (on-seg (inter-lc (line B A) omega rs-arbitrary) B A)))

(assert (tangent-lc (line B C) omega))
(assert (on-ray (inter-lc (line B C) omega rs-arbitrary) B C))

(assert (tangent-lc (line A D) omega))
(assert (tangent-lc (line C D) omega))