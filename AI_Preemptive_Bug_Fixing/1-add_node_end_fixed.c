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
 * add_node_end - adds a new node at the end of a linked list
 * @head: pointer to the head of the list
 * @n: integer to add to the new node
 *
 * Return: pointer to the head of the list, or NULL if allocation fails
 *
 * FIXES:
 * 1. Added NULL check after malloc (prevents segfault)
 * 2. Fixed linking: now updates last node's next pointer
 * 3. Proper traversal: checks current->next != NULL
 */
list_t *add_node_end(list_t *head, const int n)
{
    list_t *new_node;
    list_t *current;

    /* Allocate memory for new node */
    new_node = malloc(sizeof(list_t));
    if (new_node == NULL)
        return (NULL);

    /* Initialize new node */
    new_node->n = n;
    new_node->next = NULL;

    /* If list is empty, new node becomes head */
    if (head == NULL)
        return (new_node);

    /* Traverse to the last node */
    current = head;
    while (current->next != NULL)
        current = current->next;

    /* Link the last node to the new node */
    current->next = new_node;

    return (head);
}
