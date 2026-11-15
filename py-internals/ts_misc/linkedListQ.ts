class Node {
  val: number;
  next: Node | null;
  constructor(val?: number, next?: Node | null) {
    this.val = val === undefined ? 0 : val;
    this.next = next === undefined ? null : next;
  }
}
  
function reverseKGroup(head: Node | null, k: number): Node | null {
  let current = head;
  let count = 0;
  while (current && count < k) {
    current = current.next;
    count++;
  }
  if (count === k) {
    let prev: any = null;
    current = head;
    let next: any = null;
    count = 0;
    while (count < k) {
      next = current!.next;
      current!.next = prev;
      prev = current;
      current = next;
      count++;
    }
    if (next) {
      head!.next = reverseKGroup(next, k);
    }
    return prev;
  }
  return head;
}

function detectCycle(head: Node | null): Node | null {
  if (!head || !head.next) {
    return null;
  }
  let slow: Node | null = head;
  let fast: Node | null = head;
  while (fast && fast.next) {
    slow = slow!.next;
    fast = fast.next.next;
    if (slow === fast) {
      let ptr1 = head;
      let ptr2 = slow;
      while (ptr1 !== ptr2) {
        ptr1 = ptr1!.next;
        ptr2 = ptr2!.next;
      }
      return ptr1;
    }
  }
  return null;
}

function removeCycle(head: Node | null): Node | null {
  const cycleStart = detectCycle(head);
  if (!cycleStart) {
    return head;
  }
  let ptr1 = head;
  while (ptr1 !== cycleStart) {
    ptr1 = ptr1!.next;
  }
  let ptr2 = cycleStart;
  while (ptr2!.next !== ptr1) {
    ptr2 = ptr2!.next;
  }
  ptr2!.next = null;
  return head;
}

function mergeKLists(lists: Array<Node | null>): Node | null {
  if (!lists || lists.length === 0) {
    return null;
  }
  while (lists.length > 1) {
    const mergedList: (Node | null)[] = [];
    for (let i = 0; i < lists.length; i += 2) {
      const l1 = lists[i];
      const l2 = i + 1 < lists.length ? lists[i + 1] : null;
      mergedList.push(mergeTwoLists(l1, l2));
    }
    lists = mergedList;
  }
  return lists[0];
}

function mergeTwoLists(l1: Node | null, l2: Node | null): Node | null {
  if (!l1) return l2;
  if (!l2) return l1;
  if (l1.val < l2.val) {
    l1.next = mergeTwoLists(l1.next, l2);
    return l1;
  } else {
    l2.next = mergeTwoLists(l1, l2.next);
    return l2;
  }
}

function rotateRight(head: Node | null, k: number): Node | null {
  if (!head || k === 0) {
    return head;
  }
  let length = 1;
  let tail = head;
  while (tail.next) {
    tail = tail.next;
    length++;
  }
  k = k % length;
  if (k === 0) {
    return head;
  }
  let current = head;
  for (let i = 0; i < length - k - 1; i++) {
    current = current!.next;
  }
  const newHead = current!.next;
  current!.next = null;
  tail.next = head;
  return newHead;
}

function reorderList(head: Node | null): void {
  if (!head || !head.next) {
    return;
  }
  let slow: Node | null = head;
  let fast: Node | null = head;
  while (fast && fast.next) {
    slow = slow!.next;
    fast = fast.next.next;
  }
  let secondHalf = reverseList(slow);
  let firstHalf = head;
  while (secondHalf) {
    const temp1 = firstHalf!.next;
    const temp2 = secondHalf.next;
    firstHalf!.next = secondHalf;
    secondHalf.next = temp1;
    firstHalf = temp1;
    secondHalf = temp2;
  }
}

function reverseList(head: Node | null): Node | null {
  let prev: Node | null = null;
  let current = head;
  while (current) {
    const next = current.next;
    current.next = prev;
    prev = current;
    current = next;
  }
  return prev;
}