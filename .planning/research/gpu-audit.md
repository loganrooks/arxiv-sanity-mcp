# GPU and CUDA Audit

**Audited:** 2026-03-06
**Requirement:** AUD-04
**Domain:** GPU/CUDA -- driver, toolkit, frameworks, GPU processes, version compatibility
**Status:** Complete -- document only, no changes made

## Executive Summary

The Dionysus workstation runs an NVIDIA GeForce GTX 1080 Ti (11GB VRAM) with driver 550.163.01 supporting CUDA 12.4, but the installed CUDA toolkit is version 11.8 -- a version mismatch that works today (backward compatible) but limits access to newer CUDA features. GPU memory usage is 580MB/11264MB (5%), primarily consumed by desktop processes (Xorg 390MB, gnome-shell 28MB) plus a python3 compute process at 24MB. PyTorch is installed in all 5 conda environments with varying CUDA backends (cu118 in ml-dev, cu126 in base, cu128 elsewhere), creating a fragmented ML framework landscape. This is a documentation-only audit; remediation is deferred to Phase 6 EXP-01.

## Findings

### Finding 1: CUDA Toolkit / Driver Version Mismatch

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Category** | GPU / Version Compatibility |
| **Current State** | Driver 550.163.01 supports CUDA 12.4; installed toolkit is CUDA 11.8 (released Sep 2022) |
| **Expected State** | Toolkit version matching driver capability (CUDA 12.x) for full feature access |
| **Remediation** | Phase 6 EXP-01: Evaluate toolkit upgrade to CUDA 12.x when ML experimentation begins |
| **Verified By** | `nvidia-smi` shows CUDA 12.4; `nvcc --version` shows 11.8 |

**Details:**
- Driver CUDA version: 12.4 (maximum supported)
- Installed toolkit: 11.8 (V11.8.89, built Sep 21 2022)
- CUDA_HOME: `/usr/local/cuda-11.8`
- LD_LIBRARY_PATH: includes `/usr/local/cuda-11.8/lib64` (duplicated 3x)
- Only one CUDA installation found: `/usr/local/cuda-11.8`
- Symlinks: `/usr/local/cuda` -> `/etc/alternatives/cuda`, `/usr/local/cuda-11` -> `/etc/alternatives/cuda-11`

