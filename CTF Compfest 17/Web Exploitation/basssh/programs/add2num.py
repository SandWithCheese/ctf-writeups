class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def list_to_linked(lst):
    dummy = cur = ListNode(0)
    for val in lst:
        cur.next = ListNode(int(val))
        cur = cur.next
    return dummy.next

def linked_to_list(node):
    result = []
    while node:
        result.append(str(node.val))
        node = node.next
    return result

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        left = 0
        dummy = cur = ListNode(-1)
        while l1 or l2 or left:
            left, sm = divmod(sum(l and l.val or 0 for l in (l1, l2)) + left, 10)
            cur.next = cur = ListNode(sm)
            l1 = l1 and l1.next
            l2 = l2 and l2.next
        return dummy.next

if __name__ == "__main__":
    import sys
    lines = sys.stdin.read().strip().splitlines()

    if len(lines) != 2:
        print("Please input two lines of space-separated integers", file=sys.stderr)
        sys.exit(1)

    l1 = list_to_linked(lines[0].split())
    l2 = list_to_linked(lines[1].split())

    result = Solution().addTwoNumbers(l1, l2)
    print(" ".join(linked_to_list(result)))