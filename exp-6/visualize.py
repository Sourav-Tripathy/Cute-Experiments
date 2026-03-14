import json
import matplotlib.pyplot as plt

def generate_graphs():
    # 1. Routing Benchmark
    with open("benchmark_results.json", "r") as f:
        routing_data = json.load(f)
    
    sizes = routing_data["sizes"]
    frameworks = routing_data["data"]
    
    plt.figure(figsize=(10, 6))
    for framework, results in frameworks.items():
        # results are strings ("10", "100") -> float mapping in JSON
        times = [results[str(s)] for s in sizes]
        plt.plot(sizes, times, marker='o', label=framework)
    
    plt.title("Routing Delay: Framework vs Number of Routes")
    plt.xlabel("Number of Dynamic Routes pre-configured (n)")
    plt.ylabel("Time for 10,000 requests (seconds)")
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("routing_complexity_graph.png", dpi=300)
    print("Generated routing_complexity_graph.png")
    
    # 2. Startup Benchmark
    with open("benchmark_startup_results.json", "r") as f:
        startup_data = json.load(f)
    
    sizes_startup = startup_data["sizes"]
    frameworks_startup = startup_data["data"]
    
    plt.figure(figsize=(10, 6))
    for framework, results in frameworks_startup.items():
        times = [results[str(s)] for s in sizes_startup]
        plt.plot(sizes_startup, times, marker='o', label=framework)
    
    plt.title("Startup Complexity: Framework vs Number of Routes")
    plt.xlabel("Number of Routes (n)")
    plt.ylabel("Time for 100 app startups (seconds)")
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    
    note_text = (
        "Environment: CPython 3.10.12 | Django: 5.2.12 | Flask: 3.1.3 | Falcon: 4.2.0 | Sanic: 25.12.0 | FastAPI: 0.115.6\n"
        "Hardware: 8GB RAM, 512GB SSD (Ubuntu 22.04 on a dual-boot partition)"
    )
    # Add text to the figure at the bottom
    plt.figtext(0.5, 0.01, note_text, wrap=True, horizontalalignment='center', fontsize=9, style='italic', color='dimgray')
    
    # Adjust layout to make room for note
    plt.subplots_adjust(bottom=0.15)
    
    plt.savefig("startup_complexity_graph.png", dpi=300)
    print("Generated startup_complexity_graph.png")

if __name__ == "__main__":
    generate_graphs()
