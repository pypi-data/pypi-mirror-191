import numpy as np
from math import gamma
from numba import njit, prange


def pdf_student_t(dof: int, t: np.array):
    """returns a np.array of len(t) of the probabilty density function of the student-t distrobution"""
    numerator = gamma(((dof + 1) / 2))
    denomenator = ((dof * np.pi) ** 0.5) * gamma((dof / 2))
    x = 1 + ((t**2) / dof)
    exponent = -((dof + 1) / 2)
    return (numerator / denomenator) * (x**exponent)


def pdf_normal(x: np.array, mean: float, std_dev: float):
    """returns a np.array of len(x) of the probabilty density function of the normal distrobution"""
    fraction = 1 / (std_dev * (np.sqrt(2 * np.pi)))
    exponent = -(0.5) * (((x - mean) / std_dev)) ** 2
    pdf = fraction * np.exp(exponent)
    return pdf


@njit(parallel=True)
def cal_uncerts(t: np.array, pdf: np.array, std_devs: np.array):
    """returns a np.array of len(std_devs) with the 2 sided cumulative probability from the mean and ourwards"""
    dt = t[1] - t[0]
    uncert = np.empty(len(std_devs))
    for j in prange(len(std_devs)):
        u = 0
        std_dev = std_devs[j]
        for i in range(
            len(t) - len(t[t >= -std_devs[j]]), len(t) - len(t[t >= std_devs[j]]) - 1
        ):
            u = u + ((pdf[i] + pdf[i + 1]) / 2) * dt
        uncert[j] = u
    return uncert


def get_confidence_intervall(coverage_factor: float):
    """returns the confidence intervall of a std.normal distributed with any given coverage factor or num. of std-devs"""
    x = np.linspace(-20, 20, 20000)
    # Std normal distrobution
    mean = 0
    std_dev = 1
    std_normal_pdf = pdf_normal(x, mean, std_dev)
    dx = x[1] - x[0]
    u = 0
    for i in range(
        len(x) - len(x[x >= -std_dev * coverage_factor]),
        len(x) - len(x[x >= std_dev * coverage_factor]),
    ):
        u = u + std_normal_pdf[i] * dx
    # print(u)
    return u


# Range conversion factor from range of valuse to approximate observed values standard deviation
d_n = [
    0,
    0,
    1.128,
    1.693,
    2.059,
    2.326,
    2.534,
    2.704,
    2.847,
    2.970,
    3.078,
    3.173,
    3.258,
]


def d(n: int):
    """
    int n = the number of samples
    getting the convertion factor for better estimation of standard deviation for w (range of values) of the values.
    ~Davies, O. L., Statistical Methods in Research and Production, 2nd Edition, Longman, 1984
    """
    if n <= 1:
        raise Exception("Sorry, no numbers below 1, for getting d_n")
    if n <= 12:
        return d_n[n]
    else:
        return np.sqrt(n)


def calculate_uncertanity(x, **params):
    """
    x : list, np.ndarray of values
    params:
        confidence_intervall = 0.95,
        repetability = True,
        coverage_factor = 0.0
        print_result = False
    return: dict:
            'uncertanity_fraction',
            'uncertanity_prcent',
            'uncertanity_in_unit',
            'standard_deviaton' (bessel corrected),
            'mean',
            'repetability',
            'n',
            'dof',
            'confidence_intervall'
    """
    # Default values
    confidence_intervall = 0.95
    repetability = True
    print_result = False

    # overwrite default with params
    if len(params) != 0:
        if (
            "confidence_intervall" not in params.keys()
            and "coverage_factor" not in params.keys()
        ):
            confidence_intervall = 0.95
        if "repetability" not in params.keys():
            repetability = True
        if "print_result" not in params.keys():
            print_result = False

        for key, value in params.items():
            if key == "confidence_intervall":
                if (
                    "coverage_factor" in params.keys()
                    and params["coverage_factor"] > 0.0
                ):
                    raise "both coverage factor and confidence intevall is set into this function, only one allowed"
                else:
                    confidence_intervall = value

            if key == "coverage_factor":
                if (
                    "confidence_intervall" in params.keys()
                    and params["confidence_intervall"] > 0.0
                ):
                    if "confidence_intervall" in params.keys():
                        raise "both coverage factor and confidence intevall is set into this function, only one allowed"
                else:
                    confidence_intervall = get_confidence_intervall(value)

            if key == "repetability":
                repetability = value
            if key == "print_result":
                print_result = value

    # Thebasics
    x_bar = np.mean(x)
    n = len(x)
    # Break out if not enough datapoints
    if n <= 2:
        result = {
            "uncertanity_fraction": np.nan,
            "uncertanity_prcent": np.nan,
            "uncertanity_in_unit": np.nan,
            "standard_deviaton": np.nan,
            "mean": x_bar,
            "n": n,
        }
        return result

    w = (
        max(x) - min(x)
    ) / x_bar  # Repeatability of datapints as a fraction aka range of values
    dof = n - 1
    x_n = x_n = np.array(x) / x_bar  # Noralized datapoints as a fraction
    x_t = (np.array(x) - x_bar) / np.std(
        x, ddof=1
    )  # centerd and scaled the data points
    x_t_b = (np.array(x) - x_bar) / (
        np.std(x, ddof=1) / np.sqrt(n)
    )  # centerd and scaled the data points - bessel corrected

    # create the probability density distrobution
    t = np.linspace(-20, 20, 20000)
    pdf = pdf_student_t(dof, t)

    std_devs = np.linspace(0, max(t), int(len(t) / 2))
    uncert = cal_uncerts(t, pdf, std_devs)  # cumulative pfd, dual sided.
    t_ci_dof = std_devs[len(uncert) - len(uncert[uncert >= confidence_intervall])]
    if repetability:
        s_y = w / d(n)
    else:
        s_y = np.std(x_n, ddof=1)

    s_y_bar = s_y / np.sqrt(n)

    uncertanity_fraction = t_ci_dof * s_y_bar
    uncertanity_in_unit = x_bar * uncertanity_fraction
    if print_result:
        print(w)
        print("Result = {:.3f}".format(x_bar) + " ± {:.3f}".format(uncertanity_in_unit))
        print(
            "Result = {:.3f}".format(x_bar)
            + " ± {:.4f}%".format(uncertanity_fraction * 100)
        )

    result = {
        "uncertanity_fraction": uncertanity_fraction,
        "uncertanity_prcent": uncertanity_fraction * 100,
        "uncertanity_in_unit": uncertanity_in_unit,
        "standard_deviaton": s_y,
        "mean": x_bar,
        "repetability": w,
        "n": n,
        "dof": dof,
        "confidence_intervall": confidence_intervall,
    }
    return result
