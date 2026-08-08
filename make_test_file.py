import pandas as pd

columns = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes","land",
    "wrong_fragment","urgent","hot","num_failed_logins","logged_in","num_compromised",
    "root_shell","su_attempted","num_root","num_file_creations","num_shells",
    "num_access_files","num_outbound_cmds","is_host_login","is_guest_login","count",
    "srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate",
    "same_srv_rate","diff_srv_rate","srv_diff_host_rate","dst_host_count",
    "dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate",
    "dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate",
    "label","difficulty"
]

df = pd.read_csv("dataset/KDDTest+.txt", names=columns)

# Take first 10 rows, drop label/difficulty (app doesn't need them)
sample = df.head(10).drop(["label", "difficulty"], axis=1)

# Save WITHOUT header, WITHOUT index — matches what app.py expects
sample.to_csv("test_sample.csv", index=False, header=False)

print("✅ test_sample.csv created with 10 rows")