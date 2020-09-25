(joint (A B C) (triangle A B C) (acutes A B C))

(param   D (onL D (line A B)) (btw D A B))
(param   E (onL E (line A C)) (btw E A C))

(assert (= (dist A D) (dist A E)))

(compute F (interLC (perpBis B D) (circ A B C) (rsNeq (midp B D))))
(compute G (interLC (perpBis C E) (circ A B C) (rsNeq (midp C E))))

(prove (para (line D E) (line F G)))
