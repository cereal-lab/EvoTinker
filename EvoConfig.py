config = {
    'number_of_trials'          :   32, 
    'max_iterations'            :   100_000,
    'DOP_epoch_duration'        :   20_000,

    'DOP_transition_mirror'     :   True,
    'DOP_transition_alternate'  :   False,

    'SAT_instances'             :   ['CNFs/uf20-04.cnf'], # for DOP_transition_mirror
    #'SAT_instances'             :   ['CNFs/uf20-04.cnf', # for DOP_transition_alternate w/ epock 20k / 100k
    #                                 'CNFs/uf20-05.cnf',
    #                                 'CNFs/uf20-04.cnf',
    #                                 'CNFs/uf20-05.cnf',
    #                                 'CNFs/uf20-04.cnf'],
        # NOTE:
        #   1. value is always a list, even if it has only 1 element
        #   2. Len of list must be max_iterations / DOP_epoch_duration
        # pick from:    uf20-04.cnf     then    uf20-05.cnf
        #               uf100-04.cnf    then    uf100-05.cnf
        #               uf250-032.cnf   then    uf250-033.cnf
    'max_fitness'               :   91,
        #                           91      -->     uf20
        #                           430     -->     uf100
        #                           1065    -->     uf250
    'geno_size'                 :   20, 
        # pick from:                250     -->     uf250
        #                           100     -->     uf100
        #                           20      -->     uf20
    'pop_size'                  :   25, 
        # pick from:                50      -->     uf100 & uf250
        #                           25      -->     uf20
    
    'kt'                        :   2,  
    'crossover_rate'            :   1.0, 
    'mutation_rate'             :   0.05,

    #local_search=True,
    'random_immigrant'          :   'cached', 
        # Pick from:                'original', 
        #                           'cached' 
        #                           'cached+criterion'
    'pareto_select'             :   False
}