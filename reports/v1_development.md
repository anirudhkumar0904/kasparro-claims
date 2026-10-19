# Run report: v1 / development

- run_id: `b7d69fb0-0bf6-4368-8f9d-40c273a4369d`  status: **completed**
- provider/model: `anthropic` / `claude-sonnet-5-5`
- prompt: `prompts/v1.md` sha256 `03ce5227421ab02c…`
- dataset `long-brand-answers-50-v4`, facts `speaker-catalogue-v4`, evaluator `sentence-spans-and-labels-v4 (claimcheck-scorer-1)`
- source revision: `58f67d7543cf0c918a066881d1d22d1b74f711e0`
- started 2026-10-19T07:53:46.587247+00:00, finished 2026-10-19T08:00:31.128501+00:00
- settings: `{"model": "claude-sonnet-5-5", "api_base": "https://api.anthropic.com", "provider": "anthropic", "sampling": "provider-default (temperature not accepted by model)", "max_turns": 3, "max_tokens": 16000, "sdk_max_retries": 0, "request_timeout_s": 180.0}`
- file hashes: `{"answers.csv": "fa28e813ea54b4e5ea985585f22f084d826241e1182accbc27ace17066125724", "brand_facts.csv": "2190d40fad2dd167ef2437956c43d595aaf2554ea673a4789b9343cb7e2936f2", "development_gold.csv": "afe84cc78f304afb6a4aaa505dd7504af80fcbf8bc507806aa5ff0aab6bf4850"}`

## Counts

| scheduled | ok | errors | empty ok | P | G | M | C | latency total (s) | tokens in/out |
|---|---|---|---|---|---|---|---|---|---|
| 40 | 40 | 0 | 0 | 376 | 376 | 376 | 376 | 403.5 | 440541/64741 |

## Metrics

| | precision | recall | F1 |
|---|---|---|---|
| extraction | 1.0000 | 1.0000 | 1.0000 |
| joint (span + label) | 1.0000 | 1.0000 | **1.0000** |

Gold claim coverage C/G: 1.0000

## Evidence agreement (secondary diagnostic, not a required metric)

Predicted fact_ids vs gold evidence_fact_ids on 376 span-matched claims: exact set 259/376 (0.6888); fact-ID precision 0.8192, recall 0.8883, F1 0.8524 (tp 358, fp 79, fn 45). Exact-set rate by expected label: `{"contradicted": 0.608, "supported": 0.775, "unknown": 0.684}`

## Label confusion (rows = expected)

| expected \ predicted | supported | contradicted | unknown | missed |
|---|---|---|---|---|
| supported | 120 | 0 | 0 | 0 |
| contradicted | 0 | 120 | 0 | 0 |
| unknown | 0 | 0 | 136 | 0 |

## By difficulty tag

| tag | total | correct | wrong label | missed |
|---|---|---|---|---|
| policy_scope | 52 | 52 | 0 | 0 |
| negation | 43 | 43 | 0 | 0 |
| arithmetic | 33 | 33 | 0 | 0 |
| unit_conversion | 32 | 32 | 0 | 0 |
| model_scope | 29 | 29 | 0 | 0 |
| explicit_false | 27 | 27 | 0 | 0 |
| missing_fact | 25 | 25 | 0 | 0 |
| qualification | 24 | 24 | 0 | 0 |
| feature_conflation | 23 | 23 | 0 | 0 |
| inference | 22 | 22 | 0 | 0 |
| date_scope | 21 | 21 | 0 | 0 |
| comparison | 20 | 20 | 0 | 0 |
| policy_vs_capability | 17 | 17 | 0 | 0 |
| historical_scope | 15 | 15 | 0 | 0 |
| price | 13 | 13 | 0 | 0 |
| condition_scope | 13 | 13 | 0 | 0 |
| scope | 12 | 12 | 0 | 0 |
| capability_vs_connector | 12 | 12 | 0 | 0 |
| price_vs_shipping | 11 | 11 | 0 | 0 |
| future_scope | 11 | 11 | 0 | 0 |
| box_scope | 9 | 9 | 0 | 0 |
| variant_transfer | 8 | 8 | 0 | 0 |
| missing_condition | 7 | 7 | 0 | 0 |
| condition_swap | 6 | 6 | 0 | 0 |
| feature_scope | 6 | 6 | 0 | 0 |
| outdated_fact | 6 | 6 | 0 | 0 |
| requirement_vs_availability | 6 | 6 | 0 | 0 |
| negative_missing_fact | 6 | 6 | 0 | 0 |
| conditions | 5 | 5 | 0 | 0 |
| capability_vs_rating | 4 | 4 | 0 | 0 |
| region_scope | 4 | 4 | 0 | 0 |
| cross_brand_comparison | 2 | 2 | 0 | 0 |

## Missed gold claims (0)


## Extra / unmatched predictions (0)


## Matched but wrong label (0)


## Answer outcomes and predictions

### A01: ok
turns=2 latency=9870ms claims=9 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A01.json`

- `A01:306:460` **supported** ✓span ✓label ['cleartrail.mini.price_2026', 'cleartrail.plus.price_2026']: For the current India catalogue, ClearTrail Mini is listed at INR 1,200 less than ClearTrail Plus, comparing the two tax-inclusive prices before shipping.
  - Mini is INR 1,299 and Plus is INR 2,499, both tax-inclusive and excluding shipping, so the difference is INR 1,200.
- `A01:461:647` **contradicted** ✓span ✓label ['cleartrail.mini.warranty_india']: For an authorized India purchase with the original invoice and a manufacturing defect, ClearTrail Mini receives a standard manufacturer warranty lasting 18 months from the purchase date.
  - The catalogue gives a 12-month India warranty for Mini, not 18 months.
- `A01:649:832` **unknown** ✓span ✓label []: An opened ClearTrail Mini can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
  - The catalogue has no return or refund policy rows.
- `A01:833:1040` **unknown** ✓span ✓label []: The sustained amplifier output of ClearTrail Mini is forty watts per channel during ordinary playback, which allows a direct loudness comparison with other speakers advertised using electrical power figures.
  - The catalogue has no amplifier power output rows.
- `A01:1237:1439` **unknown** ✓span ✓label []: An authorized India service centre guarantees repair of ClearTrail Mini within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
  - The catalogue has no repair turnaround or service guarantee rows.
- `A01:1440:1619` **contradicted** ✓span ✓label ['cleartrail.mini.battery_100_percent', 'cleartrail.mini.battery_50_percent']: The stated laboratory playback time for ClearTrail Mini, using a new battery with EQ off at one hundred percent volume, remains 12 hours without any reduction for louder playback.
  - At 100 percent volume the stated time is 6 hours. The 12 hours applies only at 50 percent volume.
- `A01:1620:1767` **supported** ✓span ✓label ['cleartrail.mini.price_2026']: For an India purchase at the official catalogue list price on 1 October 2026, ClearTrail Mini costs INR 1,299 including tax but excluding shipping.
  - The 2026 India list price is INR 1,299, tax included and shipping excluded.
- `A01:1769:1942` **contradicted** ✓span ✓label ['cleartrail.mini.adapter_included']: The official India retail box for ClearTrail Mini includes a wall charging adapter, even though separate accessory lists may make the charging arrangement look less obvious.
  - The official India retail box does not include an adapter. It includes only a USB-C cable.
- `A01:1943:2104` **supported** ✓span ✓label ['cleartrail.mini.wifi', 'cleartrail.mini.bluetooth_version', 'cleartrail.mini.app_required_bluetooth']: The built-in Wi-Fi capability of ClearTrail Mini is absent, which should be treated as a separate specification from its ability to receive audio over Bluetooth.
  - Mini has no built-in Wi-Fi. It has Bluetooth 5.3, and basic Bluetooth playback is a separate listed capability.

### A02: ok
turns=2 latency=9591ms claims=10 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A02.json`

- `A02:306:506` **supported** ✓span ✓label ['cloudnote.studio.water_damage_covered']: Whatever conclusions a buyer draws from the water-resistance rating, water damage remains excluded from the standard India manufacturer warranty covering CloudNote Studio after an authorized purchase.
  - The catalogue says water damage is not covered under the India standard warranty, independent of the water resistance rating.
- `A02:507:689` **contradicted** ✓span ✓label ['cloudnote.studio.adapter_included']: The official India retail box for CloudNote Studio does not include a wall charging adapter, even though separate accessory lists may make the charging arrangement look less obvious.
  - The catalogue says the official India retail box for Studio includes an adapter.
- `A02:691:875` **unknown** ✓span ✓label []: An opened CloudNote Studio can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
  - The catalogue has no return or refund policy rows.
- `A02:876:1084` **unknown** ✓span ✓label []: The sustained amplifier output of CloudNote Studio is forty watts per channel during ordinary playback, which allows a direct loudness comparison with other speakers advertised using electrical power figures.
  - The catalogue has no amplifier power output row.
- `A02:1085:1272` **unknown** ✓span ✓label ['cloudnote.studio.bluetooth_version']: CloudNote Studio supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
  - The catalogue gives only the Bluetooth version (5.4) and no codec information.
- `A02:1469:1659` **unknown** ✓span ✓label ['cloudnote.studio.battery_50_percent']: In winter weather below freezing, CloudNote Studio delivers its full 18-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
  - The 18-hour figure is a laboratory test result, and the catalogue has no data on battery runtime below freezing.
- `A02:1660:1813` **supported** ✓span ✓label ['cloudnote.studio.price_2026', 'cloudnote.air.price_2026']: For the current India catalogue, CloudNote Studio is listed at INR 1,500 more than CloudNote Air, comparing the two tax-inclusive prices before shipping.
  - The 2026 prices are 2,999 for Studio and 1,499 for Air, a difference of 1,500, both tax-inclusive and excluding shipping.
- `A02:1815:2039` **contradicted** ✓span ✓label ['cloudnote.studio.water_damage_covered']: Water damage to CloudNote Studio is included in the standard India manufacturer warranty after an authorized purchase, because water resistance should be understood as warranty coverage rather than just a product capability.
  - The catalogue says water damage is not covered, independent of the water resistance rating.
- `A02:2040:2223` **contradicted** ✓span ✓label ['cloudnote.studio.stereo_pairing_scope', 'cloudnote.air.stereo_pairing_scope']: The manufacturer supports a stereo pair made from one CloudNote Studio and one CloudNote Air, since being members of the same brand is sufficient for cross-model stereo compatibility.
  - The catalogue says stereo pairing works only with two units of the same model, and cross-model pairing is unsupported.
- `A02:2224:2372` **supported** ✓span ✓label ['cloudnote.studio.price_2026']: For an India purchase at the official catalogue list price on 1 October 2026, CloudNote Studio costs INR 2,999 including tax but excluding shipping.
  - The 2026 India list price is INR 2,999, tax included and shipping excluded.

### A03: ok
turns=2 latency=9662ms claims=9 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A03.json`

- `A03:335:505` **unknown** ✓span ✓label []: Orders for CloudNote Air receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
  - The catalogue has no delivery or shipping-charge policy rows.
- `A03:506:687` **unknown** ✓span ✓label []: An opened CloudNote Air can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
  - The catalogue has no return or refund policy rows. The warranty rows cover manufacturing defects only.
- `A03:689:861` **supported** ✓span ✓label ['cloudnote.air.microphone']: The built-in microphone is included on CloudNote Air, so microphone availability should be checked for this exact model instead of copied from another speaker in the range.
  - The catalogue says CloudNote Air has a built-in microphone.
- `A03:862:1043` **supported** ✓span ✓label ['cloudnote.air.weight']: Considering the speaker alone and leaving retail packaging and accessories out of the measurement, CloudNote Air has a stated mass of 0.35 kilograms for carrying-weight comparisons.
  - The catalogue gives 350 g for the speaker only, which is 0.35 kg.
- `A03:1240:1409` **contradicted** ✓span ✓label ['cloudnote.air.microphone']: The built-in microphone is not included on CloudNote Air, without needing an accessory to change the hardware specification being described for this exact speaker model.
  - The catalogue says CloudNote Air has a built-in microphone.
- `A03:1410:1563` **supported** ✓span ✓label ['cloudnote.air.price_2026', 'cloudnote.studio.price_2026']: For the current India catalogue, CloudNote Air is listed at INR 1,500 less than CloudNote Studio, comparing the two tax-inclusive prices before shipping.
  - The 2026 India prices are 1,499 for Air and 2,999 for Studio, a difference of 1,500.
- `A03:1564:1742` **contradicted** ✓span ✓label ['cloudnote.air.weight', 'cloudnote.studio.weight']: When measuring just the speaker rather than the retail box and accessories, CloudNote Air weighs 1100 grams, matching the carrying-weight figure associated with CloudNote Studio.
  - CloudNote Air weighs 350 g. Only Studio weighs 1100 g.
- `A03:1744:1917` **supported** ✓span ✓label ['cloudnote.air.water_rating', 'cloudnote.air.immersion_allowed']: Despite the declared IPX4 water-resistance rating, the manufacturer does not permit fresh-water immersion of CloudNote Air, even with all of the port covers properly closed.
  - Air is rated IPX4, and immersion is not allowed in fresh water with all port covers closed.
- `A03:1918:2069` **contradicted** ✓span ✓label ['cloudnote.air.price_2026', 'cloudnote.air.price_2025']: For an India purchase at the official catalogue list price on 1 October 2026, CloudNote Air still costs INR 1,199 including tax but excluding shipping.
  - The 2026 list price is INR 1,499. INR 1,199 was the 2025 price.

### A04: ok
turns=2 latency=11611ms claims=11 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A04.json`

- `A04:324:493` **contradicted** ✓span ✓label ['stonewave.max.microphone']: The built-in microphone is not included on StoneWave Max, without needing an accessory to change the hardware specification being described for this exact speaker model.
  - The catalogue says StoneWave Max has a built-in microphone (true), so the claim that it is not included is refuted.
- `A04:494:694` **unknown** ✓span ✓label []: An authorized India service centre guarantees repair of StoneWave Max within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
  - The catalogue has no repair turnaround or repair guarantee information.
- `A04:696:899` **unknown** ✓span ✓label ['stonewave.max.warranty_india']: A retail purchase of StoneWave Max in Germany qualifies for the same 18-month manufacturer warranty described for authorized India purchases, without any different regional terms affecting that duration.
  - The 18-month warranty row applies only to India purchases from authorized sellers, and nothing covers Germany.
- `A04:900:1097` **supported** ✓span ✓label ['stonewave.max.water_damage_covered']: Whatever conclusions a buyer draws from the water-resistance rating, water damage remains excluded from the standard India manufacturer warranty covering StoneWave Max after an authorized purchase.
  - Water damage is not covered under the India standard manufacturer warranty, independent of the water-resistance rating.
- `A04:1098:1267` **supported** ✓span ✓label ['stonewave.max.price_2025', 'stonewave.max.price_2026']: The move from the 2025 India catalogue to the 2026 catalogue raised the tax-inclusive list price of StoneWave Max by INR 200, with shipping excluded in both comparisons.
  - The price went from INR 3,299 in 2025 to INR 3,499 in 2026, a rise of INR 200, with tax included and shipping excluded in both.
