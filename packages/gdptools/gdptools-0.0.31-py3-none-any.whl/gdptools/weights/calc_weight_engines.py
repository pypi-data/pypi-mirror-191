# sourcery skip: inline-immediately-returned-variable
"""Abstract Base Class for Template behavior pattern for calculating weights."""
import logging
import os
import time
from abc import ABC
from abc import abstractmethod
from collections.abc import Generator
from typing import Any
from typing import List
from typing import Tuple
from typing import Union

import dask.bag as db
import dask_geopandas as dgpd
import geopandas as gpd
import numpy as np
import numpy.typing as npt
import pandas as pd
import pygeos
from joblib import delayed
from joblib import Parallel
from joblib import parallel_backend

from gdptools.utils import _check_feature_crs
from gdptools.utils import _check_grid_cell_crs
from gdptools.utils import _check_poly_idx
from gdptools.utils import _get_crs
from gdptools.utils import _reproject_for_weight_calc

logger = logging.getLogger(__name__)


class CalcWeightEngine(ABC):
    """Abstract Base Class (ABC) implementing the template behavioral pattern.

    Abstract Base Class for calculating weights.  There are several weight generation
    methods implemented and they all share a common workflow with different methods
    for calculating the weights.  This ABC defines the calc_weights() workflow, with
    an @abstractmethod for get_weight_components() where new methods can be plugged
    in for weight generation.
    """

    def calc_weights(
        self,
        poly: gpd.GeoDataFrame,
        poly_idx: str,
        grid_cells: gpd.GeoDataFrame,
        wght_gen_crs: Any,
        filename: str = "",
        intersections: bool = False,
        jobs: int = -1,
        verbose: bool = False,
    ) -> Union[Tuple[pd.DataFrame, gpd.GeoDataFrame], pd.DataFrame]:
        """Template method for calculating weights.

        Args:
            poly (gpd.GeoDataFrame): _description_
            poly_idx (str): _description_
            grid_cells (gpd.GeoDataFrame): _description_
            wght_gen_crs (Any): _description_
            filename (str): _description_. Defaults to "".
            intersections (bool): _description_. Defaults to False.
            jobs (int): _description_. Defaults to 1.
            verbose (bool): _description_. Defaults to False.

        Returns:
            Union[pd.DataFrame, Optional[gpd.GeoDataFrame]]: _description_
        """
        self.poly = poly
        self.poly_idx = poly_idx
        self.grid_cells = grid_cells
        self.wght_gen_crs = wght_gen_crs
        self.filename = filename
        self.intersections = intersections
        self.jobs = jobs
        self.verbose = verbose
        _check_poly_idx(self.poly, self.poly_idx)
        _check_feature_crs(poly=self.poly)
        _check_grid_cell_crs(grid_cells=self.grid_cells)
        self.grid_out_crs = _get_crs(self.wght_gen_crs)
        self.poly, self.grid_cells = _reproject_for_weight_calc(
            poly=self.poly,
            grid_cells=self.grid_cells,
            grid_out_crs=self.grid_out_crs,
            wght_gen_crs=self.wght_gen_crs,
        )
        if not self.intersections:
            (
                self.plist,
                self.ilist,
                self.jlist,
                self.wghtlist,
            ) = self.get_weight_components()
        else:
            print(f"Intersections = {self.intersections}")
            (
                self.plist,
                self.ilist,
                self.jlist,
                self.wghtlist,
                self.calc_intersect,
            ) = self.get_weight_components_and_intesections()
        self.wght_df = self.create_wght_df()
        if self.filename:
            self.wght_df.to_csv(self.filename)
        if self.intersections:
            return self.wght_df, self.calc_intersect
        else:
            return self.wght_df
        # return (  # type: ignore
        #     self.wght_df, self.calc_intersect
        #     if self.intersections
        #     else self.wght_df
        # )

    @abstractmethod
    def get_weight_components(
        self,
    ) -> Tuple[List[object], List[int], List[int], List[float]]:
        """Abstract method for calculating weights.

        Classes that inherit this method will override this method for \
            weight-generation.

        Returns:
            Tuple[List[object], List[int], List[int], List[float]]:
            Returned tuples in order:
                1) plist: list of poly_idx strings.
                2) ilist i-index of grid_cells.
                3) jlist j-index of grid_cells.
                4) wghtslist weight values of i,j index of grid_cells.
        """
        pass

    @abstractmethod
    def get_weight_components_and_intesections(
        self,
    ) -> Tuple[List[object], List[int], List[int], List[float], gpd.GeoDataFrame]:
        """Abstract method for calculating weights.

        Classes that inherit this method will override this method for \
            weight-generation.

        Returns:
            Tuple[List[object], List[int], List[int], List[float]]:
            Returned tuples in order:
                1) plist: list of poly_idx strings.
                2) ilist i-index of grid_cells.
                3) jlist j-index of grid_cells.
                4) wghtslist weight values of i,j index of grid_cells.
        """
        pass

    def create_wght_df(self) -> pd.DataFrame:
        """Create dataframe from weight components."""
        wght_df = pd.DataFrame(
            {
                self.poly_idx: self.plist,
                "i": self.ilist,
                "j": self.jlist,
                "wght": self.wghtlist,
            }
        )
        wght_df = wght_df.astype(
            {"i": int, "j": int, "wght": float, self.poly_idx: str}
        )
        return wght_df


