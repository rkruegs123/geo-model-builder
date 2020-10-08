(param lineA line)
(param gamma circle)
(compute D point (interLC lineA gamma rsArbitrary))
(compute E point (interLC lineA gamma (rsNeq D)))