# Datasheet trace - where every critical value/pin came from

All documents were downloaded from the manufacturer during the design session and parsed. `[figure]` = value read from a rendered figure.

| Topic | Value used | Source (document, section) |
|---|---|---|
| TCAN4550 pinout (20-pin VQFN RGY) | 1 OSC1, 2 nWKRQ, 3 GPIO1, 4 SCLK, 5 SDI, 6 SDO, 7 nCS, 8 nINT, 9 GPO2, 10 CANL, 11 CANH, 12 WAKE, 13 GND, 14 VSUP, 15 INH, 16 VCCOUT, 17 VIO, 18 FLTR, 19 RST, 20 OSC2, EP = GND | TCAN4550-Q1 SLLSEZ5D Table 5-1 |
| TCAN ratings | VSUP 5.5-30 V rec (42 V abs); VIO 3.135-5.25 V; bus +/-58 V; HBM bus 15 kV; C(FLTR) >=300 nF; C(VCCOUT) >=10 uF | SLLSEZ5D 6.1, 6.2, 6.4 |
| TCAN supporting circuit | 100 nF VSUP & VIO; WAKE 33 k/3 k/10 nF; INH 100 k pulldown; nINT/GPO2 pull-ups 2-10 k; series R on OSC1; 40 MHz crystal | SLLSEZ5D 8.3.x, 10, 11.1, Fig 9-6/9-7 |
| TCAN RST | active-high pulse, weak internal pull-down | SLLSEZ5D 8.3.8 |
| TCAN nWKRQ | defaults to internal 3.6 V rail; bit 0800h[19] selects VIO | SLLSEZ5D 8.3.10 |
| TCAN supply current | ISUP normal dominant 80/90 mA typ; sleep 25-42 uA | SLLSEZ5D 6.5 |
| CC2340R5-Q1 pinout (QFN32 RHB) | see `lib/bytebeam.kicad_sym`; VDDS 6/14/25/30, VDDR 1/27 (tied), VDDD 22 (1 uF), DCDC 24, RSTN 19 (no pull-up), X48P/N 28/29, X32P/N 20/21, ANT 31, RFGND 32, EGP | CC2340R5-Q1 SWRS292A Table 6-1 |
| CC2340 SPI0 mux | SCLK DIO8 (mux1), CSN DIO11 (mux1), POCI DIO12 (mux1), PICO DIO13 (mux2) | SWRS292A pin-attribute tables |
| CC2340 SWD | DIO16=SWDIO, DIO17=SWDCK | SWRA834A Table 3-5 |
| CC2340 DCDC | 10 uH + 10 uF on VDDR mandatory | SWRS272F 7.4 note |
| CC2340 crystals | HFXT 48 MHz, CL 5-9 pF, ESR <=60 R; validated Tai-Saw TZ3908AAAO43; LFXT CL 6-12 pF, 15 pF caps in reference | SWRS272F 7.20.3 |
| RF start-point values | 1.2 pF, 2 nH?, 2.8 nH, 0.7 pF, 1.5 pF, 12 pF, 15 pF, 10 uH, 10 uF, 1 uF, 0.1 uF | **text extracted from the LP-EM-CC2340R53 schematic figure in SWRA834A Fig 3-1 - topology could not be read; used only as starting values** |
| IFA geometry | Table 1-1 dimensions + Fig 1-1 vectorised (scale from L1 = 25.58 mm; feed width measured 0.48 vs 0.46 published) | TI SWRU120D |
| LM5164-Q1 | pins 1 GND, 2 VIN, 3 EN/UVLO, 4 RON, 5 FB, 6 PGOOD, 7 BST, 8 SW, EP; VREF 1.2 V; IPEAK 1.25-1.75 A; example components | SNVSB51C 4, 5, 7.2 |
| LM74700-Q1 (DBV-6) | 1 VCAP, 2 GND, 3 EN, 4 CATHODE, 5 GATE, 6 ANODE; ANODE +/-60 V rec/65 V abs; caps ANODE 22 nF, VCAP 0.1 uF; GATE-ANODE 15 V | SNOSD17G |
| BQ24074 (RGT-16) | pinout; OVP 10.5 V; VOUT(REG) 4.4 V; KISET 890, KILIM 1550 (1610 typ table); TS 10 k NTC | SLUS810N |
| TPS62A01-Q1 | pins; VFB 0.6 V; 22 uF/1 uH/4.7 uF; C3 27 pF for 3.3 V | SLUSF43A 5, 8.2 |
| PESD2CAN | pin 1/2 lines, 3 common; VRWM 24 V; AEC-Q101 | Nexperia PESD2CAN Rev.2 |
| ACT45B | 4.5 x 3.2 mm, 51 uH, 50 V, 200 mA, land pattern 5.9 x 3.4 (gaps 3.2 / 1.6) [figure] | TDK ACT45B 04/2025 |
| SMDJ36CA | VRWM 36 V, Vc(max) 58.1 V, AEC-Q101 | Littelfuse SMDJ series (web listing) |
| BUK7Y41-80E | 80 V, LFPAK56, AEC-Q101 (BUK9Y41 logic-level rejected: VGS limit) | Nexperia product page/datasheet listing |
| XGL6060-473MEC | 47 uH, Isat 2.5 A, Irms 3.7 A, DCR <=107 mOhm, AEC-Q200 | Coilcraft listing (via search, land pattern NOT confirmed) |
| XGL4020-102MEC | 1 uH, Isat 6.3-8.8 A, AEC-Q200 | Coilcraft listing (TI reference uses XGL3520-102MEC) |
| 33 uF/50 V EEE-FN1H330P | 6.3 x 5.8 mm, 105 C max | Panasonic listing via distributors |
| 50 ohm width | Hammerstad microstrip, er 4.4, h 0.2104 mm | calculated (Hammerstad) |

Not obtained / could not be verified: CC2340R40 datasheet (does not appear to exist), LP-EM-CC2340R5-Q1 design files (RF network topology), Coilcraft land patterns (site blocked), Tai-Saw crystal drawing, TCAN455x clock design guide (crystal load values).
