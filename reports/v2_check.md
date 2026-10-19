# Run report: v2 / check

- run_id: `4daea87a-9aec-4e8f-8798-b098e0f99972`  status: **completed**
- provider/model: `anthropic` / `claude-sonnet-5-5`
- prompt: `prompts/v2.md` sha256 `230ad943b3d838c0…`
- dataset `long-brand-answers-50-v4`, facts `speaker-catalogue-v4`, evaluator `sentence-spans-and-labels-v4 (claimcheck-scorer-1)`
- source revision: `4c490ce1ad143bfeefcd6023827d278b1b4c6bdb`
- started 2026-10-19T08:11:39.098635+00:00, finished 2026-10-19T08:13:26.897434+00:00
- settings: `{"model": "claude-sonnet-5-5", "api_base": "https://api.anthropic.com", "provider": "anthropic", "sampling": "provider-default (temperature not accepted by model)", "max_turns": 3, "max_tokens": 16000, "sdk_max_retries": 0, "request_timeout_s": 180.0}`
- file hashes: `{"answers.csv": "fa28e813ea54b4e5ea985585f22f084d826241e1182accbc27ace17066125724", "brand_facts.csv": "2190d40fad2dd167ef2437956c43d595aaf2554ea673a4789b9343cb7e2936f2", "development_gold.csv": "afe84cc78f304afb6a4aaa505dd7504af80fcbf8bc507806aa5ff0aab6bf4850"}`

## Counts

| scheduled | ok | errors | empty ok | P | G | M | C | latency total (s) | tokens in/out |
|---|---|---|---|---|---|---|---|---|---|
| 10 | 10 | 0 | 0 | 94 | null | null | null | 107.6 | 114952/17235 |

## Metrics

Check split: the candidate has no gold labels. G, M, C, matches, expected labels and all quality metrics are intentionally null; the reviewer scores the saved predictions.

## Answer outcomes and predictions

### A41: ok
turns=2 latency=10413ms claims=9 trace=`traces/4daea87a-9aec-4e8f-8798-b098e0f99972/A41.json`

- `A41:371:551` **unknown** []: An opened StoneWave Go can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
  - The catalogue has no return or refund policy rows for this model.
- `A41:552:732` **unknown** ['stonewave.go.price_2026']: The official India catalogue price of StoneWave Go will drop by INR 300 during January 2027, with that future reduction applying before shipping to purchases from the brand itself.
  - The catalogue gives only the 2026 price. It says nothing about a future price change in 2027.
- `A41:734:910` **unknown** []: Using a twenty-watt wall adapter, a fully discharged StoneWave Go reaches a complete charge in ninety minutes, so a short charging stop is enough to restore the entire battery.
  - The catalogue has no charging-time or adapter-wattage facts.
- `A41:911:1071` **contradicted** ['stonewave.go.battery_50_percent']: At fifty percent volume with EQ off and a new battery in the laboratory, StoneWave Go is rated for 1020 minutes of playback before recharging becomes necessary.
  - The catalogue rates 16 hours at 50% volume, which is 960 minutes, not 1020.
- `A41:1268:1418` **contradicted** ['stonewave.go.price_2026']: For an India purchase at the official catalogue list price on 1 October 2026, StoneWave Go still costs INR 1,799 including tax but excluding shipping.
  - The 2026 India list price is INR 1,999. INR 1,799 was the 2025 price.
- `A41:1419:1599` **supported** ['stonewave.go.weight']: Considering the speaker alone and leaving retail packaging and accessories out of the measurement, StoneWave Go has a stated mass of 0.44 kilograms for carrying-weight comparisons.
  - The catalogue lists 440 grams for the speaker only, which equals 0.44 kg.
- `A41:1600:1776` **contradicted** ['stonewave.go.battery_100_percent']: The stated laboratory playback time for StoneWave Go, using a new battery with EQ off at one hundred percent volume, remains 16 hours without any reduction for louder playback.
  - At 100% volume the catalogue rates 8 hours. 16 hours is the 50% volume figure.