class SerialWghtGenEngine(CalcWeightEngine):
    """Tobbler python package Method to generate grid-to-polygon weight.

    This class is based on methods provided in the Tobbler package. See
        area_tables_bining() method.

    Args:
        CalcWeightEngine (ABC): Abstract Base Class (ABC) employing the Template behavior
            pattern.  The abstractmethod get weight components povides a method to plug-
            in new weight generation methods.
    """

    def get_weight_components(
        self,
    ) -> Tuple[List[object], List[int], List[int], List[float]]:
        """Template method from CalcWeightEngine class for generating weight components.

        Returns:
            Tuple[List[object], List[int], List[int], List[float]]:
            Returned tuples in order:
                1) plist: list of poly_idx strings.
                2) ilist i-index of grid_cells.
                3) jlist j-index of grid_cells.
                4) wghtslist weight values of i,j index of grid_cells.
        """
        tsrt = time.perf_counter()
        (
            plist,
            ilist,
            jlist,
            wghtslist,
        ) = self.area_tables_binning(source_df=self.grid_cells, target_df=self.poly)
        tend = time.perf_counter()
        print(f"Weight gen finished in {tend-tsrt:0.4f} seconds")

        return plist, ilist, jlist, wghtslist

    def get_weight_components_and_intesections(
        self,
    ) -> Tuple[List[object], List[int], List[int], List[float], gpd.GeoDataFrame]:
        """Template method from CalcWeightEngine class for generating weight components.

        Returns:
            Tuple[List[object], List[int], List[int], List[float]]:
            Returned tuples in order:
                1) plist: list of poly_idx strings.
                2) ilist i-index of grid_cells.
                3) jlist j-index of grid_cells.
                4) wghtslist weight values of i,j index of grid_cells.
        """
        tsrt = time.perf_counter()
        (
            plist,
            ilist,
            jlist,
            wghtslist,
            gdf,
        ) = self.area_tables_binning_and_intersections(
            source_df=self.grid_cells, target_df=self.poly
        )
        tend = time.perf_counter()
        print(f"Weight gen finished in {tend-tsrt:0.4f} seconds")

        return plist, ilist, jlist, wghtslist, gdf

    def area_tables_binning(
        self: "SerialWghtGenEngine",
        source_df: gpd.GeoDataFrame,
        target_df: gpd.GeoDataFrame,
    ) -> Tuple[List[object], List[int], List[int], List[float]]:
        """Construct intersection tables.

        Construct area allocation and source-target correspondence tables using
        a parallel spatial indexing approach. This method and its associated functions
        are based on and adapted from the Tobbler package:

        https://github.com/pysal/tobler.

        Tobler License:
        BSD 3-Clause License

        Copyright 2018 pysal-spopt developers

        Redistribution and use in source and binary forms, with or without modification,
            are permitted provided that the following conditions are met:

        1.  Redistributions of source code must retain the above copyright notice, this
            list of conditions and the following disclaimer.

        2.  Redistributions in binary form must reproduce the above copyright notice,
            this list of conditions and the following disclaimer in the documentation
            and/or other materials provided with the distribution.

        3.  Neither the name of the copyright holder nor the names of its contributors
            may be used to endorse or promote products derived from this software
            without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
        AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
        IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
        DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
        ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
        (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
        LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
        ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
        (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
        SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

        Args:
            source_df (gpd.GeoDataFrame): GeoDataFrame containing input data and
                polygons
            target_df (gpd.GeoDataFrame): GeoDataFrame defining the output geometries

        Returns:
            Returns:
            Tuple[List[object], List[int], List[int], List[float]]:
            Returned tuples in order:
                1) plist: list of poly_idx strings.
                2) ilist i-index of grid_cells.
                3) jlist j-index of grid_cells.
                4) wghtslist weight values of i,j index of grid_cells.
        """
        tstrt = time.perf_counter()
        df1 = _make_valid(source_df)
        df2 = _make_valid(target_df)
        tend = time.perf_counter()
        print(f"Validate polygons finished in {tend - tstrt:0.4f} seconds")

        tstrt = time.perf_counter()
        ids_tgt, ids_src = df1.sindex.query_bulk(df2.geometry, predicate="intersects")

        areas = (
            df1.geometry.values[ids_src].intersection(df2.geometry.values[ids_tgt]).area
            / df2.geometry.values[ids_tgt].area
        )
        tend = time.perf_counter()
        print(f"Intersections finished in {tend - tstrt:0.4f} seconds")

        return (
            df2[self.poly_idx].iloc[ids_tgt].values.astype(object).tolist(),
            df1.i_index.iloc[ids_src].values.astype(int).tolist(),
            df1.j_index.iloc[ids_src].values.astype(int).tolist(),
            areas.astype(float).tolist(),
        )

    def area_tables_binning_and_intersections(
        self: "SerialWghtGenEngine",
        source_df: gpd.GeoDataFrame,
        target_df: gpd.GeoDataFrame,
    ) -> Tuple[List[object], List[int], List[int], List[float], gpd.GeoDataFrame]:
        """Construct intersection tables.

        Construct area allocation and source-target correspondence tables using
        a parallel spatial indexing approach. This method and its associated functions
        are based on and adapted from the Tobbler package:

        https://github.com/pysal/tobler.

        Tobler License:
        BSD 3-Clause License

        Copyright 2018 pysal-spopt developers

        Redistribution and use in source and binary forms, with or without modification,
            are permitted provided that the following conditions are met:

        1.  Redistributions of source code must retain the above copyright notice, this
            list of conditions and the following disclaimer.

        2.  Redistributions in binary form must reproduce the above copyright notice,
            this list of conditions and the following disclaimer in the documentation
            and/or other materials provided with the distribution.

        3.  Neither the name of the copyright holder nor the names of its contributors
            may be used to endorse or promote products derived from this software
            without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
        AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
        IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
        DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
        ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
        (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
        LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
        ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
        (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
        SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

        Args:
            source_df (gpd.GeoDataFrame): GeoDataFrame containing input data and
                polygons
            target_df (gpd.GeoDataFrame): GeoDataFrame defining the output geometries

        Returns:
            Returns:
            Tuple[List[object], List[int], List[int], List[float]]:
            Returned tuples in order:
                1) plist: list of poly_idx strings.
                2) ilist i-index of grid_cells.
                3) jlist j-index of grid_cells.
                4) wghtslist weight values of i,j index of grid_cells.
        """
        tstrt = time.perf_counter()
        df1 = _make_valid(source_df)
        df2 = _make_valid(target_df)
        tend = time.perf_counter()
        print(f"Validate polygons finished in {tend - tstrt:0.4f} seconds")

        tstrt = time.perf_counter()
        ids_tgt, ids_src = df1.sindex.query_bulk(df2.geometry, predicate="intersects")
        f_intersect = df1.geometry.values[ids_src].intersection(
            df2.geometry.values[ids_tgt]
        )
        areas = f_intersect.area / df2.geometry.values[ids_tgt].area
        gdf_inter = df2.iloc[ids_tgt]
        gdf_inter.set_geometry(f_intersect, inplace=True)
        tend = time.perf_counter()
        print(f"Intersections finished in {tend - tstrt:0.4f} seconds")

        return (
            df2[self.poly_idx].iloc[ids_tgt].values.astype(object).tolist(),
            df1.i_index.iloc[ids_src].values.astype(int).tolist(),
            df1.j_index.iloc[ids_src].values.astype(int).tolist(),
            areas.astype(float).tolist(),
            gdf_inter,
        )


