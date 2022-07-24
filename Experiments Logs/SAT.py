from encodings import search_function
from termios import CS5, TIOCPKT_DOSTOP
TODOs
    .   try novelty search
    .   try pareto selection of pareto dominant CS
    .   try just the local search alone

#-----------------------------------------------------------------        

    # SAT
# NOTE
# - first run in parallel, repeat of the previous one
# - did NOT confirm that pareto selection is not working
#   --> try with more clauses?! nah
#   --> check for bugs in implementation
#   --> we have high fitness very often, > 80, so many clauses are satisfied
#       two pareto incomparable CS have less clauses in common maybe?
#       BUT mix and matching these CS introduces incompatibilities
#       e.g., one has a var true that gives 3 first clauses, the other
#       has it false which gives the last 3 clauses... 
#  
    fitness_evaluator = FitnessEvaluator(sat.evaluate_formula, 91)
    for i in range(number_of_trials):        
        with ProcessPoolExecutor(2) as executor:
            future_1a = executor.submit( evolve, 
                                        geno_size=20, 
                                        max_iterations=400_000, 
                                        pop_size=25, 
                                        kt=2, 
                                        local_search=True,
                                        crossover_rate=1.0, 
                                        fitness_evaluator=fitness_evaluator)
            future_1b = executor.submit( evolve, 
                                        geno_size=20, 
                                        max_iterations=400_000, 
                                        pop_size=25, 
                                        kt=2, 
                                        local_search=True,
                                        crossover_rate=1.0, 
                                        fitness_evaluator=fitness_evaluator)
            future_2a = executor.submit( evolve, 
                                        geno_size=20, 
                                        max_iterations=400_000, 
                                        pop_size=25, 
                                        kt=2, 
                                        pareto_select=True, # <---
                                        local_search=True,
                                        crossover_rate=1.0, 
                                        fitness_evaluator=fitness_evaluator)
            future_2b = executor.submit( evolve, 
                                        geno_size=20, 
                                        max_iterations=400_000, 
                                        pop_size=25, 
                                        kt=2, 
                                        pareto_select=True, # <---
                                        local_search=True,
                                        crossover_rate=1.0, 
                                        fitness_evaluator=fitness_evaluator)
            result1a = future_1a.result()
            result1b = future_1b.result()
            result2a = future_2a.result()
            result2b = future_2b.result()
        print(f"Run #{i}\t{result1a}\t{result2a}")
        print(f"Run #{i}\t{result1b}\t{result2b}")
        results1.append(result1a)
        results1.append(result1b)
        results2.append(result2a)
        results2.append(result2b)

# Run #24 (91, 201896, 869558, 341849)    (90, 399999, 1822593, 577432)
# Run #24 (91, 164431, 698186, 288431)    (91, 38283, 138609, 91120)
# Run #25 (90, 399999, 1835966, 564059)   (91, 80960, 321768, 164023)
# Run #25 (90, 399999, 1833705, 566320)   (90, 399999, 1805842, 594183)
# Run #26 (91, 98982, 408567, 185356)     (91, 59803, 230039, 128810)
# Run #26 (90, 399999, 1834171, 565854)   (90, 399999, 1820424, 579601)
# Run #27 (90, 399999, 1834243, 565782)   (90, 399999, 1822048, 577977)
# Run #27 (91, 17303, 66322, 37527)       (90, 399999, 1823376, 576649)
# Run #28 (91, 44918, 177964, 91575)      (90, 399999, 1820565, 579460)
# Run #28 (91, 227538, 989772, 375487)    (91, 110919, 419419, 246126)
# Run #29 (90, 399999, 1834282, 565743)   (91, 153117, 633006, 285727)
# Run #29 (91, 102241, 421747, 191730)    (91, 116266, 474703, 222924)


# Statistic #0
#         Series 1 mean = 90.55
#         Series 2 mean = 90.53333333333333
#         Shapiro:         stat=     0.633, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=     0.176, p=     0.861   --> SAME distribution
#         Mann-Whitney:    stat=  1813.500, p=     0.937   --> SAME distribution


# Statistic #1
#         Series 1 mean = 266121.43333333335
#         Series 2 mean = 267490.45
#         Shapiro:         stat=     0.802, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=    -0.053, p=     0.958   --> SAME distribution
#         Mann-Whitney:    stat=  1794.500, p=     0.978   --> SAME distribution


# Statistic #2
#         Series 1 mean = 1197716.0666666667
#         Series 2 mean = 1189064.7666666666
#         Shapiro:         stat=     0.798, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=     0.071, p=     0.944   --> SAME distribution
#         Mann-Whitney:    stat=  2174.000, p=     0.050   --> DIFFERENT distribution


# Statistic #3
#         Series 1 mean = 399043.5333333333
#         Series 2 mean = 415908.93333333335
#         Shapiro:         stat=     0.812, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=    -0.498, p=     0.620   --> SAME distribution
#         Mann-Whitney:    stat=  1369.000, p=     0.024   --> DIFFERENT distribution


