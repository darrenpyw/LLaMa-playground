---
name: cpp_reviewer
description: C/C++ code review skill
license: MIT
allowed-tools:
  - read
  - bash
---

# GOAL
Your primary goal is to perform a comprehensive analysis of C/C++ source code. You must not stop at the first obvious flaw.


## INSTRUCTIONS
You must check for these vulnerabilities:
- Boundary Condition & Memory Safety: Trace all external inputs (user-controlled parameters, network lengths, counts) through the function. Verify that every memory operation (memcpy, strcpy, pointer arithmetic) is strictly bounded by the allocated destination buffer size. Target: Buffer Overflows (Stack/Heap), Integer Overflows.
- Resource Management: Evaluate the lifecycle management of complex data structures (e.g., connection handles, credential objects, allocated buffers). Ensure every malloc/mem_alloc has a corresponding free under all code paths, including error exits. Target: Memory Leaks, Use-After-Free (UAF).
- Taint Analysis: Follow any untrusted data from its entry point until it influences a security-critical operation (like a function call or a memory write). Ensure validation occurs at the point of entry.
- Logic Integrity: Scrutinize complex logic (e.g., state machines, sequence window arithmetic, complex pointer manipulation) for potential logical errors, off-by-one errors, or unexpected side effects.
- Concurrency and Threading: Identify all shared global resources (lists, counters, caches, static variables). Determine if locks, mutexes, or atomic operations are used correctly across all access points. Target: Race Conditions, Deadlocks, Thread Safety.

## WORKFLOW
1. Analyze each code function according to the tasks list.
2. Read the C header files (e.g. main.h) for additional contexts like data structures or variables.
3. Read the included header files (e.g. #include <rpc/rpcsec_gss.h>) for additional contexts like data structures or variables.