- `A04:1464:1636` **supported** ✓span ✓label ['stonewave.max.usb_audio', 'stonewave.max.charging_port']: For wired digital audio specifically, the USB-C connector on StoneWave Max does provide an audio-input path, regardless of the fact that the connector also serves charging.
  - USB audio is true for the USB-C port, which is also the charging port.
- `A04:1637:1798` **contradicted** ✓span ✓label ['stonewave.max.battery_50_percent']: At fifty percent volume with EQ off and a new battery in the laboratory, StoneWave Max is rated for 1500 minutes of playback before recharging becomes necessary.
  - The rating is 24 hours, which is 1440 minutes, not 1500.
- `A04:1800:1983` **contradicted** ✓span ✓label ['stonewave.max.immersion_duration', 'stonewave.max.immersion_depth', 'stonewave.max.immersion_allowed']: With all port covers closed, StoneWave Max is permitted to remain immersed in fresh water at a depth of one metre for a full hour under the manufacturer's stated laboratory allowance.
  - The maximum laboratory duration at 1 metre is 30 minutes, not a full hour.
- `A04:1984:2165` **unknown** ✓span ✓label []: An opened StoneWave Max can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
  - The catalogue has no return or refund policy.
- `A04:2166:2361` **unknown** ✓span ✓label []: StoneWave Max accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
  - The catalogue has no multipoint Bluetooth information; it lists only the Bluetooth version.
- `A04:2363:2540` **contradicted** ✓span ✓label ['stonewave.max.price_2025']: In the 2025 India catalogue, before the current-year revision, StoneWave Max already carried the same tax-inclusive list price of INR 3,499, excluding shipping from that amount.
  - The 2025 India list price was INR 3,299, not INR 3,499.

### A05: ok
turns=2 latency=8250ms claims=8 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A05.json`

- `A05:371:531` **contradicted** ✓span ✓label ['stonewave.go.battery_50_percent']: At fifty percent volume with EQ off and a new battery in the laboratory, StoneWave Go is rated for 1020 minutes of playback before recharging becomes necessary.
  - The catalogue rates 16 hours (960 minutes) under these conditions, not 1020 minutes.
- `A05:532:697` **supported** ✓span ✓label ['stonewave.go.adapter_included', 'stonewave.go.charging_port']: The official India retail box for StoneWave Go does not contain a wall charging adapter, so the box contents should not be inferred just from the charging-port type.
  - The official India retail box has no adapter, even though the port is USB-C.
- `A05:699:890` **unknown** ✓span ✓label ['stonewave.go.bluetooth_version']: The Bluetooth connection on StoneWave Go maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
  - The catalogue gives only the Bluetooth version (5.2) and has no range or source-switching data.
- `A05:891:1095` **unknown** ✓span ✓label []: The sustained amplifier output of StoneWave Go is forty watts per channel during ordinary playback, which allows a direct loudness comparison with other speakers advertised using electrical power figures.
  - The catalogue has no amplifier power output rows.
- `A05:1292:1467` **supported** ✓span ✓label ['stonewave.go.microphone']: The built-in microphone is not included on StoneWave Go, so microphone availability should be checked for this exact model instead of copied from another speaker in the range.
  - The catalogue says StoneWave Go has no built-in microphone.
- `A05:1468:1651` **contradicted** ✓span ✓label ['stonewave.go.app_required_bluetooth']: Basic Bluetooth playback on StoneWave Go requires the manufacturer companion app to be installed first, rather than allowing a listener to pair a source and start playback without it.
  - The catalogue says basic Bluetooth playback does not require the manufacturer app.
- `A05:1652:1828` **unknown** ✓span ✓label []: Using a twenty-watt wall adapter, a fully discharged StoneWave Go reaches a complete charge in ninety minutes, so a short charging stop is enough to restore the entire battery.
  - The catalogue has no charging time or adapter wattage data.
- `A05:1830:1980` **contradicted** ✓span ✓label ['stonewave.go.price_2026', 'stonewave.go.price_2025']: For an India purchase at the official catalogue list price on 1 October 2026, StoneWave Go still costs INR 1,799 including tax but excluding shipping.
  - The 2026 India list price is INR 1,999. INR 1,799 was the 2025 price.

### A06: ok
turns=2 latency=12635ms claims=10 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A06.json`

- `A06:306:494` **contradicted** ✓span ✓label ['cleartrail.plus.usb_audio']: For wired digital audio specifically, the USB-C connector on ClearTrail Plus does not provide an audio-input path, so the connector can be treated accordingly when choosing a wired source.
  - The catalogue says ClearTrail Plus supports wired digital audio through its USB-C port.
- `A06:495:697` **unknown** ✓span ✓label []: No version of ClearTrail Plus has ever been offered in blue, including previous-year retail stock and editions supplied only through independent authorized sellers rather than the official online store.
  - The catalogue has no colour or edition information.
- `A06:699:897` **unknown** ✓span ✓label []: The plastic used in the enclosure of ClearTrail Plus contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
  - The catalogue has no recycled-material information.
- `A06:898:1081` **unknown** ✓span ✓label ['cleartrail.plus.price_2026']: The official India catalogue price of ClearTrail Plus will drop by INR 300 during January 2027, with that future reduction applying before shipping to purchases from the brand itself.
  - The catalogue has no 2027 price or future price-change information.
- `A06:1082:1235` **contradicted** ✓span ✓label ['cleartrail.plus.price_2026', 'cleartrail.plus.price_2025']: For an India purchase at the official catalogue list price on 1 October 2026, ClearTrail Plus still costs INR 2,199 including tax but excluding shipping.
  - The 2026 list price is INR 2,499. INR 2,199 was the 2025 price.
- `A06:1432:1621` **unknown** ✓span ✓label ['cleartrail.plus.battery_50_percent']: In winter weather below freezing, ClearTrail Plus delivers its full 20-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
  - The 20 hours at 50% volume is a laboratory figure, and the catalogue has no data on how freezing temperatures affect it.
- `A06:1622:1801` **contradicted** ✓span ✓label ['cleartrail.plus.battery_100_percent', 'cleartrail.plus.battery_50_percent']: The stated laboratory playback time for ClearTrail Plus, using a new battery with EQ off at one hundred percent volume, remains 20 hours without any reduction for louder playback.
  - At 100% volume the stated laboratory time is 10 hours. 20 hours applies only at 50% volume.
- `A06:1803:1957` **supported** ✓span ✓label ['cleartrail.plus.price_2026', 'cleartrail.mini.price_2026']: For the current India catalogue, ClearTrail Plus is listed at INR 1,200 more than ClearTrail Mini, comparing the two tax-inclusive prices before shipping.
  - The 2026 prices are INR 2,499 for Plus and INR 1,299 for Mini, a difference of INR 1,200.
- `A06:1958:2132` **supported** ✓span ✓label ['cleartrail.plus.microphone']: The built-in microphone is included on ClearTrail Plus, so microphone availability should be checked for this exact model instead of copied from another speaker in the range.
  - The catalogue confirms a built-in microphone on ClearTrail Plus.
- `A06:2133:2356` **contradicted** ✓span ✓label ['cleartrail.plus.water_damage_covered']: Water damage to ClearTrail Plus is included in the standard India manufacturer warranty after an authorized purchase, because water resistance should be understood as warranty coverage rather than just a product capability.
  - The standard India warranty does not cover water damage, independent of the water resistance rating.

### A07: ok
turns=2 latency=8944ms claims=8 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A07.json`

- `A07:306:511` **unknown** ✓span ✓label ['cleartrail.plus.warranty_india']: A retail purchase of ClearTrail Plus in Germany qualifies for the same 12-month manufacturer warranty described for authorized India purchases, without any different regional terms affecting that duration.
  - The catalogue only gives a 12-month warranty for authorized India purchases and says nothing about Germany or regional terms.
- `A07:512:698` **unknown** ✓span ✓label ['cleartrail.plus.bluetooth_version']: ClearTrail Plus supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
  - The catalogue lists Bluetooth 5.3 but has no codec row, and a Bluetooth version does not establish AAC support.
- `A07:700:884` **contradicted** ✓span ✓label ['cleartrail.plus.stereo_pairing_scope', 'cleartrail.mini.stereo_pairing_scope']: The manufacturer supports a stereo pair made from one ClearTrail Plus and one ClearTrail Mini, since being members of the same brand is sufficient for cross-model stereo compatibility.
  - Both models are listed as same-model-only stereo pairing, with cross-model pairing unsupported.
- `A07:987:1153` **supported** ✓span ✓label ['cleartrail.plus.immersion_allowed', 'cleartrail.plus.immersion_depth', 'cleartrail.plus.immersion_duration']: With all port covers closed, the laboratory immersion allowance for ClearTrail Plus is limited to fresh water at no more than one metre for no more than half an hour.
  - The catalogue gives fresh water, ports closed, a 1 metre maximum depth and a 30 minute maximum duration, which is half an hour.
- `A07:1350:1533` **supported** ✓span ✓label ['cleartrail.plus.weight']: Considering the speaker alone and leaving retail packaging and accessories out of the measurement, ClearTrail Plus has a stated mass of 0.58 kilograms for carrying-weight comparisons.
  - 580 grams for the speaker alone equals 0.58 kg.
- `A07:1534:1719` **supported** ✓span ✓label ['cleartrail.plus.app_required_bluetooth', 'cleartrail.plus.app_available']: Basic Bluetooth listening on ClearTrail Plus does not require the manufacturer companion app to be installed, even if a buyer is interested in optional app-related features or settings.
  - Basic Bluetooth playback does not require the app, and the app does support this model.
- `A07:1721:1919` **unknown** ✓span ✓label []: The plastic used in the enclosure of ClearTrail Plus contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
  - The catalogue has no recycled-material content row.
- `A07:1920:2143` **contradicted** ✓span ✓label ['cleartrail.plus.water_damage_covered']: Water damage to ClearTrail Plus is included in the standard India manufacturer warranty after an authorized purchase, because water resistance should be understood as warranty coverage rather than just a product capability.
  - The India standard warranty does not cover water damage, independent of the water resistance rating.

### A08: ok
turns=2 latency=9707ms claims=10 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A08.json`

- `A08:335:525` **supported** ✓span ✓label ['cleartrail.mini.warranty_invoice_required', 'cleartrail.mini.warranty_india']: Even when other warranty conditions are met for an authorized India purchase, the original purchase invoice is still required to claim the standard manufacturer warranty for ClearTrail Mini.
  - The catalogue says the India standard warranty requires the original invoice, with an authorized-seller purchase.
- `A08:526:685` **contradicted** ✓span ✓label ['cleartrail.mini.wifi']: The built-in Wi-Fi capability of ClearTrail Mini is present, independently of whatever Bluetooth connection a listener might also choose for everyday playback.
  - The catalogue lists built-in Wi-Fi as false for ClearTrail Mini.
- `A08:687:889` **unknown** ✓span ✓label []: An authorized India service centre guarantees repair of ClearTrail Mini within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
  - The catalogue has no repair turnaround or service guarantee.
- `A08:890:1083` **supported** ✓span ✓label ['cleartrail.mini.stereo_pairing_scope']: The manufacturer permits stereo pairing only between two units of the exact ClearTrail Mini model, rather than treating every speaker sharing the same brand name as a compatible stereo partner.
  - Stereo pairing is same-model only, and cross-model pairing is unsupported.
- `A08:1084:1282` **unknown** ✓span ✓label []: The plastic used in the enclosure of ClearTrail Mini contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
  - The catalogue has no recycled-material information.
- `A08:1479:1676` **unknown** ✓span ✓label ['cleartrail.mini.bluetooth_version']: ClearTrail Mini accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
  - The catalogue gives only the Bluetooth version and says nothing about multipoint connections.
- `A08:1677:1855` **supported** ✓span ✓label ['cleartrail.mini.usb_audio', 'cleartrail.mini.charging_port']: For wired digital audio specifically, the USB-C connector on ClearTrail Mini does not provide an audio-input path, regardless of the fact that the connector also serves charging.
  - USB audio is false for the USB-C port, and that port is the charging port.
- `A08:1857:2036` **contradicted** ✓span ✓label ['cleartrail.mini.warranty_invoice_required', 'cleartrail.mini.warranty_india']: An original invoice is unnecessary when claiming the standard India manufacturer warranty for ClearTrail Mini, provided the buyer says the purchase came from an authorized seller.
  - The India standard warranty requires the original invoice.
- `A08:2037:2200` **supported** ✓span ✓label ['cleartrail.mini.price_2025']: Looking back specifically at the 2025 India catalogue rather than the current offer, the listed tax-inclusive price of ClearTrail Mini was INR 999 before shipping.
  - The 2025 India list price is INR 999, tax included and shipping excluded.
- `A08:2201:2395` **unknown** ✓span ✓label []: The normal manufacturing origin of ClearTrail Mini is India, even when the unit is purchased through an authorized seller rather than ordered directly from the manufacturer's own retail channel.
  - The catalogue has no manufacturing-origin information.

### A09: ok
turns=2 latency=10365ms claims=9 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A09.json`

- `A09:324:491` **supported** ✓span ✓label ['cloudnote.studio.immersion_allowed', 'cloudnote.studio.immersion_depth', 'cloudnote.studio.immersion_duration']: With all port covers closed, the laboratory immersion allowance for CloudNote Studio is limited to fresh water at no more than one metre for no more than half an hour.
  - The catalogue allows fresh-water immersion with port covers closed, with a maximum of 1 metre and 30 minutes (half an hour).
- `A09:492:655` **contradicted** ✓span ✓label ['cloudnote.studio.price_2026', 'cloudnote.air.price_2026']: For a current India catalogue comparison before shipping, CloudNote Studio is INR 1,500 less expensive than CloudNote Air, with tax included in both listed prices.
  - Studio is INR 2,999 and Air is INR 1,499 in 2026, so Studio costs INR 1,500 more, not less.
- `A09:657:844` **unknown** ✓span ✓label ['cloudnote.studio.bluetooth_version']: CloudNote Studio supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
  - The catalogue lists only Bluetooth version 5.4 and has no codec information, so AAC support is not established.
- `A09:845:1048` **unknown** ✓span ✓label []: An authorized India service centre guarantees repair of CloudNote Studio within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
  - The catalogue has no repair turnaround or service-guarantee facts.
- `A09:1245:1430` **supported** ✓span ✓label ['cloudnote.studio.battery_50_percent']: With a new battery, EQ disabled and volume held at fifty percent in the laboratory, CloudNote Studio has a stated playback duration of 1080 minutes under those specific test conditions.
  - 18 hours equals 1080 minutes under the matching test conditions.
- `A09:1431:1614` **contradicted** ✓span ✓label ['cloudnote.studio.stereo_pairing_scope', 'cloudnote.air.stereo_pairing_scope']: The manufacturer supports a stereo pair made from one CloudNote Studio and one CloudNote Air, since being members of the same brand is sufficient for cross-model stereo compatibility.
  - Stereo pairing is same-model only, and cross-model pairing is unsupported.
- `A09:1615:1781` **supported** ✓span ✓label ['cloudnote.studio.price_2025']: Looking back specifically at the 2025 India catalogue rather than the current offer, the listed tax-inclusive price of CloudNote Studio was INR 2,799 before shipping.
  - The 2025 India list price is INR 2,799, tax included and shipping excluded.
- `A09:1783:1963` **contradicted** ✓span ✓label ['cloudnote.studio.warranty_invoice_required', 'cloudnote.studio.warranty_india']: An original invoice is unnecessary when claiming the standard India manufacturer warranty for CloudNote Studio, provided the buyer says the purchase came from an authorized seller.
  - The India standard warranty requires the original invoice.
- `A09:1964:2148` **unknown** ✓span ✓label []: An opened CloudNote Studio can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
  - The catalogue has no return-policy facts.

### A10: ok
turns=2 latency=9503ms claims=10 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A10.json`

