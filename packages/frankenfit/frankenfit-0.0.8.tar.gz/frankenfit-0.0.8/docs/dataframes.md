---
jupytext:
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

import numpy as np
import pandas as pd
import frankenfit as ff

from pydataset import data
diamonds_df = data("diamonds")
```

# Working with `DataFrames` and `DataFramePipelines`

While the core functionality of Frankenfit doesn't make any assumptions about the type
or shape of one's data, the expectation is that most users will be working with
two-dimensional Pandas [`DataFrame`
objects](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html).
The library therefore includes many transforms and conveniences specific to
`DataFrames`, exposed via the methods of
[`DataFramePipeline`](frankenfit.DataFramePipeline).

This page is not an exhaustive catalogue of all of the transforms on `DataFrames` (for
that see the [API Reference](transform-library)); it covers more high-level idioms and
recommendations for working with them.

+++

## `do`-notation

`ff.DataFramePipeline()` is a long phrase to type repeatedly while writing pipelines.
Therefore the author of Frankenfit recommends defining a more succinct variable to use
as shorthand for a fresh, empty `DataFramePipeline`, for example:

```{code-cell} ipython3
do = ff.DataFramePipeline()
```

Your pipelines then all look like `do.z_score().then(...)`, which is nice because it
almost reads like English, and in any case it's quicker to type.

Another advantage of writing pipelines this way is that eventually you may build up your
own collection of custom `Transform` subclasses, and define your own subclass of
`DataFramePipeline` that exposes these transforms with new call-chain methods (see
{doc}`implementing_transforms` and
[`with_methods()`](frankenfit.Pipeline.with_methods)). If you've been using
`do`-notation, then you can simply swap in your own pipeline class instead of
`DataFramePipeline` in the definition of `do`, and you'll be able to keep writing
pipelines just as you always have, but with the new methods available. For example:

+++

```python
MyPipeline = ff.DataFramePipeline.with_methods(
    my_transform=MyTransform,
    ...
)

do = MyPipeline()

some_pipeline = (
    do
    .z_score()
    .my_transform(...)
    ...
)
```

+++

## Selecting columns and rows

You'll often want to select some subset of your data, either to restrict the input to
subsequent transforms, or to select from the output of preceding transforms. To select
columns of data you can use [`Select`](frankenfit.dataframe.Select) (call-chain methods
`select()` and `[]`), and to keep specified rows of data you can use
[`Filter`](frankenfit.dataframe.Filter) (call-chain method `filter()`). These are both
[`StatelessTransforms`](frankenfit.StatelessTransform).

`select()` is interchangeable with `__getitem__`, i.e. the square-bracket syntax, on
`DataFramePipelines`. So for example the following two pipelines are equivalent:

```{code-cell} ipython3
do.select(["col1", "col2"])
do[["col1", "col2"]]
```

As with other transforms on `DataFrames`, instead of a list of column names, one can
also provide a single column name, which is automatically converted to a list of one:

```{code-cell} ipython3
do.select("col1")  # same as do.select(["col1"])
do["col1"]  # same as do[["col1"]]
```

:::{note}
Selecting a single column from a `DataFramePipeline` always results in a `DataFrame`
with one column, never a `Series` object as `DataFrame.__getitem__` would. It's an
important invariant of Frankenfit's `DataFrame` transforms that they always accept a
`DataFrame` as input (fitting data or apply data) and return a `DataFrame` as their
result. This ensures that you can always compose transforms in whatever order and not
worry about the type of the data changing somewhere in the chain.
:::

As discussed in {doc}`hyperparams`, the columns may incorporate hyperparamters as
formatting fields:

```{code-cell} ipython3
do[["{response_col}_train", "col1"]]
```

```{code-cell} ipython3
do[["{response_col}_train", "col1"]].hyperparams()
```

To select rows of data, [`filter()`](frankenfit.dataframe.Filter) accepts a function
(typically a `lambda`) that will receive the input `DataFrame` and is expected to return
something compatible with
[`DataFrame.loc[]`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html).

```{code-cell} ipython3
(
    do.filter(lambda df: (df["cut"] == "Good") & (df["color"] == "E"))
).apply(diamonds_df).head()
```

Any additional arguments of the function are interpreted as the names of hyperparameters
whose bindings are supplied when the function is called. Again see {doc}`hyperparams`
for details.

```{code-cell} ipython3
pip = (
    do.filter(
        lambda df, which_color="E": (df["cut"] == "Good") & (df["color"] == which_color)
    )
)
pip.hyperparams()
```

```{code-cell} ipython3
pip.apply(diamonds_df, which_color="D").head()
```

## Adding columns with `Assign`

You'll often have a need to add new columns to your data somewhere in a pipeline. If the
new column is derived from existing columns, we've already seen that it's possible to do
this with [`copy()`](frankenfit.dataframe.Copy):

```{code-cell} ipython3
(
    do
    .copy("price", "price_train")
    .winsorize(0.05, "price_train")
    # ...
);
```

But this is a bit clunky, and in any case doesn't help you if the new columns are not
derived from existing ones so straightforwardly. Of course for very simple cases you can
always use [`pipe()`](frankenfit.dataframe.Pipe) or
[`stateless_lambda()`](frankenfit.universal.StatelessLambda), e.g.:

```{code-cell} ipython3
(
    do
    .stateless_lambda(lambda df: df.assign(ones=1.0))
);
```

```{code-cell} ipython3
do["price"].winsorize(0.05).apply(diamonds_df).head()
```

But often you'll want the new column or set of columns to be the result of some
pipeline, possibly with its own state to be fit. That's where
[`Assign`](frankenfit.dataframe.Assign) (call-chain method `assign()`) comes in.
Syntactically it's inspired by Pandas'
[`DataFrame.assign()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.assign.html):
each keyword parameter is interpreted as the name of new column to create, whose value
should be a pipeline that produces a one-column `DataFrame`. Thus our earlier example of
`price_train` can be written as:

