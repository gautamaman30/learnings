class ListNode {
    val: number;
    next: ListNode | null;
    constructor(val?: number, next?: ListNode | null) {
      this.val = val === undefined ? 0 : val;
      this.next = next === undefined ? null : next;
    }
  }
  
class TreeNode {
  val: number;
  left: TreeNode | null;
  right: TreeNode | null;
  constructor(val?: number, left?: TreeNode | null, right?: TreeNode | null) {
    this.val = val === undefined ? 0 : val;
    this.left = left === undefined ? null : left;
    this.right = right === undefined ? null : right;
  }
}
  
  function bstFromPreorder(preorder: number[]): TreeNode | null {
    let index = 0;
    function buildTree(lowerBound: number, upperBound: number): TreeNode | null {
      if (index === preorder.length || preorder[index] < lowerBound || preorder[index] > upperBound) {
        return null;
      }
      const rootValue = preorder[index++];
      const root = new TreeNode(rootValue);
      root.left = buildTree(lowerBound, rootValue);
      root.right = buildTree(rootValue, upperBound);
      return root;
    }
    return buildTree(-Infinity, Infinity);
  }
  
  function sortedListToBST(head: ListNode | null): TreeNode | null {
    if (!head) {
      return null;
    }
    let size = 0;
    let current = head;
    while (current) {
      size++;
      current = current.next;
    }
    let listPtr = head;
    function buildBST(start: number, end: number): TreeNode | null {
      if (start > end) {
        return null;
      }
      const mid = Math.floor((start + end) / 2);
      const left = buildBST(start, mid - 1);
      const root = new TreeNode(listPtr!.val);
      root.left = left;
      listPtr = listPtr!.next;
      root.right = buildBST(mid + 1, end);
      return root;
    }
    return buildBST(0, size - 1);
  }
  
  function kthSmallest(root: TreeNode | null, k: number): number {
    const stack: TreeNode[] = [];
    let current = root;
    while (current || stack.length > 0) {
      while (current) {
        stack.push(current);
        current = current.left;
      }
      current = stack.pop()!;
      k--;
      if (k === 0) {
        return current.val;
      }
      current = current.right;
    }
    return -1;
  }
  
  function lowestCommonAncestorBST(root: TreeNode | null, p: TreeNode | null, q: TreeNode | null): TreeNode | null {
    if (!root || root === p || root === q) {
      return root;
    }
    if ((p!.val < root.val && q!.val > root.val) || (p!.val > root.val && q!.val < root.val)) {
      return root;
    } else if (p!.val < root.val && q!.val < root.val) {
      return lowestCommonAncestorBST(root.left, p, q);
    } else {
      return lowestCommonAncestorBST(root.right, p, q);
    }
  }
  
  function isValidBST(root: TreeNode | null): boolean {
    function validate(node: TreeNode | null, low: number, high: number): boolean {
      if (!node) {
        return true;
      }
      if (node.val <= low || node.val >= high) {
        return false;
      }
      return validate(node.left, low, node.val) && validate(node.right, node.val, high);
    }
    return validate(root, -Infinity, Infinity);
  }