- `A10:371:563` **unknown** ✓span ✓label []: The normal manufacturing origin of CloudNote Air is India, even when the unit is purchased through an authorized seller rather than ordered directly from the manufacturer's own retail channel.
  - The catalogue has no manufacturing-origin fact for CloudNote Air.
- `A10:564:733` **supported** ✓span ✓label ['cloudnote.air.price_2025', 'cloudnote.air.price_2026']: The move from the 2025 India catalogue to the 2026 catalogue raised the tax-inclusive list price of CloudNote Air by INR 300, with shipping excluded in both comparisons.
  - The price went from INR 1,199 in 2025 to INR 1,499 in 2026, an increase of INR 300. Both prices are tax-inclusive and exclude shipping.
- `A10:735:923` **supported** ✓span ✓label ['cloudnote.air.warranty_invoice_required', 'cloudnote.air.warranty_india']: Even when other warranty conditions are met for an authorized India purchase, the original purchase invoice is still required to claim the standard manufacturer warranty for CloudNote Air.
  - The India standard warranty requires the original invoice.
- `A10:924:1087` **supported** ✓span ✓label ['cloudnote.air.price_2025']: Looking back specifically at the 2025 India catalogue rather than the current offer, the listed tax-inclusive price of CloudNote Air was INR 1,199 before shipping.
  - The 2025 India list price is INR 1,199, tax included and shipping excluded.
- `A10:1088:1265` **contradicted** ✓span ✓label ['cloudnote.air.warranty_invoice_required', 'cloudnote.air.warranty_india']: An original invoice is unnecessary when claiming the standard India manufacturer warranty for CloudNote Air, provided the buyer says the purchase came from an authorized seller.
  - The catalogue says the original invoice is required for the India standard warranty.
- `A10:1462:1643` **unknown** ✓span ✓label []: The official India catalogue price of CloudNote Air will drop by INR 300 during January 2027, with that future reduction applying before shipping to purchases from the brand itself.
  - The catalogue has no information about a future price change in 2027.
- `A10:1644:1821` **contradicted** ✓span ✓label ['cloudnote.air.price_2025', 'cloudnote.air.price_2026']: In the 2025 India catalogue, before the current-year revision, CloudNote Air already carried the same tax-inclusive list price of INR 1,499, excluding shipping from that amount.
  - The 2025 price was INR 1,199. INR 1,499 is the 2026 price.
- `A10:1823:2004` **unknown** ✓span ✓label []: An opened CloudNote Air can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
  - The catalogue has no return-policy facts.
- `A10:2005:2200` **unknown** ✓span ✓label ['cloudnote.air.bluetooth_version']: CloudNote Air accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
  - The catalogue gives only the Bluetooth version (5.3) and has no multipoint connection fact.
- `A10:2201:2372` **contradicted** ✓span ✓label ['cloudnote.air.adapter_included']: The official India retail box for CloudNote Air includes a wall charging adapter, even though separate accessory lists may make the charging arrangement look less obvious.
  - The official India retail box does not include an adapter. It includes only a USB-C cable.

### A11: ok
turns=2 latency=8880ms claims=10 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A11.json`

- `A11:306:483` **contradicted** ✓span ✓label ['stonewave.max.price_2025']: In the 2025 India catalogue, before the current-year revision, StoneWave Max already carried the same tax-inclusive list price of INR 3,499, excluding shipping from that amount.
  - The 2025 India list price of StoneWave Max was INR 3,299, not INR 3,499.
- `A11:484:653` **contradicted** ✓span ✓label ['stonewave.max.microphone']: The built-in microphone is not included on StoneWave Max, without needing an accessory to change the hardware specification being described for this exact speaker model.
  - The catalogue says StoneWave Max has a built-in microphone.
- `A11:655:855` **unknown** ✓span ✓label []: An authorized India service centre guarantees repair of StoneWave Max within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
  - The catalogue has no repair turnaround or repair guarantee information.
- `A11:856:1026` **unknown** ✓span ✓label ['stonewave.max.price_2026']: Orders for StoneWave Max receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
  - The catalogue only says list prices exclude shipping. It has no delivery or shipping policy.
- `A11:1027:1172` **supported** ✓span ✓label ['stonewave.max.price_2026']: For an India purchase at the official catalogue list price on 1 October 2026, StoneWave Max costs INR 3,499 including tax but excluding shipping.
  - The 2026 India list price is INR 3,499, tax included and shipping excluded.
- `A11:1369:1532` **supported** ✓span ✓label ['stonewave.max.price_2025']: Looking back specifically at the 2025 India catalogue rather than the current offer, the listed tax-inclusive price of StoneWave Max was INR 3,299 before shipping.
  - The 2025 India list price is INR 3,299, tax included and shipping excluded.
- `A11:1533:1697` **supported** ✓span ✓label ['stonewave.max.immersion_allowed', 'stonewave.max.immersion_depth', 'stonewave.max.immersion_duration']: With all port covers closed, the laboratory immersion allowance for StoneWave Max is limited to fresh water at no more than one metre for no more than half an hour.
  - The catalogue gives a maximum of 1 metre and 30 minutes in fresh water with port covers closed.
- `A11:1699:1895` **unknown** ✓span ✓label []: The plastic used in the enclosure of StoneWave Max contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
  - The catalogue has no information on recycled material content.
- `A11:1896:2091` **unknown** ✓span ✓label ['stonewave.max.bluetooth_version']: StoneWave Max accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
  - The catalogue lists only the Bluetooth version, with nothing on multipoint connections.
- `A11:2092:2264` **supported** ✓span ✓label ['stonewave.max.microphone']: The built-in microphone is included on StoneWave Max, so microphone availability should be checked for this exact model instead of copied from another speaker in the range.
  - The catalogue confirms StoneWave Max has a built-in microphone.

### A12: ok
turns=2 latency=9600ms claims=9 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A12.json`

- `A12:335:515` **unknown** ✓span ✓label ['stonewave.go.price_2026']: The official India catalogue price of StoneWave Go will drop by INR 300 during January 2027, with that future reduction applying before shipping to purchases from the brand itself.
  - The catalogue only has 2025 and 2026 prices, so a future January 2027 reduction can't be established.
- `A12:516:674` **supported** ✓span ✓label ['stonewave.go.wifi', 'stonewave.go.bluetooth_version']: The built-in Wi-Fi capability of StoneWave Go is absent, which should be treated as a separate specification from its ability to receive audio over Bluetooth.
  - The catalogue lists no built-in Wi-Fi for the Go and gives it Bluetooth 5.2.
- `A12:676:871` **unknown** ✓span ✓label []: The plastic used in the enclosure of StoneWave Go contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
  - The catalogue has no recycled-material content facts.
- `A12:872:1032` **contradicted** ✓span ✓label ['stonewave.go.battery_50_percent']: At fifty percent volume with EQ off and a new battery in the laboratory, StoneWave Go is rated for 1020 minutes of playback before recharging becomes necessary.
  - The catalogue gives 16 hours (960 minutes) under these conditions, not 1020 minutes.
- `A12:1229:1378` **supported** ✓span ✓label ['stonewave.go.price_2026', 'stonewave.max.price_2026']: For the current India catalogue, StoneWave Go is listed at INR 1,500 less than StoneWave Max, comparing the two tax-inclusive prices before shipping.
  - The 2026 prices are 3499 for the Max and 1999 for the Go, a difference of 1500.
- `A12:1379:1559` **unknown** ✓span ✓label []: An opened StoneWave Go can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
  - The catalogue has no return or refund policy facts.
- `A12:1560:1741` **contradicted** ✓span ✓label ['stonewave.go.usb_audio', 'stonewave.go.charging_port']: For wired digital audio specifically, the USB-C connector on StoneWave Go does provide an audio-input path, so the connector can be treated accordingly when choosing a wired source.
  - The catalogue says the Go's USB-C port does not support wired digital audio.
- `A12:1743:1916` **contradicted** ✓span ✓label ['stonewave.go.weight', 'stonewave.max.weight']: When measuring just the speaker rather than the retail box and accessories, StoneWave Go weighs 900 grams, matching the carrying-weight figure associated with StoneWave Max.
  - The Go's speaker-only weight is 440 grams. Only the Max weighs 900 grams.
- `A12:1917:2113` **supported** ✓span ✓label ['stonewave.go.water_damage_covered', 'stonewave.go.warranty_india']: Whatever conclusions a buyer draws from the water-resistance rating, water damage remains excluded from the standard India manufacturer warranty covering StoneWave Go after an authorized purchase.
  - The India standard warranty does not cover water damage, and this is independent of the water resistance rating.

### A13: ok
turns=2 latency=8671ms claims=10 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A13.json`

- `A13:324:510` **unknown** ✓span ✓label ['stonewave.go.battery_50_percent']: In winter weather below freezing, StoneWave Go delivers its full 16-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
  - The 16-hour figure applies only to laboratory test conditions, and the catalogue has no data on sub-freezing temperatures.
- `A13:511:680` **unknown** ✓span ✓label []: Orders for StoneWave Go receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
  - The catalogue has no delivery or shipping policy rows.
- `A13:682:902` **contradicted** ✓span ✓label ['stonewave.go.water_damage_covered']: Water damage to StoneWave Go is included in the standard India manufacturer warranty after an authorized purchase, because water resistance should be understood as warranty coverage rather than just a product capability.
  - The catalogue says water damage is not covered by the India standard warranty, whatever the water resistance rating.
- `A13:903:1067` **contradicted** ✓span ✓label ['stonewave.go.microphone']: The built-in microphone is included on StoneWave Go, without needing an accessory to change the hardware specification being described for this exact speaker model.
  - The catalogue says StoneWave Go has no built-in microphone.
- `A13:1068:1270` **unknown** ✓span ✓label ['stonewave.go.warranty_india']: A retail purchase of StoneWave Go in Germany qualifies for the same 18-month manufacturer warranty described for authorized India purchases, without any different regional terms affecting that duration.
  - The 18-month warranty row covers India purchases only, and the catalogue has nothing on Germany.
- `A13:1467:1623` **contradicted** ✓span ✓label ['stonewave.go.wifi']: The built-in Wi-Fi capability of StoneWave Go is present, independently of whatever Bluetooth connection a listener might also choose for everyday playback.
  - The catalogue says StoneWave Go has no built-in Wi-Fi.
- `A13:1624:1804` **supported** ✓span ✓label ['stonewave.go.battery_50_percent']: With a new battery, EQ disabled and volume held at fifty percent in the laboratory, StoneWave Go has a stated playback duration of 960 minutes under those specific test conditions.
  - 16 hours equals 960 minutes under the same new-battery, 50 percent volume, EQ-off laboratory conditions.
- `A13:1806:1950` **supported** ✓span ✓label ['stonewave.go.price_2026']: For an India purchase at the official catalogue list price on 1 October 2026, StoneWave Go costs INR 1,999 including tax but excluding shipping.
  - The 2026 India list price is INR 1999, tax included and shipping excluded.
- `A13:1951:2126` **supported** ✓span ✓label ['stonewave.go.usb_audio', 'stonewave.go.charging_port']: For wired digital audio specifically, the USB-C connector on StoneWave Go does not provide an audio-input path, regardless of the fact that the connector also serves charging.
  - USB audio is false and the USB-C port is the charging port.
- `A13:2127:2307` **unknown** ✓span ✓label []: An opened StoneWave Go can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
  - The catalogue has no return or refund policy rows.

### A14: ok
turns=2 latency=11902ms claims=9 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A14.json`

- `A14:371:557` **unknown** ✓span ✓label ['cleartrail.plus.bluetooth_version']: ClearTrail Plus supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
  - The catalogue lists Bluetooth 5.3 but has no codec row, so AAC support is not established.
- `A14:558:756` **unknown** ✓span ✓label []: The plastic used in the enclosure of ClearTrail Plus contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
  - The catalogue has no recycled-material information.
- `A14:758:943` **contradicted** ✓span ✓label ['cleartrail.plus.immersion_depth', 'cleartrail.plus.immersion_duration']: With all port covers closed, ClearTrail Plus is permitted to remain immersed in fresh water at a depth of one metre for a full hour under the manufacturer's stated laboratory allowance.
  - The depth of 1 metre matches, but the maximum duration is 30 minutes, not a full hour.
- `A14:944:1127` **unknown** ✓span ✓label ['cleartrail.plus.price_2026']: The official India catalogue price of ClearTrail Plus will drop by INR 300 during January 2027, with that future reduction applying before shipping to purchases from the brand itself.
  - The catalogue only has 2025 and 2026 prices, so a future 2027 price change can't be verified.
- `A14:1324:1471` **supported** ✓span ✓label ['cleartrail.plus.price_2026']: For an India purchase at the official catalogue list price on 1 October 2026, ClearTrail Plus costs INR 2,499 including tax but excluding shipping.
  - The 2026 India list price is INR 2,499, tax included and shipping excluded.
- `A14:1472:1662` **supported** ✓span ✓label ['cleartrail.plus.warranty_invoice_required', 'cleartrail.plus.warranty_india']: Even when other warranty conditions are met for an authorized India purchase, the original purchase invoice is still required to claim the standard manufacturer warranty for ClearTrail Plus.
  - The India standard warranty requires the original invoice.
- `A14:1663:1837` **supported** ✓span ✓label ['cleartrail.plus.usb_audio', 'cleartrail.plus.charging_port']: For wired digital audio specifically, the USB-C connector on ClearTrail Plus does provide an audio-input path, regardless of the fact that the connector also serves charging.
  - USB audio through the USB-C port is true, and USB-C is also the charging port.
- `A14:1839:2018` **contradicted** ✓span ✓label ['cleartrail.plus.warranty_invoice_required']: An original invoice is unnecessary when claiming the standard India manufacturer warranty for ClearTrail Plus, provided the buyer says the purchase came from an authorized seller.
  - The standard India warranty requires the original invoice.
- `A14:2019:2198` **contradicted** ✓span ✓label ['cleartrail.plus.battery_100_percent', 'cleartrail.plus.battery_50_percent']: The stated laboratory playback time for ClearTrail Plus, using a new battery with EQ off at one hundred percent volume, remains 20 hours without any reduction for louder playback.
  - At 100 percent volume the laboratory playback time is 10 hours. The 20 hours figure applies at 50 percent volume.

