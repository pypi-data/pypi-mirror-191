UNIVARIATE_DEFAULT_THRESHOLD = 0.95
UNIVARIATE_DEFAULT_ZSCORE = 1.96
UNIVARIATE_CI_TO_ZSCORE = {
    0.9: 1.65,
    UNIVARIATE_DEFAULT_THRESHOLD: UNIVARIATE_DEFAULT_ZSCORE,
    0.99: 2.58
}


def validate(values: list, threshold: float, get_mu_sd):
    z = UNIVARIATE_CI_TO_ZSCORE[threshold]
    mu, sd = get_mu_sd()
    min = mu-(z*sd) if mu is not None else None
    max = mu+(z*sd) if mu is not None else None
    passes = [min <= y <= max if mu is not None else True for y in values]
    outliers = [y for y in values if not min <= y <= max] if mu is not None else []
    return all(passes), outliers, min, max
