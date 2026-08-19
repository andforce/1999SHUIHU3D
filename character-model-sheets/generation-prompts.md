# 试制生成提示词记录

生成模式：Codex 内置 `imagegen`。所有原图仅作为视觉参考，输出采用项目内独立文件，不改写原图。

## 001 人物五视图

```text
Use case: stylized-concept
Asset type: professional game/animation character five-view model sheet
Input images: Image 1 is the sole primary visual reference for character 001; preserve its identity and design, do not copy its action or storm background.
Primary request: Create one complete landscape five-view turnaround of the exact same character, arranged left to right as front, front three-quarter, true side profile, back three-quarter, and true back.
Subject: the same tall muscular adult man with narrow dignified face, straight strong brows, thin moustache, short side beard and pointed black goatee; black rigid ceremonial crown with upward angular side wings, small gold central crest, and the observed fan of thin gold rods behind the wearer's left side only; deep crimson layered robe and broad drapery wrapped over green-backed bright-gold lamellar armor; white inner collar; black-and-gold belt; green armor skirt edging; cream cloth gaps; bright-gold thigh, knee, shin and foot armor; green bracers with gold plates.
Style/medium: faithful to Image 1's bold black ink contours, late-1990s hand-painted cel shading and watercolor coloring; clean production model sheet, not photorealistic.
Composition/framing: all five full-body figures fully visible, identical height and head-body ratio, identical head and foot baselines, equal spacing, neutral natural stance, arms slightly away from torso, hands relaxed. No held prop so the costume remains unobscured.
Confirmed invariants: preserve the exact face type, facial hair, crown silhouette, crimson-over-gold-and-green costume layering, belt, lamellar rhythm, and gold leg armor.
Inferred restraint: continue the crimson garment cleanly across the back, use near-symmetrical leg armor, and do not invent new back emblems. Keep the unobserved opposite crown side simple.
Scene/backdrop: plain warm light-gray neutral studio background, even flat working light.
Constraints: exactly five views of one character; same identity and costume in every view; true side and true back must be structurally readable; no weapon, no white long prop, no action pose, no scenery, no lightning, no title, no labels, no text, no watermark, no extra people, no duplicate costume parts, no extra limbs, no cropping.
```

### 001 人物定点返修

```text
Use case: precise-object-edit
Asset type: production character turnaround correction
Input images: Image 1 is the edit target; Image 2 is the original evidence reference.
Primary request: Edit Image 1 only. In the fifth, pure-back figure at the far right, remove the mistakenly duplicated fan of thin gold crown rods from the figure's anatomical right side (the left side of that back-view figure as seen on the canvas). Keep the fan of gold rods only on the wearer's anatomical left side (the right side of that back-view figure as seen on the canvas), consistent with the first four views and Image 2.
Constraints: change only this crown-rod duplication on the fifth figure. Preserve the exact canvas, five-view arrangement, face, body, crown shape, remaining left-side rods, hair, crimson robes, armor, belt, hands, feet, proportions, colors, linework, background and every other pixel-level design feature. Do not add text, labels, props, scenery, or any new detail.
```

## 001 标志道具表

```text
Use case: stylized-concept
Asset type: professional game/animation standalone signature-prop model sheet
Input images: Image 1 is the original visual evidence; Image 2 is the approved character turnaround and scale/style anchor.
Primary request: Create a single clean landscape design sheet for character 001's distinctive long white scroll-or-command-baton-shaped handheld prop. Do not decide or label its historical name; reproduce only the visible geometry from Image 1.
Subject: one long, continuous, narrow, flattened white-to-pale-gray object with a crisp black outline; both ends terminate in short gray-white necks and small round red bead caps. Preserve the two red bead ends and the simple undecorated white body. Do not turn it into a sword, spear, banner, firearm, or magic staff.
Views/layout: show a large complete main face view, complete reverse view, true thinnest side profile, enlarged detail of each red bead end and the transition into the white body, a two-hand grip relationship matching Image 1, and a small full-body silhouette of character 001 for accurate scale. Multiple orthographic depictions are expected, but each must show the same single object design and proportions.
Style/medium: same bold black ink contours and late-1990s hand-painted cel/watercolor rendering as both references; precise production drawing.
Inferred restraint: reverse and edge are plain and unmarked; thickness is minimal and easy to revise; no internal mechanism.
Scene/backdrop: plain warm light-gray neutral background, even working light, generous spacing.
Constraints: complete uncropped object in every key orthographic view; consistent length, width, end-cap size and color; no title, labels, arrows, measurements, symbols, writing, watermark, scenery, effects, extra props, decorative tassels, blade edge, or fused hands.
```

## 072 人物五视图

