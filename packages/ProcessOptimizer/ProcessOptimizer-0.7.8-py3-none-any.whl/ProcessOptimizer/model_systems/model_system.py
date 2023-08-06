import numpy as np
from ProcessOptimizer import expected_minimum

class ModelSystem:
    """
    Model System for testing the ProcessOptimizer. Instances of this class 
    will be used in the example notebooks. 

    Parameters:
    * `score` [callable]:
        Function for calculating the score of the system at a given point in 
        the parameter space. It is expected to have the following signature:

            def score(x, rng=np.random.default_rng(), noise_std=noise_value):
                # * x is the point in the parameter space where the score will 
                #   be evaluated. Note that x is in the original coordinates of
                #   the parameter space, not normalized coordinates. 
                # * rng is the random number generator used for adding noise 
                #   to the system. The user can set a seed through this 
                #   parameter. There must be a default value for this parameter. 
                # * noise_std is the standard deviation of the noise. There
                #   must be a default value for this parameter. 
                ....
                # The score of the system is returned
                return score

    * `space` [Space]:
        The parameter space in the form of a Space object. 

    * `true_min` [float]:
        The true minimum value of the score function within the parameter space. 
    """
    def __init__(self, score, space, true_min=None):
        self.space = space
        self.score = score
        if true_min is None:
            ndims = space.n_dims()
            points = space.lhs(ndims*10)
            scores = [score(point) for point in points]
            true_min = np.min(scores)
        self.true_min = true_min
        
    def result_loss(self, result):
        """Calculate the loss of the optimization result. 

        Parameters:
        * `result` [OptimizeResult object of scipy.optimize.optimize module]:
            The result of an optimization. 

        Returns
        * loss [float]:
            The loss of the system, i.e. the difference between the true system 
            value at the location of the model's expected minimum and the best 
            possible system value. 
        """
        # Get the location of the expected minimum
        model_x,_ = expected_minimum(result)
        # Calculate the difference between the score at model_x and the true minimum value
        loss = self.score(model_x, noise_std=0) - self.true_min
        return loss