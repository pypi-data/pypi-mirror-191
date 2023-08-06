"""Aggregation engines."""
import time
from abc import ABC
from abc import abstractmethod
from collections import namedtuple
from collections.abc import Generator
from typing import Any
from typing import List
from typing import Tuple
from typing import Type
from typing import Union

import dask
import geopandas as gpd
import numpy as np
import numpy.typing as npt
import pandas as pd
from joblib import delayed
from joblib import Parallel
from joblib import parallel_backend

from gdptools.agg.stats_methods import MAWeightedAverage
from gdptools.agg.stats_methods import StatsMethod
from gdptools.agg.stats_methods import WeightedAverage
from gdptools.data.agg_gen_data import AggData
from gdptools.data.user_data import UserData
from gdptools.utils import _get_default_val
from gdptools.utils import _get_interp_array
from gdptools.utils import _get_wieght_df


AggChunk = namedtuple("AggChunk", ["ma", "wghts", "def_val", "index"])


class AggEngine(ABC):
    """Abstract aggregation class."""

    def calc_agg_from_dictmeta(
        self,
        user_data: UserData,
        weights: Union[str, pd.DataFrame],
        stat: Union[Type[MAWeightedAverage], Type[WeightedAverage]],
        jobs: int = -1,
    ) -> Tuple[
        dict[str, AggData],
        gpd.GeoDataFrame,
        List[npt.NDArray[Union[np.int_, np.double]]],
    ]:
        """Abstract Base Class for calculating aggregations from dictionary metadata.

        _extended_summary_

        Args:
            user_data (UserData): _description_
            weights (Union[str, gpd.GeoDataFrame]): _description_
            stat (StatsMethod): _description_
            jobs (int): _description_. Defaults to -1.

        Returns:
            Tuple[gpd.GeoDataFrame, List[NDArray[np.double]]]: _description_
        """
        self.usr_data = user_data
        self.id_feature = user_data.get_feature_id()
        self.vars = user_data.get_vars()
        self.stat = stat
        self.period = None
        self.wghts = _get_wieght_df(weights, self.id_feature)
        self._jobs = jobs

        return self.agg_w_weights()

    @abstractmethod
    def agg_w_weights(
        self,
    ) -> Tuple[
        dict[str, AggData],
        gpd.GeoDataFrame,
        List[npt.NDArray[Union[np.int_, np.double]]],
    ]:
        """Abstract method for calculating weights."""
        pass


