from typing import Optional


class Node:
    def __init__(self, data) -> None:
        self.data = data
        self.next = None


class SLL:
    def __init__(self) -> None:
        self.head = None

    def insert_first(self, data) -> None:
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            new_node.next = self.head
            self.head = new_node

    def insert_last(self, data) -> None:
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            curr = self.head
            while curr.next is not None:
                curr = curr.next
            curr.next = new_node

    def insert_at_pos(self, pos, data) -> None:  # index starts from '0'
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        if pos < 0:
            raise Exception("Position should be greater than zero")
        if pos == 0:
            new_node.next = self.head
            self.head = new_node
        elif pos > 0:
            curr = self.head
            while pos - 1 != 0 and curr.next is not None:
                curr = curr.next
                pos -= 1
            after = curr.next
            curr.next = new_node
            new_node.next = after

    def traverse(self) -> None:
        curr = self.head
        output = []
        while curr is not None:
            output.append(curr.data)
            curr = curr.next
        print(output)

    def search(self, element) -> Optional[int]:
        curr = self.head
        index = 0
        while curr is not None:
            if curr.data == element:
                return index
            else:
                curr = curr.next
                index += 1
        return -1  # If element is not found

    def delete_first(self) -> None:
        if self.head is not None:
            self.head = self.head.next
        else:
            raise Exception("Cannot delete from empty linkedlist")

    def delete_last(self) -> None:
        if self.head is not None:
            curr = self.head
            prev = None
            while curr.next is not None:
                prev = curr
                curr = curr.next
            if prev is not None:
                prev.next = None
            else:
                self.head = None
        else:
            raise Exception("Cannot delete from empty linkedlist")

    def delete(self, element) -> None:
        if self.head is None:
            raise Exception("Cannot delete from empty linkedlist")
        if self.head.data == element:
            to_delete = self.head
            self.head = self.head.next
            del to_delete
        else:
            prev = None
            curr = self.head
            while curr is not None:
                if curr.data != element:
                    prev = curr
                    curr = curr.next
                else:
                    break
            if curr is not None:
                to_del = curr
                prev.next = curr.next
                del to_del
            else:
                raise Exception("The element is not present in the linkedlist")

    def delete_at_pos(self, pos) -> None:
        if self.head is None:
            raise Exception("Cannot delete from empty linkedlist")
        if pos < 0:
            raise Exception("The position should be greater than zero")
        if pos == 0:
            self.head = self.head.next
        if pos > 0:
            curr = self.head
            while pos - 1 != 0 and curr.next is not None:
                curr = curr.next
                pos -= 1
            if curr.next is not None:
                curr.next = curr.next.next
            else:
                raise Exception("The position should be less than size of linkedlist")

    def reverse(self) -> None:
        prev = None
        curr = self.head
        while curr is not None:
            after = curr.next
            curr.next = prev
            prev = curr
            curr = after
        self.head = prev

    def sort(self) -> None:
        def getMiddle(dummy):
            if (dummy == None):
                return dummy
            slow = dummy
            fast = dummy
            while (fast.next != None and fast.next.next != None):
                slow = slow.next
                fast = fast.next.next
            tup = dummy, slow.next
            slow.next = None
            return tup

        def sortedMerge(a, b):
            if a is None:
                return b
            elif b is None:
                return a
            if a.data <= b.data:
                result = a
                result.next = sortedMerge(a.next, b)
            else:
                result = b
                result.next = sortedMerge(a, b.next)
            return result

        def mergesort(dummy):
            if dummy is None or dummy.next is None:
                return dummy
            front, back = getMiddle(dummy)
            front = mergesort(front)
            back = mergesort(back)
            return sortedMerge(front, back)

        sorted_head = mergesort(self.head)
        self.head = sorted_head

    def size(self) -> int:
        curr = self.head
        count = 0
        while curr is not None:
            count += 1
            curr = curr.next
        return count
