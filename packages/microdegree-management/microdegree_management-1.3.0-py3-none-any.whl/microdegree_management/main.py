from typing import Optional, Union, Literal, Dict, Set
from pathlib import Path
from pydantic import Extra
from pydantic_yaml import YamlModel
import logging
import os
import tempfile
import click
import re
import json

# unfortunately there is no type info ATM
import graphviz  # type: ignore
import yaml
import networkx as nx  # type: ignore


logging.basicConfig(level=logging.DEBUG)


class URL(YamlModel):
    url: str
    description: str


class Assignment(YamlModel):
    description: str
    path: Path
    attachments: Optional[tuple[Path, ...]]

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "examples": [
                {
                    "description": "Oefening for lus",
                    "path": "/oefeningen/TypeScript/oefening-for-lus.md",
                    "attachments": ["/oefeningen/TypeScript/screenshot-for-lus.png"],
                }
            ]
        }


class Job(YamlModel, extra=Extra.forbid):
    kind: Literal["text"] | Literal["video"] | Literal["proof"] | Literal["assignments"]
    assignee: str
    status: Literal["planned"] | Literal["drafted"] | Literal["reviewable"] | Literal[
        "accepted"
    ] | Literal["needs_update"]
    notes: Optional[str]


class Node(YamlModel, extra=Extra.forbid):
    """A set of learning materials local to the cluster being described."""

    id: str
    title: Optional[str]
    assignments: Optional[tuple[Assignment, ...]]
    urls: Optional[tuple[URL, ...]]
    jobs: Optional[tuple[Job, ...]]

    def __hash__(self):
        return hash(self.id)


class NodePlaceholder(YamlModel, extra=Extra.forbid):
    """A reference to a Node belonging to a different cluster."""

    cluster: str
    id: str


class Edge(YamlModel, extra=Extra.forbid):
    """A "knowledge dependency" from end_id on start_id."""

    start_id: str
    end_id: str


class Motivation(YamlModel, extra=Extra.forbid):
    """A "motivation dependency" from end_id on start_id."""

    start_id: str
    end_id: str


class Cluster(YamlModel, extra=Extra.forbid):
    """A grouping of thematically related nodes, collected in a single data structure."""

    namespace_prefix: str
    nodes: list[Node]
    edges: list[Edge]
    motivations: Optional[list[Motivation]]


class Module(YamlModel, extra=Extra.forbid):
    clusters: list[Cluster]


@click.group()
def cli() -> None:
    pass


@click.command()
@click.argument("paths", type=click.Path(exists=True), nargs=-1)
def visualize_module(paths) -> None:
    """Show a visual representation of a complete module, with full namespacing."""
    module = Module(clusters=[])
    for path in paths:
        module.clusters.append(Cluster.parse_file(path))
    nxgraph = _module_dependency_graph(module)
    dot = graphviz.Digraph()
    for node in nxgraph.nodes:
        dot.node(node.id, node.title or node.id)
    for (u, v) in nxgraph.edges:
        kind = nxgraph.get_edge_data(u, v)["kind"]
        if kind == "dependency":
            dot.edge(u.id, v.id)
        elif kind == "motivation":
            dot.edge(u.id, v.id, style="dotted")
    dot.render("module.gv", directory=tempfile.gettempdir(), cleanup=True, view=True)


cli.add_command(visualize_module)


@click.command()
@click.argument("path", type=click.Path(exists=True))
def visualize_cluster(path) -> None:
    """Show a visual representation of a cluster, with minimal namespacing."""
    # does not seem worthwhile rewriting with networkx
    cluster: Cluster = Cluster.parse_file(path)
    dot = graphviz.Digraph()
    nodes: list[Node] = cluster.nodes
    for node in nodes:
        dot.node(f"{cluster.namespace_prefix}__{node.id}", node.title or node.id)
    edges: list[Edge] = cluster.edges
    for edge in edges:
        start_id = edge.start_id
        end_id = edge.end_id
        if "__" not in start_id:
            start_id = f"{cluster.namespace_prefix}__{start_id}"
        if "__" not in end_id:
            end_id = f"{cluster.namespace_prefix}__{end_id}"
        dot.edge(start_id, end_id)
    if cluster.motivations:
        for motivation in cluster.motivations:
            start_id = motivation.start_id
            end_id = motivation.end_id
            if "__" not in start_id:
                start_id = f"{cluster.namespace_prefix}__{start_id}"
            if "__" not in end_id:
                end_id = f"{cluster.namespace_prefix}__{end_id}"
            dot.edge(start_id, end_id, style="dotted")
    dot.render("cluster.gv", directory=tempfile.gettempdir(), cleanup=True, view=True)


cli.add_command(visualize_cluster)


