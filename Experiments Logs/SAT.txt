#-----------------------------------------------------------------        
    # SAT 
    # NOTE - the pbm yield the EA to re-explore a lot, hence the high hit-rate on cache
    # with high mutation, we explore more of the search space

    fitness_evaluator = FitnessEvaluator(sat.evaluate_formula, 91)
    for i in range(number_of_trials):        
        result1 = evolve(   geno_size=20, 
                            max_iterations=800_000, 
                            pop_size=25, 
                            kt=2, 
                            crossover_rate=1.0, 
                            fitness_evaluator=fitness_evaluator)
        result2 = evolve(   geno_size=20, 
                            max_iterations=800_000, 
                            pop_size=25, 
                            kt=2, 
                            mutation_rate=-1,
                            crossover_rate=1.0, 
                            fitness_evaluator=fitness_evaluator)
        print(f"Run #{i}\t{result1}\t{result2}")
        results1.append(result1)
        results2.append(result2)

    # Run #96 (89, 799999, 1588071, 11954)    (91, 49380, 103023, 94526)
    # Run #97 (89, 799999, 1585458, 14567)    (91, 173872, 399526, 295991)
    # Run #98 (89, 799999, 1588323, 11702)    (91, 279340, 684118, 433271)
    # Run #99 (89, 799999, 1589501, 10524)    (91, 117595, 259476, 210933)
    # Series 1 mean = 767125.12
    # Series 2 mean = 274288.87
    # Shapiro:         stat=     0.230, p=     0.000   --> Probably not Gaussian
    # Student T:       stat=    16.082, p=     0.000   --> DIFFERENT distributions
    # Mann-Whitney:    stat=  8948.000, p=     0.000   --> DIFFERENT distribution

#-----------------------------------------------------------------        