```{code-cell} ipython3
(
    do
    .assign(
        price_train=do["price"].winsorize(0.05)
    )
).apply(diamonds_df).head()
```

Note how the example above uses column-selection to initiate a sub-pipeline for
`price_train` that will produce a single winsorized column. This sub-pipeline is
stateful because [`Winsorize`](frankenfit.dataframe.Winsorize) is stateful (at fit time
it records the relevant quantiles of the fitting data)

Most of the `DataFrame` transforms built in to Frankenfit (like `Winsorize`,
[`ZScore`](frankenfit.dataframe.ZScore), and so on), which accept a `cols` parameter,
are designed to operate on all of the columns that they receive (which might be
controlled by an earlier `select()` in the pipeline) when `cols` is omitted, precisely
so that they play nicely with `Assign`. Thus to winsorize just three of the column in
our data, we can write something like this:

```{code-cell} ipython3
do[["carat", "depth", "table"]].winsorize(0.05).apply(diamonds_df).head()
```

Notice how `Winsorize` *replaces* all of the columns that it winsorizes with their
winsorized values. All of the `DataFrame` transforms follow this same convention. If you
wish to give the transformed columns new names, then the
[`Affix`](frankenfit.dataframe.Affix) family of transforms (including
[`Prefix`](frankenfit.dataframe.Prefix) and [`Suffix`](frankenfit.dataframe.Suffix)) can
be mixed in freely:

```{code-cell} ipython3
do[["carat", "depth", "table"]].winsorize(0.05).suffix("_fea").apply(diamonds_df).head()
```

This works especially well with `Assign`. Aside from using keyword parameters to name
new columns that are the result of one-column pipelines, you can also provide
multi-column pipelines as *positional parameters* of `Assign`. Whatever columns are in
the output get added to the data by `Assign`, and so by using one of the `Affix`
transforms you can elegantly assign a batch of columns with new names, all resulting
from some complex sup-pipeline:

```{code-cell} ipython3
(
    do
    .assign(
        do[["carat", "depth", "table"]].winsorize(0.05).suffix("_fea")
    )
).apply(diamonds_df).head()
```

`Assign` has a few other quality-of-life features. If you provide a bare callable object
(like a `lambda` function) for some column, it is automatically wrapped by a
[`StatelessLambda`](frankenfit.universal.StatelessLambda) transform:

