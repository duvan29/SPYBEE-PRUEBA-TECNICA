# ADR-0005: Native Revit elements via add-in, not IFC import

- Status: Accepted
- Date: 2026-11-02

## Context

Revit's IFC import produces hard-to-edit elements (often DirectShapes); modellers need native walls and floors
to correct quickly.

## Decision

A C# add-in reads building.json and creates native elements (Level, Wall, Floor, structural columns, openings,
rooms), marks them AUTO/REVIEW, creates review views and sets shared coordinates. IFC4 is still exported for
openBIM and other tools.

## Consequences

+ Fast correction with standard Revit tools; we control types, naming and marking.
- Requires per-version builds and manual testing inside Revit.
