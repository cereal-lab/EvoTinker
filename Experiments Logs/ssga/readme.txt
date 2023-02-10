
Run duration = 186.00410695798928

                    executor.submit(    evolve_ssga, 
                                        geno_size=20, 
                                        max_iterations=400_000, 
                                        pop_size=25, 
                                        kt=2, 
                                        #local_search=True,
                                        crossover_rate=1.0, 
                                        fitness_evaluator=fitness_evaluator))

fitness_evaluator = FitnessEvaluator(sat.evaluate_formula, 91)




