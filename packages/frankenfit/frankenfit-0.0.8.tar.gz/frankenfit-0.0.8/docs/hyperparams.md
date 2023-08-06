---
jupytext:
  formats: notebooks///ipynb,docs///md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.4
kernelspec:
  display_name: .venv-dev
  language: python
  name: python3
---

```{code-cell} ipython3
:tags: [remove-cell]

# FIXME: this cell should not appear in docs output
import matplotlib.pyplot as plt
plt.style.use('./dracula.mplstyle')

from pydataset import data
diamonds_df = data("diamonds")
```

# Hyperparameters

Any parameter of any [`Transform`](frankenfit.Transform) can be provided as a
**hyperparameter**, indicating that its value is **deferred** and
will not be known until [`fit()`](frankenfit.Transform.fit) is called, at which point
the caller of `fit()` must provide **bindings** for any needed hyperparameters, giving
them concrete values.

Hyperparameters can make a pipeline more re-usable: write the pipeline once, but get a
range of different behaviors by supplying different bindings at fit-time. In this way
one might build up a library of re-usable learning pipelines, ready to be composed with
each other and applied to different situations. Frankenfit also provides a library of
built-in transforms that use hyperparameter bindings to control how **child transforms**
are fit, which can be used to implement workflows like hyperparameter-search.

+++

## Replacing parameters with hyperparameters

If any parameter of a transform is an instance of [`ff.HP`](frankenfit.HP), then it is a
hyperparameter. For example, let's start with a small feature-preparation pipeline:

```{code-cell} ipython3
import numpy as np
import frankenfit as ff

prepare_features = (
    ff.DataFramePipeline()
    .winsorize(0.05, ["carat", "table", "depth"])
    .pipe(np.log1p, "carat")
    .z_score(["carat", "table", "depth"])
)
```

The pipeline above winsorizes three columns with a `limit` parameter of `0.05`, I the
top and bottom 5% of outliers are trimmed. We can replace this parameter with a
hyperparameter named `"my_limit"` like so:

```{code-cell} ipython3
prepare_features = (
    ff.DataFramePipeline()
    .winsorize(ff.HP("my_limit"), ["carat", "table", "depth"], tag="mywin")
    .pipe(np.log1p, "carat")
    .z_score(["carat", "table", "depth"])
)
prepare_features.visualize()
```

Notice that we've given the [`Winsorize`](frankenfit.dataframe.Winsorize) transform a
[tag](tagging-selecting-transforms) (`"mywin"`) so that we can select it by name. Doing
so shows that its `limit` paramater is indeed an `HP` object:

```{code-cell} ipython3
mywin = prepare_features.find_by_name("Winsorize#mywin")
mywin
```

Every `Transorm` object has a method [`hyperparams()`](frankenfit.Transform.hyperparams)
that returns the set of all hyperparameter names referenced by its parameters:

```{code-cell} ipython3
mywin.hyperparams()
```

If the transform in question has child transforms, then `hyperparams()` collects
hyperparameters recursively. For example, the pipeline `prepare_features`, which
contains the `Winsorize` transform, can tell us the hyperparameters used by all of its
children:

```{code-cell} ipython3
prepare_features.hyperparams()
```

### Resolving hyperparamters

We call the process of replacing the hyperparameters with concrete values **resolving**
the hyperparameters. A transform or pipeline with hyperparamters must be resolved before
it can be fit. For example, if we try to fit `prepare_features` without doing so, it
raises an [`UnresolvedHyperparameterError`](frankenfit.UnresolvedHyperparameterError):

```{code-cell} ipython3
try:
    prepare_features.fit(diamonds_df)
except ff.UnresolvedHyperparameterError as e:
    print(e)
```

