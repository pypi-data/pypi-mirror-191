# %%
import os
os.environ["MKL_NUM_THREADS"] = "4"
os.environ["NUMEXPR_NUM_THREADS"] = "4"
os.environ["OMP_NUM_THREADS"] = "4"
from joblib import delayed, Parallel

import numpy as np
import pandas as pd
# from scipy.stats import norm
from numba_stats import norm
from statsmodels.base.model import GenericLikelihoodModel
import warnings
np.errstate(all="raise")
import functools

from linearmodels.panel.data import PanelData
from linearmodels import PanelOLS
from linearmodels.panel.model import PanelFormulaParser
from linearmodels.panel.utility import check_absorbed, not_absorbed, AbsorbingEffectError

from .cm import cm_4, cm_10

from functools import reduce

class UnequalRowException(Exception):
    pass


def get_mle_betas(res, regimes):

    beta0_mle = res.params[0:regimes]

    beta1_mle = res.params[regimes : 2 * regimes]

    return beta0_mle, beta1_mle, np.append(beta0_mle, beta1_mle)


def get_mle_sigmas(res, regimes):
    """
    Get sigmas from MLE estimation, then transform back (take absolute value)
    """

    return np.abs(res.params[2 * regimes : 3 * regimes])

def _reorganize_gaul_ind(ind):
    ind[5], ind[6] = ind[6], ind[5]
    ind[8], ind[9] = ind[9], ind[8]
    return ind