#-----------------------------------------------------------------        
    # SAT
# NOTE
# - comparing regular selection to pareto selection
# - last run without parallelisation
# --> Pareto select makes no differences OR it is bugged OR not used enough
#       Last possibility => try with longer genotypes to raise probability
#       of incompatible outcome vectors (or longer formulas)

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
                            kt=2, 
                            pareto_select=True, # <---
                            local_search=True,
                            crossover_rate=1.0, 
                            fitness_evaluator=fitness_evaluator)
        print(f"Run #{i}\t{result1}\t{result2}")
        results1.append(result1)
        results2.append(result2)
# Run #24 (91, 322344, 1446177, 487918)   (90, 399999, 1822438, 577587)
# Run #25 (90, 399999, 1834169, 565856)   (91, 191694, 798806, 351389)
# Run #26 (91, 195288, 838685, 333074)    (91, 70042, 277202, 143081)
# Run #27 (91, 60401, 242250, 120187)     (90, 399999, 1814971, 585054)
# Run #28 (91, 388694, 1778303, 553892)   (90, 399999, 1813086, 586939)
# Run #29 (91, 5213, 19475, 11834)        (91, 327762, 1457155, 509448)


# Statistic #0
#         Series 1 mean = 90.7
#         Series 2 mean = 90.6
#         Shapiro:         stat=     0.577, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=     0.803, p=     0.425   --> SAME distribution
#         Mann-Whitney:    stat=   495.000, p=     0.426   --> SAME distribution


# Statistic #1
#         Series 1 mean = 261295.53333333333
#         Series 2 mean = 244860.66666666666
#         Shapiro:         stat=     0.864, p=     0.001   --> Probably not Gaussian
#         Student T:       stat=     0.427, p=     0.671   --> SAME distribution
#         Mann-Whitney:    stat=   460.000, p=     0.886   --> SAME distribution


# Statistic #2
#         Series 1 mean = 1172603.0333333334
#         Series 2 mean = 1091061.4666666666
#         Shapiro:         stat=     0.863, p=     0.001   --> Probably not Gaussian
#         Student T:       stat=     0.455, p=     0.651   --> SAME distribution
#         Mann-Whitney:    stat=   528.000, p=     0.252   --> SAME distribution


# Statistic #3
#         Series 1 mean = 395201.1666666667
#         Series 2 mean = 378133.5333333333
#         Shapiro:         stat=     0.857, p=     0.001   --> Probably not Gaussian
#         Student T:       stat=     0.328, p=     0.744   --> SAME distribution
#         Mann-Whitney:    stat=   394.000, p=     0.412   --> SAME distribution

        
#-----------------------------------------------------------------        
# SAT
# NOTE adding RI does not seem to change the # of cache misses i.e., 
# the # of points in the search space that are considered during the search

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
                            kt=2, 
                            local_search=True,
                            random_immigrant=True, # <---
                            crossover_rate=1.0, 
                            fitness_evaluator=fitness_evaluator)
        print(f"Run #{i}\t{result1}\t{result2}")
        results1.append(result1)
#         results2.append(result2)
# Run #94 (90, 399999, 1834389, 565636)   (91, 93031, 535474, 487903)
# Run #95 (91, 130035, 543776, 236465)    (91, 59392, 306733, 346615)
# Run #96 (90, 399999, 1834310, 565715)   (90, 399999, 3423152, 976873)
# Run #97 (91, 5330, 19067, 12944)        (91, 31613, 144213, 203566)
# Run #98 (91, 351764, 1591998, 518617)   (91, 127944, 802187, 605233)
# Run #99 (90, 399999, 1834670, 565355)   (91, 131172, 828004, 614924)


# Statistic #0
#         Series 1 mean = 90.56
#         Series 2 mean = 90.91
#         Shapiro:         stat=     0.631, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=    -6.078, p=     0.000   --> DIFFERENT distributions
#         Mann-Whitney:    stat=  3250.000, p=     0.000   --> DIFFERENT distribution


# Statistic #1
#         Series 1 mean = 269755.28
#         Series 2 mean = 104432.77
#         Shapiro:         stat=     0.812, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=     8.953, p=     0.000   --> DIFFERENT distributions
#         Mann-Whitney:    stat=  8023.000, p=     0.000   --> DIFFERENT distribution


# Statistic #2
#         Series 1 mean = 1215746.3
#         Series 2 mean = 739191.72
#         Shapiro:         stat=     0.811, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=     3.903, p=     0.000   --> DIFFERENT distributions
#         Mann-Whitney:    stat=  7310.000, p=     0.000   --> DIFFERENT distribution


# Statistic #3
#         Series 1 mean = 402816.38
#         Series 2 mean = 409604.75
#         Shapiro:         stat=     0.810, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=    -0.195, p=     0.846   --> SAME distribution
#         Mann-Whitney:    stat=  5322.000, p=     0.432   --> SAME distribution
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