def writeschema() -> None:
    with open("tests/testschema.json", mode="w") as fh:
        fh.write(Cluster.schema_json(indent=2))


@click.command()
@click.argument("assignments_path", type=click.Path(exists=True), nargs=1)
@click.argument("paths", type=click.Path(exists=True), nargs=-1)
def validate_module(assignments_path, paths) -> None:
    """Run sanity checks on the graph structure and contents of a complete module."""
    assignments_path = Path(assignments_path)
    messages: list[str] = []
    module = Module(clusters=[])
    for path in paths:
        module.clusters.append(Cluster.parse_file(path))
    # an inventory of all qualified names is constructed in a first pass
    # this can be used to check whether or not a node ID used in a dependency is valid
    # CHECKS: no node is namespaced inside its cluster
    qualified_names: set[str] = set()
    for cluster in module.clusters:
        for node in cluster.nodes:
            if "__" in node.id:
                messages.append(
                    f"Node {node.id} in cluster {cluster.namespace_prefix} should not mention namespace."
                )
            qualified_names.add(f"{cluster.namespace_prefix}__{node.id}")
    # CHECKS: all sources / sinks are valid IDs
    for cluster in module.clusters:
        cluster_node_ids = [node.id for node in cluster.nodes]
        for edge in cluster.edges:
            if (
                edge.start_id not in cluster_node_ids
                and edge.start_id not in qualified_names
            ):
                messages.append(
                    f"(Cluster {cluster.namespace_prefix}) Edge {edge.start_id} -> {edge.end_id} contains unknown start node"
                )
            if (
                edge.end_id not in cluster_node_ids
                and edge.end_id not in qualified_names
            ):
                messages.append(
                    f"(Cluster {cluster.namespace_prefix}) Edge {edge.start_id} -> {edge.end_id} contains unknown end node"
                )
        if cluster.motivations:
            for motivation in cluster.motivations:
                if (
                    motivation.start_id not in cluster_node_ids
                    and motivation.start_id not in qualified_names
                ):
                    messages.append(
                        f"(Cluster {cluster.namespace_prefix}) Motivation {motivation.start_id} -> {motivation.end_id} contains unknown start node"
                    )
                if (
                    motivation.end_id not in cluster_node_ids
                    and motivation.end_id not in qualified_names
                ):
                    messages.append(
                        f"(Cluster {cluster.namespace_prefix}) Motivation {motivation.start_id} -> {motivation.end_id} contains unknown end node"
                    )
    for path in paths:
        path = Path(path)
        cluster = Cluster.parse_file(path)
        for node in cluster.nodes:
            if node.assignments:
                for assignment in node.assignments:
                    if assignment.path.is_absolute():
                        assignment_path = assignment.path
                    else:
                        assignment_path = path.parent.joinpath(assignment.path)
                    if not assignment_path.exists():
                        messages.append(
                            f"Path {assignment_path} mentioned in file {path} for node {node.id} does not exist!"
                        )
                    elif assignments_path not in assignment_path.parents:
                        messages.append(
                            f"Path {assignment_path} does not extend {assignments_path}!"
                        )
                    if assignment.attachments:
                        for attachment in assignment.attachments:
                            if attachment.is_absolute():
                                locatable_attachment = attachment
                            else:
                                locatable_attachment = path.parent.joinpath(attachment)
                            if not locatable_attachment.exists():
                                messages.append(
                                    f"Path {locatable_attachment} mentioned in file {path} for node {node.id} as an attachment to assignment {assignment.description} does not exist!"
                                )
                            elif assignments_path not in locatable_attachment.parents:
                                messages.append(
                                    f"Path {locatable_attachment} does not extend {assignments_path}!"
                                )
    # printing out messages first time here
    # reason is because malformed graph may cause issues
    for message in messages:
        print(message)
    messages = []
    module_dag = _retain_edges(_module_dependency_graph(module), "dependency")
    cycles = list(nx.simple_cycles(module_dag))
    if cycles:
        messages.append(f"Cycles: {list(cycles)}")
    module_tr = nx.transitive_reduction(module_dag)
    for edge in module_dag.edges:
        if edge not in module_tr.edges:
            messages.append(f"Redundant edge: {edge}")
    for message in messages:
        print(message)


cli.add_command(validate_module)


@click.command()
@click.argument("node_id")
@click.argument("cluster_path", type=click.Path(exists=True))
def show_hard_dependencies_in_cluster(node_id, cluster_path: Path) -> None:
    """Show all knowledge dependencies of a given node within a particular cluster."""
    # not worth rewriting with networkx ATM
    cluster: Cluster = Cluster.parse_file(cluster_path)
    node_in_cluster = False
    for present_node in cluster.nodes:
        if present_node.id == node_id:
            dependencies: set[str] = set()
            added_nodes = set([node_id])
            node_in_cluster = True
    assert node_in_cluster, "Desired node is not in the cluster. Note that namespacing this node is not currently supported."
    while len(added_nodes) > 0:
        moved_nodes: set[str] = set(added_nodes)
        dependencies = dependencies.union(moved_nodes)
        for moved_node in moved_nodes:
            added_nodes = set(
                [edge.start_id for edge in cluster.edges if edge.end_id == moved_node]
            )
    dependencies.remove(node_id)
    for node_id in sorted(dependencies):
        print(node_id)


