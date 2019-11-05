import numpy as np
import tensorrec
import tensorflow as tf
from scipy.special import softmax

# Build the model with default parameters
model = tensorrec.TensorRec()

# Generate some dummy data
interactions, user_features, item_features = tensorrec.util.generate_dummy_data(
    num_users=1000,
    num_items=20,
    interaction_density=.05,
    num_item_features=10,
    num_user_features=10,
    n_features_per_user=10,
    n_features_per_item=10
)

# print(interactions)
# print(user_features.toarray()[0])
# print(item_features)

# Fit the model for 5 epochs
model.fit(interactions, user_features, item_features, epochs=100, verbose=True)

# Predict scores and ranks for all users and all items
predictions = model.predict(user_features=user_features,
                            item_features=item_features)
predicted_ranks = model.predict_rank(user_features=user_features,
                                     item_features=item_features)
# print(predicted_ranks)
#
# # Calculate and print the recall at 10
r_at_k = tensorrec.eval.recall_at_k(predicted_ranks, interactions, k=10)
print(np.mean(r_at_k))
# print(predictions[0].shape)
