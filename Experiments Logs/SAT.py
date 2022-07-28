TODOs
    .   try novelty search
    .   try pareto selection of pareto dominant CS
    x   try just the local search alone
    .   paper: need to look at not just iterations but unique hits
        e.g., see [*] experiment

#-----------------------------------------------------------------        
# reset vs. reset + tabu
#-----------------------------------------------------------------        
# --> no differences in terms of quality of solution 
# more uniques points considered by tabu reset but same # of iterations

    number_of_cores = 4
    number_of_trials = 25
    random.seed(422399)
    results1 = []
    results2 = []
    fitness_evaluator = FitnessEvaluator(sat.evaluate_formula, 91)

    for i in range(number_of_trials):        
        print(f"Algo #1 Run #{i}", end='\t')
        futures = []
        with ProcessPoolExecutor(4) as executor:
            for core in range(number_of_cores):
                futures.append(
                    executor.submit(    evolve_1plus1ga, 
                                        geno_size=20, 
                                        mutation_rate = 0.75,
                                        max_iterations=400_000, 
                                        improve_method="by_tabu_reset",
                                        fitness_evaluator=fitness_evaluator))
            print(f"Started", end='\t')
        results = []
        results += [tuple(r.result()) for r in futures]    
        results1 += [tuple(r) for r in results]
        print(f"DONE")
    
    for i in range(number_of_trials):        
        print(f"Algo #2 Run #{i}", end='\t')
        futures = []
        with ProcessPoolExecutor(4) as executor:
            for core in range(number_of_cores):
                futures.append(
                    executor.submit(    evolve_1plus1ga, 
                                        geno_size=20, 
                                        mutation_rate=0.75,
                                        max_iterations=400_000, 
                                        improve_method="by_reset",
                                        fitness_evaluator=fitness_evaluator))
            print(f"Started", end='\t')
        results = []
        for core in range(number_of_cores):
            results.append(futures[core].result())    
        results2 += [tuple(r) for r in results]
        print(f"DONE")
 





Statistic #0
        Series 1 mean = 90.71
        Series 2 mean = 90.66
        Shapiro:         stat=     0.569, p=     0.000   --> Probably not Gaussian
        Student T:       stat=     0.758, p=     0.449   --> SAME distribution
        Mann-Whitney:    stat=  5250.000, p=     0.449   --> SAME distribution


Statistic #1
        Series 1 mean = 235238.57
        Series 2 mean = 234344.16
        Shapiro:         stat=     0.881, p=     0.000   --> Probably not Gaussian
        Student T:       stat=     0.043, p=     0.966   --> SAME distribution
        Mann-Whitney:    stat=  5000.000, p=     1.000   --> SAME distribution


Statistic #2
        Series 1 mean = 0.0
        Series 2 mean = 33190.84