class ParallelWghtGenEngine(CalcWeightEngine):
    """Tobbler package Method to generate grid-to-polygon weight.

    This class is based on methods provided in the Tobbler package. See
        area_tables_bining_parallel() method.

    Args:
        CalcWeightEngine (ABC): Abstract Base Class (ABC) employing the Template behavior
            pattern.  The abstractmethod get weight components povides a method to plug-
            in new weight generation methods.
    """

    def get_weight_components(
        self,
    ) -> Tuple[List[object], List[int], List[int], List[float]]:
        """Template method from CalcWeightEngine class for generating weight components.

        Returns:
            Tuple[List[object], List[int], List[int], List[float]]:
            Returned tuples in order:
                1) plist: list of poly_idx strings.
                2) ilist i-index of grid_cells.
                3) jlist j-index of grid_cells.
                4) wghtslist weight values of i,j index of grid_cells.
        """
        tsrt = time.perf_counter()
        plist, ilist, jlist, wghtslist = _area_tables_binning_parallel(
            source_df=self.grid_cells,
            target_df=self.poly,
            poly_idx=self.poly_idx,
            n_jobs=self.jobs,
        )
        tend = time.perf_counter()
        print(f"Weight gen finished in {tend-tsrt:0.4f} seconds")

        return plist, ilist, jlist, wghtslist

    def get_weight_components_and_intesections(
        self,
    ) -> Tuple[List[object], List[int], List[int], List[float], gpd.GeoDataFrame]:
        """Template method from CalcWeightEngine class for generating weight components.

        Returns:
            Tuple[List[object], List[int], List[int], List[float]]:
            Returned tuples in order:
                1) plist: list of poly_idx strings.
                2) ilist i-index of grid_cells.
                3) jlist j-index of grid_cells.
                4) wghtslist weight values of i,j index of grid_cells.
        """
        tsrt = time.perf_counter()
        (
            plist,
            ilist,
            jlist,
            wghtslist,
            gdf,
        ) = _area_tables_binning_parallel_and_intersections(
            source_df=self.grid_cells,
            target_df=self.poly,
            poly_idx=self.poly_idx,
            n_jobs=self.jobs,
        )
        tend = time.perf_counter()
        print(f"Weight gen finished in {tend-tsrt:0.4f} seconds")

        return plist, ilist, jlist, wghtslist, gdf