### A15: ok
turns=2 latency=11793ms claims=10 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A15.json`

- `A15:306:495` **unknown** ✓span ✓label ['cleartrail.mini.battery_50_percent']: In winter weather below freezing, ClearTrail Mini delivers its full 12-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
  - The 12-hour figure applies to a new battery at 50 percent volume with EQ off in a laboratory test. The catalogue has no row on how temperature affects runtime.
- `A15:496:698` **unknown** ✓span ✓label []: An authorized India service centre guarantees repair of ClearTrail Mini within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
  - The catalogue has no repair turnaround or repair guarantee row.
- `A15:700:889` **contradicted** ✓span ✓label ['cleartrail.mini.immersion_allowed']: With all port covers closed, ClearTrail Mini is explicitly permitted to be immersed in fresh water, rather than being restricted to the non-immersion use implied by a more cautious reading.
  - Immersion in fresh water with all port covers closed is not allowed for the Mini (false).
- `A15:890:1074` **contradicted** ✓span ✓label ['cleartrail.mini.stereo_pairing_scope', 'cleartrail.plus.stereo_pairing_scope']: The manufacturer supports a stereo pair made from one ClearTrail Mini and one ClearTrail Plus, since being members of the same brand is sufficient for cross-model stereo compatibility.
  - Stereo pairing works only between two units of the same model. Cross-model pairing is unsupported.
- `A15:1075:1236` **supported** ✓span ✓label ['cleartrail.mini.wifi', 'cleartrail.mini.bluetooth_version']: The built-in Wi-Fi capability of ClearTrail Mini is absent, which should be treated as a separate specification from its ability to receive audio over Bluetooth.
  - The Mini has no built-in Wi-Fi, and it lists Bluetooth 5.3 as a separate specification.
- `A15:1433:1627` **unknown** ✓span ✓label []: The normal manufacturing origin of ClearTrail Mini is India, even when the unit is purchased through an authorized seller rather than ordered directly from the manufacturer's own retail channel.
  - The catalogue has no manufacturing origin row.
- `A15:1628:1825` **unknown** ✓span ✓label ['cleartrail.mini.bluetooth_version']: ClearTrail Mini accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
  - The catalogue gives only the Bluetooth version and has no multipoint connection information.
- `A15:1827:2026` **supported** ✓span ✓label ['cleartrail.mini.water_damage_covered']: Whatever conclusions a buyer draws from the water-resistance rating, water damage remains excluded from the standard India manufacturer warranty covering ClearTrail Mini after an authorized purchase.
  - The India standard warranty does not cover water damage, independent of the water resistance rating.
- `A15:2027:2174` **supported** ✓span ✓label ['cleartrail.mini.price_2026']: For an India purchase at the official catalogue list price on 1 October 2026, ClearTrail Mini costs INR 1,299 including tax but excluding shipping.
  - The 2026 India list price is INR 1299, tax included and shipping excluded.
- `A15:2175:2354` **contradicted** ✓span ✓label ['cleartrail.mini.warranty_invoice_required', 'cleartrail.mini.warranty_india']: An original invoice is unnecessary when claiming the standard India manufacturer warranty for ClearTrail Mini, provided the buyer says the purchase came from an authorized seller.
  - The India standard warranty requires an original invoice.

### A16: ok
turns=2 latency=9508ms claims=9 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A16.json`

- `A16:306:454` **supported** ✓span ✓label ['cloudnote.studio.price_2026']: For an India purchase at the official catalogue list price on 1 October 2026, CloudNote Studio costs INR 2,999 including tax but excluding shipping.
  - The 2026 India list price for Studio is INR 2,999, tax included and shipping excluded.
- `A16:455:618` **contradicted** ✓span ✓label ['cloudnote.studio.price_2026', 'cloudnote.air.price_2026']: For a current India catalogue comparison before shipping, CloudNote Studio is INR 1,500 less expensive than CloudNote Air, with tax included in both listed prices.
  - Studio is INR 2,999 and Air is INR 1,499, so Studio costs INR 1,500 more, not less.
- `A16:620:828` **unknown** ✓span ✓label []: The sustained amplifier output of CloudNote Studio is forty watts per channel during ordinary playback, which allows a direct loudness comparison with other speakers advertised using electrical power figures.
  - The catalogue has no amplifier power or loudness comparison facts.
- `A16:829:1001` **supported** ✓span ✓label ['cloudnote.studio.price_2025', 'cloudnote.studio.price_2026']: The move from the 2025 India catalogue to the 2026 catalogue raised the tax-inclusive list price of CloudNote Studio by INR 200, with shipping excluded in both comparisons.
  - The price went from INR 2,799 in 2025 to INR 2,999 in 2026, a rise of INR 200, under the same tax and shipping conditions.
- `A16:1198:1422` **contradicted** ✓span ✓label ['cloudnote.studio.water_damage_covered']: Water damage to CloudNote Studio is included in the standard India manufacturer warranty after an authorized purchase, because water resistance should be understood as warranty coverage rather than just a product capability.
  - The standard India warranty does not cover water damage, and this is independent of the water resistance rating.
- `A16:1423:1613` **unknown** ✓span ✓label ['cloudnote.studio.battery_50_percent']: In winter weather below freezing, CloudNote Studio delivers its full 18-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
  - The 18-hour figure is a laboratory result at 50 percent volume, and the catalogue has no facts on sub-freezing temperature.
- `A16:1614:1797` **supported** ✓span ✓label ['cloudnote.studio.weight']: Considering the speaker alone and leaving retail packaging and accessories out of the measurement, CloudNote Studio has a stated mass of 1.1 kilograms for carrying-weight comparisons.
  - The speaker-only weight is 1,100 grams, which is 1.1 kg.
- `A16:1799:1976` **contradicted** ✓span ✓label ['cloudnote.studio.weight', 'cloudnote.air.weight']: When measuring just the speaker rather than the retail box and accessories, CloudNote Studio weighs 350 grams, matching the carrying-weight figure associated with CloudNote Air.
  - Studio weighs 1,100 grams. Only Air weighs 350 grams.
- `A16:1977:2138` **supported** ✓span ✓label ['cloudnote.studio.adapter_included', 'cloudnote.studio.charging_port']: The official India retail box for CloudNote Studio contains a wall charging adapter, so the box contents should not be inferred just from the charging-port type.
  - The official India retail box for Studio includes an adapter, and the charging port is listed separately as USB-C.

### A17: ok
turns=2 latency=11348ms claims=11 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A17.json`

- `A17:335:506` **contradicted** ✓span ✓label ['cloudnote.air.adapter_included']: The official India retail box for CloudNote Air includes a wall charging adapter, even though separate accessory lists may make the charging arrangement look less obvious.
  - The catalogue says the official India retail box for CloudNote Air does not include an adapter.
- `A17:507:694` **unknown** ✓span ✓label ['cloudnote.air.battery_50_percent']: In winter weather below freezing, CloudNote Air delivers its full 10-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
  - The 10-hour figure is a laboratory result with no temperature condition, so the catalogue says nothing about runtime below freezing.
- `A17:696:879` **contradicted** ✓span ✓label ['cloudnote.air.stereo_pairing_scope', 'cloudnote.studio.stereo_pairing_scope']: The manufacturer supports a stereo pair made from one CloudNote Air and one CloudNote Studio, since being members of the same brand is sufficient for cross-model stereo compatibility.
  - Both models are listed as same-model stereo pairing only, and cross-model pairing is unsupported.
- `A17:880:1054` **supported** ✓span ✓label ['cloudnote.air.battery_50_percent', 'cloudnote.air.battery_100_percent']: Turning CloudNote Air up from fifty to one hundred percent volume in the stated new-battery, EQ-off laboratory tests halves its listed playback time from 10 hours to 5 hours.
  - The listed laboratory playback times are 10 hours at 50 percent volume and 5 hours at 100 percent, which is a halving.
- `A17:1055:1247` **unknown** ✓span ✓label []: The normal manufacturing origin of CloudNote Air is India, even when the unit is purchased through an authorized seller rather than ordered directly from the manufacturer's own retail channel.
  - The catalogue has no manufacturing origin facts.
- `A17:1444:1607` **contradicted** ✓span ✓label ['cloudnote.air.price_2026', 'cloudnote.studio.price_2026']: For a current India catalogue comparison before shipping, CloudNote Air is INR 1,500 more expensive than CloudNote Studio, with tax included in both listed prices.
  - Air is INR 1,499 and Studio is INR 2,999, so Air is INR 1,500 cheaper, not more expensive.
- `A17:1608:1785` **unknown** ✓span ✓label []: Using a twenty-watt wall adapter, a fully discharged CloudNote Air reaches a complete charge in ninety minutes, so a short charging stop is enough to restore the entire battery.
  - The catalogue has no charging time or charging power facts.
- `A17:1787:1932` **supported** ✓span ✓label ['cloudnote.air.price_2026']: For an India purchase at the official catalogue list price on 1 October 2026, CloudNote Air costs INR 1,499 including tax but excluding shipping.
  - The 2026 India list price is INR 1,499 with tax included and shipping excluded.
- `A17:1933:2114` **supported** ✓span ✓label ['cloudnote.air.weight']: Considering the speaker alone and leaving retail packaging and accessories out of the measurement, CloudNote Air has a stated mass of 0.35 kilograms for carrying-weight comparisons.
  - The speaker-only weight is 350 grams, which is 0.35 kg.
- `A17:2115:2336` **contradicted** ✓span ✓label ['cloudnote.air.water_damage_covered', 'cloudnote.air.warranty_india']: Water damage to CloudNote Air is included in the standard India manufacturer warranty after an authorized purchase, because water resistance should be understood as warranty coverage rather than just a product capability.
  - The standard India warranty does not cover water damage, and this is independent of the water resistance rating.
- `A17:2338:2519` **unknown** ✓span ✓label []: The official India catalogue price of CloudNote Air will drop by INR 300 during January 2027, with that future reduction applying before shipping to purchases from the brand itself.
  - The catalogue has no facts about future 2027 prices.

### A18: ok
turns=2 latency=8769ms claims=8 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A18.json`

- `A18:324:490` **supported** ✓span ✓label ['stonewave.max.adapter_included', 'stonewave.max.charging_port']: The official India retail box for StoneWave Max does not contain a wall charging adapter, so the box contents should not be inferred just from the charging-port type.
  - The catalogue says the official India retail box for the Max has no adapter, and the charging port is USB-C.
- `A18:491:661` **unknown** ✓span ✓label []: Orders for StoneWave Max receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
  - The catalogue has no delivery or shipping-charge policy. It only says list prices exclude shipping.
- `A18:663:840` **contradicted** ✓span ✓label ['stonewave.max.price_2025', 'stonewave.max.price_2026']: In the 2025 India catalogue, before the current-year revision, StoneWave Max already carried the same tax-inclusive list price of INR 3,499, excluding shipping from that amount.
  - The 2025 India list price was INR 3,299. INR 3,499 is the 2026 price.
- `A18:943:1138` **unknown** ✓span ✓label ['stonewave.max.bluetooth_version']: StoneWave Max accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
  - The catalogue gives the Bluetooth version but nothing about multipoint connections.
- `A18:1335:1518` **contradicted** ✓span ✓label ['stonewave.max.immersion_allowed', 'stonewave.max.immersion_depth', 'stonewave.max.immersion_duration']: With all port covers closed, StoneWave Max is permitted to remain immersed in fresh water at a depth of one metre for a full hour under the manufacturer's stated laboratory allowance.
  - The maximum laboratory duration at 1 metre is 30 minutes, not a full hour.
- `A18:1519:1691` **supported** ✓span ✓label ['stonewave.max.usb_audio', 'stonewave.max.charging_port']: For wired digital audio specifically, the USB-C connector on StoneWave Max does provide an audio-input path, regardless of the fact that the connector also serves charging.
  - USB audio is true for the Max, and the USB-C port is also its charging port.
- `A18:1693:1874` **unknown** ✓span ✓label ['stonewave.max.price_2026']: The official India catalogue price of StoneWave Max will drop by INR 300 during January 2027, with that future reduction applying before shipping to purchases from the brand itself.
  - The catalogue has no 2027 price or any future price-change promise.
- `A18:1875:2044` **contradicted** ✓span ✓label ['stonewave.max.microphone']: The built-in microphone is not included on StoneWave Max, without needing an accessory to change the hardware specification being described for this exact speaker model.
  - The catalogue says the Max has a built-in microphone.

### A19: ok
turns=2 latency=10014ms claims=10 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A19.json`

- `A19:371:555` **contradicted** ✓span ✓label ['stonewave.max.warranty_india']: For an authorized India purchase with the original invoice and a manufacturing defect, StoneWave Max receives a standard manufacturer warranty lasting 24 months from the purchase date.
  - The catalogue gives an 18-month India warranty for StoneWave Max under these conditions, not 24 months.
- `A19:556:729` **contradicted** ✓span ✓label ['stonewave.max.weight', 'stonewave.go.weight']: When measuring just the speaker rather than the retail box and accessories, StoneWave Max weighs 440 grams, matching the carrying-weight figure associated with StoneWave Go.
  - The speaker-only weight of StoneWave Max is 900 g. 440 g is the weight of the Go.
- `A19:731:902` **contradicted** ✓span ✓label ['stonewave.max.adapter_included']: The official India retail box for StoneWave Max includes a wall charging adapter, even though separate accessory lists may make the charging arrangement look less obvious.
  - The official India retail box for the Max does not include an adapter.
- `A19:903:1067` **supported** ✓span ✓label ['stonewave.max.immersion_allowed', 'stonewave.max.immersion_depth', 'stonewave.max.immersion_duration']: With all port covers closed, the laboratory immersion allowance for StoneWave Max is limited to fresh water at no more than one metre for no more than half an hour.
  - Immersion is allowed in fresh water with port covers closed, up to 1 metre and 30 minutes.
- `A19:1068:1268` **unknown** ✓span ✓label []: No version of StoneWave Max has ever been offered in blue, including previous-year retail stock and editions supplied only through independent authorized sellers rather than the official online store.
  - The catalogue has no colour or edition history for this model.
- `A19:1465:1654` **unknown** ✓span ✓label []: After an announced firmware update next quarter, StoneWave Max will gain a built-in voice assistant that can answer spoken questions without requiring a paired phone to process the request.
  - This is a future promise about firmware and a voice assistant, and the catalogue has no information on either.
- `A19:1655:1832` **contradicted** ✓span ✓label ['stonewave.max.warranty_invoice_required']: An original invoice is unnecessary when claiming the standard India manufacturer warranty for StoneWave Max, provided the buyer says the purchase came from an authorized seller.
  - The catalogue says the original invoice is required for the India standard warranty.
- `A19:1834:2008` **supported** ✓span ✓label ['stonewave.max.warranty_india']: For manufacturing defects following an authorized India purchase with the original invoice, the standard manufacturer warranty on StoneWave Max lasts 1.5 years from purchase.
  - 18 months equals 1.5 years under the stated conditions.
- `A19:2009:2201` **unknown** ✓span ✓label ['stonewave.max.bluetooth_version']: The Bluetooth connection on StoneWave Max maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
  - The catalogue lists only the Bluetooth version and has no range or playback-continuity data.
- `A19:2202:2372` **unknown** ✓span ✓label ['stonewave.max.price_2026']: Orders for StoneWave Max receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
  - The catalogue price excludes shipping and has no delivery policy, so free delivery is not established.

### A20: ok
turns=2 latency=8403ms claims=8 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A20.json`

- `A20:306:485` **contradicted** ✓span ✓label ['stonewave.go.stereo_pairing_scope', 'stonewave.max.stereo_pairing_scope']: The manufacturer supports a stereo pair made from one StoneWave Go and one StoneWave Max, since being members of the same brand is sufficient for cross-model stereo compatibility.
  - Both models are listed as same-model-only, and cross-model stereo pairing is unsupported.
