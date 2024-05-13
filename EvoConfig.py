config = {
    'number_of_trials'          :   32, 
    'max_iterations'            :   100_000,
    'DOP_epoch_duration'        :   20_000,

    'DOP_transition_mirror'     :   False,
    'DOP_transition_alternate'  :   True,

    'SAT_instances'             :   ['CNFs/uf20-04.cnf', 
                                     'CNFs/uf20-05.cnf',
                                     'CNFs/uf20-04.cnf',
                                     'CNFs/uf20-05.cnf',
                                     'CNFs/uf20-04.cnf' ],
        # NOTE:
        #   1. value is always a list, even if it has only 1 element
        #   2. Len of list must be max_iterations / DOP_epoch_duration
        # pick from:    uf20-04.cnf     then    uf20-05.cnf
        #               uf100-04.cnf    then    uf100-05.cnf
        #               uf250-032.cnf   then    uf250-033.cnf
    'max_fitness'               :   91,
        # uf20  --> 91
        # uf100 --> 430
        # uf250 --> 1065
    'geno_size'                 :   250, 
        # pick from:    250     for     uf250-032.cnf
        #               100     for     uf100-04.cnf
        #               20      for     uf20-04.cnf
    'pop_size'                  :   50, 
        # pick from:    50  for     uf100-04.cnf & uf250-033.cnf
        #               25  for     uf20-04.cnf
    
    'kt'                        :   2,  
    'crossover_rate'            :   1.0, 
    'mutation_rate'             :   0.50,

    #local_search=True,
    'random_immigrant'          :   '', #'original', #'cached' #'cached+criterion'
    'pareto_select'             :   True
}