import pandas as pd
import numpy as np

# NSL-KDD has 41 features. We'll generate 10 random-but-valid rows
# matching typical column names your model expects.
columns = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
    "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations",
    "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login",
    "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate",
    "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
    "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate"
]

np.random.seed(42)
n_rows = 10

data = {}
for col in columns:
    if col == "protocol_type":
        data[col] = np.random.choice(["tcp", "udp", "icmp"], n_rows)
    elif col == "service":
        data[col] = np.random.choice(["http", "ftp", "smtp", "telnet"], n_rows)
    elif col == "flag":
        data[col] = np.random.choice(["SF", "S0", "REJ"], n_rows)
    elif "rate" in col:
        data[col] = np.round(np.random.uniform(0, 1, n_rows), 2)
    else:
        data[col] = np.random.randint(0, 100, n_rows)

df = pd.DataFrame(data)
df.to_excel("test_sample.xlsx", index=False, header=False, engine="openpyxl")
print("✅ test_sample.xlsx created")