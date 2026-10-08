# Validation plan (nothing below has been executed - this is what must be verified before / after fabrication)

Status legend: **DONE-DESIGN** = checked on paper/CAD in this package; **TODO** = requires hardware.

## A. Pre-fabrication (design review) checks

| # | Check | Method | Status |
|---|---|---|---|
| A1 | ERC clean | `kicad-cli sch erc` (see `../manufacturing/reports/erc.rpt`) | DONE-DESIGN |
| A2 | DRC clean / connectivity | `kicad-cli pcb drc` incl. unconnected items (`../manufacturing/reports/drc.rpt`) | DONE-DESIGN (0 errors, 0 unconnected; 45 warnings, see README) |
| A3 | Symbol pin numbers vs footprint pads | symbol-pin vs footprint-pad script check | DONE-DESIGN |
| A4 | Pinouts vs datasheets | `docs/DATASHEET_TRACE.md` | DONE-DESIGN (TCAN4550, CC2340R5-Q1, LM5164-Q1, LM74700-Q1, BQ24074, TPS62A01-Q1, PESD2CAN, ACT45B) |
| A5 | Land patterns of non-stock parts (XGL6060/XGL4020 via XAL footprints, TZ3908 crystal, JST, Micro-Fit) | compare with vendor drawings | TODO |
| A6 | RF network values/topology | obtain LP-EM-CC2340R5-Q1 design files; EM-simulate feed line + IFA on this stackup | TODO |
| A7 | 50 ohm feed width on final stackup | fab impedance calculator with real dielectric constant | calculated 0.40 mm (Hammerstad, er 4.4, h 0.21 mm; 0.40 mm is what the layout uses), TODO confirm with fab |
| A8 | Component derating | 100 V MLCC / 80 V FET / 105 C bulk capacitor review | DONE-DESIGN (see BOM notes) |

## B. Bench bring-up (per board, in order)

1. Visual/AOI, continuity GND/V6P0/+3V3 to ground (> 1 kOhm).
2. Apply 12 V, current limit 100 mA: VIN_PROT = VIN - 0.1 V (TP3), V6P0 = 6.0 V +/- 3 % (TP4), +3V3 = 3.32 V (TP8).
3. Reverse polarity to -36 V at 100 mA limit: input current < 1 mA, no rail present.
4. Attach SWD (J2) -> read CC2340 ID, flash blinky (LED D4).
5. SPI read TCAN4550 device-ID registers (0x0000-0x0003 = "TCAN"), set nWKRQ/VIO bit, start CAN FD loopback, then bus with second node (split termination jumpers per test).
6. Power-fail: ramp VIN 12 V -> 5 V -> 12 V; observe V6P0 drop, BQ24074 PGOOD, VBATSYS continuity, MCU no reset, TCAN re-init.
7. Battery: charge with lab Li-ion pack + NTC simulator (10 kOhm, 0 C/45 C thresholds), verify ICHG = 100 mA (ISET voltage), termination, TS fault.
8. Sleep current on battery (target: measure; budget in POWER_BUDGET is calculated only).

## C. RF

| Test | Equipment | Acceptance (proposed, from BLE spec / TI reference) |
|---|---|---|
| Conducted TX power, harmonics | fit R66, remove R65, J4 U.FL -> spectrum analyser | ~ +5..8 dBm settings per TI; 2nd/3rd harmonics per ETSI/FCC limits |
| S11 of antenna | VNA at pi-match (R65 removed, cable to feed) | S11 < -10 dB 2.40-2.48 GHz in enclosure |
| HFXT / LFXT | frequency counter via DIO output (SWRA834A 6.3/6.4) | +/-10 ppm after tuning cap array |
| OTA range/PER | reference phone / BLE tester in final enclosure | PER < 30.8 % at spec sensitivity distance |

## D. Automotive environmental / EMC (test-house, not done)

ISO 16750-2 (reverse battery 4.7, load dump 4.6, starting profile 4.6.3, jump start 4.3), ISO 7637-2 pulses 1/2a/3a/3b/5b, ISO 11452 / CISPR 25 conducted+radiated emission, IEC 61000-4-2 / ISO 10605 ESD at J1 (CAN pins), ISO 11898-2 / -3 (CAN FD bit timing, SIC not required), thermal cycling (-40/+85 C), vibration (ISO 16750-3), humidity. Acceptance: functional class A/B per OEM spec.
