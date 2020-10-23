(param (P0 P1 P2 P3 P4) polygon)

(compute Q1 point (inter-ll (line P0 P1) (line P2 P3)))
(compute Q2 point (inter-ll (line P1 P2) (line P3 P4)))
(compute Q3 point (inter-ll (line P2 P3) (line P4 P0)))
(compute Q4 point (inter-ll (line P3 P4) (line P0 P1)))
(compute Q0 point (inter-ll (line P4 P0) (line P1 P2)))

(compute M1 point (inter-cc (circ Q0 P0 P1) (circ Q1 P1 P2) (rs-neq P1)))
(compute M2 point (inter-cc (circ Q1 P1 P2) (circ Q2 P2 P3) (rs-neq P2)))
(compute M3 point (inter-cc (circ Q2 P2 P3) (circ Q3 P3 P4) (rs-neq P3)))
(compute M4 point (inter-cc (circ Q3 P3 P4) (circ Q4 P4 P0) (rs-neq P4)))
(compute M0 point (inter-cc (circ Q4 P4 P0) (circ Q0 P0 P1) (rs-neq P0)))

(confirm (on-circ M3 (circ M0 M1 M2)))
(confirm (on-circ M4 (circ M0 M1 M2)))