```text
Use case: stylized-concept
Asset type: professional game/animation character five-view model sheet
Input images: Image 1 is the sole primary visual reference for character 072; preserve its identity and design, do not copy its airborne action.
Primary request: Create one complete landscape five-view turnaround of the exact same character, arranged left to right as front, front three-quarter, true side profile, back three-quarter, and true back.
Subject: the same extremely muscular adult man with a square-long face, high thick black eyebrows, deep-set eyes, wide toothy grin, no beard, heavy sideburns; black hair pulled into a high long ponytail with a blue-violet tie, with white painted highlights only as gloss; bare muscular arms; purple sleeveless underlayer; silver scale/lamellar cuirass with thick green edging and simple silver shoulder plates; deep-red long neck scarf and multiple red binding bands around chest and waist; loose pale-yellow trousers; matching pair of black high boots with silver plates, gold edging, and red ankle ties.
Style/medium: faithful to Image 1's bold black ink contours, exaggerated heroic anatomy, late-1990s hand-painted cel shading and watercolor coloring; clean production model sheet, not photorealistic.
Composition/framing: all five full-body figures fully visible, identical height and head-body ratio, identical head and foot baselines, equal spacing, neutral natural stance, arms slightly away from torso, hands relaxed. No held polearm so the armor, sash and footwear remain visible.
Confirmed invariants: preserve the square face, thick brows, grin, high black ponytail, extreme arm musculature, silver scale armor with green trim, red scarf and bands, pale-yellow trousers.
Inferred restraint: close the armor at the back with simple straps and the same scale size; use the same boot design on both feet; do not invent banners, crests, tattoos, or extra armor.
Scene/backdrop: plain warm light-gray neutral studio background, even flat working light.
Constraints: exactly five views of one character; same identity, ponytail length, armor panel count and sash placement in every view; true side and true back; no weapon, no polearm, no airborne pose, no scenery, no title, no labels, no text, no watermark, no extra people, no extra limbs, no cropping.
```

## 072 武器表

```text
Use case: stylized-concept
Asset type: professional game/animation standalone weapon model sheet
Input images: Image 1 is the original weapon evidence; Image 2 is the approved character turnaround and scale/style anchor.
Primary request: Create a single clean landscape design sheet for the exact same extra-long polearm from character 072.
Subject: a very long straight golden-brass shaft, approximately 1.6 times the character's standing height; near the blade is a segmented dark-brown and black wrapped two-hand grip; the head is one polished silver-white elongated spear/glaive blade with an angular flared root, one long smooth cutting edge and a row of sharp saw teeth along only the opposite edge. The shaft's cropped far end is completed conservatively with a simple small metal butt cap. No tassel, no second blade, no writing, no ornament not visible in Image 1.
Views/layout: show a large complete main face view of the entire weapon, complete reverse view, true thinnest side profile, enlarged blade-root and single serrated-edge detail, enlarged wrapped-grip detail, a natural two-hand holding relationship, and a small full-body silhouette of character 072 for accurate scale. Every orthographic view depicts the same weapon and proportions.
Style/medium: same bold black ink contours and late-1990s hand-painted cel/watercolor rendering as both references; clean precise production art.
Scene/backdrop: plain warm light-gray neutral background, even working light, generous spacing.
Constraints: all weapon views fully visible and uncropped; same total length, blade shape, serration count rhythm, grip placement and shaft thickness; no title, labels, arrows, measurements, text, watermark, scenery, action effect, duplicate unrelated weapon, extra blades, chains, or fusion with hands.
```

### 072 武器定点返修

```text
Use case: precise-object-edit
Asset type: production weapon-sheet correction
Input images: Image 1 is the edit target; Image 2 is the original weapon evidence; Image 3 is the character/style anchor.
Primary request: Edit Image 1 only. Correct every blade depiction so the same polearm has saw teeth along exactly one long edge of the silver blade, matching Image 2, while the opposite long cutting edge is completely smooth and uninterrupted. In reversed orthographic views the serrated edge may visually swap top/bottom because the weapon is flipped, but it must still represent the same one physical serrated edge. Correct the large blade detail at lower left in particular: remove all teeth from one side and keep one side only.
Constraints: change only the serration geometry. Preserve the exact canvas and layout, golden shaft length and thickness, simple butt cap, black-and-brown segmented grip, blade outline and root, character holding pose, scale silhouette, colors, linework, background and all other details. No text, labels, arrows, measurements, watermark, extra blades, tassels, or decorations.
```

## 108 人物五视图