- `A41:1778:1940` **supported** ['stonewave.go.price_2025']: Looking back specifically at the 2025 India catalogue rather than the current offer, the listed tax-inclusive price of StoneWave Go was INR 1,799 before shipping.
  - The 2025 India list price is INR 1,799, tax included and shipping excluded.
- `A41:1941:2116` **supported** ['stonewave.go.usb_audio', 'stonewave.go.charging_port']: For wired digital audio specifically, the USB-C connector on StoneWave Go does not provide an audio-input path, regardless of the fact that the connector also serves charging.
  - USB audio is false for the Go, and the USB-C port is its charging port.

### A42: ok
turns=2 latency=10977ms claims=10 trace=`traces/4daea87a-9aec-4e8f-8798-b098e0f99972/A42.json`

- `A42:306:489` **unknown** []: An opened ClearTrail Plus can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
  - The catalogue has no return or refund policy rows for ClearTrail Plus.
- `A42:490:689` **supported** ['cleartrail.plus.water_damage_covered']: Whatever conclusions a buyer draws from the water-resistance rating, water damage remains excluded from the standard India manufacturer warranty covering ClearTrail Plus after an authorized purchase.
  - The row says water damage is not covered under the India standard warranty, independent of the water rating.
- `A42:691:877` **unknown** ['cleartrail.plus.bluetooth_version']: ClearTrail Plus supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
  - The catalogue gives only the Bluetooth version (5.3) and has no codec information, so AAC support is not established.
- `A42:878:1046` **supported** ['cleartrail.plus.adapter_included', 'cleartrail.plus.charging_port']: The official India retail box for ClearTrail Plus does not contain a wall charging adapter, so the box contents should not be inferred just from the charging-port type.
  - The adapter is not included in the official India retail box, and the charging port is a separate fact (USB-C).
- `A42:1047:1236` **unknown** ['cleartrail.plus.battery_50_percent']: In winter weather below freezing, ClearTrail Plus delivers its full 20-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
  - The 20-hour figure is a laboratory result at 50 percent volume. The catalogue has no sub-freezing temperature data.
- `A42:1433:1597` **supported** ['cleartrail.plus.price_2026', 'cleartrail.mini.price_2026']: For a current India catalogue comparison before shipping, ClearTrail Plus is INR 1,200 less expensive than ClearTrail Mini, with tax included in both listed prices.
  - The 2026 prices are INR 2,499 for Plus and INR 1,299 for Mini, both tax included. That makes Plus INR 1,200 more expensive, not less, so the claim is wrong.
- `A42:1598:1777` **contradicted** ['cleartrail.plus.warranty_invoice_required', 'cleartrail.plus.warranty_india']: An original invoice is unnecessary when claiming the standard India manufacturer warranty for ClearTrail Plus, provided the buyer says the purchase came from an authorized seller.
  - The catalogue says the original invoice is required for the India standard warranty.
- `A42:1779:1953` **supported** ['cleartrail.plus.warranty_india']: For manufacturing defects following an authorized India purchase with the original invoice, the standard manufacturer warranty on ClearTrail Plus lasts 1 years from purchase.
  - The warranty is 12 months under those conditions, which equals 1 year.
- `A42:1954:2156` **unknown** ['cleartrail.plus.warranty_india']: An authorized India service centre guarantees repair of ClearTrail Plus within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
  - The catalogue has no repair turnaround or guarantee rows.
- `A42:2157:2336` **contradicted** ['cleartrail.plus.price_2025']: In the 2025 India catalogue, before the current-year revision, ClearTrail Plus already carried the same tax-inclusive list price of INR 2,499, excluding shipping from that amount.
  - The 2025 India list price for Plus was INR 2,199, not INR 2,499.

### A43: ok
turns=2 latency=10592ms claims=9 trace=`traces/4daea87a-9aec-4e8f-8798-b098e0f99972/A43.json`

