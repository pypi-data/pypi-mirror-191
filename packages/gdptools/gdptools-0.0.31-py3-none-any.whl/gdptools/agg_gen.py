"""Calculate aggregation methods."""
from typing import Dict
from typing import List
from typing import Literal
from typing import Tuple
from typing import Type
from typing import Union

import geopandas as gpd
import numpy as np
import numpy.typing as npt
import pandas as pd

from gdptools.agg.agg_data_writers import CSVWriter
from gdptools.agg.agg_data_writers import NetCDFWriter
from gdptools.agg.agg_data_writers import ParquetWriter
from gdptools.agg.agg_engines import DaskAgg
from gdptools.agg.agg_engines import ParallelAgg
from gdptools.agg.agg_engines import SerialAgg
from gdptools.agg.stats_methods import MAWeightedAverage
from gdptools.agg.stats_methods import WeightedAverage
from gdptools.data.agg_gen_data import AggData
from gdptools.data.user_data import UserData

STATSMETHODS = Literal["masked_average", "average"]
""" List of available stats methods to apply to AggGen class.

masked_average: Accounts for missing gridded values and returns the partial weighted
    value.
average: Returns the weighted avarage.  If a polygon contains a cell value that is
    missing/nan then it will return a nan for that polygon.


Raises:
    TypeError: If supplied value is not one of STATSMETHODS

Returns:
    _type_: str
"""

AGGENGINES = Literal["serial", "parallel", "dask"]
""" List of aggregation methods.

serial: performes weighted-area aggregation by iterating through polygons.
parallel: performes weighted-area aggregation by number of jobs.
dask: performs weighted-area aggregation in the presence of a dask client.

TODO: parallel

Raises:
    TypeError: If supplied attribute is not one of AGGENGINES.

Returns:
    _type_: str
"""

AGGWRITERS = Literal["csv", "parquet", "netcdf"]
""" List of available writers applied to the aggregation.

csv: Output data in csv format.
parquet: Output data to parquet.gzip file.
netcdf: Output data in netcdf format.

Raises:
    TypeError: If supplied attribute is not one of AGGWRITERS.

Returns:
    _type_: str
"""


class AggGen:
    """Class for aggregating grid-to-polygons."""

    def __init__(
        self,
        user_data: UserData,
        stat_method: STATSMETHODS,
        agg_engine: AGGENGINES,
        agg_writer: AGGWRITERS,
        weights: Union[str, pd.DataFrame],
        out_path: str,
        file_prefix: str,
        append_date: bool = False,
        jobs: int = -1,
    ) -> None:
        """Initialize AggGen.

        Args:
            user_data (UserData): _description_
            stat_method (STATSMETHODS): _description_
            agg_engine (AGGENGINES): _description_
            agg_writer (AGGWRITERS): _description_
            weights (Union[str, pd.DataFrame]): _description_
            out_path (str): _description_
            file_prefix (str): _description_
            append_date (bool): _description_. Defaults to False.
            jobs (int): _description_. Defaults to -1

        Raises:
            TypeError: _description_
            TypeError: _description_
            TypeError: _description_
        """
        self._user_data = user_data
        self._stat_method = stat_method
        self._agg_engine = agg_engine
        self._agg_writer = agg_writer
        self._weights = weights
        self._out_path = out_path
        self._file_prefix = file_prefix
        self._append_date = append_date
        self._jobs = jobs
        self._agg_data: Dict[str, AggData]

        self._stat: Union[Type[MAWeightedAverage], Type[WeightedAverage]]
        if self._stat_method == "masked_average":
            self._stat = MAWeightedAverage
        elif self._stat_method == "average":
            self._stat = WeightedAverage
        else:
            raise TypeError(f"stat_method: {self._stat_method} not in {STATSMETHODS}")

        self.agg: Union[Type[SerialAgg], Type[ParallelAgg], Type[DaskAgg]]
        if self._agg_engine == "serial":
            self.agg = SerialAgg
        elif self._agg_engine == "parallel":
            self.agg = ParallelAgg
        elif self._agg_engine == "dask":
            self.agg = DaskAgg
        else:
            raise TypeError(f"agg_engine: {self._agg_engine} not in {AGGENGINES}")

        self.__writer: Union[Type[CSVWriter], Type[ParquetWriter], Type[NetCDFWriter]]
        if self._agg_writer == "csv":
            self.__writer = CSVWriter
        elif self._agg_writer == "parquet":
            self.__writer = ParquetWriter
        elif self._agg_writer == "netcdf":
            self.__writer = NetCDFWriter
        else:
            raise TypeError(f"agg_writer: {self._agg_writer} not in {AGGWRITERS}")

    def calculate_agg(
        self,
    ) -> Tuple[gpd.GeoDataFrame, List[npt.NDArray[Union[np.int_, np.double]]]]:
        """Calculate aggregations.

        Returns:
            Tuple[gpd.GeoDataFrame, List[npt.NDArray]]: _description_
        """
        self._agg_data, new_gdf, agg_vals = self.agg().calc_agg_from_dictmeta(
            user_data=self._user_data,
            weights=self._weights,
            stat=self._stat,
            jobs=self._jobs,
        )
        self.__writer().save_file(
            agg_data=self._agg_data,
            feature=new_gdf,
            vals=agg_vals,
            p_out=self._out_path,
            file_prefix=self._file_prefix,
            append_date=self._append_date,
        )

        return new_gdf, agg_vals

    @property
    def agg_data(self) -> dict[str, AggData]:
        """Return agg_data."""
        return self._agg_data