def _area_tables_binning_parallel_and_intersections(
    source_df: gpd.GeoDataFrame,
    target_df: gpd.GeoDataFrame,
    poly_idx: str,
    n_jobs: int = -1,
) -> Tuple[List[object], List[int], List[int], List[float], gpd.GeoDataFrame]:
    """Construct intersection tables.

    Construct area allocation and source-target correspondence tables using
    a parallel spatial indexing approach. This method and its associated functions
    are based on and adapted from the Tobbler package:

    https://github.com/pysal/tobler.

    Tobler License:
    BSD 3-Clause License

    Copyright 2018 pysal-spopt developers

    Redistribution and use in source and binary forms, with or without modification,
        are permitted provided that the following conditions are met:

    1.  Redistributions of source code must retain the above copyright notice, this
        list of conditions and the following disclaimer.

    2.  Redistributions in binary form must reproduce the above copyright notice,
        this list of conditions and the following disclaimer in the documentation
        and/or other materials provided with the distribution.

    3.  Neither the name of the copyright holder nor the names of its contributors
        may be used to endorse or promote products derived from this software
        without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
    ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
    ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    Args:
        source_df (gpd.GeoDataFrame): GeoDataFrame containing input data and
            polygons
        target_df (gpd.GeoDataFrame): GeoDataFrame defining the output geometries
        poly_idx (str): id string of feature
        n_jobs (int): [Default=-1]
            Number of processes to run in parallel. If -1, this is set to the
            number of CPUs available

    Returns:
        Tuple[List[object], List[int], List[int], List[float]]:
        Returned tuples in order:
            1) plist: list of poly_idx strings.
            2) ilist i-index of grid_cells.
            3) jlist j-index of grid_cells.
            4) wghtslist weight values of i,j index of grid_cells.
    """
    if n_jobs == -1:
        n_jobs = os.cpu_count()  # type: ignore
        logger.info(" ParallelWghtGenEngine getting jobs from os.cpu_count()")
    logger.info(f"  ParallelWghtGenEngine using {n_jobs} jobs")
    # Buffer polygons with self-intersections
    tstrt = time.perf_counter()
    df1 = _make_valid(source_df)
    df2 = _make_valid(target_df)
    tend = time.perf_counter()
    print(f"Validate polygons finished in {tend - tstrt:0.4f} seconds")

    # Chunk the largest, ship the smallest in full
    to_chunk, df_full = _get_chunks_for_parallel(df1, df2)

    # Spatial index query: Reindex on positional IDs
    to_workers = _chunk_dfs(
        gpd.GeoSeries(to_chunk.geometry.values, crs=to_chunk.crs),
        gpd.GeoSeries(df_full.geometry.values, crs=df_full.crs),
        n_jobs,
    )

    worker_out = _get_ids_for_parallel(n_jobs, to_workers)
    ids_src, ids_tgt = np.concatenate(worker_out).T

    # Intersection + area calculation
    chunks_to_intersection = _chunk_polys(
        np.vstack([ids_src, ids_tgt]).T, df1.geometry, df2.geometry, n_jobs
    )
    worker_out = _get_areas_and_intersections_for_parallel(
        n_jobs, chunks_to_intersection
    )
    areas = np.concatenate([item[0] for item in worker_out])
    inter_geom = np.concatenate([item[1] for item in worker_out])

    print("Processing intersections for output.")
    inter_sect = df2.iloc[ids_tgt, :].set_geometry(inter_geom)
    weights = areas.astype(float) / df2.geometry[ids_tgt].area
    inter_sect["weights"] = weights

    return (
        df2[poly_idx].iloc[ids_tgt].values.astype(object).tolist(),
        df1.i_index.iloc[ids_src].values.astype(int).tolist(),
        df1.j_index.iloc[ids_src].values.astype(int).tolist(),
        (areas.astype(float) / df2.geometry[ids_tgt].area).tolist(),
        inter_sect,
    )


def _get_areas_and_intersections_for_parallel(
    n_jobs: int,
    chunks_to_intersection: Generator[Tuple[npt.ArrayLike, npt.ArrayLike], Any, Any],
) -> Any:
    """Get poly-to-poly intersections."""
    with parallel_backend("loky", inner_max_num_threads=1):
        worker_out = Parallel(n_jobs=n_jobs)(
            delayed(_intersect_area_on_chunk)(*chunk_pair)
            for chunk_pair in chunks_to_intersection
        )
    return worker_out


def _get_areas_for_parallel(
    n_jobs: int,
    chunks_to_intersection: Generator[Tuple[npt.ArrayLike, npt.ArrayLike], Any, Any],
) -> Any:
    """Get poly-to-poly intersections."""
    with parallel_backend("loky", inner_max_num_threads=1):
        worker_out = Parallel(n_jobs=n_jobs)(
            delayed(_area_on_chunk)(*chunk_pair)
            for chunk_pair in chunks_to_intersection
        )
    return worker_out


def _get_ids_for_parallel(
    n_jobs: int, to_workers: Generator[Tuple[gpd.GeoSeries, gpd.GeoSeries], Any, Any]
) -> Any:
    """Get poly-to-poly intersection ids."""
    with parallel_backend("loky", inner_max_num_threads=1):
        worker_out = Parallel(n_jobs=n_jobs)(
            delayed(_index_n_query)(*chunk_pair) for chunk_pair in to_workers
        )
    return worker_out