- `A20:486:662` **contradicted** ✓span ✓label ['stonewave.go.price_2025', 'stonewave.go.price_2026']: In the 2025 India catalogue, before the current-year revision, StoneWave Go already carried the same tax-inclusive list price of INR 1,999, excluding shipping from that amount.
  - The 2025 India list price was INR 1,799, not INR 1,999.
- `A20:664:855` **unknown** ✓span ✓label []: The normal manufacturing origin of StoneWave Go is India, even when the unit is purchased through an authorized seller rather than ordered directly from the manufacturer's own retail channel.
  - The catalogue has no manufacturing origin information.
- `A20:856:1046` **supported** ✓span ✓label ['stonewave.go.stereo_pairing_scope']: The manufacturer permits stereo pairing only between two units of the exact StoneWave Go model, rather than treating every speaker sharing the same brand name as a compatible stereo partner.
  - The Go's stereo pairing scope is same-model only, with cross-model pairing unsupported.
- `A20:1243:1434` **unknown** ✓span ✓label ['stonewave.go.bluetooth_version']: The Bluetooth connection on StoneWave Go maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
  - The catalogue gives only the Bluetooth version and has no range or playback continuity information.
- `A20:1435:1607` **supported** ✓span ✓label ['stonewave.go.water_rating', 'stonewave.go.immersion_allowed']: Despite the declared IPX5 water-resistance rating, the manufacturer does not permit fresh-water immersion of StoneWave Go, even with all of the port covers properly closed.
  - The Go is declared IPX5, and immersion is not allowed in fresh water with all port covers closed.
- `A20:1608:1752` **supported** ✓span ✓label ['stonewave.go.price_2026']: For an India purchase at the official catalogue list price on 1 October 2026, StoneWave Go costs INR 1,999 including tax but excluding shipping.
  - The 2026 India list price is INR 1,999, tax included and shipping excluded.
- `A20:1754:1949` **unknown** ✓span ✓label []: The plastic used in the enclosure of StoneWave Go contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
  - The catalogue has no recycled material information.

### A21: ok
turns=2 latency=9031ms claims=8 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A21.json`

- `A21:335:558` **contradicted** ✓span ✓label ['cleartrail.plus.water_damage_covered']: Water damage to ClearTrail Plus is included in the standard India manufacturer warranty after an authorized purchase, because water resistance should be understood as warranty coverage rather than just a product capability.
  - The catalogue says water damage is not covered under the India standard warranty, independent of the water resistance rating.
- `A21:559:722` **contradicted** ✓span ✓label ['cleartrail.plus.battery_50_percent']: At fifty percent volume with EQ off and a new battery in the laboratory, ClearTrail Plus is rated for 1260 minutes of playback before recharging becomes necessary.
  - The catalogue gives 20 hours (1200 minutes) under these conditions, not 1260 minutes.
- `A21:724:892` **supported** ✓span ✓label ['cleartrail.plus.adapter_included', 'cleartrail.plus.charging_port']: The official India retail box for ClearTrail Plus does not contain a wall charging adapter, so the box contents should not be inferred just from the charging-port type.
  - The catalogue shows adapter_included is false for the official India retail box, and the charging port is listed separately as USB-C.
- `A21:893:1087` **unknown** ✓span ✓label []: The normal manufacturing origin of ClearTrail Plus is India, even when the unit is purchased through an authorized seller rather than ordered directly from the manufacturer's own retail channel.
  - The catalogue has no manufacturing-origin fact.
- `A21:1284:1478` **unknown** ✓span ✓label ['cleartrail.plus.bluetooth_version']: The Bluetooth connection on ClearTrail Plus maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
  - The catalogue lists only the Bluetooth version and has no range or uninterrupted-playback fact.
- `A21:1479:1676` **unknown** ✓span ✓label []: ClearTrail Plus accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
  - The catalogue has no multipoint connection fact.
- `A21:1677:1848` **supported** ✓span ✓label ['cleartrail.plus.price_2025', 'cleartrail.plus.price_2026']: The move from the 2025 India catalogue to the 2026 catalogue raised the tax-inclusive list price of ClearTrail Plus by INR 300, with shipping excluded in both comparisons.
  - The price rose from INR 2199 to INR 2499, which is INR 300, on the same tax-inclusive, shipping-excluded basis.
- `A21:1850:2028` **contradicted** ✓span ✓label ['cleartrail.plus.weight', 'cleartrail.mini.weight']: When measuring just the speaker rather than the retail box and accessories, ClearTrail Plus weighs 320 grams, matching the carrying-weight figure associated with ClearTrail Mini.
  - The Plus weighs 580 g speaker-only, not 320 g. Only the Mini weighs 320 g.

### A22: ok
turns=2 latency=10952ms claims=10 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A22.json`

- `A22:324:503` **contradicted** ✓span ✓label ['cleartrail.mini.battery_100_percent']: The stated laboratory playback time for ClearTrail Mini, using a new battery with EQ off at one hundred percent volume, remains 12 hours without any reduction for louder playback.
  - The catalogue lists 6 hours at 100 percent volume (new battery, EQ off, laboratory), not 12 hours.
- `A22:504:666` **contradicted** ✓span ✓label ['cleartrail.mini.battery_50_percent']: At fifty percent volume with EQ off and a new battery in the laboratory, ClearTrail Mini is rated for 780 minutes of playback before recharging becomes necessary.
  - 12 hours is 720 minutes, not 780.
- `A22:668:843` **supported** ✓span ✓label ['cleartrail.mini.water_rating', 'cleartrail.mini.immersion_allowed']: Despite the declared IPX4 water-resistance rating, the manufacturer does not permit fresh-water immersion of ClearTrail Mini, even with all of the port covers properly closed.
  - The Mini is rated IPX4, and immersion in fresh water with port covers closed is not allowed.
- `A22:844:1033` **unknown** ✓span ✓label ['cleartrail.mini.battery_50_percent']: In winter weather below freezing, ClearTrail Mini delivers its full 12-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
  - The 12-hour figure applies to laboratory conditions, and the catalogue has no data on battery runtime in freezing weather.
- `A22:1034:1201` **contradicted** ✓span ✓label ['cleartrail.mini.microphone']: The built-in microphone is included on ClearTrail Mini, without needing an accessory to change the hardware specification being described for this exact speaker model.
  - The catalogue says the Mini has no built-in microphone.
- `A22:1398:1552` **supported** ✓span ✓label ['cleartrail.mini.price_2026', 'cleartrail.plus.price_2026']: For the current India catalogue, ClearTrail Mini is listed at INR 1,200 less than ClearTrail Plus, comparing the two tax-inclusive prices before shipping.
  - The 2026 India prices are 2,499 for the Plus and 1,299 for the Mini, a difference of 1,200.
- `A22:1553:1704` **contradicted** ✓span ✓label ['cleartrail.mini.price_2026', 'cleartrail.mini.price_2025']: For an India purchase at the official catalogue list price on 1 October 2026, ClearTrail Mini still costs INR 999 including tax but excluding shipping.
  - The 2026 India list price is INR 1,299. INR 999 was the 2025 price.
- `A22:1706:1892` **unknown** ✓span ✓label ['cleartrail.mini.bluetooth_version']: ClearTrail Mini supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
  - The catalogue gives only Bluetooth 5.3 and has no codec information, so AAC support is not established.
- `A22:1893:2087` **unknown** ✓span ✓label ['cleartrail.mini.bluetooth_version']: The Bluetooth connection on ClearTrail Mini maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
  - The catalogue has no Bluetooth range or connection-stability data.
- `A22:2088:2271` **unknown** ✓span ✓label ['cleartrail.mini.warranty_india']: An opened ClearTrail Mini can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
  - The catalogue has no return or refund policy. It covers only the 12-month warranty for manufacturing defects.

### A23: ok
turns=2 latency=9133ms claims=8 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A23.json`

- `A23:371:548` **contradicted** ✓span ✓label ['cloudnote.studio.weight', 'cloudnote.air.weight']: When measuring just the speaker rather than the retail box and accessories, CloudNote Studio weighs 350 grams, matching the carrying-weight figure associated with CloudNote Air.
  - The catalogue gives the speaker-only weight of CloudNote Studio as 1100 grams, not 350. 350 grams is the weight of the Air.
- `A23:549:744` **unknown** ✓span ✓label ['cloudnote.studio.bluetooth_version']: The Bluetooth connection on CloudNote Studio maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
  - The catalogue lists only the Bluetooth version. It has no range or playback-continuity facts.
- `A23:746:907` **supported** ✓span ✓label ['cloudnote.studio.adapter_included', 'cloudnote.studio.charging_port']: The official India retail box for CloudNote Studio contains a wall charging adapter, so the box contents should not be inferred just from the charging-port type.
  - The catalogue confirms the adapter is in the official India retail box of the Studio. The charging port (USB-C) is a separate fact.
- `A23:908:1098` **unknown** ✓span ✓label ['cloudnote.studio.battery_50_percent']: In winter weather below freezing, CloudNote Studio delivers its full 18-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
  - The 18-hour figure is a laboratory result at 50 percent volume. The catalogue has no facts about sub-freezing temperatures.
- `A23:1295:1477` **contradicted** ✓span ✓label ['cloudnote.studio.adapter_included']: The official India retail box for CloudNote Studio does not include a wall charging adapter, even though separate accessory lists may make the charging arrangement look less obvious.
  - The catalogue says the official India retail box of the Studio includes an adapter.
- `A23:1478:1662` **unknown** ✓span ✓label []: An opened CloudNote Studio can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
  - The catalogue has no return or refund policy.
- `A23:1663:1854` **supported** ✓span ✓label ['cloudnote.studio.warranty_invoice_required', 'cloudnote.studio.warranty_india']: Even when other warranty conditions are met for an authorized India purchase, the original purchase invoice is still required to claim the standard manufacturer warranty for CloudNote Studio.
  - The catalogue says the India standard warranty requires the original invoice.
- `A23:1856:2056` **supported** ✓span ✓label ['cloudnote.studio.water_damage_covered']: Whatever conclusions a buyer draws from the water-resistance rating, water damage remains excluded from the standard India manufacturer warranty covering CloudNote Studio after an authorized purchase.
  - The catalogue says water damage is not covered by the India standard warranty, independent of the water-resistance rating.

### A24: ok
turns=2 latency=10008ms claims=10 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A24.json`

- `A24:306:498` **unknown** ✓span ✓label ['cloudnote.air.bluetooth_version']: The Bluetooth connection on CloudNote Air maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
  - The catalogue gives only the Bluetooth version. It has no range or uninterrupted-playback figures.
- `A24:499:683` **contradicted** ✓span ✓label ['cloudnote.air.warranty_india']: For an authorized India purchase with the original invoice and a manufacturing defect, CloudNote Air receives a standard manufacturer warranty lasting 30 months from the purchase date.
  - The India warranty for these conditions is 24 months, not 30.
- `A24:685:890` **unknown** ✓span ✓label ['cloudnote.air.battery_50_percent']: Compared with the unlisted RivalSound Trek, CloudNote Air provides two additional hours of playback under identical new-battery, fifty-percent-volume, EQ-off laboratory testing conditions for both devices.
  - The catalogue gives the Air's 10 hours but has no data for RivalSound Trek, so the comparison can't be checked.
- `A24:891:1091` **unknown** ✓span ✓label []: An authorized India service centre guarantees repair of CloudNote Air within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
  - The catalogue has no repair turnaround or service guarantee.
- `A24:1092:1287` **unknown** ✓span ✓label []: CloudNote Air accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
  - The catalogue has no multipoint connection information.
- `A24:1484:1675` **supported** ✓span ✓label ['cloudnote.air.stereo_pairing_scope']: The manufacturer permits stereo pairing only between two units of the exact CloudNote Air model, rather than treating every speaker sharing the same brand name as a compatible stereo partner.
  - Stereo pairing is limited to two units of this exact model, and cross-model pairing is unsupported.
- `A24:1676:1854` **contradicted** ✓span ✓label ['cloudnote.air.weight', 'cloudnote.studio.weight']: When measuring just the speaker rather than the retail box and accessories, CloudNote Air weighs 1100 grams, matching the carrying-weight figure associated with CloudNote Studio.
  - The Air's speaker-only weight is 350 g. 1100 g is the Studio's weight.
- `A24:1856:2025` **supported** ✓span ✓label ['cloudnote.air.price_2025', 'cloudnote.air.price_2026']: The move from the 2025 India catalogue to the 2026 catalogue raised the tax-inclusive list price of CloudNote Air by INR 300, with shipping excluded in both comparisons.
  - The price rose from INR 1199 to INR 1499, which is INR 300, on the same tax-inclusive, shipping-excluded basis.
- `A24:2026:2214` **supported** ✓span ✓label ['cloudnote.air.warranty_invoice_required', 'cloudnote.air.warranty_india']: Even when other warranty conditions are met for an authorized India purchase, the original purchase invoice is still required to claim the standard manufacturer warranty for CloudNote Air.
  - The catalogue says the original invoice is required for the India standard manufacturer warranty.
- `A24:2215:2381` **supported** ✓span ✓label ['cloudnote.air.adapter_included', 'cloudnote.air.charging_port']: The official India retail box for CloudNote Air does not contain a wall charging adapter, so the box contents should not be inferred just from the charging-port type.
  - The official India retail box has no adapter, and the USB-C port is a separate fact from the box contents.

### A25: ok
turns=2 latency=11012ms claims=9 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A25.json`

- `A25:306:459` **supported** ✓span ✓label ['cloudnote.air.price_2026', 'cloudnote.studio.price_2026']: For the current India catalogue, CloudNote Air is listed at INR 1,500 less than CloudNote Studio, comparing the two tax-inclusive prices before shipping.
  - The 2026 India tax-inclusive list prices are INR 1,499 for Air and INR 2,999 for Studio, so Air is INR 1,500 cheaper.
- `A25:460:630` **unknown** ✓span ✓label []: Orders for CloudNote Air receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
  - The catalogue lists prices as excluding shipping and has no delivery or shipping policy rows.
- `A25:632:824` **unknown** ✓span ✓label ['cloudnote.air.bluetooth_version']: The Bluetooth connection on CloudNote Air maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
  - The catalogue gives only the Bluetooth version (5.3) and has no range or playback-continuity facts.
- `A25:825:988` **contradicted** ✓span ✓label ['cloudnote.air.price_2026', 'cloudnote.studio.price_2026']: For a current India catalogue comparison before shipping, CloudNote Air is INR 1,500 more expensive than CloudNote Studio, with tax included in both listed prices.
  - Air (INR 1,499) is INR 1,500 cheaper than Studio (INR 2,999), not more expensive.
- `A25:1185:1366` **unknown** ✓span ✓label []: An opened CloudNote Air can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
  - The catalogue has no return or refund policy rows.
- `A25:1367:1526` **supported** ✓span ✓label ['cloudnote.air.wifi', 'cloudnote.air.bluetooth_version']: The built-in Wi-Fi capability of CloudNote Air is absent, which should be treated as a separate specification from its ability to receive audio over Bluetooth.
  - Built-in Wi-Fi is false for Air, and the catalogue lists Bluetooth 5.3 as a separate specification.
- `A25:1527:1672` **supported** ✓span ✓label ['cloudnote.air.price_2026']: For an India purchase at the official catalogue list price on 1 October 2026, CloudNote Air costs INR 1,499 including tax but excluding shipping.
  - The 2026 India list price is INR 1,499, tax included and shipping excluded.
- `A25:1674:1851` **contradicted** ✓span ✓label ['cloudnote.air.warranty_invoice_required', 'cloudnote.air.warranty_india']: An original invoice is unnecessary when claiming the standard India manufacturer warranty for CloudNote Air, provided the buyer says the purchase came from an authorized seller.
  - The India standard warranty requires the original invoice.
- `A25:1852:2023` **contradicted** ✓span ✓label ['cloudnote.air.adapter_included']: The official India retail box for CloudNote Air includes a wall charging adapter, even though separate accessory lists may make the charging arrangement look less obvious.
  - The adapter is not included in the official India retail box. Only a USB-C cable is listed.

### A26: ok
turns=2 latency=9644ms claims=10 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A26.json`

