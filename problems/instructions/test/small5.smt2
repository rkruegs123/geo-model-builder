(PARAM (A B C) (iso-tri A))
(compute gamma CIRCLE (circumciRcle A B C))
(param D point (on-circ gamma))
(eval (on-circ D gamma))
