from __future__ import division
from __future__ import print_function
from ortools.sat.python import cp_model


my_dict={}
class TeachersPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, period, num_teacher, num_days, num_period, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._period = period
        self._num_teacher = num_teacher
        self._num_days = num_days
        self._num_period = num_period
        self._solutions = set(sols)
        self._solution_count = 0

    def on_solution_callback(self):
        self._solution_count += 1
        
        if self._solution_count in self._solutions:
            #print('Solution %i' % self._solution_count)
            for d in range(self._num_days):
                #print('Day %i' % d)
                my_dict[d]={}
                for n in range(self._num_teacher):
                    is_working = False
                    for s in range(self._num_period):
                        if self.Value(self._period[(n, d, s)]):
                            is_working = True
                            #print('  teacher%i teaches on period %i' % (n, s))
                            my_dict[d][s]=n
                    if not is_working:
                        #print('  teacher {} does not teach'.format(n))
                        continue
            print()
        return my_dict

    def solution_count(self):
        return self._solution_count




def main( num_teacher,num_period,num_days):
    # Data. 
    all_teachers = range(num_teacher)
    all_period = range(num_period)
    all_days = range(num_days)
    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    
    period = {}
    for n in all_teachers:
        for d in all_days:
            for s in all_period:
                period[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d,
                                                                          s))

    
    for d in all_days:
        for s in all_period:
            model.Add(sum(period[(n, d, s)] for n in all_teachers) == 1)

   
    for n in all_teachers:
        for d in all_days:
            model.Add(sum(period[(n, d, s)] for s in all_period) <= 2)

    
    min_period_per_teacher = 1 
    max_period_per_teacher = 10
    for n in all_teachers:
        num_period_worked = sum(
            period[(n, d, s)] for d in all_days for s in all_period)
        model.Add(min_period_per_teacher <= num_period_worked)
        model.Add(num_period_worked <= max_period_per_teacher)

    # Creates the solver and solve.
    solver = cp_model.CpSolver()

    a_few_solutions = range(2)
    solution_printer = TeachersPartialSolutionPrinter(
        period, num_teacher, num_days, num_period, a_few_solutions)
    solver.SearchForAllSolutions(model, solution_printer)

    return my_dict
    
    


if __name__ == '__main__':
    main()