- `A26:335:556` **contradicted** ✓span ✓label ['stonewave.max.water_damage_covered']: Water damage to StoneWave Max is included in the standard India manufacturer warranty after an authorized purchase, because water resistance should be understood as warranty coverage rather than just a product capability.
  - The catalogue says water damage is not covered by the India standard warranty, whatever the water resistance rating.
- `A26:557:727` **unknown** ✓span ✓label []: Orders for StoneWave Max receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
  - The catalogue has no delivery or shipping-charge policy.
- `A26:729:925` **unknown** ✓span ✓label []: The plastic used in the enclosure of StoneWave Max contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
  - The catalogue has no recycled-material information.
- `A26:926:1107` **unknown** ✓span ✓label ['stonewave.max.price_2026']: The official India catalogue price of StoneWave Max will drop by INR 300 during January 2027, with that future reduction applying before shipping to purchases from the brand itself.
  - The catalogue only has 2025 and 2026 prices and makes no promise about a January 2027 price change.
- `A26:1108:1265` **contradicted** ✓span ✓label ['stonewave.max.wifi']: The built-in Wi-Fi capability of StoneWave Max is present, independently of whatever Bluetooth connection a listener might also choose for everyday playback.
  - The catalogue says StoneWave Max has no built-in Wi-Fi.
- `A26:1462:1650` **supported** ✓span ✓label ['stonewave.max.warranty_invoice_required', 'stonewave.max.warranty_india']: Even when other warranty conditions are met for an authorized India purchase, the original purchase invoice is still required to claim the standard manufacturer warranty for StoneWave Max.
  - The catalogue says the India standard warranty requires the original invoice.
- `A26:1651:1796` **supported** ✓span ✓label ['stonewave.max.price_2026']: For an India purchase at the official catalogue list price on 1 October 2026, StoneWave Max costs INR 3,499 including tax but excluding shipping.
  - The 2026 India list price is INR 3,499, tax included and shipping excluded.
- `A26:1798:1975` **contradicted** ✓span ✓label ['stonewave.max.warranty_invoice_required', 'stonewave.max.warranty_india']: An original invoice is unnecessary when claiming the standard India manufacturer warranty for StoneWave Max, provided the buyer says the purchase came from an authorized seller.
  - The catalogue says the original invoice is required for the India standard warranty.
- `A26:1976:2153` **unknown** ✓span ✓label []: Using a twenty-watt wall adapter, a fully discharged StoneWave Max reaches a complete charge in ninety minutes, so a short charging stop is enough to restore the entire battery.
  - The catalogue has no charging-time information, and the Max box includes no adapter.
- `A26:2154:2351` **supported** ✓span ✓label ['stonewave.max.water_damage_covered']: Whatever conclusions a buyer draws from the water-resistance rating, water damage remains excluded from the standard India manufacturer warranty covering StoneWave Max after an authorized purchase.
  - The catalogue says water damage is not covered under the India standard warranty, independent of the water resistance rating.

### A27: ok
turns=2 latency=9163ms claims=9 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A27.json`

- `A27:324:493` **unknown** ✓span ✓label []: Orders for StoneWave Go receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
  - The catalogue lists prices with shipping excluded and has no delivery or shipping-charge policy.
- `A27:494:688` **unknown** ✓span ✓label ['stonewave.go.bluetooth_version']: StoneWave Go accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
  - The catalogue gives only the Bluetooth version and says nothing about multipoint connections.
- `A27:690:873` **contradicted** ✓span ✓label ['stonewave.go.app_required_bluetooth']: Basic Bluetooth playback on StoneWave Go requires the manufacturer companion app to be installed first, rather than allowing a listener to pair a source and start playback without it.
  - Basic Bluetooth playback does not require the manufacturer app.
- `A27:874:1033` **contradicted** ✓span ✓label ['stonewave.go.price_2026', 'stonewave.max.price_2026']: For a current India catalogue comparison before shipping, StoneWave Go is INR 1,500 more expensive than StoneWave Max, with tax included in both listed prices.
  - Go is INR 1,999 and Max is INR 3,499, so Go is INR 1,500 cheaper, not more expensive.
- `A27:1230:1392` **supported** ✓span ✓label ['stonewave.go.price_2025']: Looking back specifically at the 2025 India catalogue rather than the current offer, the listed tax-inclusive price of StoneWave Go was INR 1,799 before shipping.
  - The 2025 India list price is INR 1,799, tax included and shipping excluded.
- `A27:1393:1579` **contradicted** ✓span ✓label ['stonewave.go.immersion_allowed']: With all port covers closed, StoneWave Go is explicitly permitted to be immersed in fresh water, rather than being restricted to the non-immersion use implied by a more cautious reading.
  - Immersion is not allowed for the Go in fresh water with all port covers closed.
- `A27:1580:1745` **supported** ✓span ✓label ['stonewave.go.adapter_included', 'stonewave.go.charging_port']: The official India retail box for StoneWave Go does not contain a wall charging adapter, so the box contents should not be inferred just from the charging-port type.
  - The official India retail box has no adapter, and the USB-C port is a separate fact from the box contents.
- `A27:1747:1938` **unknown** ✓span ✓label ['stonewave.go.bluetooth_version']: The Bluetooth connection on StoneWave Go maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
  - The catalogue has no Bluetooth range or playback-continuity information.
- `A27:1939:2088` **supported** ✓span ✓label ['stonewave.go.price_2026', 'stonewave.max.price_2026']: For the current India catalogue, StoneWave Go is listed at INR 1,500 less than StoneWave Max, comparing the two tax-inclusive prices before shipping.
  - Go at INR 1,999 is INR 1,500 less than Max at INR 3,499.

### A28: ok
turns=2 latency=12074ms claims=10 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A28.json`

- `A28:371:548` **supported** ✓span ✓label ['cleartrail.plus.battery_50_percent', 'cleartrail.plus.battery_100_percent']: Turning ClearTrail Plus up from fifty to one hundred percent volume in the stated new-battery, EQ-off laboratory tests halves its listed playback time from 20 hours to 10 hours.
  - The catalogue lists 20 hours at 50% volume and 10 hours at 100% volume under the same lab conditions, which is a halving.
- `A28:549:751` **unknown** ✓span ✓label []: No version of ClearTrail Plus has ever been offered in blue, including previous-year retail stock and editions supplied only through independent authorized sellers rather than the official online store.
  - The catalogue has no colour or edition information, and it cannot confirm a negative.
- `A28:753:942` **unknown** ✓span ✓label ['cleartrail.plus.battery_50_percent']: In winter weather below freezing, ClearTrail Plus delivers its full 20-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
  - The 20-hour figure is a lab-test value, and the catalogue has no row on sub-freezing temperature effects.
- `A28:943:1122` **contradicted** ✓span ✓label ['cleartrail.plus.battery_100_percent']: The stated laboratory playback time for ClearTrail Plus, using a new battery with EQ off at one hundred percent volume, remains 20 hours without any reduction for louder playback.
  - The catalogue gives 10 hours at 100% volume under these conditions, not 20.
- `A28:1123:1302` **unknown** ✓span ✓label []: Using a twenty-watt wall adapter, a fully discharged ClearTrail Plus reaches a complete charge in ninety minutes, so a short charging stop is enough to restore the entire battery.
  - The catalogue has no charging time or adapter wattage information.
- `A28:1499:1671` **unknown** ✓span ✓label ['cleartrail.plus.price_2026']: Orders for ClearTrail Plus receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
  - The price row only says shipping is excluded and has no delivery or shipping policy.
- `A28:1672:1819` **supported** ✓span ✓label ['cleartrail.plus.price_2026']: For an India purchase at the official catalogue list price on 1 October 2026, ClearTrail Plus costs INR 2,499 including tax but excluding shipping.
  - The 2026 India list price is INR 2,499, tax included and shipping excluded.
- `A28:1821:2006` **contradicted** ✓span ✓label ['cleartrail.plus.immersion_allowed', 'cleartrail.plus.immersion_depth', 'cleartrail.plus.immersion_duration']: With all port covers closed, ClearTrail Plus is permitted to remain immersed in fresh water at a depth of one metre for a full hour under the manufacturer's stated laboratory allowance.
  - The depth of 1 metre matches, but the maximum duration is 30 minutes, not a full hour.
- `A28:2007:2180` **contradicted** ✓span ✓label ['cleartrail.plus.adapter_included']: The official India retail box for ClearTrail Plus includes a wall charging adapter, even though separate accessory lists may make the charging arrangement look less obvious.
  - The catalogue says no adapter is included in the official India retail box.
- `A28:2181:2355` **supported** ✓span ✓label ['cleartrail.plus.microphone']: The built-in microphone is included on ClearTrail Plus, so microphone availability should be checked for this exact model instead of copied from another speaker in the range.
  - The catalogue confirms ClearTrail Plus has a built-in microphone.

### A29: ok
turns=2 latency=10629ms claims=9 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A29.json`

- `A29:306:453` **supported** ✓span ✓label ['cleartrail.mini.price_2026']: For an India purchase at the official catalogue list price on 1 October 2026, ClearTrail Mini costs INR 1,299 including tax but excluding shipping.
  - The 2026 India list price is INR 1,299, tax included and shipping excluded.
- `A29:454:615` **supported** ✓span ✓label ['cleartrail.mini.wifi', 'cleartrail.mini.bluetooth_version']: The built-in Wi-Fi capability of ClearTrail Mini is absent, which should be treated as a separate specification from its ability to receive audio over Bluetooth.
  - The catalogue says built-in Wi-Fi is false, and it lists Bluetooth 5.3 as a separate field.
- `A29:617:788` **supported** ✓span ✓label ['cleartrail.mini.price_2025', 'cleartrail.mini.price_2026']: The move from the 2025 India catalogue to the 2026 catalogue raised the tax-inclusive list price of ClearTrail Mini by INR 300, with shipping excluded in both comparisons.
  - The price went from INR 999 to INR 1,299, a rise of INR 300, under the same tax and shipping conditions.
- `A29:789:975` **unknown** ✓span ✓label ['cleartrail.mini.bluetooth_version']: ClearTrail Mini supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
  - The catalogue gives only the Bluetooth version (5.3) and has no codec information, so AAC support is not established.
- `A29:1172:1369` **unknown** ✓span ✓label []: ClearTrail Mini accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
  - The catalogue has no multipoint connection information.
- `A29:1370:1549` **contradicted** ✓span ✓label ['cleartrail.mini.warranty_invoice_required', 'cleartrail.mini.warranty_india']: An original invoice is unnecessary when claiming the standard India manufacturer warranty for ClearTrail Mini, provided the buyer says the purchase came from an authorized seller.
  - The India standard warranty requires the original invoice.
- `A29:1550:1701` **contradicted** ✓span ✓label ['cleartrail.mini.price_2026']: For an India purchase at the official catalogue list price on 1 October 2026, ClearTrail Mini still costs INR 999 including tax but excluding shipping.
  - The 2026 list price is INR 1,299, not INR 999.
- `A29:1703:1882` **contradicted** ✓span ✓label ['cleartrail.mini.price_2025']: In the 2025 India catalogue, before the current-year revision, ClearTrail Mini already carried the same tax-inclusive list price of INR 1,299, excluding shipping from that amount.
  - The 2025 India list price was INR 999, not INR 1,299.
- `A29:1883:2066` **supported** ✓span ✓label ['cleartrail.mini.battery_50_percent']: With a new battery, EQ disabled and volume held at fifty percent in the laboratory, ClearTrail Mini has a stated playback duration of 720 minutes under those specific test conditions.
  - 12 hours equals 720 minutes under the same test conditions (new battery, 50% volume, EQ off, laboratory).

### A30: ok
turns=2 latency=11779ms claims=11 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A30.json`

- `A30:306:509` **unknown** ✓span ✓label []: No version of CloudNote Studio has ever been offered in blue, including previous-year retail stock and editions supplied only through independent authorized sellers rather than the official online store.
  - The catalogue has no colour or edition availability facts.
- `A30:510:676` **supported** ✓span ✓label ['cloudnote.studio.price_2025']: Looking back specifically at the 2025 India catalogue rather than the current offer, the listed tax-inclusive price of CloudNote Studio was INR 2,799 before shipping.
  - The 2025 India list price is INR 2,799, tax included and shipping excluded.
- `A30:678:860` **contradicted** ✓span ✓label ['cloudnote.studio.adapter_included']: The official India retail box for CloudNote Studio does not include a wall charging adapter, even though separate accessory lists may make the charging arrangement look less obvious.
  - The official India retail box for Studio includes an adapter.
- `A30:861:1061` **supported** ✓span ✓label ['cloudnote.studio.water_damage_covered', 'cloudnote.studio.warranty_india']: Whatever conclusions a buyer draws from the water-resistance rating, water damage remains excluded from the standard India manufacturer warranty covering CloudNote Studio after an authorized purchase.
  - Water damage is not covered by the India standard warranty, independent of the water rating.
- `A30:1062:1242` **contradicted** ✓span ✓label ['cloudnote.studio.price_2025', 'cloudnote.studio.price_2026']: In the 2025 India catalogue, before the current-year revision, CloudNote Studio already carried the same tax-inclusive list price of INR 2,999, excluding shipping from that amount.
  - The 2025 price was INR 2,799. INR 2,999 is the 2026 price.
- `A30:1439:1663` **contradicted** ✓span ✓label ['cloudnote.studio.water_damage_covered']: Water damage to CloudNote Studio is included in the standard India manufacturer warranty after an authorized purchase, because water resistance should be understood as warranty coverage rather than just a product capability.
  - Water damage is not covered by the warranty, which is independent of the water resistance rating.
- `A30:1664:1844` **contradicted** ✓span ✓label ['cloudnote.studio.warranty_invoice_required', 'cloudnote.studio.warranty_india']: An original invoice is unnecessary when claiming the standard India manufacturer warranty for CloudNote Studio, provided the buyer says the purchase came from an authorized seller.
  - The warranty requires an original invoice.
- `A30:1846:2030` **unknown** ✓span ✓label []: The official India catalogue price of CloudNote Studio will drop by INR 300 during January 2027, with that future reduction applying before shipping to purchases from the brand itself.
  - The catalogue has no facts about future price changes.