def _get_chunks_for_parallel(
    df1: gpd.GeoDataFrame, df2: gpd.GeoDataFrame
) -> Tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """Chunk dataframes."""
    to_chunk = df1
    df_full = df2
    return to_chunk, df_full


def _area_tables_binning_parallel(
    source_df: gpd.GeoDataFrame,
    target_df: gpd.GeoDataFrame,
    poly_idx: str,
    n_jobs: int = -1,
) -> Tuple[List[object], List[int], List[int], List[float]]:
    """Construct intersection tables.

    Construct area allocation and source-target correspondence tables using
    a parallel spatial indexing approach. This method and its associated functions
    are based on and adapted from the Tobbler package:

    https://github.com/pysal/tobler.

    Tobler License:
    BSD 3-Clause License

    Copyright 2018 pysal-spopt developers

    Redistribution and use in source and binary forms, with or without modification,
        are permitted provided that the following conditions are met:

    1.  Redistributions of source code must retain the above copyright notice, this
        list of conditions and the following disclaimer.

    2.  Redistributions in binary form must reproduce the above copyright notice,
        this list of conditions and the following disclaimer in the documentation
        and/or other materials provided with the distribution.

    3.  Neither the name of the copyright holder nor the names of its contributors
        may be used to endorse or promote products derived from this software
        without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
    ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
    ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    Args:
        source_df (gpd.GeoDataFrame): GeoDataFrame containing input data and
            polygons
        target_df (gpd.GeoDataFrame): GeoDataFrame defining the output geometries
        poly_idx (str): string id of feature
        n_jobs (int): [Default=-1]
            Number of processes to run in parallel. If -1, this is set to the
            number of CPUs available

    Returns:
        Tuple[List[object], List[int], List[int], List[float]]:
        Returned tuples in order:
            1) plist: list of poly_idx strings.
            2) ilist i-index of grid_cells.
            3) jlist j-index of grid_cells.
            4) wghtslist weight values of i,j index of grid_cells.
    """
    if n_jobs == -1:
        n_jobs = os.cpu_count()  # type: ignore
        logger.info(" ParallelWghtGenEngine getting jobs from os.cpu_count()")
    logger.info(f"  ParallelWghtGenEngine using {n_jobs} jobs")

    # Buffer polygons with self-intersections
    tstrt = time.perf_counter()
    df1 = _make_valid(source_df)
    df2 = _make_valid(target_df)
    tend = time.perf_counter()
    print(f"Validate polygons finished in {tend - tstrt:0.4f} seconds")

    # Chunk the largest, ship the smallest in full
    to_chunk, df_full = _get_chunks_for_parallel(df1, df2)

    # Spatial index query: Reindex on positional IDs
    to_workers = _chunk_dfs(
        gpd.GeoSeries(to_chunk.geometry.values, crs=to_chunk.crs),
        gpd.GeoSeries(df_full.geometry.values, crs=df_full.crs),
        n_jobs,
    )

    worker_out = _get_ids_for_parallel(n_jobs, to_workers)
    ids_src, ids_tgt = np.concatenate(worker_out).T

    # Intersection + area calculation
    chunks_to_intersection = _chunk_polys(
        np.vstack([ids_src, ids_tgt]).T, df1.geometry, df2.geometry, n_jobs
    )
    worker_out = _get_areas_for_parallel(n_jobs, chunks_to_intersection)
    areas = np.concatenate(worker_out)

    return (
        df2[poly_idx].iloc[ids_tgt].values.astype(object).tolist(),
        df1.i_index.iloc[ids_src].values.astype(int).tolist(),
        df1.j_index.iloc[ids_src].values.astype(int).tolist(),
        (areas.astype(float) / df2.geometry[ids_tgt].area).tolist(),
    )


class DaskWghtGenEngine(CalcWeightEngine):
    """Tobbler package Method to generate grid-to-polygon weight.

    This class is based on methods provided in the Tobbler package. See
        area_tables_bining_parallel() method.

    Args:
        CalcWeightEngine (ABC): Abstract Base Class (ABC) employing the Template behavior
            pattern.  The abstractmethod get weight components povides a method to plug-
            in new weight generation methods.
    """

    def get_weight_components(
        self,
    ) -> Tuple[List[object], List[int], List[int], List[float]]:
        """Template method from CalcWeightEngine class for generating weight components.

        Returns:
            Tuple[List[object], List[int], List[int], List[float]]:
            Returned tuples in order:
                1) plist: list of poly_idx strings.
                2) ilist i-index of grid_cells.
                3) jlist j-index of grid_cells.
                4) wghtslist weight values of i,j index of grid_cells.
        """
        tsrt = time.perf_counter()
        plist, ilist, jlist, wghtslist = _area_tables_binning_for_dask(
            source_df=self.grid_cells,
            target_df=self.poly,
            poly_idx=self.poly_idx,
            n_jobs=self.jobs,
        )
        tend = time.perf_counter()
        print(f"Weight gen finished in {tend-tsrt:0.4f} seconds")

        return plist, ilist, jlist, wghtslist

    def get_weight_components_and_intesections(
        self,
    ) -> Tuple[List[object], List[int], List[int], List[float], gpd.GeoDataFrame]:
        """Template method from CalcWeightEngine class for generating weight components.

        Returns:
            Tuple[List[object], List[int], List[int], List[float]]:
            Returned tuples in order:
                1) plist: list of poly_idx strings.
                2) ilist i-index of grid_cells.
                3) jlist j-index of grid_cells.
                4) wghtslist weight values of i,j index of grid_cells.
        """
        tsrt = time.perf_counter()
        (
            plist,
            ilist,
            jlist,
            wghtslist,
            gdf,
        ) = _area_tables_binning_and_intersections_for_dask(
            source_df=self.grid_cells,
            target_df=self.poly,
            poly_idx=self.poly_idx,
            n_jobs=self.jobs,
        )
        tend = time.perf_counter()
        print(f"Weight gen finished in {tend-tsrt:0.4f} seconds")

        return plist, ilist, jlist, wghtslist, gdf


