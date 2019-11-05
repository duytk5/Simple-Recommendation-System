import config
import mysql.connector
import tensorrec
from scipy.special import softmax


class Module:
    def __init__(self):
        # self.connection = mysql.connector.connect(host=config.HOST_DB,
        #                                           database=config.NAME_DB,
        #                                           user=config.USER_DB,
        #                                           password=config.PASS_DB)

        self.model = tensorrec.TensorRec()
        self.get_data()

    def get_data(self):
        interactions, user_features, item_features = tensorrec.util.generate_dummy_data(
            num_users=1000,
            num_items=20,
            interaction_density=.05,
            num_item_features=10,
            num_user_features=10,
            n_features_per_user=10,
            n_features_per_item=10
        )
        self.interactions, self.user_features, self.item_features = interactions, user_features, item_features

    def fit(self, epochs=1000):
        self.get_data()
        self.model.fit(self.interactions, self.user_features, self.item_features, epochs=epochs, verbose=True)
        pass

    def update(self):
        self.fit()
        return True

    def get_all(self):
        predictions = self.model.predict(user_features=self.user_features,
                                         item_features=self.item_features)
        result = []
        for x in predictions:
            result.append(softmax(x))
        return result
