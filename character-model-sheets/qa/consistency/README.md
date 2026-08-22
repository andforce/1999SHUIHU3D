# 人物跨图一致性审计

审计日期：2026-08-21

## 基准与范围

- 以每名角色的 `character-turnaround.png` 作为人物身份、头部、体型、服装、配色与左右非对称结构的最高基准。
- 核对 108 份 `character-turnaround-original-pose.png`。
- 核对并补齐 108 份 `head-sheet.png`。
- 核对 91 份 `weapon-sheet.png` 中的人物比例图、穿戴关系与兵器关联。
- 核对 14 份 `mount-sheet.png` 中的站立／骑乘人物、服装和配色。

## 结果

- 确定问题：角色 `008`、`021` 缺少独立头部四视图。
- 已修复：按各自 `character-turnaround.png` 生成 `head-sheet.png`，并复核正面、背面、左侧面、右侧面的身份与结构一致性。
- 其余身体动作图、兵器图与坐骑图未发现串角色、明显脸型／体型漂移、主要服装或配色冲突；无需改图。
- 本结论基于整套配对接触表的视觉审查；接触表保留在本目录，便于逐项复核。

## 接触表

- `head-pairs-01.jpg` 至 `head-pairs-06.jpg`
- `pose-pairs-01.jpg` 至 `pose-pairs-12.jpg`
- `weapon-pairs-01.jpg` 至 `weapon-pairs-11.jpg`
- `mount-pairs-01.jpg` 至 `mount-pairs-02.jpg`
