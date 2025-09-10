# Gantt & WBS

```mermaid
gantt
  title Project Plan (12 weeks)
  dateFormat  YYYY-MM-DD
  section Planning
  Literature Review       :a1, 2025-07-01, 10d
  Gaps & Objectives       :a2, after a1, 5d
  section Data & Modeling
  Data Integration        :b1, 2025-07-20, 7d
  Baselines + Tuning      :b2, after b1, 10d
  Model Selection         :b3, after b2, 3d
  section Backend
  API Scaffold            :c1, 2025-08-05, 7d
  Auth + History          :c2, after c1, 5d
  Tests + CI + Docker     :c3, after c2, 5d
  section Frontend
  UI Scaffold             :d1, 2025-08-20, 5d
  Predict + History Chart :d2, after d1, 5d
  section Docs
  SRS & Diagrams          :e1, 2025-08-30, 7d
  Final Report & Slides   :e2, after e1, 7d
```

## WBS (high‑level)
- 1.0 Planning (Review, Gaps, Objectives)
- 2.0 Data & Modeling (Integration, Baselines, Tuning, Selection)
- 3.0 Backend (API, Auth, History, Tests, CI, Docker)
- 4.0 Frontend (Scaffold, Forms, Charting, Polish)
- 5.0 Documentation (SRS, Diagrams, Report, Slides)