cli.add_command(show_hard_dependencies_in_cluster)


def get_hard_dependencies_in_module(
    node_id: str, cluster_paths: list[Path]
) -> set[str]:
    module = Module(clusters=[])
    for path in cluster_paths:
        module.clusters.append(Cluster.parse_file(path))
    nxgraph = _retain_edges(_module_dependency_graph(module), "dependency")
    nodes = [node for node in nxgraph.nodes if node.id == node_id]
    if len(nodes) == 0:
        raise ValueError(
            f"Desired node {node_id} is not in the module. Did you check the namespace?"
        )
    return set([node.id for node in nx.ancestors(nxgraph, nodes[0])])


@click.command()
@click.argument("node_id")
@click.argument("cluster_paths", type=click.Path(exists=True), nargs=-1)
def show_hard_dependencies_in_module(node_id: str, cluster_paths: list[Path]) -> None:
    """Show all knowledge dependencies of a given node within a complete module."""
    dependencies = get_hard_dependencies_in_module(node_id, cluster_paths)
    for node_id in sorted(dependencies):
        print(node_id)


cli.add_command(show_hard_dependencies_in_module)


# TODO: don't print directly to facilitate testing
@click.command()
@click.argument("cluster_paths", type=click.Path(exists=True), nargs=-1)
def check_learning_path(cluster_paths: list[Path]) -> None:
    """Provide a newline-separated list of namespaced node IDs and check whether it is a valid linear learning path."""
    module = Module(clusters=[])
    for path in cluster_paths:
        module.clusters.append(Cluster.parse_file(path))
    learning_path: list[str] = []
    comment_pattern = re.compile(r" *#.*")
    try:
        while True:
            line = re.sub(comment_pattern, "", input()).strip()
            if line != "":
                learning_path.append(line)
    except EOFError:
        pass
    if len(learning_path) > 0:
        complete_graph = _module_dependency_graph(module)
        motivations_graph = _retain_edges(complete_graph, "motivation")
        dependency_graph = _retain_edges(complete_graph, "dependency")
        seen_nodes: set[Node] = set()
        for (index, namespaced_node_id) in enumerate(learning_path):
            matching_nodes = [
                node for node in complete_graph.nodes if node.id == namespaced_node_id
            ]
            assert len(matching_nodes) > 0, f"Node does not occur in the graph: {namespaced_node_id}"
            node = matching_nodes[0]
            namespaced_hard_dependencies = get_hard_dependencies_in_module(
                namespaced_node_id, cluster_paths
            )
            # first node has to be accessible and has to motivate something
            if index == 0:
                if namespaced_hard_dependencies:
                    print(f"Starting node has hard dependencies:")
                    for dependency in namespaced_hard_dependencies:
                        print(dependency)
                if not len(nx.descendants(motivations_graph, node)):
                    print(f"Starting node does not motivate anything.")
            else:
                unmet_dependencies = namespaced_hard_dependencies.difference(
                    set((node.id for node in seen_nodes))
                )
                for dependency in unmet_dependencies:
                    print(
                        f"Node {index} ({namespaced_node_id}) has unmet dependency {dependency}."
                    )
                # "self" here is the node currently being checked
                self_and_dependents = nx.descendants(dependency_graph, node).union(
                    set([node])
                )
                is_motivated = False
                for seen_node in seen_nodes:
                    motivated_by_seen_node = nx.descendants_at_distance(motivations_graph, seen_node, 1)
                    if len(motivated_by_seen_node.intersection(self_and_dependents)):
                        is_motivated = True
                        break
                if not is_motivated:
                    print(
                        f"Node {index} ({node.id}) is not a motivated part of the learning path."
                    )
            seen_nodes.add(node)
    else:
        print("Empty learning path is technically valid, but pointless.")
    print("Done checking path.")


cli.add_command(check_learning_path)


