#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

PROJECT = Path('/Users/dywang/Desktop/1999年小浣熊水浒/character-model-sheets')


def joined(values: list[str]) -> str:
    return '；'.join(v.rstrip('。') for v in values if v)


def character_prompt(spec: dict) -> str:
    ident = spec['id']
    c = spec['character']
    ev = spec['evidence']
    entity_items = set(spec['entities']['weapon']['items'] + spec['entities']['mount']['items'] + spec['entities']['pet']['items'])
    character_must = [value for value in c['must_preserve'] if value not in entity_items]
    return f'''Use case: stylized-concept
Asset type: professional game/animation character five-view model sheet
Input images: Image 1 is the sole primary visual evidence for character {ident}. Preserve this exact individual and design; do not copy the original action, effects, scenery, animals, or camera angle.
Primary request: Create one complete landscape five-view turnaround of the exact same character, arranged left to right as front, front three-quarter, true side profile, back three-quarter, and true back.
Identity and body: {c['identity']['face']}; {c['identity']['hair']}; {c['identity']['facial_hair']}; {c['identity']['body_type']}.
Costume and colors: {joined(c['costume_layers'])}. Palette: {joined(c['palette'])}.
Must preserve: {joined(character_must)}.
Confirmed visual evidence: {joined(ev['confirmed'][:3])}.
Inferred restraint: {joined(ev['inferred'][:2])}.
Unknown and editable: {joined(ev['unknown'][-1:])}.
Style/medium: faithful to Image 1's bold black ink contours, late-1990s hand-painted cel shading and watercolor coloring; use the approved project baseline's clean warm-light-gray production-sheet presentation, not photorealistic.
Composition/framing: exactly five full-body figures, fully visible and uncropped, identical height and head-body ratio, identical head and foot baselines, equal spacing, neutral natural stance, arms slightly away from torso, hands relaxed. Remove large held weapons and separate animals from this character sheet so costume structure stays unobscured; keep only permanently worn scabbards, quivers, small accessories or fixed tools when visible in Image 1.
Constraints: same identity, face, hair, facial hair, body type, garment layers, palette, patterns, armor and fixed accessories in every view; true side and true back must be structurally readable; do not invent back emblems, text, new armor or accessories. Plain warm light-gray background, even working light. No title, labels, letters, watermark, scenery, action pose, motion effects, extra people, extra animals, duplicate weapons, fused props, extra limbs, accidental mirroring, or cropping.'''


def weapon_prompt(spec: dict) -> str:
    ident = spec['id']
    item = joined(spec['entities']['weapon']['items'])
    ev = spec['evidence']
    return f'''Use case: stylized-concept
Asset type: professional game/animation standalone weapon or signature-equipment model sheet
Input images: Image 1 is the original visual evidence for character {ident}; Image 2 is the generated character turnaround and scale/style anchor.
Primary request: Create one clean landscape independent design sheet for this exact weapon or signature equipment: {item}.
Confirmed evidence to preserve: {joined(ev['confirmed'])}.
Inferred restraint: {joined(ev['inferred'])}.
Unknown and editable: {joined(ev['unknown'])}.
Views/layout: show a large complete main face view, complete reverse view, true thinnest side profile, key construction details, natural grip/holding relationship, storage or body-attachment relationship when visible, and a small full-body silhouette of character {ident} for accurate scale. If the specification contains multiple related items, arrange them as one readable arsenal/equipment sheet without shrinking key objects.
Style/medium: same bold black ink contours and late-1990s hand-painted cel/watercolor rendering as both references; precise production drawing on plain warm light-gray background with even working light.
Constraints: every orthographic depiction must represent the same object design, proportions, materials, colors, blade orientation, grip placement and attachment logic. Complete and uncropped. Do not add unseen tassels, emblems, writing, magical effects, mechanisms, extra blades, metal hooks or decoration. No title, labels, arrows, measurements, text, watermark, scenery, unrelated weapons, duplicated components, fused hands, extra limbs, or cropping.'''


def mount_prompt(spec: dict) -> str:
    ident = spec['id']
    item = joined(spec['entities']['mount']['items'])
    ev = spec['evidence']
    return f'''Use case: stylized-concept
Asset type: professional game/animation mount model sheet
Input images: Image 1 is the sole primary visual evidence for the mount of character {ident}; Image 2 is the generated owner turnaround and scale/style anchor.
Primary request: Create one complete landscape five-view model sheet of the exact same mount: {item}.
Confirmed evidence to preserve: {joined(ev['confirmed'])}.
Inferred restraint: {joined(ev['inferred'])}.
Unknown and editable: {joined(ev['unknown'])}.
Views/layout: arrange the same full-body mount as front, front three-quarter, true side, back three-quarter and true back with consistent height, anatomy, coat colors, markings, mane, tail and tack; all feet/hooves visible. Add one smaller owner-and-mount standing scale comparison and one small natural riding-contact reference. Show saddle, bridle, reins, armor, blanket, bags and ornaments only when visible in Image 1; do not invent missing tack.
Style/medium: same bold black ink contours and late-1990s hand-painted cel/watercolor rendering as both references; clean production model sheet on plain warm light-gray background with even working light.
Constraints: one mount identity across all views; accurate animal anatomy; consistent tack attachment and owner scale; complete and uncropped. No title, labels, arrows, measurements, text, watermark, scenery, extra mounts, extra riders, extra limbs, malformed hooves, duplicated tack, accidental mirroring or unsupported decoration.'''


def main() -> None:
    count = {'character': 0, 'weapon': 0, 'mount': 0}
    for spec_path in sorted((PROJECT / 'characters').glob('*/character-spec.json')):
        spec = json.loads(spec_path.read_text(encoding='utf-8'))
        if spec['id'] in {'001', '072', '108'}:
            continue
        out_dir = spec_path.parent
        (out_dir / 'character-prompt.txt').write_text(character_prompt(spec) + '\n', encoding='utf-8')
        count['character'] += 1
        if spec['entities']['weapon']['presence'] == 'present':
            (out_dir / 'weapon-prompt.txt').write_text(weapon_prompt(spec) + '\n', encoding='utf-8')
            count['weapon'] += 1
        if spec['entities']['mount']['presence'] == 'present':
            (out_dir / 'mount-prompt.txt').write_text(mount_prompt(spec) + '\n', encoding='utf-8')
            count['mount'] += 1
    print(json.dumps(count, ensure_ascii=False))


if __name__ == '__main__':
    main()
