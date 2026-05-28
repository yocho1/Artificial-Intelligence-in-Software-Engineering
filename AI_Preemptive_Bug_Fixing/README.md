# AI: Preemptive Bug Fixing

## 📖 Task Description
Analyze a vulnerable C function that adds a node to the end of a singly linked list. The original code contains two critical bugs that need to be identified and fixed.

## 🐛 Bugs Identified in Vulnerable Code

### 1. Memory Safety Error (Missing NULL Check)
| Aspect | Details |
|--------|---------|
| **Location** | Line: `list_t *new_node = malloc(sizeof(list_t));` |
| **Problem** | No check if `malloc` returns `NULL` |
| **Consequence** | If malloc fails, `new_node = NULL`, then `new_node->n = n` causes **Segmentation Fault** |
| **Fix** | Add: `if (new_node == NULL) return (NULL);` |

### 2. Logical Error (Wrong Linking)
| Aspect | Details |
|--------|---------|
| **Location** | Line: `current = new_node;` |
| **Problem** | After traversal, `current = NULL`. Assigning `new_node` to `current` only changes local pointer |
| **Consequence** | New node never gets linked to the list → **Memory leak** |
| **Fix** | Use: `current->next = new_node;` (must stop at last node, not after it) |

## 📊 Bug Comparison Table

| Bug Type | Original Code | Fixed Code |
|----------|---------------|------------|
| **malloc check** | `new_node = malloc(...);` (no check) | `if (new_node == NULL) return (NULL);` |
| **Traversal condition** | `while (current)` | `while (current->next != NULL)` |
| **Linking** | `current = new_node;` | `current->next = new_node;` |

## 📁 Files in This Folder

| File | Description |
|------|-------------|
| `0-add_node_end_vulnerable.c` | Original vulnerable code with bugs |
| `1-add_node_end_fixed.c` | Corrected version after AI review |

## 🔧 How to Compile and Test

```bash
# Compile the vulnerable version (will have bugs)
gcc -Wall -pedantic -Werror -Wextra -std=gnu89 0-add_node_end_vulnerable.c -o vulnerable

# Compile the fixed version
gcc -Wall -pedantic -Werror -Wextra -std=gnu89 1-add_node_end_fixed.c -o fixed