/Users/alessio/.local/share/virtualenvs/EvoTinker-vWdniWIs/lib/python3.8/site-packages/scipy/stats/_morestats.py:1758: UserWarning: Input data for shapiro has range zero. The results may not be accurate.
  warnings.warn("Input data for shapiro has range zero. The results "
        Shapiro:         stat=     1.000, p=     1.000   --> Probably Gaussian
        Student T:       stat=   -11.578, p=     0.000   --> DIFFERENT distributions
        Mann-Whitney:    stat=    50.000, p=     0.000   --> DIFFERENT distribution


Statistic #3
        Series 1 mean = 235240.57
        Series 2 mean = 201155.32
        Shapiro:         stat=     0.881, p=     0.000   --> Probably not Gaussian
        Student T:       stat=     1.824, p=     0.070   --> SAME distribution
        Mann-Whitney:    stat=  5841.000, p=     0.040   --> DIFFERENT distribution
((EvoTinker) ) alessio@Alessios-MBP EvoTinker %  
#-----------------------------------------------------------------        
# 0.75 mutation rate vs. reset CS at every iteration
#-----------------------------------------------------------------        
# [*] --> need to look at not just iterations but also hits / misses
#           on the fitness cache
# NOTE 
# - less iterations needed + better solution achieved
# - way less hits and more uniques (i.e., misses)
# - hits + uniques are < for the rset-based local search which makes
#   sense w/r to # of iterations also being lower
# Interpretation
#   does more uniques means better search

    number_of_cores = 4
    number_of_trials = 25
    random.seed(422399)
    results1 = []
    results2 = []
    fitness_evaluator = FitnessEvaluator(sat.evaluate_formula, 91)
    
    for i in range(number_of_trials):        
        print(f"Algo #1 Run #{i}", end='\t')
        futures = []
        with ProcessPoolExecutor(4) as executor:
            for core in range(number_of_cores):
                futures.append(
                    executor.submit(    evolve_1plus1ga, 
                                        geno_size=20, 
                                        mutation_rate = 0.75,
                                        max_iterations=400_000, 
                                        fitness_evaluator=fitness_evaluator))
            print(f"Started", end='\t')
        results = []
        results += [tuple(r.result()) for r in futures]    
        results1 += [tuple(r) for r in results]
        print(f"DONE")
    
    for i in range(number_of_trials):        
        print(f"Algo #2 Run #{i}", end='\t')
        futures = []
        with ProcessPoolExecutor(4) as executor:
            for core in range(number_of_cores):
                futures.append(
                    executor.submit(    evolve_1plus1ga, 
                                        geno_size=20, 
                                        max_iterations=400_000,
                                        #mutation_rate=None, # means that we reset the solution each time
                                        fitness_evaluator=fitness_evaluator))
            print(f"Started", end='\t')
        results = []
        for core in range(number_of_cores):
            results.append(futures[core].result())    
        results2 += [tuple(r) for r in results]
        print(f"DONE")
 
# Statistic #0
#         Series 1 mean = 90.25
#         Series 2 mean = 90.67
#         Shapiro:         stat=     0.633, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=    -6.239, p=     0.000   --> DIFFERENT distributions
#         Mann-Whitney:    stat=  2967.000, p=     0.000   --> DIFFERENT distribution


# Statistic #1
#         Series 1 mean = 333811.27
#         Series 2 mean = 235496.76
#         Shapiro:         stat=     0.581, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=     5.167, p=     0.000   --> DIFFERENT distributions
#         Mann-Whitney:    stat=  6994.500, p=     0.000   --> DIFFERENT distribution


# Statistic #2
#         Series 1 mean = 210087.51
#         Series 2 mean = 32410.68
#         Shapiro:         stat=     0.684, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=    19.390, p=     0.000   --> DIFFERENT distributions
#         Mann-Whitney:    stat=  9173.000, p=     0.000   --> DIFFERENT distribution


# Statistic #3
#         Series 1 mean = 123725.76
#         Series 2 mean = 203088.08
#         Shapiro:         stat=     0.760, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=    -6.452, p=     0.000   --> DIFFERENT distributions
#         Mann-Whitney:    stat=  3198.000, p=     0.000   --> DIFFERENT distribution
# ((EvoTinker) ) alessio@Alessios-MBP EvoTinker % 





#-----------------------------------------------------------------        
# different mutations rates just for the local search
#-----------------------------------------------------------------        
# NOTE
# - 75% mutation in the LS yields better results in terms of unique
#   points from the search space being considered
# - however, it also results in more iterations / hits on the 
#   fitness cache
    
    number_of_cores = 4
    number_of_trials = 25
    random.seed(422399)
    results1 = []
    results2 = []
    fitness_evaluator = FitnessEvaluator(sat.evaluate_formula, 91)
    
    for i in range(number_of_trials):        
        print(f"Algo #1 Run #{i}", end='\t')
        futures = []
        with ProcessPoolExecutor(4) as executor:
            for core in range(number_of_cores):
                futures.append(
                    executor.submit(    evolve_1plus1ga, 
                                        geno_size=20, 
                                        mutation_rate = 0.5,
                                        max_iterations=400_000, 
                                        fitness_evaluator=fitness_evaluator))
            print(f"Started", end='\t')
        results = []
        for core in range(number_of_cores):
            results.append(futures[core].result())    
        results1 += [tuple(r) for r in results]
        print(f"DONE")

    for i in range(number_of_trials):        
        print(f"Algo #2 Run #{i}", end='\t')
        futures = []
        with ProcessPoolExecutor(4) as executor:
            for core in range(number_of_cores):
                futures.append(
                    executor.submit(    evolve_1plus1ga, 
                                        geno_size=20, 
                                        max_iterations=400_000,
                                        mutation_rate=0.75,
                                        fitness_evaluator=fitness_evaluator))
            print(f"Started", end='\t')
        results = []
        for core in range(number_of_cores):
            results.append(futures[core].result())    
        results2 += [tuple(r) for r in results]
        print(f"DONE")

# Statistic #0
#         Series 1 mean = 90.63
#         Series 2 mean = 90.23
#         Shapiro:         stat=     0.611, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=     5.466, p=     0.000   --> DIFFERENT distributions
#         Mann-Whitney:    stat=  6811.000, p=     0.000   --> DIFFERENT distribution


# Statistic #1
#         Series 1 mean = 239488.41
#         Series 2 mean = 316401.84
#         Shapiro:         stat=     0.855, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=    -3.785, p=     0.000   --> DIFFERENT distributions
#         Mann-Whitney:    stat=  3506.500, p=     0.000   --> DIFFERENT distribution


# Statistic #2
#         Series 1 mean = 33407.31
#         Series 2 mean = 200895.27
#         Shapiro:         stat=     0.792, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=   -16.206, p=     0.000   --> DIFFERENT distributions
#         Mann-Whitney:    stat=  1278.500, p=     0.000   --> DIFFERENT distribution


# Statistic #3
#         Series 1 mean = 206083.1
#         Series 2 mean = 115508.57
#         Shapiro:         stat=     0.861, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=     7.192, p=     0.000   --> DIFFERENT distributions
#         Mann-Whitney:    stat=  7230.000, p=     0.000   --> DIFFERENT distribution
# ((EvoTinker) ) alessio@Alessios-MBP EvoTinker % 




#-----------------------------------------------------------------        
# comparing to local search only
#-----------------------------------------------------------------        
# NOTE
# - exps are run all in parallel for SSGA, then with a 2nd loop
#   for local search
# - need to refactor this junk w/ loops

    number_of_trials = 25
    results1 = []
    results2 = []
    random.seed(422399)
    fitness_evaluator = FitnessEvaluator(sat.evaluate_formula, 91)
    
    for i in range(number_of_trials):        
        with ProcessPoolExecutor(2) as executor:
            future_1a = executor.submit( evolve_ssga, 
                                        geno_size=20, 
                                        max_iterations=400_000, 
                                        pop_size=25, 
                                        kt=2, 
                                        local_search=True,
                                        crossover_rate=1.0, 
                                        fitness_evaluator=fitness_evaluator)
            future_1b = executor.submit( evolve_ssga, 
                                        geno_size=20, 
                                        max_iterations=400_000, 
                                        pop_size=25, 
                                        kt=2, 
                                        local_search=True,
                                        crossover_rate=1.0, 
                                        fitness_evaluator=fitness_evaluator)
            future_2a = executor.submit( evolve_ssga, 
                                        geno_size=20, 
                                        max_iterations=400_000, 
                                        pop_size=25, 
                                        kt=2, 
                                        local_search=True,
                                        crossover_rate=1.0, 
                                        fitness_evaluator=fitness_evaluator)
            future_2b = executor.submit( evolve_ssga, 
                                        geno_size=20, 
                                        max_iterations=400_000, 
                                        pop_size=25, 
                                        kt=2, 
                                        local_search=True,
                                        crossover_rate=1.0, 
                                        fitness_evaluator=fitness_evaluator)
            result1a = future_1a.result()
            result1b = future_1b.result()
            result2a = future_2a.result()
            result2b = future_2b.result()
        print(f"Algo #1 Run #{i}\t{result1a}\t{result2a}\t{result1b}\t{result2b}")
        results1.append(result1a)
        results1.append(result1b)
        results1.append(result2a)
        results1.append(result2b)

    for i in range(number_of_trials):        
        with ProcessPoolExecutor(2) as executor:
            future_1a = executor.submit( evolve_1plus1ga, 
                                        geno_size=20, 
                                        max_iterations=400_000, 
                                        fitness_evaluator=fitness_evaluator)
            future_1b = executor.submit( evolve_1plus1ga, 
                                        geno_size=20, 
                                        max_iterations=400_000, 
                                        fitness_evaluator=fitness_evaluator)
            future_2a = executor.submit( evolve_1plus1ga, 
                                        geno_size=20, 
                                        max_iterations=400_000, 
                                        fitness_evaluator=fitness_evaluator)
            future_2b = executor.submit( evolve_1plus1ga, 
                                        geno_size=20, 
                                        max_iterations=400_000, 
                                        fitness_evaluator=fitness_evaluator)
            result1a = future_1a.result()
            result1b = future_1b.result()
            result2a = future_2a.result()
            result2b = future_2b.result()
        print(f"Algo #2 Run #{i}\t{result1a}\t{result2a}\t{result1b}\t{result2b}")
        results2.append(result1a)
        results2.append(result1b)
        results2.append(result2a)
        results2.append(result2b)

# Statistic #0
#         Series 1 mean = 90.57
#         Series 2 mean = 90.64
#         Shapiro:         stat=     0.629, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=    -1.010, p=     0.314   --> SAME distribution
#         Mann-Whitney:    stat=  4650.000, p=     0.313   --> SAME distribution


# Statistic #1
#         Series 1 mean = 253568.72
#         Series 2 mean = 238718.86
#         Shapiro:         stat=     0.811, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=     0.701, p=     0.484   --> SAME distribution
#         Mann-Whitney:    stat=  5353.000, p=     0.374   --> SAME distribution


# Statistic #2
#         Series 1 mean = 1141284.28
#         Series 2 mean = 33712.62
#         Shapiro:         stat=     0.806, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=    15.780, p=     0.000   --> DIFFERENT distributions
#         Mann-Whitney:    stat=  9675.000, p=     0.000   --> DIFFERENT distribution


# Statistic #3
#         Series 1 mean = 380159.04
#         Series 2 mean = 205008.24
#         Shapiro:         stat=     0.822, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=     7.563, p=     0.000   --> DIFFERENT distributions
#         Mann-Whitney:    stat=  7380.000, p=     0.000   --> DIFFERENT distribution




#-----------------------------------------------------------------        
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
#     fitness_evaluator = FitnessEvaluator(sat.evaluate_formula, 91)
#     for i in range(number_of_trials):        
#         with ProcessPoolExecutor(2) as executor:
#             future_1a = executor.submit( evolve, 
#                                         geno_size=20, 
#                                         max_iterations=400_000, 
#                                         pop_size=25, 
#                                         kt=2, 
#                                         local_search=True,
#                                         crossover_rate=1.0, 
#                                         fitness_evaluator=fitness_evaluator)
#             future_1b = executor.submit( evolve, 
#                                         geno_size=20, 
#                                         max_iterations=400_000, 
#                                         pop_size=25, 
#                                         kt=2, 
#                                         local_search=True,
#                                         crossover_rate=1.0, 
#                                         fitness_evaluator=fitness_evaluator)
#             future_2a = executor.submit( evolve, 
#                                         geno_size=20, 
#                                         max_iterations=400_000, 
#                                         pop_size=25, 
#                                         kt=2, 
#                                         pareto_select=True, # <---
#                                         local_search=True,
#                                         crossover_rate=1.0, 
#                                         fitness_evaluator=fitness_evaluator)
#             future_2b = executor.submit( evolve, 
#                                         geno_size=20, 
#                                         max_iterations=400_000, 
#                                         pop_size=25, 
#                                         kt=2, 
#                                         pareto_select=True, # <---
#                                         local_search=True,
#                                         crossover_rate=1.0, 
#                                         fitness_evaluator=fitness_evaluator)
#             result1a = future_1a.result()
#             result1b = future_1b.result()
#             result2a = future_2a.result()
#             result2b = future_2b.result()
#         print(f"Run #{i}\t{result1a}\t{result2a}")
#         print(f"Run #{i}\t{result1b}\t{result2b}")
#         results1.append(result1a)
#         results1.append(result1b)
#         results2.append(result2a)
#         results2.append(result2b)




# # ------------ 50 trials w/ doubles
# # same as below


# Statistic #0
#         Series 1 mean = 90.56
#         Series 2 mean = 90.54
#         Shapiro:         stat=     0.631, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=     0.283, p=     0.778   --> SAME distribution
#         Mann-Whitney:    stat=  5100.000, p=     0.778   --> SAME distribution


# Statistic #1
#         Series 1 mean = 260220.39
#         Series 2 mean = 269737.53
#         Shapiro:         stat=     0.798, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=    -0.445, p=     0.657   --> SAME distribution
#         Mann-Whitney:    stat=  4848.000, p=     0.698   --> SAME distribution


# Statistic #2
#         Series 1 mean = 1173855.57
#         Series 2 mean = 1205064.86
#         Shapiro:         stat=     0.796, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=    -0.313, p=     0.755   --> SAME distribution
#         Mann-Whitney:    stat=  5892.000, p=     0.029   --> DIFFERENT distribution


# Statistic #3
#         Series 1 mean = 387497.77
#         Series 2 mean = 413391.32
#         Shapiro:         stat=     0.801, p=     0.000   --> Probably not Gaussian
#         Student T:       stat=    -0.900, p=     0.369   --> SAME distribution
#         Mann-Whitney:    stat=  3680.000, p=     0.001   --> DIFFERENT distribution




# ------------ 30 trials w/ doubles
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

    # Series 1 mean = 767125.12
    # Series 2 mean = 274288.87
    # Shapiro:         stat=     0.230, p=     0.000   --> Probably not Gaussian
    # Student T:       stat=    16.082, p=     0.000   --> DIFFERENT distributions
    # Mann-Whitney:    stat=  8948.000, p=     0.000   --> DIFFERENT distribution

#-----------------------------------------------------------------        
