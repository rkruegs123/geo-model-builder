(param (A B C D) polygon)
(assert (not (cong B A B C)))

(compute omega_1 circle (incircle A B C))
(compute omega_2 circle (incircle A D C))

(param Z point (onRay B A))
(assert (not (between Z B A)))

(param omega circle (through Z))
(assert (tangentAt Z (line A B) omega))

(param W point (onRay B C))
(assert (not (between W B C)))
(assert (tangentAt W (line B C) omega))

(assert (tangent (line A D) omega))
(assert (tangent (line C D) omega))
