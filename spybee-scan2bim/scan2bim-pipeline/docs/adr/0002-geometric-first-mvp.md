# ADR-0002: Geometric-first MVP, ML later

- Status: Accepted
- Date: 2026-11-02

## Context

The best open pretrained segmentation weights are non-commercial, public datasets are non-commercial and
differ from Colombian construction sites, and we have no labelled data yet.

## Decision

The MVP uses geometry only (RANSAC planes, 2D slices, histograms, primitive fitting, rules). ML segmentation
is added after the MVP with our own weights trained on scan-BIM pairs and synthetic scans of client models.

## Consequences

+ Works from the first cloud, explainable, cheap to run on a CPU, no licence risk.
- Weaker on heavy clutter (scaffolding, materials) until the ML phase.
