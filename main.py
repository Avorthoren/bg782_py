import dataclasses
from typing import Hashable, Iterable


CNT = 0

NodeID_T = Hashable


@dataclasses.dataclass(slots=True)
class Node:
	_id: NodeID_T
	links: set[NodeID_T] = dataclasses.field(default_factory=set)
	visited: bool = dataclasses.field(init=False, default=False)

	@property
	def id(self) -> NodeID_T:
		return self._id


Nodes_T = dict[NodeID_T, Node]


def make_nodes_by_div(numbers: Iterable[int]) -> Nodes_T:
	nodes = {}
	nums = []
	for n in numbers:
		n_node = Node(n)
		nodes[n] = n_node
		for m in nums:
			if n % m and m % n:
				continue
			n_node.links.add(m)
			nodes[m].links.add(n)

		nums.append(n)

	return nodes


# def del_node(node_id: NodeID_T, nodes: Nodes_T) -> None:
# 	for link in nodes[node_id].links:
# 		nodes[link].links.remove(node_id)
#
# 	del nodes[node_id]


def process_node(
	node_id: NodeID_T,
	nodes: Nodes_T,
	current_path: list[NodeID_T],
	longest_cycle: list[NodeID_T]
) -> None:
	node = nodes[node_id]
	node.visited = True
	current_path.append(node_id)

	for link in node.links:
		if link == current_path[0]:
			if len(current_path) >= len(longest_cycle):
				longest_cycle.clear()
				longest_cycle.extend(current_path)
				print(f"{len(longest_cycle):02}: {longest_cycle}")
			continue

		link_node = nodes[link]
		if link_node.visited:
			continue

		process_node(link, nodes, current_path, longest_cycle)

	current_path.pop()
	node.visited = False


def search_longest_cycle(nodes: Nodes_T, start_node_id: NodeID_T) -> list[NodeID_T]:
	assert start_node_id in nodes

	longest_cycle = []
	current_path = []
	process_node(start_node_id, nodes, current_path, longest_cycle)

	return longest_cycle


def main():
	nodes = make_nodes_by_div((1, 2, 4, 8, 16, 3, 6, 9, 12, 18, 24, 27, 5, 10, 15, 20, 25, 30, 7, 14, 21, 28, 11, 22))
	longest_cycle = search_longest_cycle(nodes, start_node_id=1)
	print()
	print(f"Longest cycle has length {len(longest_cycle)}")
	print(longest_cycle)


if __name__ == "__main__":
	main()