- `A43:306:484` **contradicted** ['cleartrail.plus.weight', 'cleartrail.mini.weight']: When measuring just the speaker rather than the retail box and accessories, ClearTrail Plus weighs 320 grams, matching the carrying-weight figure associated with ClearTrail Mini.
  - The catalogue lists the speaker-only weight of ClearTrail Plus as 580 grams, not 320 grams. 320 grams is the Mini's weight.
- `A43:485:644` **contradicted** ['cleartrail.plus.wifi']: The built-in Wi-Fi capability of ClearTrail Plus is present, independently of whatever Bluetooth connection a listener might also choose for everyday playback.
  - The catalogue says ClearTrail Plus has no built-in Wi-Fi.
- `A43:646:840` **unknown** ['cleartrail.plus.bluetooth_version']: The Bluetooth connection on ClearTrail Plus maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
  - The catalogue gives only the Bluetooth version (5.3). It has no range or playback-continuity information.
- `A43:841:1043` **unknown** []: No version of ClearTrail Plus has ever been offered in blue, including previous-year retail stock and editions supplied only through independent authorized sellers rather than the official online store.
  - The catalogue has no colour or edition information, and a missing negative fact stays unknown.
- `A43:1240:1423` **supported** ['cleartrail.plus.weight']: Considering the speaker alone and leaving retail packaging and accessories out of the measurement, ClearTrail Plus has a stated mass of 0.58 kilograms for carrying-weight comparisons.
  - 580 grams equals 0.58 kilograms, and the row is speaker-only.
- `A43:1424:1578` **supported** ['cleartrail.plus.price_2026', 'cleartrail.mini.price_2026']: For the current India catalogue, ClearTrail Plus is listed at INR 1,200 more than ClearTrail Mini, comparing the two tax-inclusive prices before shipping.
  - 2,499 minus 1,299 is 1,200, under the same India tax-inclusive, shipping-excluded conditions.
- `A43:1579:1750` **supported** ['cleartrail.plus.price_2025', 'cleartrail.plus.price_2026']: The move from the 2025 India catalogue to the 2026 catalogue raised the tax-inclusive list price of ClearTrail Plus by INR 300, with shipping excluded in both comparisons.
  - 2,499 minus 2,199 is 300, and both rows carry the same conditions.
- `A43:1752:1935` **unknown** ['cleartrail.plus.warranty_india']: An opened ClearTrail Plus can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
  - The catalogue has only a warranty row, which covers manufacturing defects. It has no return or refund policy.
- `A43:1936:2124` **contradicted** ['cleartrail.plus.usb_audio']: For wired digital audio specifically, the USB-C connector on ClearTrail Plus does not provide an audio-input path, so the connector can be treated accordingly when choosing a wired source.
  - The catalogue says ClearTrail Plus supports wired digital audio through its USB-C port.

### A44: ok
turns=2 latency=10340ms claims=10 trace=`traces/4daea87a-9aec-4e8f-8798-b098e0f99972/A44.json`

- `A44:335:526` **unknown** ['cleartrail.mini.microphone']: After an announced firmware update next quarter, ClearTrail Mini will gain a built-in voice assistant that can answer spoken questions without requiring a paired phone to process the request.
  - The catalogue has no information on future firmware or a voice assistant. It only lists the current microphone status.
- `A44:527:695` **supported** ['cleartrail.mini.adapter_included', 'cleartrail.mini.charging_port']: The official India retail box for ClearTrail Mini does not contain a wall charging adapter, so the box contents should not be inferred just from the charging-port type.
  - The official India retail box has no adapter, and the USB-C port is listed as a separate fact.
- `A44:697:880` **unknown** []: An opened ClearTrail Mini can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
  - The catalogue has no return or refund policy rows.
- `A44:881:1044` **supported** ['cleartrail.mini.price_2025']: Looking back specifically at the 2025 India catalogue rather than the current offer, the listed tax-inclusive price of ClearTrail Mini was INR 999 before shipping.
  - The 2025 India list price is INR 999, tax included and shipping excluded.
