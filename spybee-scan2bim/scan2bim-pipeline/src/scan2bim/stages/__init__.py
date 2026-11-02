"""Pipeline stages. Each stage reads from work/ and writes to work/ + out/debug/<stage>/.

Implemented: inspect, prep (voxel/offset; normals need open3d).
Planned (see docs/plan/EXECUTION_PLAN.md): levels, slabs, walls, columns, openings, spaces,
confidence, export (JSON/IFC/local cloud), qa, evaluate.
"""