class SerialAgg(AggEngine):
    """SerialAgg data by feature and time period."""

    def get_period_from_ds(self, data: AggData) -> List[str]:
        """Get starting and ending time string from previously subsetted Dataset.

        Args:
            data (AggData): _description_

        Returns:
            List[str]: _description_
        """
        # tname = list(data.cat_param.values())[0]["T_name"]
        tname = data.cat_param.T_name
        tstrt = str(data.da.coords[tname].values[0])
        tend = str(data.da.coords[tname].values[-1])
        return [tstrt, tend]

    def agg_w_weights(
        self,
    ) -> Tuple[
        dict[str, AggData],
        gpd.GeoDataFrame,
        List[npt.NDArray[Union[np.int_, np.double]]],
    ]:
        """Standard aggregate method.

        Returns:
            Tuple[List[AggData], gpd.GeoDataFrame, List[NDArray[np.double]]]:
                _description_
        """
        # ds_time = self.ds.coords[list(self.param_dict.values())[0]["T_name"]].values
        # date_bracket = np.array_split(ds_time, self.numdiv)
        # print(date_bracket)
        # date_bracket = list(_date_range(self.period[0], self.period[1], self.numdiv))
        r_gdf = []
        r_vals = []
        r_agg_dict = {}
        avars = self.usr_data.get_vars()
        for index, key in enumerate(avars):
            print(f"Processing: {key}")
            tstrt = time.perf_counter()
            agg_data: AggData = self.usr_data.prep_agg_data(key=key)
            tend = time.perf_counter()
            print(f"    Data prepped for aggregation in {tend-tstrt:0.4f} seconds")
            tstrt = time.perf_counter()
            newgdf, nvals = self.calc_agg(key=key, data=agg_data)
            tend = time.perf_counter()
            print(f"    Data aggregated in {tend -tstrt:0.4f} seconds")
            if index == 0:
                # all new GeoDataFrames will be the same so save and return only one.
                r_gdf.append(newgdf)
            r_vals.append(nvals)
            r_agg_dict[key] = agg_data
        return r_agg_dict, r_gdf[0], r_vals

    def calc_agg(
        self: "SerialAgg", key: str, data: AggData
    ) -> Tuple[gpd.GeoDataFrame, npt.NDArray[Union[np.int_, np.double]]]:
        """Calculate aggregation.

        Args:
            key (str): _description_
            data (AggData): _description_

        Returns:
            Tuple[gpd.GeoDataFrame, NDArray[np.double]]: _description_
        """
        cp = data.cat_param
        period = self.get_period_from_ds(data=data)
        gdf = data.feature
        gdf.reset_index(drop=True, inplace=True)
        gdf = gdf.sort_values(data.id_feature).dissolve(by=data.id_feature)
        geo_index = np.asarray(gdf.index, dtype=type(gdf.index.values[0]))
        n_geo = len(geo_index)
        unique_geom_ids = self.wghts.groupby(self.id_feature)
        t_name = cp.T_name
        selection = {t_name: slice(period[0], period[1])}
        da = data.da.sel(**selection)  # type: ignore
        # print(da)
        nts = len(da.coords[t_name].values)
        native_dtype = da.dtype
        # gdptools will handle floats and ints - catch if gridded type is different
        try:
            dfval = _get_default_val(native_dtype=native_dtype)
        except TypeError as e:
            print(e)

        val_interp = _get_interp_array(
            n_geo=n_geo, nts=nts, native_dtype=native_dtype, default_val=dfval
        )

        mdata = np.ma.masked_array(da.values, np.isnan(da.values))  # type: ignore

        for i in np.arange(len(geo_index)):
            try:
                weight_id_rows = unique_geom_ids.get_group(str(geo_index[i]))
            except KeyError:
                continue
            tw = weight_id_rows.wght.values
            i_ind = np.array(weight_id_rows.i.values).astype(int)
            j_ind = np.array(weight_id_rows.j.values).astype(int)

            val_interp[:, i] = self.stat(
                array=mdata[:, i_ind, j_ind], weights=tw, def_val=dfval
            ).get_stat()

        return gdf, val_interp


class ParallelAgg(AggEngine):
    """SerialAgg data by feature and time period."""

    def get_period_from_ds(self, data: AggData) -> List[str]:
        """Get starting and ending time string from previously subsetted Dataset.

        Args:
            data (AggData): _description_

        Returns:
            List[str]: _description_
        """
        # tname = list(data.cat_param.values())[0]["T_name"]
        tname = data.cat_param.T_name
        tstrt = str(data.da.coords[tname].values[0])
        tend = str(data.da.coords[tname].values[-1])
        return [tstrt, tend]

    def agg_w_weights(
        self,
    ) -> Tuple[
        dict[str, AggData],
        gpd.GeoDataFrame,
        List[npt.NDArray[Union[np.int_, np.double]]],
    ]:
        """Standard aggregate method.

        Returns:
            Tuple[List[AggData], gpd.GeoDataFrame, List[NDArray[np.double]]]:
                _description_
        """
        # ds_time = self.ds.coords[list(self.param_dict.values())[0]["T_name"]].values
        # date_bracket = np.array_split(ds_time, self.numdiv)
        # print(date_bracket)
        # date_bracket = list(_date_range(self.period[0], self.period[1], self.numdiv))
        r_gdf = []
        r_vals = []
        r_agg_dict = {}
        avars = self.usr_data.get_vars()
        for index, key in enumerate(avars):
            print(f"Processing: {key}")
            tstrt = time.perf_counter()
            agg_data: AggData = self.usr_data.prep_agg_data(key=key)
            tend = time.perf_counter()
            print(f"    Data prepped for aggregation in {tend-tstrt:0.4f} seconds")
            tstrt = time.perf_counter()
            newgdf, nvals = self.calc_agg(key=key, data=agg_data)
            tend = time.perf_counter()
            print(f"    Data aggregated in {tend -tstrt:0.4f} seconds")
            if index == 0:
                # all new GeoDataFrames will be the same so save and return only one.
                r_gdf.append(newgdf)
            r_vals.append(nvals)
            r_agg_dict[key] = agg_data
        return r_agg_dict, r_gdf[0], r_vals

    def calc_agg(
        self: "ParallelAgg", key: str, data: AggData
    ) -> Tuple[gpd.GeoDataFrame, npt.NDArray[Union[np.int_, np.double]]]:
        """Calculate aggregation.

        Args:
            key (str): _description_
            data (AggData): _description_

        Returns:
            Tuple[gpd.GeoDataFrame, NDArray[np.double]]: _description_
        """
        cp = data.cat_param
        period = self.get_period_from_ds(data=data)
        gdf = data.feature
        gdf.reset_index(drop=True, inplace=True)
        gdf = gdf.sort_values(data.id_feature).dissolve(by=data.id_feature)
        geo_index = np.asarray(gdf.index, dtype=type(gdf.index.values[0]))
        # geo_index_chunk = np.array_split(geo_index, self._jobs)
        n_geo = len(geo_index)
        unique_geom_ids = self.wghts.groupby(self.id_feature)
        t_name = cp.T_name
        selection = {t_name: slice(period[0], period[1])}
        da = data.da.sel(**selection)  # type: ignore
        # print(da)
        nts = len(da.coords[t_name].values)
        native_dtype = da.dtype
        # gdptools will handle floats and ints - catch if gridded type is different
        try:
            dfval = _get_default_val(native_dtype=native_dtype)
        except TypeError as e:
            print(e)

        val_interp = _get_interp_array(
            n_geo=n_geo, nts=nts, native_dtype=native_dtype, default_val=dfval
        )

        mdata = np.ma.masked_array(da.values, np.isnan(da.values))  # type: ignore

        chunks = get_weight_chunks(
            unique_geom_ids=unique_geom_ids, mdata=mdata, dfval=dfval
        )

        worker_out = get_stats_parallel(
            n_jobs=self._jobs,
            stat=self.stat,
            bag=bag_generator(jobs=self._jobs, chunks=chunks),
        )

        for index, val in worker_out:
            val_interp[:, index] = val

        return gdf, val_interp


