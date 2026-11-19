# Recommended Reference Books & Documentation for Kernel & Driver Development

## 1. For Phase C (2.6 Era) — *Linux Kernel Development (3rd Edition)* by Robert Love
* **When to read:** Keep this by your side around May/June 2027.
* **Why it matters:** It is the best high-level conceptual book ever written on how the scheduler, system calls, interrupt handlers, and kernel memory allocators work together.

## 2. For Phase D (Modern Kernels) — *Linux Kernel Programming (2nd Edition, 2024)* by Kaiwan N. Billimoria
* **When to read:** Open it when you hit D6 and modern kernel development.
* **Why it matters:** This is a modern, up-to-date guide written for Linux 6.x. Use it to cross-reference modern module loading, concurrency, memory allocators, and driver models.

## 3. The Best Driver Manual in the World (Already Free on Your Disk):
* The Linux source tree itself! Inside `Documentation/driver-api/`:
  - `pci/pci.rst` (How PCIe drivers work)
  - `dma-api.rst` (How DMA buffers and coherency work)
  - `memory-barriers.txt` (The ultimate guide to CPU memory ordering)

---

## Strategic Rule: "Desk Reference", Not Prerequisite
Do not read these books cover-to-cover before starting. Use them as on-demand lookup companions when the curriculum reaches the corresponding subsystems. Let the code and labs create the questions; let these references provide the answers.
