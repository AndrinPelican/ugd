
## Planned changes:

* implementation of optimal test-statistic

* make a draw object, which as lowest input has:
    * adjacency matrix
    * opt (control dict, with desired control variables)
    
    * opt Mixing time, and anz of simulation
    
Then generates the draws, and creates a weight matrix with the 
weights for the optimal statistic:

Further input, which can be changed also after generating the graphs

* statistic of interest: (either Utility, or edge utility, or testvariable)

    * this gets all parsed to edge utility function

Not changeable by the user:
    
* internally build up a dictionary, of info variables (on mixing)
    
* two matrices for calculating the statistic

    * the all one matrix minus the identity matrix
    * the matrix with the weights in the paper used


### Methods:

* plot
* test one sides
* test optimal, vs plain

