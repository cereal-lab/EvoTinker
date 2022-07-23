#-----------------------------------------------------------------        
    # SAT
    # NOTE no differences between k=2 and k=5
    fitness_evaluator = FitnessEvaluator(sat.evaluate_formula, 91)
    for i in range(number_of_trials):        
        result1 = evolve(   geno_size=20, 
                            max_iterations=400_000, 
                            pop_size=25, 
                            kt=2, 
                            local_search=True,
                            crossover_rate=1.0, 
                            fitness_evaluator=fitness_evaluator)
        result2 = evolve(   geno_size=20, 
                            max_iterations=400_000, 
                            pop_size=25, 
                            kt=5, 
                            local_search=True,
                            #random_immigrant=True,
                            crossover_rate=1.0, 
                            fitness_evaluator=fitness_evaluator)
        print(f"Run #{i}\t{result1}\t{result2}")
        results1.append(result1)
        results2.append(result2)


# Run #94 (90, 399999, 1834259, 565766)   (91, 58766, 237085, 115542)
# Run #95 (90, 399999, 1834746, 565279)   (90, 399999, 1836496, 563529)
# Run #96 (91, 104452, 433084, 193659)    (91, 249168, 1091857, 403182)
# Run #97 (91, 156808, 664107, 276772)    (91, 230620, 1005456, 378295)
# Run #98 (90, 399999, 1835459, 564566)   (90, 399999, 1835008, 565017)
# Run #99 (91, 351940, 1593165, 518506)   (91, 120057, 499530, 220843)


# Statistic #0
#         Series 1 mean = 90.49
#         Series 2 mean = 90.52
#         Shapiro:         stat=     0.636, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=    -0.422, p=     0.673   --> SAME distribution
#         Mann-Whitney:    stat=  4850.000, p=     0.673   --> SAME distribution


# Statistic #1
#         Series 1 mean = 280815.84
#         Series 2 mean = 274826.91
#         Shapiro:         stat=     0.743, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=     0.284, p=     0.777   --> SAME distribution
#         Mann-Whitney:    stat=  5149.000, p=     0.699   --> SAME distribution


# Statistic #2
#         Series 1 mean = 1271505.72
#         Series 2 mean = 1243278.4
#         Shapiro:         stat=     0.743, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=     0.286, p=     0.776   --> SAME distribution
#         Mann-Whitney:    stat=  4786.500, p=     0.603   --> SAME distribution


# Statistic #3
#         Series 1 mean = 413420.32
#         Series 2 mean = 405714.06
#         Shapiro:         stat=     0.742, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=     0.275, p=     0.783   --> SAME distribution
#         Mann-Whitney:    stat=  5511.500, p=     0.212   --> SAME distribution
        
        
        
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
                            mutation_rate=-1, # was used to trigger local_search
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



