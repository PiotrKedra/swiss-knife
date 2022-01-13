import os
import json
from glob import glob
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# styling of plots
# partially taken from: https://github.com/Mic92/rkt-io (21.11.2021, 18:00 (UTC))
sns.set(rc={"figure.figsize": (3, 5)})
sns.set_style("whitegrid")
sns.set_style("ticks", {"xtick.major.size": 7, "ytick.major.size": 7})
sns.set_context("paper", rc={"font.size": 6, "axes.titlesize": 12, "axes.labelsize": 12})
sns.set_palette(sns.color_palette(palette="gray", n_colors=2))


def load_data(exp: str):
    data = {
        "throughput": [],
        "read_avg_lat": [],
        "update_avg_lat": []
    }

    for file_name in glob(f"benchmarks/{exp}/*.json"):
        with open(os.path.join(ROOT_DIR, file_name)) as json_file:
            output = json.load(json_file)
            data["throughput"].append(
                list(
                    filter(lambda val: val["measurement"] == "Throughput(ops/sec)", output)
                )[0]["value"] / 1e5
            )
            data["read_avg_lat"].append(
                list(
                    filter(lambda val: val["metric"] == "READ" and val["measurement"] == "AverageLatency(us)", output)
                )[0]["value"]
            )
            data["update_avg_lat"].append(
                list(
                    filter(lambda val: val["metric"] == "UPDATE" and val["measurement"] == "AverageLatency(us)", output)
                )[0]["value"]
            )

    df = pd.DataFrame(data=data)

    return df


def generate_plot(operation: str) -> None:
    df_memcached = load_data("memcached")
    df_rocksdb = load_data("rocksdb")
    df_redis = load_data("redis")
    df_redis_cluster = load_data("redis_cluster")

    sns.lineplot(x="throughput", y=f"{operation}_avg_lat", data=df_memcached, markers=True, marker="X", color="red")
    sns.lineplot(x="throughput", y=f"{operation}_avg_lat", data=df_rocksdb, markers=True, marker="o", color="blue")
    sns.lineplot(x="throughput", y=f"{operation}_avg_lat", data=df_redis, markers=True, marker="s", color="green")
    sns.lineplot(x="throughput", y=f"{operation}_avg_lat", data=df_redis_cluster, markers=True, marker="P", color="purple")

    plt.xlabel("Throughput ($10^5$ ops/sec)")
    plt.ylabel(f"Average {operation} latency (ms)")
    plt.tight_layout()

    plt.savefig(f"results/plot_result_{operation}.svg")
    plt.clf()


if __name__ == "__main__":
    generate_plot("read")
    generate_plot("update")
