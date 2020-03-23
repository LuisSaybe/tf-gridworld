import tensorflow as tf
import random

class QEpsilonGreedyPolicy:
    def __init__(self, model, greedy_probability):
        self.model = model
        self.greedy_probability = greedy_probability

    def getAction(self, state, available_actions):
        random_action = random.choices([True, False], [self.greedy_probability, 1 - self.greedy_probability])[0]

        if random_action:
            return random.choice(available_actions)

        state_tensor = tf.one_hot([state], dtype='float32', depth=3)
        prediction = self.model.predict(state_tensor)
        values = prediction.tolist()[0]

        indexes = range(len(values))
        available_indexes = list(filter(lambda i : i in available_actions, indexes))
        maximum_value = max(map(lambda i : values[i], available_indexes))
        maximum_indexes = list(filter(lambda i : values[i] == maximum_value, available_indexes))

        return random.choice(maximum_indexes)
