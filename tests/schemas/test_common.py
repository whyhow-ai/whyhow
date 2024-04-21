"""This module contains tests for the common schemas."""

import pytest

from whyhow.schemas.common import Entity, Graph, Node, Relationship, Triple


class TestGraph:
    """Tests for the Graph schema."""

    def test_no_nodes(self):
        """Test creating a graph with no nodes."""
        graph = Graph(relationships=[])
        assert graph.nodes == []
        assert graph.relationships == []

    def test_1_node(self):
        """Test creating a graph with one node."""
        node = Node(labels=["Person"], properties={"name": "Alice"})
        graph = Graph(nodes=[node], relationships=[])
        assert graph.nodes == [node]
        assert graph.relationships == []

    def test_3_nodes_1_rel(self):
        """Test creating a graph with three nodes and one relationship."""
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
    """Tests for the Entity schema."""

    def test_overall(self):
        """Test creating an entity."""
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
        """Test creating an entity with missing name."""
        node = Node(labels=["Person"], properties={})

        with pytest.raises(ValueError, match="Node must have a name property"):
            Entity.from_node(node)


class TestTriple:
    """Tests for the Triple schema."""

    def test_missing_name(self):
        """Test creating a triple with missing name."""
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