- `A44:1045:1224` **contradicted** ['cleartrail.mini.warranty_invoice_required', 'cleartrail.mini.warranty_india']: An original invoice is unnecessary when claiming the standard India manufacturer warranty for ClearTrail Mini, provided the buyer says the purchase came from an authorized seller.
  - The India standard warranty requires the original invoice.
- `A44:1421:1575` **supported** ['cleartrail.mini.price_2026', 'cleartrail.plus.price_2026']: For the current India catalogue, ClearTrail Mini is listed at INR 1,200 less than ClearTrail Plus, comparing the two tax-inclusive prices before shipping.
  - The 2026 prices are 2499 for Plus and 1299 for Mini, a difference of 1200.
- `A44:1576:1778` **unknown** []: No version of ClearTrail Mini has ever been offered in blue, including previous-year retail stock and editions supplied only through independent authorized sellers rather than the official online store.
  - The catalogue has no colour information, and a missing fact does not establish a negative.
- `A44:1780:1985` **unknown** ['cleartrail.mini.warranty_india']: A retail purchase of ClearTrail Mini in Germany qualifies for the same 12-month manufacturer warranty described for authorized India purchases, without any different regional terms affecting that duration.
  - The 12-month warranty row covers India purchases only. Nothing is stated about Germany.
- `A44:1986:2172` **contradicted** ['cleartrail.mini.warranty_india']: For an authorized India purchase with the original invoice and a manufacturing defect, ClearTrail Mini receives a standard manufacturer warranty lasting 18 months from the purchase date.
  - The India warranty under these conditions is 12 months, not 18.
- `A44:2173:2359` **contradicted** ['cleartrail.mini.app_required_bluetooth']: Basic Bluetooth playback on ClearTrail Mini requires the manufacturer companion app to be installed first, rather than allowing a listener to pair a source and start playback without it.
  - Basic Bluetooth playback does not require the manufacturer app.

### A45: ok
turns=2 latency=12404ms claims=9 trace=`traces/4daea87a-9aec-4e8f-8798-b098e0f99972/A45.json`

- `A45:324:510` **contradicted** ['cloudnote.studio.immersion_duration']: With all port covers closed, CloudNote Studio is permitted to remain immersed in fresh water at a depth of one metre for a full hour under the manufacturer's stated laboratory allowance.
  - The maximum laboratory immersion duration is 30 minutes, not a full hour.
- `A45:511:710` **unknown** []: The plastic used in the enclosure of CloudNote Studio contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
  - The catalogue has no rows on recycled material content.
- `A45:712:878` **supported** ['cloudnote.studio.price_2025']: Looking back specifically at the 2025 India catalogue rather than the current offer, the listed tax-inclusive price of CloudNote Studio was INR 2,799 before shipping.
  - The 2025 India list price for Studio is INR 2,799, tax included and shipping excluded.
- `A45:981:1170` **contradicted** ['cloudnote.studio.usb_audio']: For wired digital audio specifically, the USB-C connector on CloudNote Studio does not provide an audio-input path, so the connector can be treated accordingly when choosing a wired source.
  - The catalogue says Studio supports wired digital audio through its USB-C port.
- `A45:1367:1520` **supported** ['cloudnote.studio.price_2026', 'cloudnote.air.price_2026']: For the current India catalogue, CloudNote Studio is listed at INR 1,500 more than CloudNote Air, comparing the two tax-inclusive prices before shipping.
  - The 2026 prices are 2,999 for Studio and 1,499 for Air, which is a difference of 1,500.
- `A45:1521:1704` **contradicted** ['cloudnote.studio.stereo_pairing_scope', 'cloudnote.air.stereo_pairing_scope']: The manufacturer supports a stereo pair made from one CloudNote Studio and one CloudNote Air, since being members of the same brand is sufficient for cross-model stereo compatibility.
  - Stereo pairing works only between two units of the same model, and cross-model pairing is unsupported.