- `A30:2031:2229` **unknown** ✓span ✓label []: CloudNote Studio accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
  - The catalogue has no multipoint connection facts.
- `A30:2230:2417` **unknown** ✓span ✓label ['cloudnote.studio.bluetooth_version']: CloudNote Studio supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
  - The catalogue lists only Bluetooth version 5.4 and has no codec facts.
- `A30:2419:2572` **supported** ✓span ✓label ['cloudnote.studio.price_2026', 'cloudnote.air.price_2026']: For the current India catalogue, CloudNote Studio is listed at INR 1,500 more than CloudNote Air, comparing the two tax-inclusive prices before shipping.
  - Studio is INR 2,999 and Air is INR 1,499, a difference of INR 1,500.

### A31: ok
turns=2 latency=10745ms claims=10 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A31.json`

- `A31:324:477` **supported** ✓span ✓label ['cloudnote.studio.price_2026', 'cloudnote.air.price_2026']: For the current India catalogue, CloudNote Studio is listed at INR 1,500 more than CloudNote Air, comparing the two tax-inclusive prices before shipping.
  - The 2026 India tax-inclusive prices are INR 2,999 for Studio and INR 1,499 for Air, a difference of INR 1,500.
- `A31:478:653` **supported** ✓span ✓label ['cloudnote.studio.usb_audio', 'cloudnote.studio.charging_port']: For wired digital audio specifically, the USB-C connector on CloudNote Studio does provide an audio-input path, regardless of the fact that the connector also serves charging.
  - Studio has USB audio over its USB-C port, and that port is also the charging port.
- `A31:655:854` **unknown** ✓span ✓label []: The plastic used in the enclosure of CloudNote Studio contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
  - The catalogue has no recycled-content information.
- `A31:855:1050` **unknown** ✓span ✓label []: The normal manufacturing origin of CloudNote Studio is India, even when the unit is purchased through an authorized seller rather than ordered directly from the manufacturer's own retail channel.
  - The catalogue has no manufacturing-origin information.
- `A31:1051:1238` **unknown** ✓span ✓label ['cloudnote.studio.bluetooth_version']: CloudNote Studio supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
  - The catalogue gives only Bluetooth version 5.4 and no codec information, and the version does not establish codec support.
- `A31:1435:1615` **contradicted** ✓span ✓label ['cloudnote.studio.warranty_invoice_required', 'cloudnote.studio.warranty_india']: An original invoice is unnecessary when claiming the standard India manufacturer warranty for CloudNote Studio, provided the buyer says the purchase came from an authorized seller.
  - The catalogue says the original invoice is required for the India standard warranty.
- `A31:1616:1793` **contradicted** ✓span ✓label ['cloudnote.studio.weight', 'cloudnote.air.weight']: When measuring just the speaker rather than the retail box and accessories, CloudNote Studio weighs 350 grams, matching the carrying-weight figure associated with CloudNote Air.
  - Studio's speaker-only weight is 1100 grams. The 350 grams belongs to Air.
- `A31:1795:1963` **contradicted** ✓span ✓label ['cloudnote.studio.microphone']: The built-in microphone is included on CloudNote Studio, without needing an accessory to change the hardware specification being described for this exact speaker model.
  - The catalogue lists Studio's built-in microphone as false.
- `A31:1964:2155` **supported** ✓span ✓label ['cloudnote.studio.warranty_invoice_required', 'cloudnote.studio.warranty_india']: Even when other warranty conditions are met for an authorized India purchase, the original purchase invoice is still required to claim the standard manufacturer warranty for CloudNote Studio.
  - The catalogue says the original invoice is required for the India standard warranty on an authorized-seller purchase.
- `A31:2156:2351` **unknown** ✓span ✓label ['cloudnote.studio.bluetooth_version']: The Bluetooth connection on CloudNote Studio maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
  - The catalogue has no Bluetooth range or playback-continuity information.

### A32: ok
turns=2 latency=10313ms claims=9 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A32.json`

- `A32:371:576` **unknown** ✓span ✓label []: The sustained amplifier output of CloudNote Air is forty watts per channel during ordinary playback, which allows a direct loudness comparison with other speakers advertised using electrical power figures.
  - The catalogue has no amplifier output power fact for CloudNote Air.
- `A32:577:749` **supported** ✓span ✓label ['cloudnote.air.microphone']: The built-in microphone is included on CloudNote Air, so microphone availability should be checked for this exact model instead of copied from another speaker in the range.
  - The catalogue confirms CloudNote Air has a built-in microphone.
- `A32:751:928` **contradicted** ✓span ✓label ['cloudnote.air.price_2025', 'cloudnote.air.price_2026']: In the 2025 India catalogue, before the current-year revision, CloudNote Air already carried the same tax-inclusive list price of INR 1,499, excluding shipping from that amount.
  - The 2025 India price was INR 1,199, not INR 1,499, which is the 2026 price.
- `A32:1031:1205` **supported** ✓span ✓label ['cloudnote.air.battery_50_percent', 'cloudnote.air.battery_100_percent']: Turning CloudNote Air up from fifty to one hundred percent volume in the stated new-battery, EQ-off laboratory tests halves its listed playback time from 10 hours to 5 hours.
  - The listed times are 10 hours at 50% volume and 5 hours at 100% volume under the same test conditions, so playback time halves.
- `A32:1402:1583` **supported** ✓span ✓label ['cloudnote.air.weight']: Considering the speaker alone and leaving retail packaging and accessories out of the measurement, CloudNote Air has a stated mass of 0.35 kilograms for carrying-weight comparisons.
  - 350 grams equals 0.35 kg for the speaker only.
- `A32:1584:1771` **contradicted** ✓span ✓label ['cloudnote.air.immersion_allowed']: With all port covers closed, CloudNote Air is explicitly permitted to be immersed in fresh water, rather than being restricted to the non-immersion use implied by a more cautious reading.
  - Immersion in fresh water with port covers closed is not allowed for CloudNote Air.
- `A32:1773:1960` **unknown** ✓span ✓label ['cloudnote.air.battery_50_percent']: In winter weather below freezing, CloudNote Air delivers its full 10-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
  - The 10-hour figure is a laboratory result, and the catalogue has no data on runtime in freezing temperatures.
- `A32:1961:2134` **supported** ✓span ✓label ['cloudnote.air.water_rating', 'cloudnote.air.immersion_allowed']: Despite the declared IPX4 water-resistance rating, the manufacturer does not permit fresh-water immersion of CloudNote Air, even with all of the port covers properly closed.
  - The rating is IPX4 and immersion in fresh water with port covers closed is not allowed.
- `A32:2135:2319` **contradicted** ✓span ✓label ['cloudnote.air.app_required_bluetooth']: Basic Bluetooth playback on CloudNote Air requires the manufacturer companion app to be installed first, rather than allowing a listener to pair a source and start playback without it.
  - Basic Bluetooth playback does not require the manufacturer app.

### A33: ok
turns=2 latency=10182ms claims=11 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A33.json`

- `A33:306:498` **unknown** ✓span ✓label ['stonewave.max.bluetooth_version']: The Bluetooth connection on StoneWave Max maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
  - The catalogue gives only the Bluetooth version for the Max. It has no range or playback-continuity information.
- `A33:499:656` **contradicted** ✓span ✓label ['stonewave.max.wifi']: The built-in Wi-Fi capability of StoneWave Max is present, independently of whatever Bluetooth connection a listener might also choose for everyday playback.
  - The catalogue says the Max has no built-in Wi-Fi.
- `A33:658:842` **contradicted** ✓span ✓label ['stonewave.max.warranty_india']: For an authorized India purchase with the original invoice and a manufacturing defect, StoneWave Max receives a standard manufacturer warranty lasting 24 months from the purchase date.
  - The India warranty under these conditions is 18 months, not 24.
- `A33:843:1027` **contradicted** ✓span ✓label ['stonewave.max.app_required_bluetooth']: Basic Bluetooth playback on StoneWave Max requires the manufacturer companion app to be installed first, rather than allowing a listener to pair a source and start playback without it.
  - The catalogue says basic Bluetooth playback does not require the app.
- `A33:1028:1203` **supported** ✓span ✓label ['stonewave.max.battery_50_percent', 'stonewave.max.battery_100_percent']: Turning StoneWave Max up from fifty to one hundred percent volume in the stated new-battery, EQ-off laboratory tests halves its listed playback time from 24 hours to 12 hours.
  - The catalogue lists 24 hours at 50% volume and 12 hours at 100% volume under these test conditions, which is half.
- `A33:1400:1574` **supported** ✓span ✓label ['stonewave.max.warranty_india']: For manufacturing defects following an authorized India purchase with the original invoice, the standard manufacturer warranty on StoneWave Max lasts 1.5 years from purchase.
  - 18 months equals 1.5 years under the same conditions.
- `A33:1575:1780` **unknown** ✓span ✓label []: The sustained amplifier output of StoneWave Max is forty watts per channel during ordinary playback, which allows a direct loudness comparison with other speakers advertised using electrical power figures.
  - The catalogue has no amplifier output or power rating for the Max.
- `A33:1782:1951` **contradicted** ✓span ✓label ['stonewave.max.microphone']: The built-in microphone is not included on StoneWave Max, without needing an accessory to change the hardware specification being described for this exact speaker model.
  - The catalogue says the Max has a built-in microphone.
- `A33:1952:2111` **supported** ✓span ✓label ['stonewave.max.wifi', 'stonewave.max.bluetooth_version']: The built-in Wi-Fi capability of StoneWave Max is absent, which should be treated as a separate specification from its ability to receive audio over Bluetooth.
  - The Max has no built-in Wi-Fi, and the catalogue lists Bluetooth 5.4 as a separate specification.
- `A33:2112:2307` **unknown** ✓span ✓label []: StoneWave Max accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
  - The catalogue has no multipoint Bluetooth information.
- `A33:2309:2509` **unknown** ✓span ✓label []: No version of StoneWave Max has ever been offered in blue, including previous-year retail stock and editions supplied only through independent authorized sellers rather than the official online store.
  - The catalogue has no colour or edition information, and it cannot confirm a negative.

### A34: ok
turns=2 latency=9152ms claims=8 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A34.json`

- `A34:306:479` **supported** ✓span ✓label ['stonewave.go.battery_50_percent', 'stonewave.go.battery_100_percent']: Turning StoneWave Go up from fifty to one hundred percent volume in the stated new-battery, EQ-off laboratory tests halves its listed playback time from 16 hours to 8 hours.
  - The catalogue lists 16 hours at 50 percent and 8 hours at 100 percent under the same lab conditions, and 8 is half of 16.
- `A34:480:656` **contradicted** ✓span ✓label ['stonewave.go.warranty_invoice_required', 'stonewave.go.warranty_india']: An original invoice is unnecessary when claiming the standard India manufacturer warranty for StoneWave Go, provided the buyer says the purchase came from an authorized seller.
  - The India warranty requires the original invoice, so saying it is unnecessary is wrong.
- `A34:658:808` **contradicted** ✓span ✓label ['stonewave.go.price_2026', 'stonewave.go.price_2025']: For an India purchase at the official catalogue list price on 1 October 2026, StoneWave Go still costs INR 1,799 including tax but excluding shipping.
  - The 2026 list price is INR 1,999; INR 1,799 was the 2025 price.
- `A34:809:958` **supported** ✓span ✓label ['stonewave.go.price_2026', 'stonewave.max.price_2026']: For the current India catalogue, StoneWave Go is listed at INR 1,500 less than StoneWave Max, comparing the two tax-inclusive prices before shipping.
  - The 2026 prices are INR 3,499 for Max and INR 1,999 for Go, a difference of INR 1,500.
- `A34:1155:1315` **contradicted** ✓span ✓label ['stonewave.go.battery_50_percent']: At fifty percent volume with EQ off and a new battery in the laboratory, StoneWave Go is rated for 1020 minutes of playback before recharging becomes necessary.
  - 16 hours is 960 minutes, not 1020 minutes.
- `A34:1316:1496` **unknown** ✓span ✓label []: The official India catalogue price of StoneWave Go will drop by INR 300 during January 2027, with that future reduction applying before shipping to purchases from the brand itself.
  - The catalogue has no information about future price changes in 2027.
- `A34:1497:1683` **unknown** ✓span ✓label ['stonewave.go.battery_50_percent']: In winter weather below freezing, StoneWave Go delivers its full 16-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
  - The 16-hour figure is for lab conditions, and the catalogue says nothing about runtime in freezing temperatures.
- `A34:1685:1854` **unknown** ✓span ✓label []: Orders for StoneWave Go receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
  - The catalogue has no shipping or delivery policy rows.

### A35: ok
turns=2 latency=10521ms claims=10 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A35.json`

- `A35:335:520` **contradicted** ✓span ✓label ['cleartrail.plus.immersion_duration', 'cleartrail.plus.immersion_depth']: With all port covers closed, ClearTrail Plus is permitted to remain immersed in fresh water at a depth of one metre for a full hour under the manufacturer's stated laboratory allowance.
  - The maximum laboratory duration at one metre is 30 minutes, not a full hour.
- `A35:521:687` **supported** ✓span ✓label ['cleartrail.plus.immersion_depth', 'cleartrail.plus.immersion_duration', 'cleartrail.plus.immersion_allowed']: With all port covers closed, the laboratory immersion allowance for ClearTrail Plus is limited to fresh water at no more than one metre for no more than half an hour.
  - The catalogue gives a maximum of 1 metre and 30 minutes in fresh water with port covers closed.
- `A35:689:883` **unknown** ✓span ✓label []: The Bluetooth connection on ClearTrail Plus maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
  - The catalogue has no Bluetooth range or playback continuity facts.
- `A35:884:1070` **unknown** ✓span ✓label ['cleartrail.plus.bluetooth_version']: ClearTrail Plus supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
  - The catalogue lists only Bluetooth 5.3 and has no codec facts, and a version does not establish codec support.
- `A35:1071:1245` **supported** ✓span ✓label ['cleartrail.plus.warranty_india', 'cleartrail.plus.warranty_invoice_required']: For manufacturing defects following an authorized India purchase with the original invoice, the standard manufacturer warranty on ClearTrail Plus lasts 1 years from purchase.
  - The India warranty is 12 months, which is 1 year, under the same conditions.
- `A35:1442:1606` **contradicted** ✓span ✓label ['cleartrail.plus.price_2026', 'cleartrail.mini.price_2026']: For a current India catalogue comparison before shipping, ClearTrail Plus is INR 1,200 less expensive than ClearTrail Mini, with tax included in both listed prices.
  - Plus is INR 2,499 and Mini is INR 1,299, so Plus costs INR 1,200 more, not less.
- `A35:1607:1804` **unknown** ✓span ✓label []: ClearTrail Plus accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
  - The catalogue has no multipoint connection facts.
- `A35:1806:1969` **contradicted** ✓span ✓label ['cleartrail.plus.battery_50_percent']: At fifty percent volume with EQ off and a new battery in the laboratory, ClearTrail Plus is rated for 1260 minutes of playback before recharging becomes necessary.
  - The rating is 20 hours, which is 1200 minutes, not 1260.
- `A35:1970:2129` **contradicted** ✓span ✓label ['cleartrail.plus.wifi']: The built-in Wi-Fi capability of ClearTrail Plus is present, independently of whatever Bluetooth connection a listener might also choose for everyday playback.
  - The catalogue says ClearTrail Plus has no built-in Wi-Fi.
- `A35:2130:2321` **unknown** ✓span ✓label []: After an announced firmware update next quarter, ClearTrail Plus will gain a built-in voice assistant that can answer spoken questions without requiring a paired phone to process the request.
  - This is a future firmware promise, and the catalogue has no facts about updates or a voice assistant.

### A36: ok
turns=2 latency=8947ms claims=8 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A36.json`