**Impact:** Backward compatibility ensures all cu11.8 code works fine. However, PyTorch cu126/cu128 packages in most environments use their own bundled CUDA runtime, bypassing the system toolkit. The system toolkit is only relevant for custom CUDA compilation (rare for this workstation's scholarly research use case).

### Finding 2: GPU Process Inventory

| Field | Value |
|-------|-------|
| **Severity** | LOW |
| **Category** | GPU / Resource Usage |
| **Current State** | 9 GPU processes consuming 580MB total (5% of 11GB VRAM) |
| **Expected State** | Desktop processes are normal; ~10.7GB VRAM available for ML workloads |
| **Remediation** | None needed -- healthy state |
| **Verified By** | `nvidia-smi` process table |

**GPU Process Breakdown:**

| PID | Process | Type | GPU Memory | Notes |
|-----|---------|------|------------|-------|
| 2825 | Xorg | G (Graphics) | 390 MiB | X11 display server -- expected |
| 3058 | gnome-shell | G | 28 MiB | GNOME desktop compositor -- expected |
| 3739 | xdg-desktop-portal-gnome | G | 6 MiB | Desktop portal -- expected |
| 4064 | code (VS Code) | G | 67 MiB | VS Code GPU acceleration |
| 717442 | gnome-clocks | G | 12 MiB | Desktop widget |
| 1090726 | nautilus | G | 17 MiB | File manager |
| 1417650 | firefox | G | 13 MiB | Snap Firefox browser |
| 1911369 | python3 | C+G (Compute+Graphics) | 24 MiB | Active compute process -- investigate origin |
| 3552593 | snapd-desktop-integration | G | 12 MiB | Snap desktop integration |

**Notable:** One python3 process (PID 1911369) is running as Compute+Graphics type, using 24MB GPU memory. This may be from a Jupyter notebook, ML inference server, or background monitoring script. Not a concern at current memory usage, but worth identifying the source during Phase 2 process audit.

### Finding 3: ML Framework Fragmentation Across Conda Environments

| Field | Value |
|-------|-------|
| **Severity** | LOW |
| **Category** | GPU / Framework Management |
| **Current State** | PyTorch installed in all 5 environments with 3 different CUDA backends |
| **Expected State** | Consolidation to fewer environments with consistent CUDA backend |
| **Remediation** | Phase 6 EXP-01: Standardize ML framework versions during experimentation setup |
| **Verified By** | `conda list` output per environment |

**Per-Environment ML Framework Inventory:**

| Environment | PyTorch Version | CUDA Backend | Triton | Other |
|-------------|----------------|--------------|--------|-------|
| base | 2.9.1+cu126 | cu12.6 | 3.5.1 | torchvision 0.24.1+cu126 |
| ml-dev | 2.2.0+cu118 | cu11.8 + cu12.8 (dual) | 2.2.0 | torchaudio 2.2.0, torchvision 0.17.0 |
| analysis | 2.8.0 | cu12.8 | 3.4.0 | -- |
| audio | 2.8.0 | cu12.8 | 3.4.0 | -- |
| university | 2.8.0 | cu12.8 | 3.4.0 | -- |
| acadlib-dev | -- | -- | -- | No ML frameworks |

**Observations:**
- **ml-dev** has BOTH cu11.8 and cu12.8 CUDA packages -- likely from sequential installs without cleanup. Oldest PyTorch (2.2.0).
- **base** has the newest PyTorch (2.9.1) with cu12.6 backend.
- **analysis, audio, university** all share identical PyTorch 2.8.0 + cu12.8 + triton 3.4.0 -- potential consolidation candidates.
- The system CUDA toolkit (11.8) is only directly used by ml-dev's cu118 build. All other environments use PyTorch's bundled CUDA runtime.

### Finding 4: GPU Hardware State

| Field | Value |
|-------|-------|
| **Severity** | INFO |
| **Category** | GPU / Hardware Health |
| **Current State** | GPU healthy: 35C, fan 28%, P8 power state (idle), 16W/250W, persistence mode on |
| **Expected State** | Current state is correct for idle workstation |
| **Remediation** | None needed |
| **Verified By** | `nvidia-smi` header |

**Hardware Summary:**

| Parameter | Value |
|-----------|-------|
| GPU | NVIDIA GeForce GTX 1080 Ti |
| VRAM | 11264 MiB (11 GB) |
| Architecture | Pascal (GP102) |
| Driver | 550.163.01 |
| Persistence Mode | On |
| Temperature | 35C |
| Fan Speed | 28% |
| Power State | P8 (idle) |
| Power Draw | 16W / 250W cap |
| GPU Utilization | 1% |
| Memory Used | 580 MiB / 11264 MiB (5%) |
| ECC | N/A (consumer GPU) |
| Compute Mode | Default |

## Raw Data

### nvidia-smi Output

```
Thu Mar  5 21:32:51 2026
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 550.163.01             Driver Version: 550.163.01     CUDA Version: 12.4     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce GTX 1080 Ti     On  |   00000000:65:00.0  On |                  N/A |
| 28%   35C    P8             16W /  250W |     580MiB /  11264MiB |      1%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A      2825      G   /usr/lib/xorg/Xorg                            390MiB |
|    0   N/A  N/A      3058      G   /usr/bin/gnome-shell                           28MiB |
|    0   N/A  N/A      3739      G   /usr/libexec/xdg-desktop-portal-gnome           6MiB |
|    0   N/A  N/A      4064      G   /usr/share/code/code                           67MiB |
|    0   N/A  N/A    717442      G   /usr/bin/gnome-clocks                          12MiB |
|    0   N/A  N/A   1090726      G   /usr/bin/nautilus                              17MiB |
|    0   N/A  N/A   1417650      G   ...irefox/7477/usr/lib/firefox/firefox         13MiB |
|    0   N/A  N/A   1911369    C+G   python3                                        24MiB |
|    0   N/A  N/A   3552593      G   ...3/usr/bin/snapd-desktop-integration         12MiB |
+-----------------------------------------------------------------------------------------+
```

### nvcc --version Output

```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2022 NVIDIA Corporation
Built on Wed_Sep_21_10:33:58_PDT_2022
Cuda compilation tools, release 11.8, V11.8.89
Build cuda_11.8.r11.8/compiler.31833905_0
```

### CUDA Environment Variables

```
CUDA_HOME=/usr/local/cuda-11.8
LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:/usr/local/cuda-11.8/lib64:/usr/local/cuda-11.8/lib64:
PATH=...:/usr/local/cuda-11.8/bin:/usr/local/cuda-11.8/bin:...
```

**Note:** Both LD_LIBRARY_PATH and PATH contain duplicated CUDA entries (3x and 2x respectively). Harmless but indicates multiple sourcing of CUDA path setup in shell init.

### GPU Compute Processes

```
pid, process_name, used_gpu_memory [MiB]
1911369, python3, 24 MiB
```

Only one compute process. All others are graphics (G) type.

### CUDA Installations

```
/usr/local/cuda -> /etc/alternatives/cuda (symlink)
/usr/local/cuda-11 -> /etc/alternatives/cuda-11 (symlink)
/usr/local/cuda-11.8/ (actual installation)
```

Single CUDA toolkit installation (11.8). No conflicting versions.

### ML Framework Inventory by Conda Environment

**base:**
```
torch                   2.9.1+cu126    pypi_0    pypi
torchvision             0.24.1+cu126   pypi_0    pypi
triton                  3.5.1          pypi_0    pypi
nvidia-cuda-cupti-cu12  12.6.80        pypi_0    pypi
nvidia-cuda-nvrtc-cu12  12.6.77        pypi_0    pypi
nvidia-cuda-runtime-cu12 12.6.77       pypi_0    pypi
```

**ml-dev:**
```
torch                   2.2.0+cu118    pypi_0    pypi
torchaudio              2.2.0+cu118    pypi_0    pypi
torchvision             0.17.0+cu118   pypi_0    pypi
triton                  2.2.0          pypi_0    pypi
nvidia-cuda-cupti-cu11  11.8.87        pypi_0    pypi
nvidia-cuda-cupti-cu12  12.8.90        pypi_0    pypi
nvidia-cuda-nvrtc-cu11  11.8.89        pypi_0    pypi
nvidia-cuda-nvrtc-cu12  12.8.93        pypi_0    pypi
nvidia-cuda-runtime-cu11 11.8.89       pypi_0    pypi
nvidia-cuda-runtime-cu12 12.8.90       pypi_0    pypi
```

**analysis, audio, university (identical):**
```
torch                   2.8.0          pypi_0    pypi
triton                  3.4.0          pypi_0    pypi
nvidia-cuda-cupti-cu12  12.8.90        pypi_0    pypi
nvidia-cuda-nvrtc-cu12  12.8.93        pypi_0    pypi
nvidia-cuda-runtime-cu12 12.8.90       pypi_0    pypi
```

**acadlib-dev:** No ML frameworks installed.

## Verification Against Research

| Claim (from CLAUDE.md / synthesis.md / research) | Actual | Status |
|--------------------------------------------------|--------|--------|
| GPU: GTX 1080 Ti (11GB) | GTX 1080 Ti, 11264 MiB | VERIFIED |
| CUDA: 11.8 (from CLAUDE.md) | Toolkit 11.8 confirmed | VERIFIED |
| Driver 550.163.01 supports CUDA 12.4 | 550.163.01, CUDA 12.4 | VERIFIED |
| Toolkit is 11.8 (mismatch) | nvcc 11.8 vs driver 12.4 | VERIFIED |
| GPU processes: Xorg ~390MB, gnome-shell ~28MB | Xorg 390MB, gnome-shell 28MB | VERIFIED |
| CUDA_HOME pointing to /usr/local/cuda-11.8 | CUDA_HOME=/usr/local/cuda-11.8 | VERIFIED |

**Additional findings not in research:**
- 9 GPU processes total (research mentioned only Xorg and gnome-shell; also found VS Code 67MB, firefox 13MB, nautilus 17MB, gnome-clocks 12MB, xdg-desktop-portal 6MB, snapd 12MB, python3 24MB compute)
- PyTorch installed in all 5 environments (research did not detail per-environment breakdown)
- ml-dev has dual cu11/cu12 CUDA packages (potential cleanup target)
- LD_LIBRARY_PATH has triplicated CUDA paths (cosmetic issue in shell init)

## Remediation Summary

| Finding | Severity | Action | Remediation Phase |
|---------|----------|--------|-------------------|
| CUDA toolkit/driver mismatch (11.8 vs 12.4) | MEDIUM | Upgrade toolkit to 12.x when ML work begins | Phase 6 EXP-01 |
| ML framework fragmentation (3 CUDA backends) | LOW | Standardize PyTorch versions across envs | Phase 6 EXP-01 |
| ml-dev dual CUDA packages | LOW | Clean up cu11 packages if cu118 torch no longer needed | Phase 6 EXP-01 |
| Triplicated CUDA paths in LD_LIBRARY_PATH | LOW | Fix shell init (cosmetic) | Phase 3 or Phase 6 |
| python3 compute process on GPU | LOW | Identify source process during Phase 1 process audit (AUD-02) | Phase 1 Plan 02 |

---
*Audit completed: 2026-03-06*
*No system changes made -- document only*