- `A45:1706:1873` **supported** ['cloudnote.studio.immersion_depth', 'cloudnote.studio.immersion_duration']: With all port covers closed, the laboratory immersion allowance for CloudNote Studio is limited to fresh water at no more than one metre for no more than half an hour.
  - The maximum laboratory depth is 1 metre and the maximum duration is 30 minutes, in fresh water with port covers closed.
- `A45:1874:2074` **supported** ['cloudnote.studio.water_damage_covered', 'cloudnote.studio.warranty_india']: Whatever conclusions a buyer draws from the water-resistance rating, water damage remains excluded from the standard India manufacturer warranty covering CloudNote Studio after an authorized purchase.
  - The India standard warranty does not cover water damage, whatever the water rating, and it applies to purchases from authorized sellers.
- `A45:2075:2259` **unknown** []: An opened CloudNote Studio can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
  - The catalogue has no return or refund policy rows. The warranty rows cover manufacturing defects only.

### A46: ok
turns=2 latency=11304ms claims=11 trace=`traces/4daea87a-9aec-4e8f-8798-b098e0f99972/A46.json`

- `A46:371:574` **unknown** ['cloudnote.air.warranty_india']: A retail purchase of CloudNote Air in Germany qualifies for the same 24-month manufacturer warranty described for authorized India purchases, without any different regional terms affecting that duration.
  - The catalogue gives a 24-month warranty only for India purchases from authorized sellers. It says nothing about Germany.
- `A46:575:762` **unknown** ['cloudnote.air.battery_50_percent']: In winter weather below freezing, CloudNote Air delivers its full 10-hour laboratory battery duration at fifty percent volume, without the outdoor temperature changing the stated runtime.
  - The 10-hour figure is a laboratory result at 50 percent volume. The catalogue has no data on sub-freezing outdoor use.
- `A46:764:956` **unknown** ['cloudnote.air.bluetooth_version']: The Bluetooth connection on CloudNote Air maintains uninterrupted playback at a distance of one hundred metres outdoors, even when a listener changes the phone used as the transmitting device.
  - The catalogue lists only the Bluetooth version. It has no range or playback-stability data.
- `A46:957:1138` **supported** ['cloudnote.air.weight']: Considering the speaker alone and leaving retail packaging and accessories out of the measurement, CloudNote Air has a stated mass of 0.35 kilograms for carrying-weight comparisons.
  - 350 grams, speaker only, equals 0.35 kg.
- `A46:1139:1316` **contradicted** ['cloudnote.air.price_2025']: In the 2025 India catalogue, before the current-year revision, CloudNote Air already carried the same tax-inclusive list price of INR 1,499, excluding shipping from that amount.
  - The 2025 India list price was INR 1,199, not 1,499. The 1,499 price applies to 2026.
- `A46:1513:1690` **contradicted** ['cloudnote.air.warranty_invoice_required', 'cloudnote.air.warranty_india']: An original invoice is unnecessary when claiming the standard India manufacturer warranty for CloudNote Air, provided the buyer says the purchase came from an authorized seller.
  - The India standard warranty requires the original invoice.
- `A46:1691:1848` **contradicted** ['cloudnote.air.wifi']: The built-in Wi-Fi capability of CloudNote Air is present, independently of whatever Bluetooth connection a listener might also choose for everyday playback.
  - The catalogue says CloudNote Air has no built-in Wi-Fi.
- `A46:1850:2019` **contradicted** ['cloudnote.air.microphone']: The built-in microphone is not included on CloudNote Air, without needing an accessory to change the hardware specification being described for this exact speaker model.
  - The catalogue says CloudNote Air has a built-in microphone.
- `A46:2020:2193` **supported** ['cloudnote.air.water_rating', 'cloudnote.air.immersion_allowed']: Despite the declared IPX4 water-resistance rating, the manufacturer does not permit fresh-water immersion of CloudNote Air, even with all of the port covers properly closed.
  - The rating is IPX4, and immersion in fresh water with port covers closed is not allowed.
