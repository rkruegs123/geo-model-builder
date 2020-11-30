(param (P0 P1 P2 P3 P4) polygon)

(define Q1 point (inter-ll (line P0 P1) (line P2 P3)))
(define Q2 point (inter-ll (line P1 P2) (line P3 P4)))
(define Q3 point (inter-ll (line P2 P3) (line P4 P0)))
(define Q4 point (inter-ll (line P3 P4) (line P0 P1)))
(define Q0 point (inter-ll (line P4 P0) (line P1 P2)))

(define M1 point (inter-cc (circ Q0 P0 P1) (circ Q1 P1 P2) (rs-neq P1)))
(define M2 point (inter-cc (circ Q1 P1 P2) (circ Q2 P2 P3) (rs-neq P2)))
(define M3 point (inter-cc (circ Q2 P2 P3) (circ Q3 P3 P4) (rs-neq P3)))
(define M4 point (inter-cc (circ Q3 P3 P4) (circ Q4 P4 P0) (rs-neq P4)))
(define M0 point (inter-cc (circ Q4 P4 P0) (circ Q0 P0 P1) (rs-neq P0)))

(eval (on-circ M3 (circ M0 M1 M2)))
(eval (on-circ M4 (circ M0 M1 M2)))
