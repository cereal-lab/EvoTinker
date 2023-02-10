fitness_evaluator = FitnessEvaluator(sat.evaluate_formula, 91)

                    executor.submit(    evolve_1plus1ga, 
                                        geno_size=20, 
                                        #mutation_rate = 0.75,
                                        max_iterations=40_000, 
                                        improve_method="by_reset",
                                        recombination=10,
                                        fitness_evaluator=fitness_evaluator))
Run duration = 1941.2101500839926