- `A46:2194:2383` **unknown** []: After an announced firmware update next quarter, CloudNote Air will gain a built-in voice assistant that can answer spoken questions without requiring a paired phone to process the request.
  - The catalogue has no firmware or voice-assistant information. The sentence is a future promise.
- `A46:2385:2576` **supported** ['cloudnote.air.stereo_pairing_scope']: The manufacturer permits stereo pairing only between two units of the exact CloudNote Air model, rather than treating every speaker sharing the same brand name as a compatible stereo partner.
  - Stereo pairing is limited to two units of the same model, and cross-model pairing is unsupported.

### A47: ok
turns=2 latency=8997ms claims=8 trace=`traces/4daea87a-9aec-4e8f-8798-b098e0f99972/A47.json`

- `A47:306:476` **unknown** ['stonewave.max.price_2026']: Orders for StoneWave Max receive free delivery to every India postal code, so there is no separate shipping charge even when a customer selects a remote delivery address.
  - The catalogue gives only a list price that excludes shipping. It has no delivery or shipping-charge policy.
- `A47:477:669` **unknown** []: The normal manufacturing origin of StoneWave Max is India, even when the unit is purchased through an authorized seller rather than ordered directly from the manufacturer's own retail channel.
  - The catalogue has no manufacturing-origin fact.
- `A47:671:830` **contradicted** ['stonewave.max.price_2026', 'stonewave.go.price_2026']: For a current India catalogue comparison before shipping, StoneWave Max is INR 1,500 less expensive than StoneWave Go, with tax included in both listed prices.
  - Max is INR 3,499 and Go is INR 1,999, so Max is INR 1,500 more expensive, not less.
- `A47:831:1022` **supported** ['stonewave.max.stereo_pairing_scope']: The manufacturer permits stereo pairing only between two units of the exact StoneWave Max model, rather than treating every speaker sharing the same brand name as a compatible stereo partner.
  - Max stereo pairing is same-model only, and cross-model pairing is unsupported.
- `A47:1219:1376` **contradicted** ['stonewave.max.wifi']: The built-in Wi-Fi capability of StoneWave Max is present, independently of whatever Bluetooth connection a listener might also choose for everyday playback.
  - The catalogue says Max has no built-in Wi-Fi.
- `A47:1377:1560` **contradicted** ['stonewave.max.immersion_depth', 'stonewave.max.immersion_duration']: With all port covers closed, StoneWave Max is permitted to remain immersed in fresh water at a depth of one metre for a full hour under the manufacturer's stated laboratory allowance.
  - The depth of 1 metre matches, but the maximum duration is 30 minutes, not an hour.
- `A47:1561:1735` **supported** ['stonewave.max.warranty_india']: For manufacturing defects following an authorized India purchase with the original invoice, the standard manufacturer warranty on StoneWave Max lasts 1.5 years from purchase.
  - The warranty is 18 months, which is 1.5 years, under the same conditions.
- `A47:1737:1937` **unknown** []: No version of StoneWave Max has ever been offered in blue, including previous-year retail stock and editions supplied only through independent authorized sellers rather than the official online store.
  - The catalogue has no colour or edition facts, and it cannot establish a negative about past offerings.

### A48: ok
turns=2 latency=9907ms claims=10 trace=`traces/4daea87a-9aec-4e8f-8798-b098e0f99972/A48.json`

- `A48:306:502` **supported** ['stonewave.go.water_damage_covered']: Whatever conclusions a buyer draws from the water-resistance rating, water damage remains excluded from the standard India manufacturer warranty covering StoneWave Go after an authorized purchase.
  - The India standard warranty row says water damage is not covered, independent of the water resistance rating.
- `A48:503:686` **contradicted** ['stonewave.go.app_required_bluetooth']: Basic Bluetooth playback on StoneWave Go requires the manufacturer companion app to be installed first, rather than allowing a listener to pair a source and start playback without it.
  - The catalogue says basic Bluetooth playback does not require the manufacturer app.
