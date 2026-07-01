import pandas as pd

def normalize(series, invert=False):
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val:
        return pd.Series([50.0] * len(series))
    normalized = (series - min_val) / (max_val - min_val) * 100
    if invert:
        normalized = 100 - normalized
    return normalized

def compute_scores(df, weight_jobs, weight_cost, weight_safety, weight_internet):
    """
    Compute weighted city scores.
    - Job Count: higher is better
    - Cost of Living: lower is better (inverted)
    - Safety Index: higher is better
    - Internet Speed: higher is better
    Weights are provided as percentages and must sum to 100.
    """
    scored = df.copy()

    scored["Job Score"]      = normalize(df["Job Count"], invert=False)
    scored["Cost Score"]     = normalize(df["Cost of Living Index"], invert=True)
    scored["Safety Score"]   = normalize(df["Safety Index"], invert=False)
    scored["Internet Score"] = normalize(df["Internet Speed (Mbps)"], invert=False)

    w_jobs     = weight_jobs / 100
    w_cost     = weight_cost / 100
    w_safety   = weight_safety / 100
    w_internet = weight_internet / 100

    scored["Final Score"] = (
        scored["Job Score"]      * w_jobs +
        scored["Cost Score"]     * w_cost +
        scored["Safety Score"]   * w_safety +
        scored["Internet Score"] * w_internet
    ).round(2)

    scored = scored.sort_values("Final Score", ascending=False).reset_index(drop=True)
    scored.index += 1
    return scored
