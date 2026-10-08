# PCB stackup, layout decisions and enclosure assumptions

## Board
80 x 60 mm, 1.5 mm corner radius, 4 copper layers, 1.6 mm, ENIG, single-sided assembly (all parts on F.Cu), 4 x M3 plated GND holes, 3 fiducials.

## Stackup (ASSUMED, JLCPCB "JLC04161H-7628" style - confirm with the chosen fab)

| Layer | Use | Thickness | Notes |
|---|---|---|---|
| F.Cu | components, signals, RF microstrip, GND pour | 35 um (1 oz) | |
| prepreg 7628 | | 0.2104 mm, er ~4.4 | L1-L2 spacing sets the RF microstrip width |
| In1.Cu | **solid GND plane** (keep-out under antenna) | 15 um | continuous return path for RF, CAN, SPI |
| core | | 1.065 mm | |
| In2.Cu | signal/power routing + GND fill | 15 um | |
| prepreg 7628 | | 0.2104 mm | |
| B.Cu | routing + GND pour | 35 um | |

50 ohm microstrip on F.Cu over In1: Hammerstad estimate **0.40 mm** (er 4.4, h 0.2104, t ignored) - the router uses 0.40 mm for RF_IFA. **CALCULATED only** - request fab impedance-controlled stackup data (er may be ~4.05-4.6) and re-tune; TI states the distance top-to-GND must match the reference design (SWRA834A 4.1) so the RF filter probably needs VNA re-tuning.

## Design rules used (JLC standard capability, 4-layer)
Default clearance 0.15 mm (router keeps >=0.2 mm on the coarse grid), track >=0.15 (0.2 default), via 0.5/0.25 mm (fan-out vias 0.45/0.20), annular ring >=0.1, copper-edge 0.3, hole-hole 0.2. Net classes: HV (VIN_RAW/FUSED/PROT, buck SW, gate) 0.3 mm clearance for the 58 V clamp region (IPC-2221 coated surface is 0.13 mm/ >50 V; 0.3 mm chosen as margin); Power 0.4-0.6 mm; RF 0.3-0.4 mm; CAN 0.25 mm.

## Placement decisions
* Antenna: TI SWRU120D inverted-F at the top-left board edge, 25.7 x 7.5 mm, copper/keep-out on all four layers (rule area), feed line straight down to the RF pi-network; the two grounded tabs are bridged to the ground pour with two 0 ohm links (R67/R68) so the DC short is tunable.
* RF chain is placed in a straight line between CC2340 pin 31 and the antenna feed: shunt C, series L, shunt C, DC-block C, pi-match (ANT1/2/3), test link to U.FL.
* CC2340 decoupling: one 100 nF per VDDS pin; because fine-pitch escape needs room, the capacitors sit 1.5-2.5 mm from the QFN and connect through fan-out vias (**trade-off**: slightly longer decoupling loops than the TI reference; validate rail noise/RF spurs).
* DCDC inductor/cap of the CC2340 near pins 24/27 (hint-based auto-placement).
* Power stage on the right/bottom: J1 at the bottom edge, fuse/TVS/ideal-diode in a line, buck at top-right with the switching loop (CIN - U2 - L1 - COUT) compact; battery connector J3 at the bottom-left, far from the antenna.
* CAN: ESD (D3) then CMC (L3) next to J1, TCAN4550 close to CC2340 SPI side (SPI stubs short), crystal Y1 beside TCAN.
* All GND pads get a via to In1 (plus via arrays under thermal pads U2/U3/U5/U6).

## Enclosure assumptions (documented, not designed)
Plastic (non-metallised) housing, >=5 mm free air above/below the antenna, no metal/battery within 10 mm of the antenna keep-out, battery placed on the side away from the antenna, harness exits at the J1 edge, four M3 screws grounded to GND (chassis bonding via case is NOT assumed).

## Known layout limitations
Auto-router quality: no length matching or differential-pair coupling (CAN pair routed as two nets); no teardrops; silkscreen refs for passives are on F.Fab only; via-in-pad on thermal pads must be plugged/filled at the fab; RF network unverified.
