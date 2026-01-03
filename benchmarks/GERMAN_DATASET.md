# German Synthetic Benchmark Dataset

## Overview

The German benchmark script is located at:

- **benchmarks/benchmark_de_comparison.py**

This script tests all German G2P configurations and measures accuracy and speed.

## Quick Start

```bash
# Run all configurations
python benchmarks/benchmark_de_comparison.py

# Test specific configuration
python benchmarks/benchmark_de_comparison.py --config "Gold + Espeak"

# Verbose output
python benchmarks/benchmark_de_comparison.py --verbose

# Export results
python benchmarks/benchmark_de_comparison.py --output results.json
```

## Benchmark Results (189 sentences)

| Configuration | Accuracy | Speed         | Recommendation  |
| ------------- | -------- | ------------- | --------------- |
| Gold + Espeak | 100.0%   | 27,178 sent/s | ✅ **Best**     |
| Gold only     | 100.0%   | 26,175 sent/s | Good            |
| Gold + Goruut | 100.0%   | 26,058 sent/s | Alternative     |
| Espeak only   | 19.0%    | 18,219 sent/s | Not recommended |
| Goruut only   | 19.0%    | 20,587 sent/s | Not recommended |

**Recommendation**: Use **Gold + Espeak** configuration for German.
