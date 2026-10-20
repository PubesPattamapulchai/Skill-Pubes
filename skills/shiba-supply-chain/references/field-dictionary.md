# Field dictionary

Starting guesses for column names. A name match is a hypothesis, not proof: confirm against the values (type, range, uniqueness, relation to other columns) before stating it as fact. Names are case-insensitive; ERP exports often rename or prefix them.

## SAP (MM / PP / SD)

| Column | Likely meaning | Check against |
|---|---|---|
| MATNR | Material number (SKU) | high-cardinality ID, often leading zeros |
| MAKTX | Material description | free text |
| MATKL | Material group (`matgrp`) | low-cardinality category |
| MTART | Material type (ROH raw, HALB semi, FERT finished) | 3-4 letter codes |
| MEINS / BSTME / VRKME | Base / order / sales unit of measure | EA, PC, KG, M, L; mixed units break sums |
| WERKS | Plant | 4-char code |
| LGORT | Storage location | 4-char code, under a plant |
| LIFNR | Vendor | ID |
| KUNNR | Customer | ID |
| EKORG / EKGRP | Purchasing org / purchasing group | codes |
| VKORG / VTWEG | Sales org / distribution channel | codes |
| EBELN / EBELP | PO number / PO item | EBELN+EBELP is usually the key |
| VBELN / POSNR | Sales or delivery document / item | |
| AUFNR | Production / process order | |
| MBLNR / MJAHR / ZEILE | Material document / year / item | |
| BSART | PO document type (NB standard, UB stock transfer) | |
| BEDAT | PO date | LT start |
| EINDT | Scheduled delivery date | promised date, not actual |
| BUDAT | Posting date | goods movement date; LT end when BWART=101 |
| BLDAT | Document date | |
| BWART | Movement type: 101 goods receipt, 102 GR reversal, 261 issue to order, 262 reversal, 601 goods issue delivery, 301/311 transfer | reversals must be netted or excluded |
| MENGE | Quantity | sign depends on movement (SHKZG S/H) |
| NETPR / PEINH | Net price / price unit | price per PEINH units, not per 1 |
| NETWR | Net value | MENGE x NETPR / PEINH |
| WAERS | Currency | mixed currencies break sums |
| PLIFZ | Planned delivery time (days), material master / info record | planned LT, not actual |
| WEBAZ | GR processing time (days) | |
| DZEIT | In-house production time (days) | |
| EISBE | Safety stock | |
| MINBE | Reorder point | |
| BESKZ | Procurement type (E in-house, F external) | |
| DISMM / DISPO | MRP type / MRP controller | |
| MAABC | ABC indicator | |
| LFIMG | Delivery quantity | |

## Generic / non-SAP

| Column | Likely meaning | Caution |
|---|---|---|
| LT, Lead time, LeadTime | Days from order to receipt | which two dates? calendar or working days? planned or actual? |
| Demand, Dem, Consumption, Usage | Quantity needed per period | sales, issues, and requirements differ; stock-outs censor demand |
| Qty, Quantity | Quantity | unit? sign? |
| UoM, UOM | Unit of measure | |
| MOQ | Minimum order quantity | |
| SS, Safety Stock | Buffer inventory | |
| ROP | Reorder point | |
| OTIF | On time in full | % or 0/1 flag? |
| SKU, Item, Part | Stock item | |
| FG / RM / WIP | Finished goods / raw material / work in progress | |
| Supplier, Vendor | Source | name vs ID, duplicates by spelling |
| Plant, Site, WH, DC | Location | |
| Cost, Price, Amount | Money | currency, per-unit or total |
