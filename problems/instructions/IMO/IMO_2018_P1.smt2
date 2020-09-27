(sample (A B C) acuteTri)

(param D (onSeg D (line A B)))
(param E (onSeg E (line A C)))

(assert (cong A D A E))

(compute F (interLC (perpBis B D) (circ A B C) (rsNeq (midp B D))))
(compute G (interLC (perpBis C E) (circ A B C) (rsNeq (midp C E))))

(confirm (para (line D E) (line F G)))