def _module_dependency_graph(module: Module):
    """Assumes the module has already been validated."""
    dag = nx.DiGraph()
    for cluster in module.clusters:
        for node in cluster.nodes:
            inserted_node = node.copy(
                update={"id": f"{cluster.namespace_prefix}__{node.id}"}
            )
            dag.add_node(inserted_node)
    for cluster in module.clusters:
        for edge in cluster.edges:
            u = (
                edge.start_id
                if "__" in edge.start_id
                else f"{cluster.namespace_prefix}__{edge.start_id}"
            )
            v = (
                edge.end_id
                if "__" in edge.end_id
                else f"{cluster.namespace_prefix}__{edge.end_id}"
            )
            u_node = [node for node in dag.nodes if node.id == u][0]
            v_node = [node for node in dag.nodes if node.id == v][0]
            dag.add_edge(u_node, v_node, kind="dependency")
        if cluster.motivations:
            for motivation in cluster.motivations:
                u = (
                    motivation.start_id
                    if "__" in motivation.start_id
                    else f"{cluster.namespace_prefix}__{motivation.start_id}"
                )
                v = (
                    motivation.end_id
                    if "__" in motivation.end_id
                    else f"{cluster.namespace_prefix}__{motivation.end_id}"
                )
                u_node = [node for node in dag.nodes if node.id == u][0]
                v_node = [node for node in dag.nodes if node.id == v][0]
                dag.add_edge(u_node, v_node, kind="motivation")
    return dag


def _retain_edges(graph, kind: Literal["dependency"] | Literal["motivation"]):
    """Produce a new graph which only has the specified kind of edges"""
    copy = graph.copy()
    removed = [
        (u, v) for (u, v) in copy.edges if copy.get_edge_data(u, v)["kind"] != kind
    ]
    for (u, v) in removed:
        copy.remove_edge(u, v)
    return copy


@click.command()
@click.argument("assignments_path", type=click.Path(exists=True), nargs=1)
@click.argument("cluster_paths", type=click.Path(exists=True), nargs=-1)
@click.option("-m", "--model-path", type=click.Path(exists=True), required=False, help="Order nodes on this path linearly (and arbitrarily order nodes not on this path, but don't intersperse with those on the path).")
def generate_moodle_structure(assignments_path: Path, cluster_paths: list[Path], model_path: Path | None) -> None:
    """Generates JSON data for the Moodle plugin.
    
    Assumes the module has been validated."""
    def sentinel_index(lst, element, sentinel):
        try:
            return lst.index(element)
        except ValueError:
            return sentinel
    assignments_path = Path(assignments_path)
    module = Module(clusters=[])
    for path in cluster_paths:
        module.clusters.append(Cluster.parse_file(path))
    dag = _module_dependency_graph(module)  # includes both kinds
    dependency_graph = _retain_edges(dag, "dependency")
    motivation_graph = _retain_edges(dag, "motivation")
    assignments_path_start = assignments_path
    comment_pattern = re.compile(r" *#.*")
    if model_path:
        with open(model_path, mode='r') as fh:
            model_path_nodes = [re.sub(comment_pattern, "", line).strip() for line in fh.readlines() if line.strip()]
    collected_nodes = []
    for node in dag:
        current_node = dict()
        current_node['id'] = node.id
        if node.title:
            current_node["title"] = node.title
        if node.assignments:
            current_node["assignments"] = []
            for assignment in node.assignments:
                list_element = {
                    "description": assignment.description,
                    "path": "/" + str(assignments_path_start.joinpath(assignment.path.relative_to(assignments_path))),
                }
                if assignment.attachments:
                    list_element["attachments"] = list(("/" + str(assignments_path_start.joinpath(path.relative_to(assignments_path))) for path in assignment.attachments))
                current_node["assignments"].append(list_element)
        if node.urls:
            current_node["URLs"] = []
            for URL in node.urls:
                current_node["URLs"].append(
                    {"url": URL.url, "description": URL.description}
                )
        collected_nodes.append(current_node)
    if model_path:
        # len... is to place all nodes not on path at the end
        collected_nodes.sort(key=lambda n: sentinel_index(model_path_nodes,n['id'],len(model_path_nodes)))
    enablers: Dict = dict()
    for node in dag.nodes():
        self_and_dependents: Set[Node] = nx.descendants(dependency_graph, node).union(
            set([node])
        )
        current_node_enablers = []
        non_dependents = set(dag.nodes())
        for non_dependent in non_dependents:
            for self_or_dependent in self_and_dependents:
                if motivation_graph.has_edge(non_dependent, self_or_dependent):
                    current_node_enablers.append(non_dependent.id)
        enablers[node.id] = current_node_enablers
    structure: Dict = {
        "nodes": collected_nodes,
        # deliberately only adding *immediate* predecessors to avoid redundancy
        "requires_all_of": {
            node.id: [
                predecessor.id for predecessor in dependency_graph.predecessors(node)
            ]
            for node in dag.nodes()
        },
        "motivated_by_any_of": enablers,
    }
    print(json.dumps(structure, sort_keys=True, indent=4))


cli.add_command(generate_moodle_structure)


if __name__ == "__main__":
    # writeschema()
    cli()
