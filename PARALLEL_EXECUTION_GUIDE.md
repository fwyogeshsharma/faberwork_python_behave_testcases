# Parallel Test Execution Guide

## Optimizations Applied

### 1. Chrome Performance Optimizations
Added 20+ Chrome flags for better parallel execution:
- Disabled background networking and timers
- Disabled unnecessary browser features (translate, sync, default apps)
- Optimized memory usage
- Muted audio and disabled component updates

### 2. Timeout Improvements
- **Page Load Timeout**: Increased from 30s to **90s minimum**
- **Feature Timeout**: Increased from 10 min to **15 min per feature**
- Handles slow page loads during parallel execution

### 3. Conservative Worker Count
- **Default Workers**: Max 6 workers or CPU_count/2 (whichever is lower)
- Prevents system resource exhaustion
- More stable execution

## Recommended Usage

### For Fastest Execution (with good hardware):
```bash
python -B run_tests_parallel.py --workers 6 --format json --generate-report
```

### For Most Stable Execution (recommended):
```bash
python -B run_tests_parallel.py --workers 3 --format json --generate-report
```

### For Systems with Limited Resources:
```bash
python -B run_tests_parallel.py --workers 2 --format json --generate-report
```

## Expected Performance

| Workers | Estimated Time | Stability |
|---------|---------------|-----------|
| 2       | ~25-30 min    | Excellent |
| 3       | ~18-22 min    | Very Good |
| 4       | ~15-18 min    | Good      |
| 6       | ~12-15 min    | Fair      |

## Troubleshooting

### If Tests Timeout or Hang:
1. Reduce number of workers
2. Check system resources (RAM, CPU)
3. Close other applications
4. Try running without `--clean` flag

### If Chrome Crashes:
- Reduce workers to 2-3
- Increase system RAM allocation
- Run tests sequentially for critical features

## Files Modified
- `utils/driver_factory.py` - Chrome optimizations + timeouts
- `run_tests_parallel.py` - Worker count + feature timeout
- `features/steps/common_steps.py` - Menu navigation fix
