import pytest

from whyhow.schemas.common import Entity, Graph, Node, Relationship, Triple


class TestGraph:
    def test_no_nodes(self):
        graph = Graph(relationships=[])
        assert graph.nodes == []
        assert graph.relationships == []

    def test_1_node(self):
        node = Node(labels=["Person"], properties={"name": "Alice"})
        graph = Graph(nodes=[node], relationships=[])
        assert graph.nodes == [node]
        assert graph.relationships == []

    def test_3_nodes_1_rel(self):
        node_1 = Node(labels=["Person"], properties={"name": "Alice"})
        node_2 = Node(labels=["Person"], properties={"name": "Bob"})
        node_3 = Node(labels=["Person"], properties={"name": "Charlie"})

        rel = Relationship(
            start_node=node_1,
            end_node=node_2,
            type="KNOWS",
            properties={"since": 1999},
        )

        graph = Graph(nodes=[node_1, node_2, node_3], relationships=[rel])
        assert graph.nodes == [node_1, node_2, node_3]
        assert graph.relationships == [rel]

        graph_implied = Graph(relationships=[rel])

        assert graph_implied.nodes == [node_1, node_2]
        assert graph_implied.relationships == [rel]


class TestEntity:
    def test_overall(self):
        entity = Entity(
            text="Alice", label="Person", properties={"foo": "bar"}
        )
        node = entity.to_node()

        assert node.labels == ["Person"]
        assert node.properties == {"name": "Alice", "foo": "bar"}

        entity_reconstructed = Entity.from_node(node)

        assert entity.text == entity_reconstructed.text
        assert entity.label == entity_reconstructed.label
        assert entity.properties == entity_reconstructed.properties

        # test properties copied
        assert entity.properties is not entity_reconstructed.properties

    def test_missing_name(self):
        node = Node(labels=["Person"], properties={})

        with pytest.raises(ValueError, match="Node must have a name property"):
            Entity.from_node(node)


class TestTriple:
    # def test_overall(self):
    #     triple = Triple(
    #         head="Alice",
    #         head_type="Person",
    #         relationship="KNOWS",
    #         tail="Bob",
    #         tail_type="Person",
    #         properties={"since": 1999},
    #     )

    #     assert triple.head == "Alice"
    #     assert triple.head_type == "Person"
    #     assert triple.relationship == "KNOWS"
    #     assert triple.tail == "Bob"
    #     assert triple.tail_type == "Person"

    #     rel = triple.to_relationship()

    #     assert rel.start_node.labels == ["Person"]
    #     assert rel.start_node.properties == {"name": "Alice"}
    #     assert rel.end_node.labels == ["Person"]
    #     assert rel.end_node.properties == {"name": "Bob"}
    #     assert rel.type == "KNOWS"
    #     assert rel.properties == {"since": 1999}

    #     triple_reconstructed = Triple.from_relationship(rel)

    #     assert triple.head == triple_reconstructed.head
    #     assert triple.head_type == triple_reconstructed.head_type
    #     assert triple.relationship == triple_reconstructed.relationship
    #     assert triple.tail == triple_reconstructed.tail
    #     assert triple.tail_type == triple_reconstructed.tail_type
    #     assert triple.properties == triple_reconstructed.properties

    #     # test properties copied
    #     assert triple.properties is not triple_reconstructed.properties

    def test_missing_name(self):
        rel = Relationship(
            start_node=Node(labels=["Person"], properties={}),
            end_node=Node(labels=["Person"], properties={"name": "Bob"}),
            type="KNOWS",
            properties={},
        )

        with pytest.raises(
            ValueError, match="Start node must have a name property"
        ):
            Triple.from_relationship(rel)

        rel = Relationship(
            start_node=Node(labels=["Person"], properties={"name": "Alice"}),
            end_node=Node(labels=["Person"], properties={}),
            type="KNOWS",
            properties={},
        )

        with pytest.raises(
            ValueError, match="End node must have a name property"
        ):
            Triple.from_relationship(rel)
