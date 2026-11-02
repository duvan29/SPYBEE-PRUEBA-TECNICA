# ADR-0004: Local offset, never rotate the cloud

- Status: Accepted
- Date: 2026-11-02

## Context

CTM12 coordinates are millions of metres; float32 loses precision and Revit degrades far from its internal
origin. Rotating clouds to 'square' them breaks the link with surveys and the client's models.

## Decision

World coordinates are kept in float64 until a round offset is subtracted (local = world - offset). The cloud
is never rotated; the dominant wall direction is only used to regularise angles. Georeferencing travels as
metadata (building.json georef, IfcMapConversion, Revit shared coordinates with angle 0).

## Consequences

+ Millimetre precision, exact alignment with surveys and client models.
- Models of rotated buildings are not axis-aligned in Revit views (use Revit's project north if desired).
