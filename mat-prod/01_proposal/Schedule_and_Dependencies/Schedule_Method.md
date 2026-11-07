# Schedule and dependencies

All months are relative to the future project start. A 36-month action is a design assumption. Task dates overlap intentionally; finish-to-start dependencies in Critical_Path.csv refer to gated releases, not to the first exploratory work.

The two gating spines reach M24: A-B-C-D-E-F and A-R-S-T-J. G cannot start until both F and J finish. G runs M25–M32; H is explicit corrective work in M33–M34; I runs M35–M36. CPM duration is 36 months. All gates on these spines have zero mathematical float because the planned correction/evidence work occupies the remaining period. H is a two-month management correction allocation, not spare labour or monetary contingency.

The original Task_Schedule.csv preserves every task interval. WP_Gantt.svg and Task_Gantt.svg are editable vector files; the Mermaid sources are editable logic diagrams. References and preliminary models allow work to start before the corresponding final material/model release.

| ID | Activity | Duration | Predecessors | Start | End | Float |
| --- | --- | --- | --- | --- | --- | --- |
| A | Service and interface contract | 2 |  | 1 | 2 | 0 |
| B | Composition screening | 7 | A | 3 | 9 | 0 |
| R | Reference rig | 6 | A | 3 | 8 | 0 |
| C | Production confirmation | 5 | B | 10 | 14 | 0 |
| S | Reference identification and ROM | 6 | R | 9 | 14 | 0 |
| D | Two shaping windows | 4 | C | 15 | 18 | 0 |
| T | Policies and HIL qualification | 6 | S | 15 | 20 | 0 |
| E | Production and process release | 3 | D | 19 | 21 | 0 |
| J | Deployment and metering closure | 4 | T | 21 | 24 | 0 |
| F | Cartridges and validation freeze | 3 | E | 22 | 24 | 0 |
| G | Prospective comparisons | 8 | F,J | 25 | 32 | 0 |
| H | Correction and repeat buffer | 2 | G | 33 | 34 | 0 |
| I | Transfer and evidence | 2 | H | 35 | 36 | 0 |
