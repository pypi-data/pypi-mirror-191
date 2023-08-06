# Geobootstrap
`geobootstrap` is a novel computer simulation method that extends the classic bootstrap method (Efron 1979) in statistical analysis, to generate representative statistical measures e.g. standard deviations, confidence intervals and probability based values).
Instead of passing the default None weights to pandas.sample, which results in equal probability weighting, kernel-based weights are used.
The weights are determined by a distance decay function, that determines how quickly weights decrease as distances increase.
This means that key statistical measures are computed by pooling or borrowing strength from neighbouring units.
Thus, geobootstrap takes advantage of the spatial structure of GeoDataFrames.

Geobootstrap is based on `pandas.sample` and operates on `geopandas.GeoDataFrames`.
The resampling takes place for each spatial entity and the fraction of samples returned is based on the fraction of the original dataset.
So a GeoDataFrame with 10 spatial entities and a fraction of 1.0 (default) will return a list of 10 entries, each containing 10 different spatial entities.
If the fraction was set to 0.8, then a list of 10 entries, each containing 8 different spatial entities would be returned.

Further descriptions about the methodology will be later provided but the contents of the package should provide enough detail for now.
The potential use cases of this methodology include areal interpolation, which are illustrated in the [coss package](https://github.com/tastatham/coss).
