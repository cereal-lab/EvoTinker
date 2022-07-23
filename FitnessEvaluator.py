class FitnessEvaluator(object):
        
    def __init__(self, fitness_function, max_fitness):
        self.max_fitness = max_fitness
        #pass # if we init fields here, the constructor is run everytime we create a singleton
        self.cache_hits = 0
        self.cache_misses = 0
        self.fitness_cache = {}
        self.outcome_cache = {}
        self.fitness_function = fitness_function
            
    def evaluate(self, genotype):
        key = tuple(genotype)
        #print("Evaluating", self.cache_hits, self.cache_misses)
        if key in self.fitness_cache.keys():
            self.cache_hits += 1
            return self.fitness_cache[key], self.outcome_cache[key]
        else:
            self.cache_misses += 1
            fitness_value, outcomes = self.fitness_function(genotype)
            self.fitness_cache[key] = fitness_value
            self.outcome_cache[key] = outcomes
            #print("after", self.fitness_cache)
            return fitness_value, outcomes
    
    def report_cache_usage(self):
        return (self.cache_hits , self.cache_misses)
    
    def zero_cache_usage(self):
        self.cache_hits = 0
        self.cache_misses = 0
        self.fitness_cache.clear()
