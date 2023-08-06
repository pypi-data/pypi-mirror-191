(api-reference)=
# Frankenfit API reference

## The `frankenfit` package
```{eval-rst}
.. automodule:: frankenfit
```

### Submodules

It is worth noting that the full library of available
[`Transform`](frankenfit.Transform) classes is *not* included among the top-level names
in `frankenfit.*`. Rather, they may be found under submodules:

* [`frankenfit.universal`](universal-api) for so-called "universal" Transforms that make
  no assumptions about the type or shape of their input data.

* [`frankenfit.dataframe`](dataframe-api) for Transforms designed to operate on pandas
  `DataFrame` objects.

This keeps the package-level API manageably small and clean, and the intention is that
the user should very rarely find herself directly instantiating Transforms from the
library (that is, rarely writing things like `ff.dataframe.DeMean(...)`). Instead, the
**call-chain** API provided by `Pipeline` subclasses
[`DataFramePipeline`](frankenfit.dataframe.DataFrameCallChain) and
[`UniversalPipeline`](frankenfit.universal.UniversalCallChain) should be the preferred
way of creating Transforms, effectively acting as a domain-specific language for doing
so.

Other submodules in the `frankenfit` package include:

* `frankenfit.core`: all of the "core" (often abstract base) classes like
  [`Transform`](frankenfit.Transform), [`FitTransform`](frankenfit.FitTransform), and so
  on are defined here. Those that users are meant to refer to directly are already
  exposed at the package level (`frankenfit.*`) and there should be little need to
  import `frankenfit.core` itself.

* `frankenfit.params`: classes and functions related to hyperparameters, as well as
  declaring and using parameters of various types when writing `Transform` subclasses.
  The most useful ones are all exposed as top-level names in the `frankenfit` package, so that the user should rarely need to import this module.

* `frankenfit.backend`: classes and functions related to specific
  [`Backend`](frankenfit.Backend) implementations (other than the core
  [`LocalBackend`](frankenfit.LocalBackend)). Currently this consists of
  [`DaskBackend`](frankenfit.DaskBackend) and related `Future`s, etc. Again, the most
  useful names are already exposed at the top level of the `frankenfit` package and the
  user should rarely have a reason to import `frankenfit.backend`.

* `frankenfit.mypy`: provides a `mypy` plugin to assist `mypy` in type-checking code
  that uses Frankenfit. If you use `mypy` as a static typechecker for your own project,
  you can enable this plugin by including the following in your `pyproject.toml` file:
  ```toml
  [tool.mypy]
  plugins = "frankenfit.mypy"
  ```

------------

## Core classes

```{eval-rst}
.. autosummary::
    Transform
    FitTransform
    frankenfit.core.PipelineMember
    StatelessTransform
    ConstantTransform
    NonInitialConstantTransformWarning
```

```{eval-rst}
.. autoclass:: Transform
    :members:
    :private-members: _fit, _apply
    :undoc-members:

.. autodata:: frankenfit.core.DEFAULT_VISUALIZE_DIGRAPH_KWARGS

.. autoclass:: FitTransform
    :members:
    :undoc-members:

.. autoclass:: frankenfit.core.PipelineMember
    :members:
    :private-members:
    :special-members: __add__

.. autoclass:: StatelessTransform
    :members:
    :show-inheritance:

.. autoclass:: ConstantTransform
    :members:
    :show-inheritance:

.. autoclass:: NonInitialConstantTransformWarning
    :show-inheritance:
```

## Hyperparameters
Foobar.

```{eval-rst}
.. autosummary::
    UnresolvedHyperparameterError
    HP
    HPFmtStr
    HPCols
    HPDict
    HPLambda
```

```{eval-rst}
.. autoexception:: UnresolvedHyperparameterError
    :show-inheritance:

.. autoclass:: HP
    :members:

.. autoclass:: HPFmtStr
    :show-inheritance:
    :members:

.. autoclass:: HPCols
    :show-inheritance:
    :members:

.. autoclass:: HPDict
    :show-inheritance:
    :members:

.. autoclass:: HPLambda
    :show-inheritance:
    :members:

```

## Pipelines
Foobar.

```{eval-rst}
.. autosummary::
    Pipeline
    frankenfit.universal.UniversalCallChain
    frankenfit.universal.UniversalPipelineInterface
    frankenfit.universal.UniversalPipeline
    frankenfit.dataframe.DataFrameCallChain
    frankenfit.dataframe.DataFramePipelineInterface
    frankenfit.dataframe.DataFramePipeline
```

### Base classes

```{eval-rst}
.. autoclass:: Pipeline
    :show-inheritance:
    :members:
    :undoc-members:
```

### Universal pipelines

```{eval-rst}
.. autoclass:: frankenfit.universal.UniversalCallChain
    :show-inheritance:
    :members:

.. autoclass:: frankenfit.universal.UniversalPipelineInterface
    :show-inheritance:
    :members:

.. autoclass:: UniversalPipeline
    :show-inheritance:
    :members:
```

### `DataFrame` pipelines

```{eval-rst}
.. autoclass:: frankenfit.dataframe.DataFrameCallChain
    :show-inheritance:
    :members:

.. autoclass:: frankenfit.dataframe.DataFramePipelineInterface
    :show-inheritance:
    :members:

.. autoclass:: DataFramePipeline
    :show-inheritance:
    :members:
```

## Computational backends and futures

```{eval-rst}
.. autosummary::
    Backend
    Future
    LocalBackend
    frankenfit.core.LocalFuture
    DaskBackend
    frankenfit.backend.DaskFuture
```

### Base classes

```{eval-rst}
.. autoclass:: Backend
    :members:

.. autoclass:: Future
    :members:
```