class DriverSpecificProbUberMLE(GenericLikelihoodModel):
    """An Uber MLE with two things different:
    - Gets rid of lambda as parameters
    - Uses driver-specific probabilities in likelihood
    - Uses bounding and constrained optimization for probabilities
    
    Uses full probabilities in classifier cols, not categoricals
    """
    
    def __init__(self, 
                 endog,
                 exog,
                 classifier_pred, 
                 classifier_true_ind=None,
                 classifier_ind = None,
                 classifier_ind_name = None,
                 entity_effects = False,
                 time_effects = False,
                 other_effects=None,
                 weights=None,
                 drop_absorbed=False,
                 check_rank=True,
                 singletons = True,
                 check_absorbed=True,
                 cm=None,
                 **kwargs):
        
        print("Initializing...")    
        
        self.cm = cm
        self.check_absorbed= check_absorbed 
        self.classifier_true_ind = classifier_true_ind
        if classifier_true_ind is not None:
            self._classifier_true_ind_name = classifier_true_ind.name

        if classifier_ind is None:
            self._group = endog.index.get_level_values(2).name
            if self._group == 'gaul':
                self.classifer_ind = _reorganize_gaul_ind(endog.index.get_level_values(2).unique().tolist())
            endog.reset_index(2, inplace=True)
            exog.reset_index(2, inplace=True)
        else:
            self.classifier_ind = classifier_ind
            self._group = classifier_ind_name
    
        if not all([classifier_ind is not None, classifier_ind_name]):
            raise Exception("If either `classifier_ind` or `classifier_ind_name` is defined, the other must be defined as well, but ")
                
        self.classifier_pred = classifier_pred
        if self.classifier_pred is not None:
            self.classifier_map = {k:v for k,v in zip(self.classifier_pred.columns, self.classifier_ind.cat.categories)}
        
        endog_cat = (
            endog
            .assign(gaul_class = self.ind)
            .assign(gaul = self.classifier_ind)
            .query(f"gaul==gaul_class")
            .drop(columns=['gaul', 'gaul_class'])
            )
        
        
        exog_cat = (
            exog
            .assign(gaul_class = self.ind)
            .assign(gaul = self.classifier_ind)
            .query(f"gaul==gaul_class")
            .drop(columns=['gaul', 'gaul_class'])
            )
        
        try:
            self.p_model = PanelOLS(dependent=endog_cat,
                    exog=exog_cat,
                    weights=weights,
                    entity_effects=entity_effects,
                    time_effects=time_effects,
                    other_effects=other_effects,
                    singletons=singletons,
                    drop_absorbed=drop_absorbed,
                    check_rank=check_rank)
        except ValueError as e:
            print(e, "skipping...")
        
        self.p_model_full = PanelOLS(dependent=endog,
                exog=exog,
                weights=weights,
                entity_effects=entity_effects,
                time_effects=time_effects,
                other_effects=other_effects,
                singletons=singletons,
                drop_absorbed=drop_absorbed,
                check_rank=check_rank)
        
        self.endog_cat = self.p_model_full.dependent.dataframe
        self.exog_cat = self.p_model_full.exog.dataframe
        
        self.endog_full = self.p_model_full.dependent.dataframe.assign(**{self._group : self.classifier_ind})
        self.exog_full = self.p_model_full.exog.dataframe.assign(**{self._group : self.classifier_ind})

        super().__init__(endog=self.endog_cat, 
                         exog=self.exog_cat, **kwargs)
    
        self.entity_effects = self.p_model_full.entity_effects
        self.time_effects = self.p_model_full.time_effects
        
        if self.entity_effects and self.time_effects:
            self.demean = 'both'
        elif self.entity_effects and not self.time_effects:
            self.demean = 'entity'
        elif not self.entity_effects and self.time_effects:
            self.demean = 'time'
        else:
            self.demean = None
        
        if self.entity_effects or time_effects:    
            # Check for multiindex
            if not isinstance(exog.index, pd.MultiIndex):
                raise Exception("Dataframe not a multi-index")
        
        self.n_regimes = classifier_ind.nunique()
            
        self._drop_absorbed = drop_absorbed
        
        self._equal_regime = True
        if self.endog_full.groupby(self._group)[self.p_model_full.dependent.vars[0]].count().nunique() > 1:
            warnings.warn("Warning: observations across regimes is not the same, switching to slower method...")
            self._equal_regime=False
            
        self._get_vars_index = []
        self._get_vars = [] 
        self.entity, self.time = self.endog_cat.index.names
            
    @classmethod
    def from_formula(
        cls,
        formula,
        data,
        classifier_pred=None, 
        classifier_true_ind=None,
        other_effects=None,
        weights=None,
        drop_absorbed=False,
        check_rank=True,
        singletons = True,
        check_absorbed=True,
        cm=None,
        **kwargs
    ):
        
        data, classifier_ind_name = data.reset_index(2), data.index.get_level_values(2).name
        
        if classifier_ind_name == 'gaul':
            classifier_ind = data[classifier_ind_name].unique().tolist()
            classifier_ind = _reorganize_gaul_ind(classifier_ind)
        else:
            classifier_ind = data[classifier_ind_name].unique().tolist()
            
        if classifier_pred is None:
            print("individual level predictions not provided, will only use confusion matrix")
            
        if classifier_pred is None and classifier_true_ind is None:
            raise Exception("Must specify either classifier_pred or classifier_true_ind")
        
        parser = PanelFormulaParser(formula, data)
        
        endog, exog = parser.data

        mod = cls(
            endog = endog,
            exog = exog,
            classifier_pred=classifier_pred, 
            classifier_true_ind = classifier_true_ind,
            classifier_ind = data[classifier_ind_name].astype(pd.CategoricalDtype(classifier_ind, ordered=True)),
            classifier_ind_name = classifier_ind_name,
            entity_effects = parser.entity_effect,
            time_effects = parser.time_effect,
            other_effects=other_effects,
            weights=weights,
            drop_absorbed=drop_absorbed,
            check_rank=check_rank,
            singletons = singletons,
            check_absorbed=check_absorbed,
            cm=cm,
            **kwargs
        )
                
        mod.formula=formula
        
        return mod
    
    def demean_data(self, data):
        if self.demean=='entity':
            return data.groupby(self.entity).transform(lambda x: x - x.mean())
        elif self.demean == 'time':
            return data.groupby(self.time).transform(lambda x: x - x.mean())
        elif self.demean == 'both':
            return data.groupby(self.entity).transform(lambda x: x - x.mean()).groupby(self.time).transform(lambda x: x - x.mean())
        else:
            return data
        
    @functools.lru_cache(maxsize=128)
    def _regime_list(self, lm):       
        return np.array([group.drop(columns=self._group).pipe(self.demean_data).values \
            for _, group in getattr(self, lm).groupby(self._group)])
              
    @functools.cached_property
    def X(self):
        X = self._regime_list('exog_full')
            
        if self.check_absorbed:
            # (regimes, rows, columns)
            
            exception_flag = False
            for i, regime in enumerate(X):
                try:
                    check_absorbed(regime, self.exog_full.columns.tolist())
                except AbsorbingEffectError as e:
                    get_vars = {i for i in self.exog_full.columns.tolist() if i in str(e)}
                    get_vars.discard("Intercept")
                    
                    print(f"""Multicollinearity Alert!
                    For regime: {list(self.classifier_map.values())[i]}
                    
                    {get_vars}
                            
                    """)
                    if self._drop_absorbed:
                        self._get_vars_index.append(self.exog_full.columns.get_indexer(get_vars))
                        self._get_vars.append(get_vars)
                    else:
                        exception_flag = True
            if exception_flag:
                raise AbsorbingEffectError
            
            if self._get_vars and reduce(lambda x, y: x.intersection(y), self._get_vars):
                raise AbsorbingEffectError(f"""
                                            Common Absorbed Variables across regimes:
                                            
                                            {reduce(lambda x, y: x.intersection(y), self._get_vars)}
                                            """)
                
        return X
    
    @functools.cached_property
    def y(self):
        return self._regime_list('endog_full')
    
    @functools.cached_property
    def ind(self):
        if self.classifier_pred is not None:
            return self.classifier_pred.idxmax(axis=1).map(self.classifier_map)
        else:
            return self.classifier_true_ind.reset_index(self._group, drop=True)
    
    @functools.cached_property
    def p(self):
        if self.classifier_pred is not None:
            return self.classifier_pred.values
        else:
            return np.ones((self.y.shape[0], self.n_regimes))
    
    @functools.cached_property
    def p_slow(self):
        
        entity = self.p_model_full.dependent.index.names[0]
        time = self.p_model_full.dependent.index.names[1]
        
        p = (
            self.classifier_pred
            .reset_index([time], drop=True)
            .reset_index()
            .drop_duplicates([entity])
            .set_index([entity])
        )
        
        # merge into y to get dates for each driver
        
        p_list = [
            i.dataframe
            .reset_index(time)
            .merge(p, left_index=True, right_index=True)
            .drop(columns=[time, self.p_model_full.dependent.vars[0]]) \
                for i in self._regime_list('endog_full')
        ]
        
        return p_list

    def _ll(self, params):
                
        if self.cm is None:
            if self.n_regimes == 4:
                cm = cm_4

            elif self.n_regimes == 10:
                cm = cm_10
        else:
            cm = self.cm.astype(float)

        # generate X so that we can for absorbed variables
        X = self.X
        
        if X.ndim ==1:
            raise Exception("Regimes not of equal size...")
        
        results_df = pd.Series(params, index=self._param_order)
        
        beta_df = results_df.loc[results_df.index != 'sigma']
        sigma = sigma = results_df.loc[results_df.index=='sigma'].values[0]
            
        if self._drop_absorbed and self._get_vars_index:
            Xb = np.empty((self.n_regimes, self.exog.shape[0]))
            # subset X and multiply by new beta vector
            for i, (x, no_retain, no_retain_names) in enumerate(zip(X, self._get_vars_index, self._get_vars)):
                beta_vec = beta_df.loc[lambda df: ~df.index.isin(no_retain_names)].values
                Xb[i, :] = np.delete(x, no_retain, axis=1) @ beta_vec
        else:
            beta_vec = beta_df.values
            Xb = X @ beta_vec
        
        # loc = (np.squeeze(self.y) - Xb)/sigma
        # rnl = (norm._pdf(loc)/sigma).T
        rnl = norm.pdf(np.squeeze(self.y), Xb, scale=np.abs(sigma)).T

        # get row_maxes for probabilities
        row_maxes = self.p.max(axis=1, keepdims=True)
        class_ind = np.where(self.p==row_maxes, self.p, 0)
        return np.log((rnl*(class_ind@cm.T)).sum(axis=1))

    def _params_to_ll(self, params):

        # Since we always put the covariates at the end, take them out from the end
        # regime_params = res.params.values[:-num_covariates]        
        
        beta_vec =params[:-1]
        sigma_vec = params[-1]
            
        return beta_vec, sigma_vec

    def nloglikeobs(self, params):
        """Negative log-likelihood for an observation. The params matrix is the strange thing here
        and needs to be better defined.

        Args:
            params (ndarray): The matrix of parameters to optimize

        """

        # beta_vec, sigma_vec = self._params_to_ll(params)

        ll = self._ll(
            params=params
        )

        return -ll

    def bounds(self, num_exog, sigma_bound):
        
        # Now set up bounds on variables
        beta_bounds = [(None, None) for i in range(num_exog-1)]
        
        sigma_bounds = [sigma_bound]

        bounds = tuple(beta_bounds + sigma_bounds)

        return bounds
    
    def _start_params(self, show_ols = False, cluster_var=None, start_params_res=None):
        """Runs OLS regression to get start params for MLE coefficients"""
                
        print("Creating starting values...")
        
        if start_params_res is not None:
            res = start_params_res
        else:
            if cluster_var is None:
                res = self.p_model.fit()
            else:
                res = self.p_model.fit(cov_type="clustered", clusters=cluster_var)
                    
        # Now get sigma
        sigma = self.endog.std()
        
        results_df = pd.concat([res.params, 
                                pd.DataFrame([sigma], index=['sigma'])])
        if show_ols:
            print(res.summary)          
        
        return results_df, res
    
    def fit(
        self,
        method=None,
        maxiter=10000,
        maxfun=5000,
        sigma_bound=None,
        cluster_var=None,
        show_ols=False,
        start_params_res=None,
        **kwds,
    ):

        results_df, pols_res = self._start_params(show_ols=show_ols, 
                                                  cluster_var=cluster_var,
                                                  start_params_res=start_params_res)
        
        self._param_order = results_df.index
        
        if kwds.get('cov_type') is None:
            cov_type='cluster'
            cov_kwds = {'groups' : cluster_var,
                        'df_correction' : True,
                        'use_correction' : True}
        else:
            cov_type = kwds.pop('cov_type', None)
            cov_kwds = kwds.pop('cov_kwds', None) 

        print("Optimizing...")
        optimize = super().fit(
            method=method,
            start_params=results_df.values,
            maxiter=maxiter,
            maxfun=maxfun,
            eps=1e-08,
            ftol=1e-10,
            bounds=self.bounds(num_exog = len(results_df), sigma_bound=sigma_bound),
            cov_type= cov_type,
            cov_kwds = cov_kwds,
            use_t=True,
            **kwds
        )
        
        return optimize, pols_res
        