To resolve the hyperparameters, we must supply a mapping from hyperparameter names to
concrete values, called the **bindings**. The
[`resolve()`](frankenfit.Transform.resolve) method returns a copy of a `Transform` with
any hyperparameters resolved against the provided bindings (or raises
`UnresolvedHyperparameterError` if it can't find some hyperparameters in the bindings):

```{code-cell} ipython3
mywin.resolve({"my_limit": 0.1})  # the limit param now has a concrete value
```

Most of the time, though, rather than calling `resolve()`, you'll want to resolve
hyperparameters when you [`fit()`](frankenfit.Transform.fit) a transform. In addition to
the fitting data, `fit()` accepts a `bindings` argument, or, as is often more
convenient, accepts any number of keyword arguments each of which is interpreted as a
binding from hyperparameter name to value:

```{code-cell} ipython3
help(prepare_features.fit)
```

Fitting the hyperparameterized `Winsorize` transform with a keyword argument for the
`"my_limit"` hyperparameter:

```{code-cell} ipython3
# Equivalent: mywin.fit(diamonds_df, {"my_limit": 0.1})
mywin_fit = mywin.fit(diamonds_df, my_limit=0.1)
mywin_fit
```

In the output above, one can see that the resulting
[`FitTransform`](frankenfit.FitTransform) instance shows a concrete value (`0.1`) for
the `limit` parameter of `Winsorize`.

Furthermore, via the [`bindings()` method](frankenfit.FitTransform.bindings), every
`FitTransform` object can tell us what bindings were used to the fit the `Transform`
from which it was obtained:

```{code-cell} ipython3
mywin_fit.bindings()
```

A copy of the originating `Transform`, with its hyperparameters resolved, is also
available via [`resolved_transform()`](frankenfit.FitTransform.resolved_transform):

```{code-cell} ipython3
mywin_fit.resolved_transform()
```

Bindings supplied to `fit()` propagate through to child transforms. Thus the
`prepare_features` pipeline, which contains the hyperparamterized `Winsorize`, can be
fit like this:

```{code-cell} ipython3
prepare_features.fit(diamonds_df, my_limit=0.2).apply(diamonds_df).head()
```

Finally, because [`Pipeline.apply()`](frankenfit.Pipeline.apply) is [syntactic sugar for
fitting-and-applying](fit-and-apply) a pipeline on the same dataset, it too accepts
hyperparameter bindings:

```{code-cell} ipython3
prepare_features.apply(diamonds_df, my_limit=0.2).head()
```

## Hyperparameters in column names

In the previous section we saw how to hyperparameterize a numerical parameter by
replacing it with an instance of [`ff.HP`](frankenfit.HP). Any sort of parameter can be
replaced by a hyperparameter in this way, but Frankenfit also provides more convenient
ways of referring to hyperparameters for more specialized situations.

A common use case is for the name of a column to be a hyperparameter, and to embed
hyperparameters in column names. To make this easy, all built-in `DataFrame` transforms
that accept column-name parameters (either individual column names or lists of column
names) treat those parameters as Python
[format-strings](https://docs.python.org/3/library/stdtypes.html#str.format) to be
formatted against the hyperparameter bindings at fit-time.

For example, suppose we have a pipeline like the following:

```{code-cell} ipython3
prepare_training_response = (
    ff.DataFramePipeline()
    .copy("price", "price_train")
    .winsorize(0.05, "price_train")
    .pipe(np.log1p, "price_train")
)
prepare_training_response.hyperparams()  # no hyperparams
```

The [`Copy`](frankenfit.dataframe.Copy), [`Winsorize`](frankenfit.dataframe.Winsorize),
and [`Pipe`](frankenfit.dataframe.Pipe) transforms all have column-name parameters.
Suppose we want to make the name of the response column (hard-coded as `"price"` above)
into a hyperparameter, so that this pipeline can be re-used more easily on other
datasets or for other prediction targets. We can write the column-name parameters as
format-strings that refer to a variable `response_col`, and Frankenfit will
automatically determine that this pipeline now expects a hyperparameter named
`"response_col"` whose value will be substituted into these parameters at fit-time:

```{code-cell} ipython3
prepare_training_response = (
    ff.DataFramePipeline()
    .copy("{response_col}", "{response_col}_train")
    .winsorize(0.05, "{response_col}_train")
    .pipe(np.log1p, "{response_col}_train")
)
prepare_training_response.hyperparams()  # "response_col" detected
```

We must now supply a value for `response_col` whenever we `fit()` this pipeline, or, as
below, whenever we `apply()` it [to its own fitting data](fit-and-apply):

```{code-cell} ipython3
prepare_training_response.apply(diamonds_df, response_col="price").head()
```

```{code-cell} ipython3
prepare_training_response.apply(diamonds_df, response_col="carat").head()
```

A somewhat more involved example demonstrates using a format-string amongst a list of
column names, allowing us to winsorize the features and training response all in the
same call to `winsorize()`:

```{code-cell} ipython3
prepare_features_and_response = (
    ff.DataFramePipeline()
    .copy("{response_col}", "{response_col}_train")
    .winsorize(ff.HP("win_limit"), ["carat", "table", "depth", "{response_col}_train"])
    .pipe(np.log1p, ["carat", "{response_col}_train"])
    .z_score(["carat", "table", "depth"])
)
prepare_features_and_response.hyperparams()
```

:::{tip}
User-defined ``Transforms`` can easily get the same behavior for own their column-like
parameters by using the field specifier `columns_field()`.
:::

:::{important}
Format strings used in this way must always refer to the *name* of a hyperparameter.
Using an empty (`{}`) or numeric (`{0}`) replacement field will fail to resolve as a
hyperparameter.
:::

+++

## Derived parameters with `HPLambda`

Writing a column-name parameter as `"{response_col}_train"` is an example of creating a
**derived parameter**, i.e., one whose fit-time value is not simply *equal to* some
hyperparameter's binding (as with [`ff.HP`](frankenfit.HP)) but is a string
*containing* a hyperparameter's binding. Using [`ff.HPLambda`](frankenfit.HPLambda), it
is possible to generalize this to any kind of derived parameter, not just a string,
whose fit-time value depends in an arbitrary way on hyperparameter bindings.

For example, here's a pipeline that copies three hard-coded columns and prepares them as
features:

```{code-cell} ipython3
prepare_features = (
    ff.DataFramePipeline()
    .copy(
        ["carat",     "table",     "depth"],
        ["carat_fea", "table_fea", "depth_fea"],
    )
    .winsorize(0.05, ["carat_fea", "table_fea", "depth_fea"])
    .z_score(["carat_fea", "table_fea", "depth_fea"])
)
```

Suppose that instead of hard-coding the list of columns to copy and transform, we want
to be able to provide the list as a hyperparameter. We can of course replace the first
parameter of copy with an `ff.HP` instance whose name will be bound to a list of column
names at fit-time, but how can we then refer to these unknown columns with a `"_fea"`
suffix added? That's where `ff.HPLambda` comes in:

```{code-cell} ipython3
hp_feature_cols = ff.HP("feature_cols")
hp_feature_cols_suffixed = ff.HPLambda(
    lambda feature_cols: [c + "_fea" for c in feature_cols]
)
prepare_features = (
    ff.DataFramePipeline()
    .copy(hp_feature_cols, hp_feature_cols_suffixed)
    .winsorize(0.05, hp_feature_cols_suffixed)
    .z_score(hp_feature_cols_suffixed)
)
prepare_features.hyperparams()
```

`HPLambda` inspects the signature of the function provided to it and treats the names of
any arguments (in this case `feature_cols`) as the names of hyperparameters whose
bindings should be passed to the function at fit-time to determine the value of the
parameter that was replaced by `HPLambda`.

Thus when we supply a binding for `feature_cols` at fit-time, the desired parameters of
`Copy`, `Winsorize`, and `ZScore` resolve as `[c + "_fea" for c in feature_cols]`:

```{code-cell} ipython3
prepare_features.apply(diamonds_df, feature_cols=["x", "y"]).head()
```

:::{tip}
Note that by combining transforms like [`assign()`](frankenfit.dataframe.Assign),
[`select()`](frankenfit.dataframe.Select) (a.k.a. `[]`) and
[`suffix()`](frankenfit.dataframe.Suffix)/[`prefix()`](frankenfit.dataframe.Prefix), one
can often avoid using `HPLambda`, and end up with more readable and idiomatic pipelines
than the one shown here. See {doc}`dataframes`.

For example, the version of `prepare_features` above could be re-written as:
```python
(
    ff.DataFramePipeline()
    .assign(
        ff.DataFramePipeline()
        .select(ff.HP("feature_cols"))
        .suffix("_fea")
        .winsorize(0.05)
        .z_score()
    )
)
```
:::

+++

## Hyperparameters in user-supplied functions

A number of transforms, like [`StatelessLambda`](frankenfit.universal.StatelessLambda),
[`StatefulLambda`](frankenfit.universal.StatefulLambda),
[`Pipe`](frankenfit.dataframe.Pipe) and others, accept a user-provided function as a
parameter. For example, earlier we provided the NumPy function `np.log1p` as the first
parameter of the `Pipe` transform to log-transform some specified columns.

```{code-cell} ipython3
(
    ff.DataFramePipeline()
    .copy("{response_col}", "{response_col}_train")
    .pipe(np.log1p, ["carat", "{response_col}_train"])
);
```

As with `HPLambda`, such a user-supplied function can also receive hyperparameter
bindings by including the desired hyperparameter names in its argument list. In the case
of `Pipe`, its parameter is expected to be a function accepting at least one positional
argument, the `DataFrame` to transform; any arguments after that are interpreted as
hyperparameter names, whose bindings will be supplied as named arguments when the
function is called.

Thus, instead of `np.log1p` (which is a mnemonic for "log of 1 plus..."), we can write
our own `log_x_plus` function that computes $\log(x + \text{df})$ where $x$ is a
hyperparameter, and pass that to `pipe()`:

```{code-cell} ipython3
import pandas as pd

def log_x_plus(df: pd.DataFrame, x: float):
    # x is a hyperparameter!
    return np.log(df + x)  # df needs to be on the left to trigger DataFrame.__add__

prepare_log_x_plus = (
    ff.DataFramePipeline()
    .copy("{response_col}", "{response_col}_train")
    .pipe(log_x_plus, ["carat", "{response_col}_train"])
)

# "x" is detected as a hyperparameter
prepare_log_x_plus.hyperparams()
```

Now if we fail to provide a binding for `x` when fitting this pipeline, it raises an
`UnresolvedHyperparameterError` as expected:

```{code-cell} ipython3
try:
    prepare_log_x_plus.apply(diamonds_df, response_col="price")
except ff.UnresolvedHyperparameterError as e:
    print(repr(e))
```

Taking $\log(100 + \text{carat})$ and $\log(100 + \text{price\_train})$:

```{code-cell} ipython3
prepare_log_x_plus.apply(diamonds_df, response_col="price", x=100.0).head()
```

Furthermore, if a hyperparameter argument of a user-supplied function has a default
value, then the hyperparameter is **optional**: if no binding is supplied at fit-time,
then the function receives the default value declared in its argument list.

Here's a variation on the above that computes $\log(n + \text{df})$ where $n$ defaults
to $1$ if it is not bound:

```{code-cell} ipython3
def log_n_plus(df: pd.DataFrame, n: float=1.0):
    # n is an optional hyperparameter with a default value of 1.0
    return np.log(df + n)

prepare_log_n_plus = (
    ff.DataFramePipeline()
    .copy("{response_col}", "{response_col}_train")
    .pipe(log_n_plus, ["carat", "{response_col}_train"])
)
prepare_log_n_plus.hyperparams()
```

Thus we may omit `n=` from the bindings:

```{code-cell} ipython3
# hyperparameter n defaults to 1.0 instead of raising UnresolvedHyperparameterError
prepare_log_n_plus.apply(diamonds_df, response_col="price").head()
```

## Dictionary parameters

Another common place to use hyperparameters is in the keys or values of a `dict`-type
parameter of a transform. For example, the [`SKLearn`](frankenfit.dataframe.SKLearn) and
[`Statsmodels`](frankenfit.dataframe.Statsmodels) transforms make it easy to use models
from the [scikit-learn](https://scikit-learn.org/) and
[statsmodels](https://www.statsmodels.org) libraries, respectively, in Frankenfit
pipelines. Their `class_params` parameters allow passing a dictionary of
library-specific arguments to the underlying models, and these dictionaries may contain
hyperparameters.

To illustrate, the following pipeline fits a
[`Lasso`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html)
regression from scikit-learn with hyperparameters determining the regularization
strength parameter `alpha` and whether to include an intercept term in the regression:

```{code-cell} ipython3
import sklearn.linear_model

lasso_regression = (
    ff.DataFramePipeline()
    .sk_learn(
        x_cols=["carat", "table"],
        response_col="{response_col}_train",
        hat_col="{response_col}_hat",
        sklearn_class=sklearn.linear_model.Lasso,
        class_params={
            "fit_intercept": ff.HP("fit_intercept"),
            "alpha": ff.HP("alpha")
        }
    )
)

lasso_regression.hyperparams()
```

## Designing pipelines with hyperparameters

Given some thought, hyperparameters allow you to create libraries of generically
re-usable pipelines that can be applied to different problems. Some built-in transforms
that are especially useful in this regard include
[`IfHyperparamIsTrue`](frankenfit.universal.IfHyperparamIsTrue) and
[`IfHyperparamLambda`](frankenfit.universal.IfHyperparamLambda), with which you can
introduce branches and conditional logic in your pipelines.

In [Concatenating pipelines](concatenating-pipelines) we decomposed our diamond-modeling
pipeline into three smaller pipelines, separating response preparation from feature
preparation and price-prediction. To give a flavor what can be done with
hyperparameters, below we take this a step further and convert those sub-pipelines into
fully generic versions that can be applied to any problem where we want to:
* prepare a training response variable by winsorizing and optionally log-transforming
  some input column;
* prepare some set of feature columns by winsorizing and z-scoring them, with some
  optional subset to be log-transformed;
* fit any scikit-learn model to predict the prepared training response with the prepared
  features.

```{code-cell} ipython3
# Use "do" as shorthand for DataFramePipeline()
do = ff.DataFramePipeline()

# Add a training response column derived from raw response.
#
# Hyperparameters
# ---------------
# response_col: str
#   The name of the column to prepare as training response.
#
# log_response: bool, optional
#   Whether to log1p-transform the training response.
prepare_training_response = (
    do
    .copy("{response_col}", "{response_col}_train")
    .winsorize(0.05, "{response_col}_train")
    .if_hyperparam_is_true(
        "log_response",
        do.pipe(np.log1p, "{response_col}_train"),
    )
)

# Prepare feature columns by replacing them with trimmed and standardized values.
#
# Hyperparameters
# ---------------
# feature_cols: list[str]
#   The names of the columns to prepare as features.
#
# log_feature_cols: list[str], optional
#   Optional names of columns to log transform before z-scoring
prepare_features = (
    do
    .winsorize(0.05, ff.HP("feature_cols"))
    .if_hyperparam_is_true(
        "log_feature_cols",
        do.pipe(np.log1p, ff.HP("log_feature_cols")),
    )
    .z_score(ff.HP("feature_cols"))
)

# Predict training response column with an sklearn model.
#
# Hyperparameters
# ---------------
# regression_class: type
#   Class object from sklearn.
#
# regression_params: dict
#   Dictionary of arguments to provide to regression_class.
#
# response_col: str
#   Target {response_col}_train.
#
# feature_cols: list[str]
#   The names of the predictor columns.
#
# log_response: bool, optional
#   Whether to expm1-transform hat column.
predict_response = (
    do
    .sk_learn(
        sklearn_class=ff.HP("regression_class"),
        x_cols=ff.HP("feature_cols"),
        response_col="{response_col}_train",
        hat_col="{response_col}_hat",
        class_params=ff.HP("regression_params")
    )
    .if_hyperparam_is_true(
        "log_response",
        do.pipe(np.expm1, "{response_col}_hat"),
    )
)
```

Because we wrote these sub-pipelines to play nicely together (for example,
`predict_response` references the same `"feature_cols"` and `"response_col"`
hyperparameters as the preparation pipelines), we can concatenate them together to
create a very generic prediction pipeline that we might use in many situations by
supplying appropriate bindings for the hyperparameters.

```{code-cell} ipython3
generic_pipeline = (
    prepare_training_response + prepare_features + predict_response
)

generic_pipeline.hyperparams()
```

For example, here we recreate our original model:

```{code-cell} ipython3
:tags: [remove-cell]

train_df = diamonds_df.sample(frac=0.5, random_state=650280486)
test_df = diamonds_df.loc[list(set(diamonds_df.index) - set(train_df.index))]
```

```{code-cell} ipython3
generic_pipeline.fit(
    train_df,
    feature_cols=["carat", "table", "depth"],
    log_feature_cols=["carat"],
    response_col="price",
    log_response=True,
    regression_class=sklearn.linear_model.LinearRegression,
    regression_params={"fit_intercept": True},
).apply(test_df).head()
```

But we can also use the same pipeline to fit a very different model, say a `Lasso`
regression with a different set of predictor, none of which needs to be log-transformed:

```{code-cell} ipython3
generic_pipeline.fit(
    train_df,
    feature_cols=["x", "y", "z", "depth", "table"],
    response_col="price",
    log_response=True,
    regression_class=sklearn.linear_model.Lasso,
    regression_params={
        "fit_intercept": True,
        "alpha": 0.01,
    }
).apply(test_df).head()
```

## Hyperparameter searches

Another important application of hyperparameters is to explore or optimize the behavior
of a pipeline across a range of values for its parameters. You can do this manually yourself:

```python
for alpha in np.arange(0.0, 1.0, 0.1):
    some_pipeline.fit(train_df, alpha=alpha).apply(test_df)
```

Or you can make use of built-in transforms
[`ForBindings`](frankenfit.universal.ForBindings) and
[`GroupByBindings`](frankenfit.dataframe.GroupByBindings), which allow you to fit a
child transform across different bindings and summarize the results.

The earlier {doc}`synopsis` shows a worked example of `GroupByBindings`, and there are
more details in {doc}`branching_and_grouping`.