```text
Use case: stylized-concept
Asset type: professional game/animation character five-view model sheet
Input images: Image 1 is the sole primary visual reference for character 108; preserve the man exactly, while the horse is only contextual evidence and must not appear on this character sheet.
Primary request: Create one complete landscape five-view turnaround of the exact same man, arranged left to right as front, front three-quarter, true side profile, back three-quarter, and true back.
Subject: the same tall slender adult man with cool pale skin and subtle lavender shadow, narrow long face, high straight nose, blue-gray eyes, shoulder-length wavy golden hair; thin golden moustache curling sideways and a pointed golden beard; bright cobalt-blue long robe with very wide billowing sleeves; white inner garment and white lower layer; thick deep-crimson layered scarf/short hooded mantle around shoulders; narrow crimson waist belt; the same coiled golden braided rope hanging at his right-front waist, kept neatly coiled and not expanded; simple dark soft boots as a restrained completion.
Style/medium: faithful to Image 1's bold black ink contours, late-1990s hand-painted cel shading and watercolor coloring; clean production model sheet, not photorealistic.
Composition/framing: all five full-body figures fully visible, identical height and head-body ratio, identical head and foot baselines, equal spacing, neutral natural stance, arms slightly away from torso, hands relaxed. Keep the rope coil consistently on the same anatomical side, never mirror it.
Confirmed invariants: preserve facial identity, wavy golden hair, curled moustache and pointed beard, cobalt wide-sleeved robe, deep-crimson shoulder mantle and belt, white lower layer, golden braided rope coil.
Inferred restraint: continue the blue robe and red mantle cleanly across the back with no new crest or pattern; footwear remains plain and easily revised.
Scene/backdrop: plain warm light-gray neutral studio background, even flat working light.
Constraints: exactly five views of one character; same identity, hair length, beard shape, garment layers and rope placement in every view; true side and true back; no horse, no riding pose, no expanded lasso, no scenery, no moon, no title, no labels, no text, no watermark, no extra people, no extra animals, no extra limbs, no cropping.
```

## 108 绳具表

```text
Use case: stylized-concept
Asset type: professional game/animation standalone rope equipment model sheet
Input images: Image 1 is the original rope evidence; Image 2 is the approved character turnaround and scale/style anchor.
Primary request: Create a single clean landscape design sheet for character 108's exact golden braided rope equipment, treated as a lasso-or-horse-lead whose exact use remains intentionally undecided.
Subject: thick golden-yellow braided cord with the same visible twisted weave; a distinctive elongated braided handle/loop near the top; several orderly hanging coils; one long loose tail ending only in the small simple woven knot visible in the reference. Do not add metal hooks, weights, blades, clasps, beads, inscriptions, or magical effects.
Views/layout: show the compact waist-hung coiled state, a complete expanded lasso/lead silhouette, front and reverse of the braided handle/loop, true rope cross-section and weave close-up, a natural hand grip, the attachment/hanging relationship at the character's right-front waist, and a small full-body character silhouette for accurate scale. Each repeated depiction must use the same rope diameter, color and handle design.
Style/medium: same bold black ink contours and late-1990s hand-painted cel/watercolor rendering as both references; clean production drawing.
Scene/backdrop: plain warm light-gray neutral background, even working light, generous spacing.
Constraints: no horse on this equipment sheet; no title, labels, arrows, measurements, text, watermark, scenery, effects, extra weapons, extra rope ends, impossible knots, fused fingers, or invented metal hardware.
```

## 108 坐骑表

```text
Use case: stylized-concept
Asset type: professional game/animation horse mount model sheet
Input images: Image 1 is the sole primary visual evidence for the horse; Image 2 anchors the owner's exact scale and illustration style.
Primary request: Create one complete landscape five-view model sheet of the exact same horse, plus owner scale and bareback contact reference.
Subject: one large powerful deep-black to charcoal-gray horse with the same long narrow head, dark muzzle, calm blue-gray highlighted eye, pointed black ears, heavy neck and barrel, long windswept silver-gray mane with darker roots, and subtle cool blue-gray highlights on the black coat. No visible markings are added. Complete unseen hindquarters conservatively; use a long full tail mixing deep gray and silver-gray strands to match the mane.
Views/layout: arrange the same horse as full-body front, front three-quarter, true side, back three-quarter and true back, consistent height and body proportions, all hooves visible; add one smaller owner-and-horse standing scale comparison and one small bareback riding-contact silhouette. The owner must match Image 2's tall slender blue-robed figure and remain clearly secondary.
Tack relationship: the original shows no saddle, bridle, bit, reins, horse armor, blanket or bags. Keep the horse completely untacked in all views. The bareback contact reference must remain simple and must not invent equipment.
Style/medium: same bold black ink contours and late-1990s hand-painted cel/watercolor rendering as both references; clean production model sheet, accurate horse anatomy.
Scene/backdrop: plain warm light-gray neutral background, even working light, generous spacing.
Constraints: exactly one horse identity across all views; no cropping; same mane side, head shape, coat colors and proportions; no title, labels, arrows, measurements, text, watermark, scenery, moon, extra horses, extra riders, extra limbs, malformed hooves, saddle, bridle, reins, armor or decorative tack.
```