- `A48:688:846` **supported** ['stonewave.go.wifi']: The built-in Wi-Fi capability of StoneWave Go is absent, which should be treated as a separate specification from its ability to receive audio over Bluetooth.
  - The Wi-Fi row is false, so built-in Wi-Fi is absent.
- `A48:847:1046` **unknown** []: No version of StoneWave Go has ever been offered in blue, including previous-year retail stock and editions supplied only through independent authorized sellers rather than the official online store.
  - The catalogue has no colour or edition history for this model.
- `A48:1047:1217` **contradicted** ['stonewave.go.adapter_included']: The official India retail box for StoneWave Go includes a wall charging adapter, even though separate accessory lists may make the charging arrangement look less obvious.
  - The official India retail box does not include an adapter.
- `A48:1414:1595` **contradicted** ['stonewave.go.usb_audio']: For wired digital audio specifically, the USB-C connector on StoneWave Go does provide an audio-input path, so the connector can be treated accordingly when choosing a wired source.
  - The USB audio row is false, so wired digital audio through USB-C is not supported.
- `A48:1596:1779` **unknown** ['stonewave.go.bluetooth_version']: StoneWave Go supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
  - The catalogue gives only the Bluetooth version (5.2) and has no codec information.
- `A48:1781:1975` **unknown** ['stonewave.go.bluetooth_version']: StoneWave Go accepts two active Bluetooth source connections at the same time and switches between them automatically, without asking the listener to disconnect one phone before using the other.
  - The catalogue has no row on multipoint or simultaneous Bluetooth connections.
- `A48:1976:2175` **unknown** ['stonewave.go.warranty_india']: An authorized India service centre guarantees repair of StoneWave Go within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
  - The catalogue gives the warranty term and conditions but has no repair turnaround guarantee.
- `A48:2176:2326` **contradicted** ['stonewave.go.price_2026']: For an India purchase at the official catalogue list price on 1 October 2026, StoneWave Go still costs INR 1,799 including tax but excluding shipping.
  - The 2026 India list price is INR 1,999. INR 1,799 was the 2025 price.

### A49: ok
turns=2 latency=10301ms claims=8 trace=`traces/4daea87a-9aec-4e8f-8798-b098e0f99972/A49.json`

- `A49:335:531` **supported** ['stonewave.go.water_damage_covered', 'stonewave.go.warranty_india']: Whatever conclusions a buyer draws from the water-resistance rating, water damage remains excluded from the standard India manufacturer warranty covering StoneWave Go after an authorized purchase.
  - The catalogue says water damage is not covered under the India standard warranty, independent of the water resistance rating. The warranty applies to purchases from an authorized India seller.
- `A49:532:694` **supported** ['stonewave.go.price_2025']: Looking back specifically at the 2025 India catalogue rather than the current offer, the listed tax-inclusive price of StoneWave Go was INR 1,799 before shipping.
  - The 2025 India list price is INR 1799, tax included and shipping excluded.
- `A49:696:872` **unknown** ['stonewave.go.charging_port']: Using a twenty-watt wall adapter, a fully discharged StoneWave Go reaches a complete charge in ninety minutes, so a short charging stop is enough to restore the entire battery.
  - The catalogue has no charging time or adapter wattage data for the Go.
- `A49:975:1135` **contradicted** ['stonewave.go.battery_50_percent']: At fifty percent volume with EQ off and a new battery in the laboratory, StoneWave Go is rated for 1020 minutes of playback before recharging becomes necessary.
  - The catalogue lists 16 hours (960 minutes) under these conditions, not 1020 minutes (17 hours).
- `A49:1332:1496` **contradicted** ['stonewave.go.microphone']: The built-in microphone is included on StoneWave Go, without needing an accessory to change the hardware specification being described for this exact speaker model.
  - The catalogue says the Go has no built-in microphone.
- `A49:1497:1677` **unknown** []: An opened StoneWave Go can be returned to any authorized India seller within thirty days for a full refund, even when the speaker has no manufacturing defect or functional problem.
  - The catalogue has no return or refund policy rows.
