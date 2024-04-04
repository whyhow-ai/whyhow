"""Shared schemas."""

from typing import Any

from pydantic import BaseModel, Field, model_validator


class Node(BaseModel):
    """Schema for a single node.

    Mirroring Neo4j"s node structure.
    """

    labels: list[str]
    properties: dict[str, Any] = Field(default_factory=dict)


class Relationship(BaseModel):
    """Schema for a single relationship.

    Mirroring Neo4j"s relationship structure.
    """

    type: str
    start_node: Node
    end_node: Node
    properties: dict[str, Any] = Field(default_factory=dict)


class Graph(BaseModel):
    """Schema for a graph.

    Mirroring Neo4j"s graph structure.
    """

    relationships: list[Relationship]
    nodes: list[Node]

    @model_validator(mode="before")
    @classmethod
    def imply_nodes(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Implies nodes from relationships if not provided."""
        if "nodes" not in data or data["nodes"] is None:
            nodes = []
            for rel in data.get("relationships", []):
                start = rel.start_node
                end = rel.end_node
                if start not in nodes:
                    nodes.append(start)
                if end not in nodes:
                    nodes.append(end)

            data["nodes"] = nodes

        return data


class Entity(BaseModel):
    """Schema for a single entity.

    Note that this is not identical to Node because
    it only allows for 1 label and the text is a required field.
    """

    text: str
    label: str
    properties: dict[str, Any] = Field(default_factory=dict)

    def to_node(self) -> Node:
        """Convert the entity to a node."""
        properties = self.properties.copy()
        properties["name"] = self.text

        return Node(labels=[self.label], properties=properties)

    @classmethod
    def from_node(cls, node: Node) -> "Entity":
        """Convert a node to an entity."""
        if "name" not in node.properties:
            raise ValueError("Node must have a name property.")

        properties = node.properties.copy()
        name = properties.pop("name")

        return cls(
            text=name,
            label=node.labels[0],  # take the first label
            properties=properties,
        )


class Triple(BaseModel):
    """Schema for a single triple.

    Note that this is not identical to RelationshipNeo4j because
    it is not using ids

    """

    head: str
    head_type: str
    relationship: str
    tail: str
    tail_type: str
    properties: dict[str, Any] = Field(default_factory=dict)

    def to_relationship(self) -> Relationship:
        """Convert the triple to a relationship."""
        start = Node(labels=[self.head_type], properties={"name": self.head})
        end = Node(labels=[self.tail_type], properties={"name": self.tail})

        return Relationship(
            type=self.relationship,
            start_node=start,
            end_node=end,
            properties=self.properties,
        )

    @classmethod
    def from_relationship(cls, relationship: Relationship) -> "Triple":
        """Convert a relationship to a triple."""
        start = relationship.start_node
        end = relationship.end_node

        if "name" not in start.properties:
            raise ValueError("Start node must have a name property.")
        if "name" not in end.properties:
            raise ValueError("End node must have a name property.")

        return cls(
            head=start.properties["name"],
            head_type=start.labels[0],  # take the first label
            relationship=relationship.type,
            tail=end.properties["name"],
            tail_type=end.labels[0],  # take the first label
            properties=relationship.properties,
        )