def _stats(
    bag: List[AggChunk], method: StatsMethod
) -> Tuple[npt.NDArray[np.int_], npt.NDArray[Union[np.int_, np.double]]]:
    vals = np.zeros((bag[0].ma.shape[0], len(bag)), dtype=bag[0].ma.dtype)
    index = np.zeros(len(bag), dtype=np.int_)
    for idx, b in enumerate(bag):
        index[idx] = b.index
        vals[:, idx] = method(
            array=b.ma, weights=b.wghts, def_val=b.def_val
        ).get_stat()  # type: ignore
    return (index, vals)


def get_stats_parallel(
    n_jobs: int,
    stat: Union[Type[MAWeightedAverage], Type[WeightedAverage]],
    bag: Generator[List[AggChunk], None, None],
) -> Any:
    """Get stats values."""
    with parallel_backend("loky", inner_max_num_threads=1):
        worker_out = Parallel(n_jobs=n_jobs)(
            delayed(_stats)(chunk, method=stat) for chunk in bag
        )
    return worker_out


def get_weight_chunks(
    unique_geom_ids: gpd.GeoDataFrame.groupby,
    mdata: np.ma.MaskedArray,  # type: ignore
    dfval: Union[np.int_, np.double],
) -> List[AggChunk]:
    """Chunk data for parallel aggregation."""
    keys = list(unique_geom_ids.groups.keys())
    chunks = []
    for idx, key in enumerate(keys):
        weight_id_rows = unique_geom_ids.get_group(key)
        chunks.append(
            AggChunk(
                mdata[
                    :,
                    np.array(weight_id_rows.i.values).astype(int),
                    np.array(weight_id_rows.j.values).astype(int),
                ],
                weight_id_rows.wght.values,
                dfval,
                idx,
            )
        )
    return chunks


def bag_generator(
    jobs: int, chunks: List[AggChunk]
) -> Generator[List[AggChunk], None, None]:
    """Function to generate chunks."""
    chunk_size = len(chunks) // jobs + 1
    for i in range(0, len(chunks), chunk_size):
        yield chunks[i : i + chunk_size]


