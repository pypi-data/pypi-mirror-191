import time

import numpy
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin, clone
from joblib import Parallel, delayed
from catboost import CatBoostRegressor, Pool
from sklearn.neighbors import NearestNeighbors
from kolibri.distances.heom import HEOM
from kolibri.distances.hvdm import HVDM
from kolibri.automl.data_inspection import get_data_info
import category_encoders as ce
from tqdm import tqdm
from time import time

class LazyRegression(BaseEstimator, RegressorMixin):
    """
    Fits a linear regression, on sub sample of size n. The sample formed by the top n similar items to the
    sample to be predicted
    """


    def __init__(self, n_neighbors:int=10, algorithm='auto',  distance='heom', leaf_size:int=30,weight_by_distance=True,
                 weights = 'distance', nb_features_to_keep=8, nb_buckets=100, num_futures_dist_importance=10,posterior_sampling=True,
                 objective='RMSE', rsm=6, depth=6, boosting_type='Ordered',bootstrap_type='Bayesian', bagging_temperature=1,
                 learning_rate=0.03, l2_leaf_reg=3.0, iterations=100, verbose=False):
        "constructor"
        RegressorMixin.__init__(self)
        BaseEstimator.__init__(self)
        self.objective=objective
        self.rsm=rsm
        self.verbose=verbose
        self.depth=depth
        self.boosting_type=boosting_type
        self.bootstrap_type=bootstrap_type
        self.bagging_temperature=bagging_temperature
        self.iterations=iterations
        self.learning_rate=learning_rate
        self.l2_leaf_reg=l2_leaf_reg
        self.posterior_sampling=posterior_sampling
        self.estimator = CatBoostRegressor(learning_rate=self.learning_rate, l2_leaf_reg=self.l2_leaf_reg, iterations=self.iterations, posterior_sampling=self.posterior_sampling, objective=self.objective, rsm=self.rsm, depth=self.depth, bootstrap_type=self.bootstrap_type, bagging_temperature=self.bagging_temperature, verbose=False)
        self.algorithm=algorithm
        self.leaf_size=leaf_size
        self.n_neighbors=n_neighbors
        self.neigberhood=NearestNeighbors(n_neighbors=n_neighbors, algorithm=algorithm, leaf_size=leaf_size)
        self.weights=weights
        self.weight_by_distance=weight_by_distance
        self.encoder=None
        self.distance=distance
        self.nb_features_to_keep=nb_features_to_keep
        self.nb_buckets=nb_buckets
        self.num_futures_dist_importance=num_futures_dist_importance
    def fit(self, X, y):
        """
        Builds the tree model.
        :param X: numpy array or sparse matrix of shape [n_samples,n_features]
            Training data
        :param y: numpy array of shape [n_samples, n_targets]
            Target values. Will be cast to X's dtype if necessary
        :param sample_weight: numpy array of shape [n_samples]
            Individual weights for each sample
        :return: self : returns an instance of self.
        Fitted attributes:
        * `classes_`: classes
        * `tree_`: tree structure, see @see cl _DecisionTreeLogisticRegressionNode
        * `n_nodes_`: number of nodes
        """


        #convert to Dataframe if X is not a Dataframe
        if not isinstance(X, pd.DataFrame):
            X=pd.DataFrame(X).convert_dtypes()
            for col in X.columns:
                if X[col].dtype=="string":
                    X[col]=X[col].astype('object')

        #get column info to detect categorical columns
        data_info=get_data_info(X)
        self.categorical_ix = [c["id"] for c in data_info["categorical_columns"]]
        self.numerical_ix=[c["id"] for c in data_info["numerical_columns"]]
        #create and fit category encoder
        self.encoder = ce.OrdinalEncoder(X, handle_missing="return_nan")
        X=self.encoder.fit_transform(X)


        #create a mixed datatype distance measure
        if self.distance=='heom':
            distance_metric = HEOM(X, cat_ix=self.categorical_ix, encode_categories=False, nan_equivalents = [12345], num_futures_dist_importance=self.num_futures_dist_importance).get_distance
        elif self.distance=='hvdm':
            bins = numpy.linspace(min(y), max(y), self.nb_buckets)
            d_y = numpy.digitize(y, bins)
            distance_metric = HVDM(X, d_y, cat_ix=self.categorical_ix).get_distance

        elif self.distance=='vdm':
            distance_metric = HEOM(X, cat_ix=self.categorical_ix, encode_categories=False).get_distance
        else:
            raise Exception("Unknow distance measure. Expected 'heom', 'hvdm' or 'vdm' got :"+ self.distance)
        if not isinstance(X, numpy.ndarray):
            if hasattr(X, 'values'):
                X = X.values
        if not isinstance(X, numpy.ndarray):
            raise TypeError("'X' must be an array.")

        self.neigberhood.metric=distance_metric

        self.neigberhood.fit(X, y)
        self._y=numpy.array(y)
        self._feature_importance=self._get_feature_importance(X, y)
        return self


    def _get_feature_importance(self, X, y):
        self.estimator.fit(X, y)
        feature_importance=self.estimator.feature_importances_
        return numpy.argsort(-feature_importance)


    def predict(self, X):
        """
        Runs the predictions.
        """
        X=self.encoder.transform(X)
        #Neigherest Neigbors do not like nan values
        for x in X:
            for i in numpy.argwhere(pd.isnull(x)):
                x[i]=12345

        return [self._predict_one([x]) for x in tqdm(X.values)]

    def _predict_one(self, X):
        """Predict the target for the provided data.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_queries, n_features), \
                or (n_queries, n_indexed) if metric == 'precomputed'
            Test samples.
        Returns
        -------
        y : ndarray of shape (n_queries,) or (n_queries, n_outputs), dtype=int
            Target values.
        """

        if self.weights == "uniform":
            # In that case, we do not need the distances to perform
            # the weighting so we do not compute them.
            neigh_ind = self.neigberhood.kneighbors(X, return_distance=False)
            neigh_dist = None
        else:
            neigh_dist, neigh_ind = self.neigberhood.kneighbors(X)

        weights = self._get_weights(neigh_dist, self.weights)

        _y = self._y
        if _y.ndim == 1:
            _y = _y.reshape((-1, 1))

        _X = self.neigberhood._fit_X[:,self._feature_importance[:self.nb_features_to_keep]]

        estimator = clone(self.estimator)
        try:
            if weights is None:
                estimator.fit(_X[neigh_ind.ravel()], _y[neigh_ind.ravel()])
            else:
                train_data = Pool(
                    data=_X[neigh_ind.ravel()],
                    weight=weights.ravel(),
                    label=_y[neigh_ind.ravel()]
                )
                estimator.fit(train_data)

            y_pred=estimator.predict([X[0][self._feature_importance[:self.nb_features_to_keep]]])
        except Exception as e:
            if weights is None:
                y_pred = numpy.mean(_y[neigh_ind], axis=1)
            else:
                y_pred = numpy.empty((neigh_dist.shape[0], _y.shape[1]), dtype=numpy.float64)
                denom = numpy.sum(weights, axis=1)

                for j in range(_y.shape[1]):
                    num = numpy.sum(_y[neigh_ind, j] * weights, axis=1)
                    y_pred[:, j] = num / denom

        if self._y.ndim == 1:
            y_pred = y_pred.ravel()

        return y_pred[0]

    def _get_weights(self, dist, weights):
        """Get the weights from an array of distances and a parameter ``weights``.
        Assume weights have already been validated.
        Parameters
        ----------
        dist : ndarray
            The input distances.
        weights : {'uniform', 'distance'}, callable or None
            The kind of weighting used.
        Returns
        -------
        weights_arr : array of the same shape as ``dist``
            If ``weights == 'uniform'``, then returns None.
        """
        if weights in (None, "uniform"):
            return None

        if weights == "distance":
            # if user attempts to classify a point that was zero distance from one
            # or more training points, those training points are weighted as 1.0
            # and the other points as 0.0
            if dist.dtype is numpy.dtype(object):
                for point_dist_i, point_dist in enumerate(dist):
                    # check if point_dist is iterable
                    # (ex: RadiusNeighborClassifier.predict may set an element of
                    # dist to 1e-6 to represent an 'outlier')
                    if hasattr(point_dist, "__contains__") and 0.0 in point_dist:
                        dist[point_dist_i] = point_dist == 0.0
                    else:
                        dist[point_dist_i] = 1.0 / point_dist
            else:
                with numpy.errstate(divide="ignore"):
                    dist = 1.0 / dist
                inf_mask = numpy.isinf(dist)
                inf_row = numpy.any(inf_mask, axis=1)
                dist[inf_row] = inf_mask[inf_row]
            return dist

        if callable(weights):
            return weights(dist)

    def decision_function(self, X):
        """
        Calls *decision_function*.
        """
        raise NotImplementedError(  # pragma: no cover
            "Decision function is not available for this model.")


if __name__ == '__main__':
    # Example code of how the HEOM metric can be used together with Scikit-Learn
    import numpy as np


    columns_to_remove = ["isThere_SST", "isThere_TRP", "CA realise", "Annee", "Numdo"]
    # Load the dataset from sklearn
    data_origin = pd.read_excel("/Users/mohamedmentis/Downloads/TrainingData_CoutPI_et_CA_082022.xlsx")

    data=data_origin.drop(columns=columns_to_remove)

    lr=LazyRegression(weight_by_distance=True)
    target=data["PRR_PI"]

    lr.fit(data.drop(columns=["PRR_PI"]), target)
    test_data=pd.read_excel("/Users/mohamedmentis/Downloads/PI MALE 24012023.xlsx").drop(columns=columns_to_remove, errors='ignore')

    print(lr.predict(test_data.drop(columns=["PRR_PI"])))