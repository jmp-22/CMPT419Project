import pandas as pd
from statsmodels.stats.inter_rater import fleiss_kappa
from collections import Counter

# Load all three annotation files
jimmy = pd.read_csv("atc_audio_annotations_Jimmy.csv")
jonathan = pd.read_csv("atc_audio_annotations_Jonathan.csv")
lucy = pd.read_csv("atc_audio_annotations_Lucy.csv")

# Merge all files on audio_path
df = jimmy.merge(jonathan, on="audio_path", suffixes=("_jimmy", "_jonathan"))
df = df.merge(lucy, on="audio_path")
df = df.rename(columns={"question_type": "question_type_lucy"})

# Get unique labels used
all_labels = sorted(set(df["question_type_jimmy"]) | set(df["question_type_jonathan"]) | set(df["question_type_lucy"]))

# Build a matrix for Fleiss' Kappa (rows = samples, columns = label counts)
def get_label_counts(row):
    labels = [row["question_type_jimmy"], row["question_type_jonathan"], row["question_type_lucy"]]
    count = Counter(labels)
    return [count.get(label, 0) for label in all_labels]

label_matrix = df.apply(get_label_counts, axis=1, result_type="expand")
label_matrix.columns = all_labels

# Compute Fleiss' Kappa
kappa = fleiss_kappa(label_matrix.values)
print("Fleiss' Kappa:", round(kappa, 4))