- `A36:324:496` **unknown** ✓span ✓label []: Orders for ClearTrail Mini receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
  - The catalogue has no delivery or shipping-charge policy rows for ClearTrail Mini.
- `A36:497:687` **supported** ✓span ✓label ['cleartrail.mini.warranty_invoice_required', 'cleartrail.mini.warranty_india']: Even when other warranty conditions are met for an authorized India purchase, the original purchase invoice is still required to claim the standard manufacturer warranty for ClearTrail Mini.
  - The India standard warranty requires the original invoice.
- `A36:689:891` **unknown** ✓span ✓label []: An authorized India service centre guarantees repair of ClearTrail Mini within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
  - The catalogue has no repair turnaround or guarantee information.
- `A36:892:1059` **contradicted** ✓span ✓label ['cleartrail.mini.microphone']: The built-in microphone is included on ClearTrail Mini, without needing an accessory to change the hardware specification being described for this exact speaker model.
  - The catalogue says ClearTrail Mini has no built-in microphone.
- `A36:1256:1463` **unknown** ✓span ✓label ['cleartrail.mini.battery_50_percent']: Compared with the unlisted RivalSound Trek, ClearTrail Mini provides two additional hours of playback under identical new-battery, fifty-percent-volume, EQ-off laboratory testing conditions for both devices.
  - RivalSound Trek is not in the catalogue, so the comparison cannot be checked.
- `A36:1464:1650` **contradicted** ✓span ✓label ['cleartrail.mini.warranty_india']: For an authorized India purchase with the original invoice and a manufacturing defect, ClearTrail Mini receives a standard manufacturer warranty lasting 18 months from the purchase date.
  - The catalogue gives a 12-month India warranty under these conditions, not 18 months.
- `A36:1651:1822` **supported** ✓span ✓label ['cleartrail.mini.price_2025', 'cleartrail.mini.price_2026']: The move from the 2025 India catalogue to the 2026 catalogue raised the tax-inclusive list price of ClearTrail Mini by INR 300, with shipping excluded in both comparisons.
  - The price rose from INR 999 to INR 1,299, which is INR 300, on the same tax-inclusive, shipping-excluded basis.
- `A36:1824:1978` **supported** ✓span ✓label ['cleartrail.mini.price_2026', 'cleartrail.plus.price_2026']: For the current India catalogue, ClearTrail Mini is listed at INR 1,200 less than ClearTrail Plus, comparing the two tax-inclusive prices before shipping.
  - ClearTrail Plus is listed at INR 2,499 and Mini at INR 1,299, a difference of INR 1,200.

### A37: ok
turns=2 latency=10970ms claims=10 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A37.json`

- `A37:371:556` **supported** ✓span ✓label ['cleartrail.mini.app_required_bluetooth']: Basic Bluetooth listening on ClearTrail Mini does not require the manufacturer companion app to be installed, even if a buyer is interested in optional app-related features or settings.
  - The catalogue says basic Bluetooth playback does not require the manufacturer app.
- `A37:557:736` **contradicted** ✓span ✓label ['cleartrail.mini.battery_100_percent', 'cleartrail.mini.battery_50_percent']: The stated laboratory playback time for ClearTrail Mini, using a new battery with EQ off at one hundred percent volume, remains 12 hours without any reduction for louder playback.
  - At 100 percent volume the laboratory battery time is 6 hours. The 12 hours applies at 50 percent volume.
- `A37:738:917` **unknown** ✓span ✓label []: Using a twenty-watt wall adapter, a fully discharged ClearTrail Mini reaches a complete charge in ninety minutes, so a short charging stop is enough to restore the entire battery.
  - The catalogue has no charging time or adapter wattage data.
- `A37:918:1096` **supported** ✓span ✓label ['cleartrail.mini.microphone']: The built-in microphone is not included on ClearTrail Mini, so microphone availability should be checked for this exact model instead of copied from another speaker in the range.
  - The Mini has no built-in microphone, and the Plus does have one, so the model-specific caution holds.
- `A37:1097:1275` **supported** ✓span ✓label ['cleartrail.mini.usb_audio', 'cleartrail.mini.charging_port']: For wired digital audio specifically, the USB-C connector on ClearTrail Mini does not provide an audio-input path, regardless of the fact that the connector also serves charging.
  - USB audio is false for the Mini, and the USB-C port is its charging port.
- `A37:1472:1658` **contradicted** ✓span ✓label ['cleartrail.mini.warranty_india']: For an authorized India purchase with the original invoice and a manufacturing defect, ClearTrail Mini receives a standard manufacturer warranty lasting 18 months from the purchase date.
  - The India warranty under these conditions is 12 months, not 18.
- `A37:1659:1853` **unknown** ✓span ✓label []: The normal manufacturing origin of ClearTrail Mini is India, even when the unit is purchased through an authorized seller rather than ordered directly from the manufacturer's own retail channel.
  - The catalogue has no manufacturing origin information.
- `A37:1855:2009` **supported** ✓span ✓label ['cleartrail.mini.price_2026', 'cleartrail.plus.price_2026']: For the current India catalogue, ClearTrail Mini is listed at INR 1,200 less than ClearTrail Plus, comparing the two tax-inclusive prices before shipping.
  - The Plus is INR 2,499 and the Mini is INR 1,299, a difference of INR 1,200, both tax-inclusive and excluding shipping.
- `A37:2010:2217` **unknown** ✓span ✓label []: The sustained amplifier output of ClearTrail Mini is forty watts per channel during ordinary playback, which allows a direct loudness comparison with other speakers advertised using electrical power figures.
  - The catalogue has no amplifier power data.
- `A37:2218:2407` **unknown** ✓span ✓label ['cleartrail.mini.battery_50_percent']: In winter weather below freezing, ClearTrail Mini delivers its full 12-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
  - The 12 hours at 50 percent volume is a laboratory figure, and the catalogue gives no data on freezing-temperature performance.

### A38: ok
turns=2 latency=9940ms claims=9 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A38.json`

- `A38:306:486` **contradicted** ✓span ✓label ['cloudnote.studio.warranty_invoice_required', 'cloudnote.studio.warranty_india']: An original invoice is unnecessary when claiming the standard India manufacturer warranty for CloudNote Studio, provided the buyer says the purchase came from an authorized seller.
  - The catalogue says the original invoice is required for the India standard warranty on CloudNote Studio.
- `A38:487:662` **supported** ✓span ✓label ['cloudnote.studio.warranty_india']: For manufacturing defects following an authorized India purchase with the original invoice, the standard manufacturer warranty on CloudNote Studio lasts 2 years from purchase.
  - The warranty is 24 months, which is 2 years, under these same conditions.
- `A38:664:843` **supported** ✓span ✓label ['cloudnote.studio.microphone', 'cloudnote.air.microphone']: The built-in microphone is not included on CloudNote Studio, so microphone availability should be checked for this exact model instead of copied from another speaker in the range.
  - Studio has no built-in microphone, while Air does, so the model-specific check is justified.
- `A38:844:1011` **supported** ✓span ✓label ['cloudnote.studio.immersion_allowed', 'cloudnote.studio.immersion_depth', 'cloudnote.studio.immersion_duration']: With all port covers closed, the laboratory immersion allowance for CloudNote Studio is limited to fresh water at no more than one metre for no more than half an hour.
  - The catalogue gives a maximum of 1 m and 30 minutes in fresh water with port covers closed.
- `A38:1208:1388` **unknown** ✓span ✓label []: Using a twenty-watt wall adapter, a fully discharged CloudNote Studio reaches a complete charge in ninety minutes, so a short charging stop is enough to restore the entire battery.
  - The catalogue has no charging time or adapter wattage information.
- `A38:1389:1592` **unknown** ✓span ✓label []: No version of CloudNote Studio has ever been offered in blue, including previous-year retail stock and editions supplied only through independent authorized sellers rather than the official online store.
  - The catalogue has no colour information.
- `A38:1593:1792` **unknown** ✓span ✓label []: The plastic used in the enclosure of CloudNote Studio contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
  - The catalogue has no recycled-material information.
- `A38:1794:1977` **contradicted** ✓span ✓label ['cloudnote.studio.stereo_pairing_scope', 'cloudnote.air.stereo_pairing_scope']: The manufacturer supports a stereo pair made from one CloudNote Studio and one CloudNote Air, since being members of the same brand is sufficient for cross-model stereo compatibility.
  - Stereo pairing is limited to two units of the same model, and cross-model pairing is unsupported.
- `A38:1978:2164` **contradicted** ✓span ✓label ['cloudnote.studio.immersion_duration', 'cloudnote.studio.immersion_depth']: With all port covers closed, CloudNote Studio is permitted to remain immersed in fresh water at a depth of one metre for a full hour under the manufacturer's stated laboratory allowance.
  - The maximum immersion duration at the stated depth is 30 minutes, not a full hour.

### A39: ok
turns=2 latency=10475ms claims=10 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A39.json`

- `A39:306:493` **contradicted** ✓span ✓label ['cloudnote.air.immersion_allowed']: With all port covers closed, CloudNote Air is explicitly permitted to be immersed in fresh water, rather than being restricted to the non-immersion use implied by a more cautious reading.
  - The catalogue says immersion is not allowed for CloudNote Air in fresh water with port covers closed.
- `A39:494:691` **supported** ✓span ✓label ['cloudnote.air.water_damage_covered', 'cloudnote.air.warranty_india']: Whatever conclusions a buyer draws from the water-resistance rating, water damage remains excluded from the standard India manufacturer warranty covering CloudNote Air after an authorized purchase.
  - Water damage is not covered by the India standard warranty, regardless of the water rating, and the warranty applies to authorized-seller purchases.
- `A39:693:869` **supported** ✓span ✓label ['cloudnote.air.usb_audio', 'cloudnote.air.charging_port']: For wired digital audio specifically, the USB-C connector on CloudNote Air does not provide an audio-input path, regardless of the fact that the connector also serves charging.
  - USB audio is false and the USB-C port is the charging port.
- `A39:870:1062` **unknown** ✓span ✓label ['cloudnote.air.bluetooth_version']: The Bluetooth connection on CloudNote Air maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
  - The catalogue gives only the Bluetooth version, with nothing on range or playback continuity.
- `A39:1063:1245` **contradicted** ✓span ✓label ['cloudnote.air.usb_audio']: For wired digital audio specifically, the USB-C connector on CloudNote Air does provide an audio-input path, so the connector can be treated accordingly when choosing a wired source.
  - The catalogue says CloudNote Air has no wired digital audio through USB-C.
- `A39:1442:1614` **supported** ✓span ✓label ['cloudnote.air.microphone']: The built-in microphone is included on CloudNote Air, so microphone availability should be checked for this exact model instead of copied from another speaker in the range.
  - CloudNote Air has a built-in microphone.
- `A39:1615:1792` **contradicted** ✓span ✓label ['cloudnote.air.warranty_invoice_required', 'cloudnote.air.warranty_india']: An original invoice is unnecessary when claiming the standard India manufacturer warranty for CloudNote Air, provided the buyer says the purchase came from an authorized seller.
  - The India standard warranty requires the original invoice.
- `A39:1794:1971` **unknown** ✓span ✓label ['cloudnote.air.charging_port']: Using a twenty-watt wall adapter, a fully discharged CloudNote Air reaches a complete charge in ninety minutes, so a short charging stop is enough to restore the entire battery.
  - The catalogue has no charging time or adapter wattage information.
- `A39:1972:2172` **unknown** ✓span ✓label []: An authorized India service centre guarantees repair of CloudNote Air within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
  - The catalogue has no repair turnaround guarantee.
- `A39:2173:2360` **unknown** ✓span ✓label ['cloudnote.air.battery_50_percent']: In winter weather below freezing, CloudNote Air delivers its full 10-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
  - The 10-hour figure is a laboratory test result, and the catalogue gives no information on sub-freezing performance.

### A40: ok
turns=2 latency=9848ms claims=9 trace=`traces/b7d69fb0-0bf6-4368-8f9d-40c273a4369d/A40.json`

- `A40:335:512` **contradicted** ✓span ✓label ['stonewave.max.price_2025', 'stonewave.max.price_2026']: In the 2025 India catalogue, before the current-year revision, StoneWave Max already carried the same tax-inclusive list price of INR 3,499, excluding shipping from that amount.
  - The 2025 India price was INR 3,299, not INR 3,499.
- `A40:513:677` **supported** ✓span ✓label ['stonewave.max.immersion_allowed', 'stonewave.max.immersion_depth', 'stonewave.max.immersion_duration']: With all port covers closed, the laboratory immersion allowance for StoneWave Max is limited to fresh water at no more than one metre for no more than half an hour.
  - The catalogue gives fresh water, closed port covers, a 1 m maximum depth and a 30-minute maximum duration.
- `A40:679:871` **unknown** ✓span ✓label []: The Bluetooth connection on StoneWave Max maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
  - The catalogue has no Bluetooth range or playback-continuity facts.
- `A40:872:1041` **supported** ✓span ✓label ['stonewave.max.price_2025', 'stonewave.max.price_2026']: The move from the 2025 India catalogue to the 2026 catalogue raised the tax-inclusive list price of StoneWave Max by INR 200, with shipping excluded in both comparisons.
  - The price rose from INR 3,299 to INR 3,499, which is INR 200, under the same tax and shipping conditions.
- `A40:1238:1422` **unknown** ✓span ✓label ['stonewave.max.bluetooth_version']: StoneWave Max supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
  - The catalogue lists Bluetooth 5.4 but has no codec facts, and a version does not establish AAC support.
- `A40:1423:1572` **supported** ✓span ✓label ['stonewave.max.price_2026', 'stonewave.go.price_2026']: For the current India catalogue, StoneWave Max is listed at INR 1,500 more than StoneWave Go, comparing the two tax-inclusive prices before shipping.
  - INR 3,499 minus INR 1,999 is INR 1,500.
- `A40:1573:1776` **unknown** ✓span ✓label ['stonewave.max.warranty_india']: A retail purchase of StoneWave Max in Germany qualifies for the same 18-month manufacturer warranty described for authorized India purchases, without any different regional terms affecting that duration.
  - The 18-month warranty is stated only for India purchases from authorized sellers, and the catalogue has no Germany terms.
- `A40:1778:1947` **contradicted** ✓span ✓label ['stonewave.max.microphone']: The built-in microphone is not included on StoneWave Max, without needing an accessory to change the hardware specification being described for this exact speaker model.
  - The catalogue says StoneWave Max has a built-in microphone.
- `A40:1948:2134` **contradicted** ✓span ✓label ['stonewave.max.usb_audio']: For wired digital audio specifically, the USB-C connector on StoneWave Max does not provide an audio-input path, so the connector can be treated accordingly when choosing a wired source.
  - The catalogue says StoneWave Max supports wired digital audio through USB-C.