def _area_tables_binning_and_intersections_for_dask(
    source_df: gpd.GeoDataFrame,
    target_df: gpd.GeoDataFrame,
    poly_idx: str,
    n_jobs: int = -1,
) -> Tuple[List[object], List[int], List[int], List[float], gpd.GeoDataFrame]:
    """Construct intersection tables.

    Construct area allocation and source-target correspondence tables using
    a parallel spatial indexing approach. This method and its associated functions
    are based on and adapted from the Tobbler package:

    https://github.com/pysal/tobler.

    Tobler License:
    BSD 3-Clause License

    Copyright 2018 pysal-spopt developers

    Redistribution and use in source and binary forms, with or without modification,
        are permitted provided that the following conditions are met:

    1.  Redistributions of source code must retain the above copyright notice, this
        list of conditions and the following disclaimer.

    2.  Redistributions in binary form must reproduce the above copyright notice,
        this list of conditions and the following disclaimer in the documentation
        and/or other materials provided with the distribution.

    3.  Neither the name of the copyright holder nor the names of its contributors
        may be used to endorse or promote products derived from this software
        without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
    ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
    ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    Args:
        source_df (gpd.GeoDataFrame): GeoDataFrame containing input data and
            polygons
        target_df (gpd.GeoDataFrame): GeoDataFrame defining the output geometries
        poly_idx (str): string id of features
        n_jobs (int): [Default=-1]
            Number of processes to run in parallel. If -1, this is set to the
            number of CPUs available

    Raises:
        ValueError: _description_

    Returns:
        Tuple[List[object], List[int], List[int], List[float]]:
        Returned tuples in order:
            1) plist: list of poly_idx strings.
            2) ilist i-index of grid_cells.
            3) jlist j-index of grid_cells.
            4) wghtslist weight values of i,j index of grid_cells.
    """
    if n_jobs == -1:
        raise ValueError(
            " Dask generator requires the Optional jobs parameter to be set"
        )

    # Buffer polygons with self-intersections
    tstrt = time.perf_counter()
    df1 = _make_valid(source_df)
    df2 = _make_valid(target_df)
    tend = time.perf_counter()
    print(f"Validate polygons finished in {tend - tstrt:0.4f} seconds")

    # Chunk the largest, ship the smallest in full
    sdf, tdf = _get_chunks_for_dask(n_jobs, df1, df2)
    sdf.calculate_spatial_partitions()

    id_chunks = _ids_for_dask_generator(sdf=sdf, tdf=tdf)
    worker_out = _get_ids_for_dask(id_chunks)
    ids_src, ids_tgt = np.concatenate(worker_out).T

    # Intersection + area calculation
    chunks_to_intersection = _chunk_polys_dask(
        np.vstack([ids_src, ids_tgt]).T, df1.geometry, df2.geometry, n_jobs
    )

    worker_out = _get_areas_and_intersections_for_dask(n_jobs, chunks_to_intersection)
    areas = np.concatenate([item[0] for item in worker_out])
    inter_geom = np.concatenate([item[1] for item in worker_out])

    print("Processing intersections for output.")
    inter_sect = df2.iloc[ids_tgt, :].set_geometry(inter_geom)
    weights = areas.astype(float) / df2.geometry[ids_tgt].area
    inter_sect["weights"] = weights

    return (
        df2[poly_idx].iloc[ids_tgt].values.astype(object).tolist(),
        df1.i_index.iloc[ids_src].values.astype(int).tolist(),
        df1.j_index.iloc[ids_src].values.astype(int).tolist(),
        (areas.astype(float) / df2.geometry[ids_tgt].area).tolist(),
        inter_sect,
    )


def _ids_for_dask_generator(
    sdf: dgpd.GeoDataFrame, tdf: dgpd.GeoDataFrame
) -> Generator[Tuple[gpd.GeoSeries, gpd.GeoSeries], Any, Any]:
    for part in tdf.partitions:
        target_chunk = part.compute()
        bnds = target_chunk.total_bounds
        source_chunk = sdf.cx[bnds[0] : bnds[1], bnds[2] : bnds[3]].compute()
        yield (
            gpd.GeoSeries(
                source_chunk.geometry.values,
                index=source_chunk.index,
                crs=source_chunk.crs,
            ),
            gpd.GeoSeries(
                target_chunk.geometry.values,
                index=target_chunk.index,
                crs=target_chunk.crs,
            ),
        )