- `A49:1679:1878` **unknown** ['stonewave.go.warranty_india']: An authorized India service centre guarantees repair of StoneWave Go within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
  - The catalogue gives warranty duration and conditions but no repair turnaround guarantee.
- `A49:1879:2054` **supported** ['stonewave.go.microphone']: The built-in microphone is not included on StoneWave Go, so microphone availability should be checked for this exact model instead of copied from another speaker in the range.
  - The catalogue confirms the Go has no built-in microphone.

### A50: ok
turns=2 latency=12327ms claims=10 trace=`traces/4daea87a-9aec-4e8f-8798-b098e0f99972/A50.json`

- `A50:324:522` **unknown** []: The plastic used in the enclosure of ClearTrail Plus contains at least sixty percent post-consumer recycled material by weight, excluding the electronic components and the external retail packaging.
  - The catalogue has no rows on recycled material content.
- `A50:523:702` **contradicted** ['cleartrail.plus.battery_100_percent']: The stated laboratory playback time for ClearTrail Plus, using a new battery with EQ off at one hundred percent volume, remains 20 hours without any reduction for louder playback.
  - At 100 percent volume the catalogue gives 10 hours, not 20. The 20-hour figure applies at 50 percent volume.
- `A50:704:895` **unknown** []: After an announced firmware update next quarter, ClearTrail Plus will gain a built-in voice assistant that can answer spoken questions without requiring a paired phone to process the request.
  - This is a future firmware promise, and the catalogue has no rows on it.
- `A50:896:1060` **contradicted** ['cleartrail.plus.price_2026', 'cleartrail.mini.price_2026']: For a current India catalogue comparison before shipping, ClearTrail Plus is INR 1,200 less expensive than ClearTrail Mini, with tax included in both listed prices.
  - Plus is INR 2,499 and Mini is INR 1,299, so Plus costs INR 1,200 more, not less.
- `A50:1061:1226` **supported** ['cleartrail.plus.price_2025']: Looking back specifically at the 2025 India catalogue rather than the current offer, the listed tax-inclusive price of ClearTrail Plus was INR 2,199 before shipping.
  - The 2025 India list price for Plus is INR 2,199, tax included and shipping excluded.
- `A50:1423:1597` **supported** ['cleartrail.plus.microphone']: The built-in microphone is included on ClearTrail Plus, so microphone availability should be checked for this exact model instead of copied from another speaker in the range.
  - The catalogue confirms Plus has a built-in microphone.
- `A50:1598:1752` **supported** ['cleartrail.plus.price_2026', 'cleartrail.mini.price_2026']: For the current India catalogue, ClearTrail Plus is listed at INR 1,200 more than ClearTrail Mini, comparing the two tax-inclusive prices before shipping.
  - 2,499 minus 1,299 is 1,200, on matching India, tax-included, shipping-excluded conditions.
- `A50:1754:1956` **unknown** ['cleartrail.plus.warranty_india']: An authorized India service centre guarantees repair of ClearTrail Plus within two working days after receiving the unit and the required purchase paperwork, regardless of replacement-part availability.
  - The catalogue gives a 12-month warranty for manufacturing defects but has no repair turnaround or guarantee.
- `A50:1957:2118` **supported** ['cleartrail.plus.wifi', 'cleartrail.plus.bluetooth_version']: The built-in Wi-Fi capability of ClearTrail Plus is absent, which should be treated as a separate specification from its ability to receive audio over Bluetooth.
  - Plus has no built-in Wi-Fi, and the catalogue lists Bluetooth 5.3 as a separate specification.
- `A50:2119:2305` **unknown** ['cleartrail.plus.bluetooth_version']: ClearTrail Plus supports the AAC Bluetooth audio codec on compatible phones, so its published Bluetooth version can be treated as evidence for that specific audio-compression capability.
  - The catalogue lists Bluetooth 5.3 but has no codec rows, and a version number does not establish AAC support.
