(param (P0 P1 P2 P3 P4) polygon)

(compute Q1 point (interLL (line P0 P1) (line P2 P3)))
(compute Q2 point (interLL (line P1 P2) (line P3 P4)))
(compute Q3 point (interLL (line P2 P3) (line P4 P0)))
(compute Q4 point (interLL (line P3 P4) (line P0 P1)))
(compute Q0 point (interLL (line P4 P0) (line P1 P2)))

(compute M1 point (interCC (circ Q0 P0 P1) (circ Q1 P1 P2) (rsNeq P1)))
(compute M2 point (interCC (circ Q1 P1 P2) (circ Q2 P2 P3) (rsNeq P2)))
(compute M3 point (interCC (circ Q2 P2 P3) (circ Q3 P3 P4) (rsNeq P3)))
(compute M4 point (interCC (circ Q3 P3 P4) (circ Q4 P4 P0) (rsNeq P4)))
(compute M0 point (interCC (circ Q4 P4 P0) (circ Q0 P0 P1) (rsNeq P0)))

(confirm (onCirc M3 (circ M0 M1 M2)))
(confirm (onCirc M4 (circ M0 M1 M2)))
