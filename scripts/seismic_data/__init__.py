import pandas as pd
from scipy.interpolate import CubicSpline
import numpy as np
from os import path

data = pd.read_excel("Accelerograms.xlsx", sheet_name=["USDS-TH", "UD-TH", "CROSS-STR"])

usds_th = data["USDS-TH"]
ud_th = data["UD-TH"]
cross_str = data["CROSS-STR"]


def get_interpolation(_data: pd.DataFrame):
    x = _data["Time [s]"]
    y = _data["[cm/s/s]"]

    return CubicSpline(x, y, extrapolate=True)


def create_new_data(max_t: float, n_points: int, _data: pd.DataFrame):
    new_t = np.linspace(0, max_t, n_points)
    interpolation = get_interpolation(_data)
    new_data = interpolation(new_t)

    return pd.DataFrame({"Time [s]": new_t, "Acceleration [cm/s/s]": new_data})


def create_seismic_data(directory: str, max_t: float, n_points: int):
    create_new_data(max_t, n_points, usds_th).to_csv(
        path.join(directory, "usds_th.csv"),
        columns=["Time [s]", "Acceleration [cm/s/s]"],
        index=False,
        header=False,
        sep=" ",
    )

    create_new_data(max_t, n_points, ud_th).to_csv(
        path.join(directory, "ud_th.csv"),
        columns=["Time [s]", "Acceleration [cm/s/s]"],
        index=False,
        header=False,
        sep=" ",
    )

    create_new_data(max_t, n_points, cross_str).to_csv(
        path.join(directory, "cross_str.csv"),
        columns=["Time [s]", "Acceleration [cm/s/s]"],
        index=False,
        header=False,
        sep=" ",
    )
