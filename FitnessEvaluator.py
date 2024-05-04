from randomdict.randomdict import RandomDict
class FitnessEvaluator(object):
        
    def __init__(self, fitness_function, max_fitness):
        self.max_fitness = max_fitness
        #pass # if we init fields here, the constructor is run everytime we create a singleton
        self.cache_hits = 0
        self.cache_misses = 0
        self.fitness_cache = RandomDict()
        self.outcome_cache = RandomDict()
        self.fitness_function = fitness_function
        self.dual_mode = False
            
    def evaluate(self, genotype):
        
        if self.dual_mode: 
            key = tuple([(1-genotype[i]) for i in range(len(genotype))])
        else:
            key = tuple(genotype)

        if key in self.fitness_cache:
            self.cache_hits += 1
            return self.fitness_cache[key], self.outcome_cache[key]
        else:
            self.cache_misses += 1
            fitness_value, outcomes = self.fitness_function(genotype)
            self.fitness_cache[key] = fitness_value
            self.outcome_cache[key] = outcomes
            return fitness_value, outcomes
    
    def report_cache_usage(self):
        return (self.cache_hits , self.cache_misses)
    
    def zero_cache_usage(self):
        self.cache_hits = 0
        self.cache_misses = 0
        self.fitness_cache.clear()
        self.outcome_cache.clear()
    
    def set_dual_mode(self, value):
        if value == True or value == False:
            self.dual_mode = value

class DualFitnessEvaluator(FitnessEvaluator):
     def evaluate(self, genotype):
        if genotype[0] == 0:
            phenotype = genotype[1:]
        else:
            phenotype = [1-x for x in genotype[1:]]

        return super().evaluate(phenotype)