class DaskAgg(AggEngine):
    """SerialAgg data by feature and time period."""

    def get_period_from_ds(self, data: AggData) -> List[str]:
        """Get starting and ending time string from previously subsetted Dataset.

        Args:
            data (AggData): _description_

        Returns:
            List[str]: _description_
        """
        # tname = list(data.cat_param.values())[0]["T_name"]
        tname = data.cat_param.T_name
        tstrt = str(data.da.coords[tname].values[0])
        tend = str(data.da.coords[tname].values[-1])
        return [tstrt, tend]

    def agg_w_weights(
        self,
    ) -> Tuple[
        dict[str, AggData],
        gpd.GeoDataFrame,
        List[npt.NDArray[Union[np.int_, np.double]]],
    ]:
        """Standard aggregate method.

        Returns:
            Tuple[List[AggData], gpd.GeoDataFrame, List[NDArray[np.double]]]:
                _description_
        """
        # ds_time = self.ds.coords[list(self.param_dict.values())[0]["T_name"]].values
        # date_bracket = np.array_split(ds_time, self.numdiv)
        # print(date_bracket)
        # date_bracket = list(_date_range(self.period[0], self.period[1], self.numdiv))
        r_gdf = []
        r_vals = []
        r_agg_dict = {}
        avars = self.usr_data.get_vars()
        for index, key in enumerate(avars):
            print(f"Processing: {key}")
            tstrt = time.perf_counter()
            agg_data: AggData = self.usr_data.prep_agg_data(key=key)
            tend = time.perf_counter()
            print(f"    Data prepped for aggregation in {tend-tstrt:0.4f} seconds")
            tstrt = time.perf_counter()
            newgdf, nvals = self.calc_agg(key=key, data=agg_data)
            tend = time.perf_counter()
            print(f"    Data aggregated in {tend -tstrt:0.4f} seconds")
            if index == 0:
                # all new GeoDataFrames will be the same so save and return only one.
                r_gdf.append(newgdf)
            r_vals.append(nvals)
            r_agg_dict[key] = agg_data
        return r_agg_dict, r_gdf[0], r_vals

    def calc_agg(
        self: "DaskAgg", key: str, data: AggData
    ) -> Tuple[gpd.GeoDataFrame, npt.NDArray[Union[np.int_, np.double]]]:
        """Calculate aggregation.

        Args:
            key (str): _description_
            data (AggData): _description_

        Returns:
            Tuple[gpd.GeoDataFrame, NDArray[np.double]]: _description_
        """
        cp = data.cat_param
        period = self.get_period_from_ds(data=data)
        gdf = data.feature
        gdf.reset_index(drop=True, inplace=True)
        gdf = gdf.sort_values(data.id_feature).dissolve(by=data.id_feature)
        geo_index = np.asarray(gdf.index, dtype=type(gdf.index.values[0]))
        # geo_index_chunk = np.array_split(geo_index, self._jobs)
        n_geo = len(geo_index)
        unique_geom_ids = self.wghts.groupby(self.id_feature)
        t_name = cp.T_name
        selection = {t_name: slice(period[0], period[1])}
        da = data.da.sel(**selection)  # type: ignore
        # print(da)
        nts = len(da.coords[t_name].values)
        native_dtype = da.dtype
        # gdptools will handle floats and ints - catch if gridded type is different
        try:
            dfval = _get_default_val(native_dtype=native_dtype)
        except TypeError as e:
            print(e)

        val_interp = _get_interp_array(
            n_geo=n_geo, nts=nts, native_dtype=native_dtype, default_val=dfval
        )

        mdata = np.ma.masked_array(da.values, np.isnan(da.values))  # type: ignore

        chunks = get_weight_chunks(
            unique_geom_ids=unique_geom_ids, mdata=mdata, dfval=dfval
        )

        worker_out = get_stats_dask(
            n_jobs=self._jobs,
            stat=self.stat,
            bag=bag_generator(jobs=self._jobs, chunks=chunks),
        )

        for index, val in worker_out[0]:
            val_interp[:, index] = val

        return gdf, val_interp


def get_stats_dask(
    n_jobs: int,
    stat: Union[Type[MAWeightedAverage], Type[WeightedAverage]],
    bag: Generator[List[AggChunk], None, None],
) -> List[Any]:
    """Get stats values."""
    worker_out = [
        dask.delayed(_stats)(chunk, method=stat) for chunk in bag  # type: ignore
    ]
    return dask.compute(worker_out)  # type: ignore