def _get_areas_and_intersections_for_dask(
    jobs: int,
    chunks_to_intersection: Generator[Tuple[gpd.GeoSeries, gpd.GeoSeries], Any, Any],
) -> Any:
    """Get poly-to-poly intersections."""
    b = db.from_sequence(chunks_to_intersection, npartitions=jobs)  # type: ignore
    b = b.map(_intersect_area_on_chunk_dask)
    return b.compute()


def _get_areas_for_dask(
    jobs: int,
    chunks_to_intersection: Generator[Tuple[npt.ArrayLike, npt.ArrayLike], Any, Any],
) -> Any:
    """Get poly-to-poly intersections."""
    b = db.from_sequence(chunks_to_intersection, npartitions=jobs)  # type: ignore
    b = b.map(_area_on_chunk_dask)
    return b.compute()


def _get_ids_for_dask(
    to_workers: Generator[Tuple[gpd.GeoSeries, gpd.GeoSeries], Any, Any]
) -> Any:
    """Get poly-to-poly intersection ids."""
    b = db.from_sequence(to_workers)  # type: ignore
    result = b.map(_index_n_query_dask)
    return result.compute()


def _area_tables_binning_for_dask(
    source_df: gpd.GeoDataFrame,
    target_df: gpd.GeoDataFrame,
    poly_idx: str,
    n_jobs: int = -1,
) -> Tuple[List[object], List[int], List[int], List[float]]:
    """Construct intersection tables.

    Construct area allocation and source-target correspondence tables using
    a parallel spatial indexing approach. This method and its associated functions
    are based on and adapted from the Tobbler package:

    https://github.com/pysal/tobler.

    Tobler License:
    BSD 3-Clause License

    Copyright 2018 pysal-spopt developers

    Redistribution and use in source and binary forms, with or without modification,
        are permitted provided that the following conditions are met:

    1.  Redistributions of source code must retain the above copyright notice, this
        list of conditions and the following disclaimer.

    2.  Redistributions in binary form must reproduce the above copyright notice,
        this list of conditions and the following disclaimer in the documentation
        and/or other materials provided with the distribution.

    3.  Neither the name of the copyright holder nor the names of its contributors
        may be used to endorse or promote products derived from this software
        without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
    ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
    ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    Args:
        source_df (gpd.GeoDataFrame): GeoDataFrame containing input data and
            polygons
        target_df (gpd.GeoDataFrame): GeoDataFrame defining the output geometries
        poly_idx (str): string id for features
        n_jobs (int): [Default=-1]
            Number of processes to run in parallel. If -1, this is set to the
            number of CPUs available

    Raises:
        ValueError: _description_

    Returns:
        Tuple[List[object], List[int], List[int], List[float]]:
        Returned tuples in order:
            1) plist: list of poly_idx strings.
            2) ilist i-index of grid_cells.
            3) jlist j-index of grid_cells.
            4) wghtslist weight values of i,j index of grid_cells.
    """
    if n_jobs == -1:
        raise ValueError(
            " Dask generator requires the Optional jobs parameter to be set"
        )

    # Buffer polygons with self-intersections
    tstrt = time.perf_counter()
    df1 = _make_valid(source_df)
    df2 = _make_valid(target_df)
    tend = time.perf_counter()
    print(f"Validate polygons finished in {tend - tstrt:0.4f} seconds")

    # Chunk the largest, ship the smallest in full
    sdf, tdf = _get_chunks_for_dask(n_jobs, df1, df2)
    sdf.calculate_spatial_partitions()

    id_chunks = _ids_for_dask_generator(sdf=sdf, tdf=tdf)
    worker_out = _get_ids_for_dask(id_chunks)
    ids_src, ids_tgt = np.concatenate(worker_out).T

    # Intersection + area calculation
    chunks_to_intersection = _chunk_polys_dask(
        np.vstack([ids_src, ids_tgt]).T, df1.geometry, df2.geometry, n_jobs
    )

    worker_out = _get_areas_for_dask(n_jobs, chunks_to_intersection)
    areas = np.concatenate(worker_out)

    return (
        df2[poly_idx].iloc[ids_tgt].values.astype(object).tolist(),
        df1.i_index.iloc[ids_src].values.astype(int).tolist(),
        df1.j_index.iloc[ids_src].values.astype(int).tolist(),
        (areas.astype(float) / df2.geometry[ids_tgt].area).tolist(),
    )


def _get_chunks_for_dask(
    jobs: int, source_df: gpd.GeoDataFrame, target_df: gpd.GeoDataFrame
) -> Tuple[dgpd.GeoDataFrame, dgpd.GeoDataFrame]:
    """Chunk dataframes."""
    return (
        dgpd.from_geopandas(source_df, npartitions=jobs),
        dgpd.from_geopandas(target_df, npartitions=jobs),
    )


