# Power architecture, budget and thermal notes (all values CALCULATED unless marked)

## 1. Power tree

```
J1 VBAT (9-36 V nominal)
  -> F1 1 A fuse -> D1 SMDJ36CA TVS (bidirectional, VRWM 36 V, Vc 58.1 V max)
  -> U1 LM74700-Q1 + Q1 BUK7Y41-80E ideal diode  ->  VIN_PROT (C3 33 uF/50 V, C4)
  -> U2 LM5164-Q1 buck (fsw ~300 kHz, UVLO 7.5/7.0 V)  ->  V6P0 = 6.01 V
        |-> FB1 (bead) -> TCAN4550 VSUP (5.5-30 V recommended, 42 V abs)
        |-> U3 BQ24074 IN (4.35-10.5 V op.)  -> VBATSYS (OUT 4.4 V with input / VBAT without)  <-> J3 1S Li-ion backup (100 mA charge)
                                              -> U4 TPS62A01-Q1 -> +3V3 = 3.32 V -> CC2340R5-Q1 VDDS (1.71-3.8 V), TCAN VIO (3.135-5.25 V), pull-ups
```
Voltage domains: 3.3 V for every logic signal (SPI, nINT, RST, nWKRQ, GPIOs). No level shifters required (TCAN VIO = CC2340 VDDS rail).

## 2. Set-points (from datasheet equations)

| Item | Equation (source) | Result |
|---|---|---|
| V6P0 | VOUT = 1.2 V x (1 + R13/R14) (LM5164-Q1 VREF 1.2 V) = 1.2 x (1+200k/49.9k) | 6.008 V (+/-1.5 % VREF, +/-1 % R) |
| LM5164 fsw | RRON = VOUT x 2500 / fsw[kHz] (TI Eq.15) -> 49.9 k | ~300 kHz |
| Buck ripple | dIL = VOUT/(fsw L) x (1-VOUT/VIN) at 24 V | 0.30 A pk-pk with 47 uH (30 % of 1 A) |
| UVLO | rising 1.5 V x (1+200k/49.9k), falling 1.4 V x (...) | 7.5 V / 7.0 V |
| Type-3 ripple | CA >= 10/(fsw x (RFB1 parallel RFB2)) = 0.84 nF -> 3.3 nF; RA x CA <= tON x (VIN-VOUT)/20 mV | RA=150 k, CA=3.3 nF, CB=56 pF (needs bench tuning) |
| +3V3 | VOUT = 0.6 V x (1 + R30/R31) (TPS62A01-Q1) = 0.6 x (1+453k/100k) | 3.318 V (+/-1.5 %) |
| Charge current | ICHG = KISET/RISET = 890 A*Ohm / 8.87 k | 100 mA (KISET 797-975 -> 90-110 mA) |
| Input limit | IIN = KILIM/RILIM = 1550 A*Ohm / 3.09 k (EN2=1, EN1=0) | ~0.5 A |

## 3. Load budget (worst-case, 25 C, values from datasheet electrical tables where cited)

| Consumer | Rail | Current | Basis |
|---|---|---|---|
| TCAN4550 normal mode, bus dominant | V6P0 (VSUP) | 80 mA typ / 90 mA (50 ohm) | TCAN datasheet ISUP, VCCOUT unloaded |
| TCAN4550 sleep | V6P0 | 25-42 uA | TCAN datasheet |
| TCAN4550 VIO (40 MHz crystal) | +3V3 | ~3 mA | TCAN datasheet IVIO |
| CC2340 radio active (0 dBm TX) | +3V3 | ~5.5 mA @3 V, allow 10 mA | CC2340 datasheet / SWRA834 ex. |
| LEDs, dividers, pull-ups | +3V3 | < 3 mA | design |
| Backup charge | V6P0 -> BAT | 100 mA | R20 |

Totals: +3V3 <= ~20 mA (66 mW). V6P0 <= 90 + 100 + 25 (3V3 via charger) = ~215 mA -> **1.3 W** max. Input power at 90 % converter efficiency ~1.45 W -> input current 0.16 A @9 V ... 0.04 A @36 V (fuse 1 A has >4x margin).

## 4. Dissipation / thermal (calculated, not simulated or measured)

| Part | Loss | Basis | Result |
|---|---|---|---|
| U2 LM5164 | ~0.2 W at 1.3 W out (est. 88 % efficiency) | RthJA 43.4 C/W (TI, datasheet board) | +9 C above ambient -> Tj ~ 94 C at 85 C ambient (limit 150 C) |
| U3 BQ24074 | (6.0-4.4) V x 25 mA + (4.4-3.8) V x 100 mA ~ 0.10 W | linear pass | small; thermal loop protects |
| Q1 BUK7Y41-80E | I^2R = (0.2 A)^2 x 41 mOhm ~ 2 mW | | negligible |
| D1 TVS | only during transients | 3 kW peak pulse | check surge test |
| U5 TCAN4550 | VSUP=6 V: LDO drop 1 V x <=10 mA + 6 V x 80 mA ~ 0.5 W max | RthJA 35 C/W | +17 C at worst -> OK; keeping VSUP low avoids the TSD case in TCAN Fig 9-8 (20 V, 70 mA load) |

Unresolved: real board thermal behaviour; ambient assumption **-40 to +85 C** (in-cabin/behind dash). 105 C-rated bulk capacitor C3 (EEE-FN1H330P) limits the design to <= 85-95 C ambient; replace with a 125 C polymer/hybrid capacitor for engine-bay use.

## 5. Behaviours requested by the brief

| Event | What happens | Status |
|---|---|---|
| Reverse battery (to -36 V) | TVS (VRWM 36 V) blocks; LM74700 gate off; FET body diode blocks; no reverse current | design intent, to test |
| Load dump (central suppression Us*=58 V) | TVS clamps VIN_FUSED <= 58.1 V; LM74700 ANODE window 60 V rec / 65 V abs; FET 80 V; LM5164 100 V | design intent, to test |
| Jump start (24 V on 12 V system) | within 9-36 V range, no clamp | design |
| Crank (down to ~4.5-6 V for ~20 ms-several s) | LM5164 stops <7.0 V; V6P0 falls; BQ24074 switches OUT to battery; MCU/BLE stay on; TCAN loses VSUP (bus goes passive, must be re-initialised) | design intent, firmware must handle |
| Brown-out (slow) | same as crank via UVLO hysteresis 7.5/7.0 V | design |
| Battery-backed operation | VBATSYS = VBAT (3.0-4.2 V) -> TPS62A01 (100 % mode at low VBAT) -> +3V3 2.9-3.3 V; TCAN held in RST | design |
| Battery absent | BQ24074 still supplies OUT=4.4 V from V6P0 | datasheet |
