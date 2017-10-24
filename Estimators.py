import random
import numpy as np
from Card import Card
from keras.models import Model, model_from_json
from keras.layers import Dense, Input


class Estimator(object):
    """
    An state-action value function estimator. All state inputs must already
    be transformed by a 'featurizer' before being used with Estimator methods.
    """

    def __init__(self):
        self.model = None

    def update(self, s, a, r, s_prime):
        raise NotImplementedError("This method must be implemented by"
                                  "your Estimator class.")

    def predict(self, s):
        raise NotImplementedError("This method must be implemented by"
                                  "your Estimator class")

    def save(self, name):
        raise NotImplementedError("This method must be implemented by"
                                  "your Estimator class")

    def load(self, name):
        raise NotImplementedError("This method must be implemented by"
                                  "your Estimator class")


class DQNEstimator(Estimator):

    def __init__(self, model=None, memory=100000, batch_size=1024, gamma=1,
                 target_update=5000):
        self.model = model
        self.target_model = None if model is None else model.copy()
        self.gamma = gamma
        self.memory = [([], 0, 0, [])]*memory
        self.batch_size = batch_size
        self.target_update = target_update
        self.update_rate = max(1, batch_size//8)
        self.t = 0

    def update(self, s, a, r, s_prime):
        """
        Fills one entry in the memory and updates the estimator.
        Args:
            s: np.array state where the action was taken
            a: int action taken at this timestep
            r: int reward after taking action a
            s_prime: np.array state after taking action a

        """
        # Circular buffer for memory.
        self.memory[self.t % len(self.memory)] = (s, a, r, s_prime)
        self.t += 1
        if self.t == len(self.memory)*2:
            # Prevent overflow, this might cause skidding in the update rate
            self.t = len(self.memory)

        if self.t >= len(self.memory) and self.t % self.target_update == 0:
            if self.target_model is not None:
                self.update_target()
        # If memory is full, we can start training
        if self.t >= len(self.memory) and self.t % self.update_rate == 0:
            # Randomly sample from experience
            minibatch = random.sample(self.memory, self.batch_size)
            # Initialize x and y for the neural network
            x = np.zeros((self.batch_size, len(s)))
            y = np.zeros((self.batch_size, Card.DIFFERENT_CARDS))

            # Iterate over the minibatch to fill x and y
            i = 0
            for ss, aa, rr, ss_prime in minibatch:
                # x is simply the state
                x[i] = ss
                # y are the q values for each action.
                y[i] = self.predict(ss)

                # We update the action taken ONLY.
                if ss_prime is not None:
                    # ss_prime is not None, so this is not a terminal state.
                    q_sa = self.predict_target(ss_prime)
                    y[i, aa] = rr/10 + self.gamma*np.max(q_sa)
                else:
                    # ss_prime is None so this is a terminal state.
                    y[i, aa] = rr/10
                i += 1

            self.model.train_on_batch(x, y)

    def predict(self, s):
        if self.model is None:
            print("Building NEW model.")
            self.model = self.build_and_compile_model(s)
        return self.model.predict(np.array(s)[np.newaxis, :])

    def predict_target(self, s):
        if self.target_model is None:
            print("Copying model to target model.")
            self.target_model = self.build_and_compile_model(s)
            if self.model is not None:
                self.update_target()
        return self.target_model.predict(np.array(s)[np.newaxis, :])

    def update_target(self):
        weights = self.model.get_weights()
        self.target_model.set_weights(weights)

    def build_and_compile_model(self, s, activation="tanh",
                                optimizer="adagrad", loss="mse"):
        """
        The model is 'lazily' initialized, so that we know the input size.
        This method initializes the model of the estimator.
        Args:
            s: Sample input to the network.
            activation: activation function for the hidden layers
            optimizer: optimizer for the neural network
            loss: loss function for the neural network

        """
        input_layer = Input(shape=(len(s),))
        denses = Dense(256, activation=activation,
                       kernel_initializer="random_uniform")(input_layer)
        denses = Dense(512, activation=activation,
                       kernel_initializer="random_uniform")(denses)
        denses = Dense(1024, activation=activation,
                       kernel_initializer="random_uniform")(denses)
        output = Dense(Card.DIFFERENT_CARDS, activation="linear")(denses)

        model = Model(input_layer, output)
        model.compile(optimizer=optimizer, loss=loss)
        return model

    def save(self, name):
        print("Saving {}".format(name))
        model_json = self.model.to_json()
        json_filename = "{}.json".format(name)
        with open(json_filename, "w") as json_file:
            json_file.write(model_json)
        weights_filename = "{}.h5".format(name)
        self.model.save_weights(weights_filename)
        print("Saved {}".format(name))

    def load(self, name, optimizer="adagrad", loss="mse"):
        json_filename = "{}.json".format(name)
        weights_filename = "{}.h5".format(name)
        json_file = open(json_filename, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        self.model.load_weights(weights_filename)
        self.model.compile(optimizer=optimizer, loss=loss)