```{code-cell} ipython3
pipeline = (
    do
    .assign(
        log_price=lambda df: np.log1p(df[["price"]]),
    )
)
pipeline.visualize()
```

```{code-cell} ipython3
pipeline.apply(diamonds_df).head()
```

This also works for multi-column positional assignments:

```{code-cell} ipython3
(
    do
    .assign(
        lambda df: np.log1p(df[["carat", "price"]]).rename(columns=lambda c: f"log_{c}"),
    )
).apply(diamonds_df).head()
```

:::{tip}
Of course it's worth noting that the example above might be written more idiomatically as:

```python
(
    do
    .assign(
        do[["carat", "price"]].pipe(np.log1p).prefix("log_")
    )
)
```
:::

+++

Finally, `Assign` also accepts scalar and `Series` values for new columns, just like
Pandas' `DataFrame.apply()`:

```{code-cell} ipython3
do.assign(one=1).apply(diamonds_df).head()
```

```{code-cell} ipython3
do.assign(
    some_series=np.repeat([6502, 80486], len(diamonds_df) / 2 + len(diamonds_df) % 2)
).apply(diamonds_df).head()
```

But beware that assigning a large `Series` object as in the second example above is
best avoided. The `Series` object, which is effectively data, becomes part of the
parameters of the `Assign` transform, but transforms [are meant to be light-weight,
abstract descriptions](abstract-descriptions) of what to do with data; any heavyweight
data itself should ideally only be introduced or generated at fit-time and apply-time.

Visualizing this pipeline makes it clear that we have a confusion between data and
parameters:

```{code-cell} ipython3
do.assign(
    some_series=np.repeat([6502, 80486], len(diamonds_df) / 2 + len(diamonds_df) % 2)
).visualize()
```

In this particular case, the preferred way to add this column would be to assign a
lambda function that creates and returns the desired series (and which, as noted above,
will become a [`StatelessLambda`](frankenfit.universal.StatelessLambda) transform):

```{code-cell} ipython3
do.assign(
    some_series=lambda df: np.repeat([6502, 80486], len(df) / 2 + len(df) % 2)
).visualize()
```

## Using `Join`

