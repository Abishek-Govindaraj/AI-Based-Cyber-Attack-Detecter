import pandas as pd
import numpy as np

# ---------- Column names (41 features, matches app.py's input_columns) ----------
input_columns = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes","land",
    "wrong_fragment","urgent","hot","num_failed_logins","logged_in","num_compromised",
    "root_shell","su_attempted","num_root","num_file_creations","num_shells",
    "num_access_files","num_outbound_cmds","is_host_login","is_guest_login","count",
    "srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate",
    "same_srv_rate","diff_srv_rate","srv_diff_host_rate","dst_host_count",
    "dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate",
    "dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate"
]

# NSL-KDD raw files have 43 columns: 41 features + label + difficulty score
raw_columns = input_columns + ["label", "difficulty"]

# ---------- 1) Pull real rows from KDDTest+.txt ----------
real_df = pd.read_csv("dataset/KDDTest+.txt", names=raw_columns)
real_sample = real_df.sample(n=30, random_state=None).reset_index(drop=True)
real_sample = real_sample[input_columns]   # drop label + difficulty, model doesn't take them

# ---------- 2) Generate random synthetic rows ----------
np.random.seed(None)
n_random = 20
random_data = {}
for col in input_columns:
    if col == "protocol_type":
        random_data[col] = np.random.choice(["tcp", "udp", "icmp"], n_random)
    elif col == "service":
        random_data[col] = np.random.choice(["http", "ftp", "smtp", "telnet"], n_random)
    elif col == "flag":
        random_data[col] = np.random.choice(["SF", "S0", "REJ"], n_random)
    elif "rate" in col:
        random_data[col] = np.round(np.random.uniform(0, 1, n_random), 2)
    else:
        random_data[col] = np.random.randint(0, 100, n_random)
random_df = pd.DataFrame(random_data)

# ---------- 3) Combine and shuffle ----------
combined = pd.concat([real_sample, random_df], ignore_index=True)
combined = combined.sample(frac=1).reset_index(drop=True)  # shuffle rows

# ---------- 4) Save, no header (app.py expects header=None) ----------
combined.to_excel("test_sample.xlsx", index=False, header=False, engine="openpyxl")
print(f"✅ test_sample.xlsx created with {len(combined)} rows (30 real + 20 random)")