# Laboratory comparison protocol: resource-design release

Task MAT61-L2-S3-T01-R1. Planning protocol, not measured data or an approved safety procedure. The module remains one nominal 10 kW mechanical unit. The authoritative condition values are generated from implementation_model.json; the 144-row Validation_Matrix.csv is a planned run manifest.

## Complete-run contract

A prospective run occupies eight rig-hours: up to two hours installation/stabilisation and prescribed preparation, four hours qualified heat service, and two hours complete reset. Metering remains active throughout all eight hours. For a two-bed set, the controller changes bed roles within the service window; time samples and successive cycles are within-run observations. A failure to attain preparation, service or reset criteria is recorded as such. Extra occupancy is charged to the 24 reserved repeat/correction runs; it is not hidden by truncating a history.

The useful-water return target is 5 K below the listed supply target. The nominal 55/25/70 C point therefore uses 65-to-70 C water and 10 kW. Use +/-0.5 K delivered-temperature and +/-5% duty bands as initial planning tolerances; agree calibrated tolerances at M2 and freeze them with the protocol at M24. Log delivered and unmet heat separately. The source column denotes the imposed aggregate source boundary, not an assumption that regeneration heat is free. Source, rejection and service-loop mass flow/temperature pairs, absolute vapour pressures, bed temperatures and loading estimates, liquid inventories, all electric feeders and realised actuator states are required.

A change in service demand uses measured flow at fixed delivery temperature. The baseline source/rejection units and the mechanical vapour map constrain all policies identically. Report feasible domains when a cell fails the nominal point. A common service of at least 5 kW can be compared only after every included cell is requalified, with the capacity reduction retained as a result.

## Condition candidates

The table gives mean or plateau conditions for resource design. For stepped, ramped and reversed histories, the precise waveform, preparation sequence and boundaries are created by the validation owner, checked against the earned actuator domain, versioned and sealed before tuning ends at M24. All policies receive the same permitted forecast and observation stream. Final trajectories and independent group C remain outside fitting. Nominal C09 retains the 55/25/70 C, 10 kW service while withholding preparation history; C10-C12 provide additional boundary/history transfer. A known nominal boundary is compatible with a withheld complete preparation/run.

| ID | Partition | Source C | Rejection C | Supply C | Target kW | History |
| --- | --- | --- | --- | --- | --- | --- |
| C01 | DEV | 55 | 25 | 70 | 10.0 | Steady nominal |
| C02 | DEV | 50 | 25 | 65 | 8.0 | Source step |
| C03 | DEV | 60 | 25 | 70 | 10.0 | Load ramp |
| C04 | DEV | 55 | 30 | 70 | 8.0 | Rejection step |
| C05 | DEV | 55 | 20 | 70 | 10.0 | Source ramp |
| C06 | DEV | 60 | 30 | 75 | 8.0 | Two-level demand |
| C07 | DEV | 50 | 20 | 65 | 10.0 | Warm/cold preparation |
| C08 | DEV | 55 | 25 | 70 | 5.0 | Part load |
| C09 | FINAL | 55 | 25 | 70 | 10.0 | Nominal boundary with withheld preparation history |
| C10 | FINAL | 58 | 23 | 72 | 10.0 | Unseen load step sequence |
| C11 | FINAL | 50 | 30 | 70 | 7.0 | Edge-of-domain disturbance and recovery |
| C12 | FINAL | 60 | 28 | 75 | 8.0 | Unseen order-reversed boundary history |

## Replication and ordering

Cross four physical cells (reference/new MOF x granule/conductive structure), three policies, four final conditions and three disjoint powder/assembly blocks: 144 runs, 1152 rig-hours. Each block contains separate route groups; policies on one set are paired repeated observations. Counterbalance the three policy orders across blocks (fixed-MPC-RL; MPC-RL-fixed; RL-fixed-MPC) and rotate condition order. Inspect drift with interleaved reference checks. Reset and recondition between policies; record any departure from the predeclared preparation.

C09 supplies nominal runs for all 12 independent sets and all three policies. The four final histories are not four independent syntheses. Estimate paired effects at the three independent block level, propagate metering uncertainty, and report the resulting precision limit. With three groups the 95% paired t half-width is approximately 2.48 times the observed group standard deviation. No gain is promised and no percentage is calculated across unequal heat service.

Initial/final inventories must match within 2% of working transfer/stored-cycle heat or have an explicit bounded correction. Target cycle mass/energy residuals are 2%/5%, with expanded useful-heat uncertainty at most 5%. Include full reset, own pumps, valves, vapour machinery, branch compression and control electricity. Report laboratory boundary-bath electricity separately from heat crossing the machine boundary. Freeze predictions and controller/model versions before the prospective run; correction results keep separate IDs.

The 32 actuator ablations and 72 physical tuning histories precede the primary freeze. The 24 corrective eight-hour histories are budgeted for M33-M34; eight eight-hour adjacent-temperature transfer histories are budgeted for M35-M36. No second machine mode or field demonstrator is added.