### The local backend

```{eval-rst}
.. autoclass:: LocalBackend
    :members:

.. autoclass:: frankenfit.core.LocalFuture
    :members:
```

### The Dask backend

```{eval-rst}
.. autoclass:: frankenfit.DaskBackend
    :members:

.. autoclass:: frankenfit.backend.DaskFuture
    :members:
```

## Writing a `Transform` subclass
Foobar.

```{eval-rst}
.. autosummary::
    params
    fmt_str_field
    columns_field
    dict_field
    frankenfit.params.UserLambdaHyperparams
```

```{eval-rst}

.. autofunction:: params

.. autofunction:: fmt_str_field

.. autofunction:: columns_field

.. autofunction:: dict_field

.. autoclass:: frankenfit.params.UserLambdaHyperparams
    :members:

```

(transform-library)=
## Transform library

```{eval-rst}
.. autosummary::
    frankenfit.core.IfPipelineIsFitting
    frankenfit.core.ApplyFitTransform
    frankenfit.universal.Identity
    frankenfit.universal.IfFittingDataHasProperty
    frankenfit.universal.IfHyperparamIsTrue
    frankenfit.universal.IfHyperparamLambda
    frankenfit.universal.ForBindings
    frankenfit.universal.LogMessage
    frankenfit.universal.Print
    frankenfit.universal.StatefulLambda
    frankenfit.universal.StatelessLambda
    frankenfit.universal.StateOf
    frankenfit.dataframe.Affix
    frankenfit.dataframe.Assign
    frankenfit.dataframe.Clip
    frankenfit.dataframe.Copy
    frankenfit.dataframe.Correlation
    frankenfit.dataframe.DeMean
    frankenfit.dataframe.Drop
    frankenfit.dataframe.Filter
    frankenfit.dataframe.GroupByCols
    frankenfit.dataframe.GroupByBindings
    frankenfit.dataframe.ImputeConstant
    frankenfit.dataframe.ImputeMean
    frankenfit.dataframe.Join
    frankenfit.dataframe.Pipe
    frankenfit.dataframe.Prefix
    frankenfit.dataframe.ReadDataFrame
    frankenfit.dataframe.ReadDataset
    frankenfit.dataframe.ReadPandasCSV
    frankenfit.dataframe.Rename
    frankenfit.dataframe.Select
    frankenfit.dataframe.SKLearn
    frankenfit.dataframe.Statsmodels
    frankenfit.dataframe.Suffix
    frankenfit.dataframe.Winsorize
    frankenfit.dataframe.WriteDataset
    frankenfit.dataframe.WritePandasCSV
    frankenfit.dataframe.ZScore
```

### Core transforms

```{eval-rst}
.. autoclass:: frankenfit.core.IfPipelineIsFitting

.. autoclass:: frankenfit.core.ApplyFitTransform
```

(universal-api)=
### Universal transforms

The module `frankenfit.universal` contains Frankenfit's built-in library of generically
useful Transforms that make no assumptions about the type or shape of the data to which
they are applied.

```{eval-rst}
.. autoclass:: frankenfit.universal.Identity

.. autoclass:: frankenfit.universal.IfFittingDataHasProperty

.. autoclass:: frankenfit.universal.IfHyperparamIsTrue

.. autoclass:: frankenfit.universal.IfHyperparamLambda

.. autoclass:: frankenfit.universal.ForBindings

.. autoclass:: frankenfit.universal.LogMessage

.. autoclass:: frankenfit.universal.Print

.. autoclass:: frankenfit.universal.StatefulLambda

.. autoclass:: frankenfit.universal.StatelessLambda

.. autoclass:: frankenfit.universal.StateOf
```

(dataframe-api)=
### `DataFrame` transforms

The module `frankenfit.dataframe` provides a library of broadly useful Transforms on 2-D
Pandas DataFrames.

```{eval-rst}
.. autoclass:: frankenfit.dataframe.Affix

.. autoclass:: frankenfit.dataframe.Assign

.. autoclass:: frankenfit.dataframe.Clip

.. autoclass:: frankenfit.dataframe.Copy

.. autoclass:: frankenfit.dataframe.Correlation

.. autoclass:: frankenfit.dataframe.DeMean

.. autoclass:: frankenfit.dataframe.Drop

.. autoclass:: frankenfit.dataframe.Filter

.. autoclass:: frankenfit.dataframe.GroupByCols

.. autoclass:: frankenfit.dataframe.GroupByBindings

.. autoclass:: frankenfit.dataframe.ImputeConstant

.. autoclass:: frankenfit.dataframe.ImputeMean

.. autoclass:: frankenfit.dataframe.Join

.. autoclass:: frankenfit.dataframe.Pipe

.. autoclass:: frankenfit.dataframe.Prefix
    :show-inheritance:

.. autoclass:: frankenfit.dataframe.ReadDataFrame
    :show-inheritance:

.. autoclass:: frankenfit.dataframe.ReadDataset
    :show-inheritance:

.. autoclass:: frankenfit.dataframe.ReadPandasCSV
    :show-inheritance:

.. autoclass:: frankenfit.dataframe.Rename

.. autoclass:: frankenfit.dataframe.Select

.. autoclass:: frankenfit.dataframe.SKLearn

.. autoclass:: frankenfit.dataframe.Statsmodels

.. autoclass:: frankenfit.dataframe.Suffix
    :show-inheritance:

.. autoclass:: frankenfit.dataframe.Winsorize

.. autoclass:: frankenfit.dataframe.WriteDataset
    :show-inheritance:

.. autoclass:: frankenfit.dataframe.WritePandasCSV
    :show-inheritance:

.. autoclass:: frankenfit.dataframe.ZScore

```
