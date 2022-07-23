#-----------------------------------------------------------------        
    # ONEMAX Small size
    fitness_evaluator = FitnessEvaluator(OneMax, 100)
    for i in range(number_of_trials):
        result1 = evolve(   geno_size=100, 
                            max_iterations=800, 
                            pop_size=25, 
                            kt=5, 
                            crossover_rate=1.0, 
                            fitness_evaluator=fitness_evaluator)
        result2 = evolve(   geno_size=100, 
                            max_iterations=800, 
                            pop_size=25, 
                            kt=2, 
                            crossover_rate=1.0, 
                            fitness_evaluator=fitness_evaluator)
        print(f"Run #{i}\t{result1}\t{result2}")
        results1.append(result1)
        results2.append(result2)
    

#-----------------------------------------------------------------


    # ONEMAX Reasonable size 
    fitness_evaluator = FitnessEvaluator(OneMax, 1000)
    for i in range(number_of_trials):
        result1 = evolve(   geno_size=1000, 
                            max_iterations=20_000, 
                            pop_size=25, 
                            kt=5, 
                            crossover_rate=1.0, 
                            fitness_evaluator=fitness_evaluator)
        result2 = evolve(   geno_size=1000,
                            max_iterations=20_000, 
                            pop_size=25, 
                            kt=5, 
                            mutation_rate=0.001,
                            crossover_rate=1.0, 
                            fitness_evaluator=fitness_evaluator)        
        print(f"Run #{i}\t{result1}\t{result2}")
        results1.append(result1)
        results2.append(result2)

#-----------------------------------------------------------------
