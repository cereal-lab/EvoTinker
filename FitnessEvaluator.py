class FitnessEvaluator(object):
        
    def __init__(self):
        #pass # if we init fields here, the constructor is run everytime we create a singleton
        self.cache_hits = 0
        self.cache_misses = 0
        self.fitness_cache = {}
        self.max_fitness = None
            
    def evaluate(self, genotype):
        key = tuple(genotype)
        #print("Evaluating", self.cache_hits, self.cache_misses)
        if key in self.fitness_cache.keys():
            self.cache_hits += 1
            return self.fitness_cache[key]
        else:
            self.cache_misses += 1
            fitness_value = self.OneMax(genotype)
            self.fitness_cache[key] = fitness_value
            #print("after", self.fitness_cache)
            return fitness_value
    
    def report_cache_usage(self):
        return (self.cache_hits , self.cache_misses)
    
    def zero_cache_usage(self):
        self.cache_hits = 0
        self.cache_misses = 0
        self.fitness_cache.clear()
    
    def OneMax(self, genotype):
        if self.max_fitness is None:
            self.max_fitness = len(genotype)
        return sum(genotype)
    



fitness_evaluator = FitnessEvaluator()