Another common operation is to join two `DataFrame` pipelines (or
"[merge](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.merge.html)"
them, in Pandas' parlance). For example, suppose we have a pipeline, `per_cut_means`,
that computes, for each distinct `cut` of diamond, the means of `price` and `carat`.
This can be accomplished with [`group_by_cols()`](frankenfit.dataframe.GroupByCols) and
[`stateful_lambda()`](frankenfit.universal.StatefulLambda):

```{code-cell} ipython3
per_cut_means = do.group_by_cols("cut").then(
    do[["price", "carat"]]
    .stateful_lambda(
        fit_fun=lambda df: df.agg(["mean"]),
        apply_fun=lambda df, means: means
    )
    .suffix("_mean_per_cut")
)

per_cut_means.apply(diamonds_df)
```

The `StatefulLambda` transform that we've created above simply computes the mean of each
column at fit-time, and, at apply-time, just returns those means. (Thus if we apply this
pipeline out-of-sample, it will produce whatever the means were on the fitting data.)

We can then take the original dataset with an observation per diamond, and join it with
these per-cut means, using [`join()`](frankenfit.dataframe.Join) (the parameters have
the same meaning as for `pandas.merge()`):

```{code-cell} ipython3
(
    do
    .join(
        per_cut_means, how="left", on="cut",
    )
).apply(diamonds_df).head()
```

One subtlety of `join()` is that it works a little bit differently than most call-chain
methods, which usually simply *append* a transform to the pipeline. By contrast,
`join()` returns a new pipeline containing only a `Join` transform, with the "parent"
transform as the its `left` parameter, and the "child" transform as its `right`
parameter. In other words, the following:

```python
p1.join(p2, ...)
```

...is equivalent to:

```python
do.then(ff.dataframe.Join(p1, p2, ...))
```

At fit-time, `Join` simply fits the left and right pipelines, and at apply-time, it
applies each of those fits to the data and then returns the result of joining their two
results (each of which ought to be a `DataFrame`) with `pandas.merge()`.

+++

## Reading and writing data

So far in the documentation, in most of the examples have we have provided the fitting
data and apply data as `DataFrame` arguments to [`fit()`](frankenfit.Transform.fit) and
[`apply()`](frankenfit.FitTransform.apply), respectively (or in the case of
[`Pipeline.apply()`](frankenfit.Pipeline.apply), the data argument is [*both* the
fitting data and the apply data](fit-and-apply)).

But it is also possible to introduce fitting data or apply data to a pipeline by reading
it from some external source, like a CSV file or a [pyarrow
dataset](https://arrow.apache.org/docs/python/dataset.html). To do so there are certain
transforms like [`read_pandas_csv()`](frankenfit.dataframe.ReadPandasCSV) and
[`read_dataset()`](frankenfit.dataframe.ReadDataset), which, at fit-time, do nothing
(they are stateless), and, at apply-time, simply read and return some data, as
determined by their parameters.

For example:

```{code-cell} ipython3
:tags: [remove-cell]

# FIXME: this cell should not be visible in docs output
diamonds_df.rename_axis(index="index").to_csv("./diamonds.csv")
```

```{code-cell} ipython3
read_diamonds_csv = do.read_pandas_csv("./diamonds.csv")
```

```{code-cell} ipython3
read_diamonds_csv.apply().head()
```

It's important to note that such data-reading transforms *ignore* any apply data that
might be provided as an argument of `apply()`. They simply read some new data and return
it. Therefore any apply data is effectively discarded. We call these
`ConstantTransforms`, because their output is constant given their parameters; they
always return the same thing regardless of the fitting data and apply data.[^foot-constant]

[^foot-constant]: technically, the output of a `ConstantTransform` needn't actually be
constant. For example, a random number-generating transform, though it produce
different output on each application, would qualify as a `ConstantTransform` because its
output is independent of its fitting data and apply data, if any.

Therefore it's generally expected that a `ConstantTransform` should be the first
transform in a pipeline. If some non-empty apply data is ever provided to a
`ConstantTransform`, it emits a `NonInitialConstantTransformWarning`:

```{code-cell} ipython3
# emits NonInitialConstantTransformWarning
read_diamonds_csv.apply(diamonds_df)
```

In fact, simply creating a pipeline in which some transform precedes a
`ConstantTransfom` will emit the same warning:

```{code-cell} ipython3
# emits NonInitialConstantTransformWarning
do.assign(foo=1).then(read_diamonds_csv)
```

Data-reading transforms allow you to separate the reading of data from the rest of your
pipelines in remixable ways. For instance, with a single pipeline like `diamond_model`,
you could create fits on different datasets as in:

```python
fit_1 = do.read_pandas_csv("./data_1.csv").then(diamond_model).fit()
fit_2 = do.read_pandas_csv("./data_2.csv").then(diamond_model).fit()
...
```

You could even replace the `filepath` parameter with a hyperparameter, and then use
[`group_by_bindings()`](frankenfit.dataframe.GroupByBindings) or
[`for_bindings()`](frankenfit.universal.ForBindings) to fit (or apply) a pipeline on
many datasets simultaneously.

Furthermore, if your pipeline will run on a [distributed backend](backends), it's
usually better to provide the fitting data and apply data via a data-reading transform,
rather than as arguments to `fit()` and `apply()`, because doing so allows the remote
workers to read the data from the source themselves (i.e. in parallel), rather than
serializing the data and sending it to the workers from your local Python process.

+++

The complements of data-reading transforms are data-writing transforms like
[`write_pandas_csv()`](frankenfit.dataframe.WritePandasCSV) and
[`write_dataset()`](frankenfit.dataframe.WriteDataset). Unlike the data readers, these
are *not* `ConstantTransforms`. Rather, they behave like the
[`Identity`](frankenfit.universal.Identity) transform but with the side-effect of, at
apply-time, writing their apply data to some destination. They can be injected anywhere
in a pipeline to save the apply data so far, without changing the behavior of the
pipeline.