def _chunk_dfs(
    geoms_to_chunk: gpd.GeoSeries, geoms_full: gpd.GeoSeries, n_jobs: int
) -> Generator[Tuple[gpd.GeoSeries, gpd.GeoSeries], Any, Any]:
    """Chunk dataframes for parallel processing."""
    chunk_size = geoms_to_chunk.shape[0] // n_jobs + 1
    for i in range(n_jobs):
        start = i * chunk_size
        yield geoms_to_chunk.iloc[start : start + chunk_size], geoms_full


def _index_n_query(geoms1: gpd.GeoSeries, geoms2: gpd.GeoSeries) -> npt.ArrayLike:
    """Get geom ids for parallel processing."""
    # Pick largest for STRTree, query_bulk the smallest

    # Build tree + query
    qry_polyids, tree_polyids = geoms1.sindex.query_bulk(geoms2, predicate="intersects")
    # Remap IDs to global
    large_global_ids = geoms1.iloc[tree_polyids].index.values
    small_global_ids = geoms2.iloc[qry_polyids].index.values

    return np.array([large_global_ids, small_global_ids]).T


def _index_n_query_dask(bag: Tuple[gpd.GeoSeries, gpd.GeoSeries]) -> npt.ArrayLike:
    """Get geom ids for parallel processing."""
    # Build tree + query
    source_df = bag[0]
    target_df = bag[1]
    qry_polyids, tree_polyids = source_df.sindex.query_bulk(
        target_df, predicate="intersects"
    )
    # Remap IDs to global
    large_global_ids = source_df.iloc[tree_polyids].index.values
    small_global_ids = target_df.iloc[qry_polyids].index.values

    return np.array([large_global_ids, small_global_ids]).T


def _chunk_polys(
    id_pairs: npt.NDArray[np.int_],
    geoms_left: gpd.GeoSeries,
    geoms_right: gpd.GeoSeries,
    n_jobs: int,
) -> Generator[Tuple[npt.ArrayLike, npt.ArrayLike], Any, Any]:
    """Chunk polys for parallel processing."""
    chunk_size = id_pairs.shape[0] // n_jobs + 1
    for i in range(n_jobs):
        start = i * chunk_size
        chunk1 = geoms_left.values.data[id_pairs[start : start + chunk_size, 0]]
        chunk2 = geoms_right.values.data[id_pairs[start : start + chunk_size, 1]]
        yield chunk1, chunk2


def _chunk_polys_dask(
    id_pairs: npt.NDArray[np.int_],
    geoms_left: gpd.GeoSeries,
    geoms_right: gpd.GeoSeries,
    n_jobs: int,
) -> Generator[Tuple[npt.ArrayLike, npt.ArrayLike], Any, Any]:
    """Chunk polys for parallel processing."""
    chunk_size = id_pairs.shape[0] // n_jobs + 1
    for i in range(n_jobs):
        start = i * chunk_size
        chunk1 = geoms_left.values.data[id_pairs[start : start + chunk_size, 0]]
        chunk2 = geoms_right.values.data[id_pairs[start : start + chunk_size, 1]]
        yield (chunk1, chunk2)


def _intersect_area_on_chunk(
    geoms1: npt.ArrayLike, geoms2: npt.ArrayLike
) -> Tuple[gpd.GeoSeries, gpd.GeoSeries]:
    """Get intersection areas."""
    f_intersect = pygeos.intersection(geoms1, geoms2)
    return pygeos.area(f_intersect), f_intersect


def _area_on_chunk(geoms1: gpd.GeoSeries, geoms2: gpd.GeoSeries) -> gpd.GeoSeries:
    """Get intersection areas."""
    return pygeos.area(pygeos.intersection(geoms1, geoms2))


def _area_on_chunk_dask(dask_bag: Tuple[npt.ArrayLike, npt.ArrayLike]) -> gpd.GeoSeries:
    """Get intersection areas."""
    geoms1 = dask_bag[0]
    geoms2 = dask_bag[1]
    return pygeos.area(pygeos.intersection(geoms1, geoms2))


def _intersect_area_on_chunk_dask(
    dask_bag: Tuple[npt.ArrayLike, npt.ArrayLike]
) -> gpd.GeoSeries:
    """Get intersection areas."""
    geoms1 = dask_bag[0]
    geoms2 = dask_bag[1]
    f_intersect = pygeos.intersection(geoms1, geoms2)
    return pygeos.area(f_intersect), f_intersect


def _make_valid(df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Make in-valid geometries valid.

    Based on the method in Shapely and slightly modified for use here:

    Copyright (c) 2007, Sean C. Gillies. 2019, Casper van der Wel. 2007-2022,
    Shapely Contributors. All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived from
    this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    Args:
        df (gpd.GeoDataFrame): _description_

    Returns:
        _type_: _description_
    """
    polys = ["Polygon", "MultiPolygon"]
    if df.geom_type.isin(polys).all():
        mask = ~df.geometry.is_valid
        col = df._geometry_column_name
        df.loc[mask, col] = df.loc[mask, col].buffer(0)
    return df
