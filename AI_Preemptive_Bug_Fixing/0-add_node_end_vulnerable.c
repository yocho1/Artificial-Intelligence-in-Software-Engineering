#include <stdlib.h>

/**
 * struct list_s - singly linked list
 * @n: integer
 * @next: points to the next node
 */
typedef struct list_s
{
    int n;
    struct list_s *next;
} list_t;

/**
 * add_node_end - VULNERABLE: adds a new node at the end
 * @head: pointer to the head of the list
 * @n: integer to add
 *
 * Return: pointer to head, or NULL if allocation fails
 *
 * BUGS:
 * 1. Memory safety: No NULL check after malloc
 * 2. Logical error: current = new_node doesn't link to list
 */
list_t *add_node_end(list_t *head, const int n)
{
    list_t *new_node = malloc(sizeof(list_t));
    list_t *current = head;

    if (!head)
        return (new_node);

    while (current)
        current = current->next;
    
    current = new_node;
    new_node->n = n;
    new_node->next = NULL;
    return (head);
}
