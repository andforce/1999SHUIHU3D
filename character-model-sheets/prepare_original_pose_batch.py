#!/usr/bin/env python3
"""Prepare original-pose turnaround variants, prompts, and generation jobs."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT = Path(__file__).resolve().parent
WORKSPACE = PROJECT.parent
CHARACTERS = PROJECT / "characters"
STYLE_ANCHOR = (CHARACTERS / "016" / "character-turnaround-original-pose.png").resolve()
SAMPLE_IDS = {"001", "002", "016"}
POSE_HINTS = {
    "003": "身体略转三分之四，双手在身前横向展开长卷轴，同时在胸前持羽扇；宽袍与卷轴保持原画的前后遮挡",
    "004": "悬浮式单腿盘坐：一腿屈膝横盘、另一脚尖向下，双手在胸腹中线合握竖直长剑，紫色宽袍向左右展开",
    "005": "骑在前蹄腾起的红棕战马上，持长柄大刀的手臂高举过头，另一手控制缰绳，躯干随马头方向扭转",
    "006": "身体大部背向观者并回头侧视，长披风横向大幅包裹和后掠；一臂从披风外伸出持细长兵器，另一件长兵器与小圆盘饰在背后保持位置",
    "007": "骑乘疾驰棕马，骑手躯干侧扭，双臂把长杆狼牙棒高举至肩头上方准备横扫，双腿持续夹持马腹",
    "008": "保持极低的前倾蹲伏/扑击姿势，双膝深屈、躯干贴近大腿；双手控制同一件巨大红黑弯月长兵器，红披风形成背后的弧形动态轮廓",
    "009": "骑乘白马并在马背上拉满长弓：持弓臂向前上伸直，拉弦手贴近面部，胸腔与头部朝箭射方向扭转",
    "010": "三分之四站姿，双臂在胸前伸展并持一件短筒/卷轴状器物，双腿交错承重，长袍与红色内裙自然下垂",
    "011": "身体腾空向前俯冲，一臂朝观者方向大幅伸出、另一臂后摆，多把长剑固定在背后，双腿前后错开并屈曲",
    "012": "长须甲士保持深马步，双膝外展、骨盆下沉、躯干侧扭；一臂前伸、一臂后收，背后长兵器保持与身体相对路径",
    "013": "壮汉腾空前冲，一拳向前猛烈伸出、另一臂后摆，双腿一前一后屈曲；长柄月牙兵器横跨背后",
    "014": "宽幅跃步刀势：前腿大幅屈曲、后腿伸展，双臂把长弯刀横置胸前，头部沿刀锋方向侧转",
    "015": "单腿承重、另一膝高抬，躯干扭转；双手横握同一根双头长枪穿过胸前，背后大幅飘带保持展开",
    "017": "身体前倾奔跃，白色斗篷和宽帽后掠；双手持续控制腰前长剑/刀鞘的拔刀关系，双腿前后错开",
    "018": "骑乘白马正向冲来，骑手双手控制斜穿身体的长柄月牙兵器，战马一条前腿抬起，人与马保持同一冲锋重心",
    "019": "侧向疾驰灰马，骑手伏低躯干并将长弯刀水平向前伸出，另一手牵缰，红披风与马鬃统一后掠",
    "020": "朝观者奔跃，一臂弧形高举过头、另一手掌向前推出，一膝高抬、另一腿向后，黑色袍摆和红腰带后扬",
    "021": "红发壮汉保持深蹲扑击姿势，双膝外展、躯干前压，双手把大型月牙长柄兵器横向压在身前",
    "022": "身体斜向腾空，一手高举大斧过头、另一手向下伸展并保持链状/第二兵器关系，双腿屈曲错开",
    "023": "裸上身人物向前跃起，一根长棍横跨双肩后方并由手臂固定，前膝抬起、后腿折叠，红腰巾后飘",
    "024": "放松站立并略侧身，一手举葫芦至肩头附近、另一手扶腰，绿色外袍和白色内裙保持原画垂坠",
    "025": "向前迈步冲刺，双手控制一柄长弯刀斜穿身体，红色披风向后展开，前腿承重、后腿跟进",
    "026": "身体直立悬浮/轻踏，双手附近保持宽刃长刀水平横过腹前，四肢姿态克制；只移除水浪场景，不改变持刀关系",
    "027": "腾空挥砍，双手在身体一侧合握巨大弯刀，刀身形成宽幅弧线；一腿伸出、另一腿屈曲，躯干强烈扭转",
    "028": "侧向高速奔跑，一手把宽刃弯刀低位横置髋前，另一臂向后，前膝抬高、后腿伸展",
    "029": "头前脚后的俯冲腾空姿势，一只装有三爪刃的前臂向前下方伸出，另一臂和双腿向后拖曳",
    "030": "单脚轻触地面/水面直立，另一腿微提，双臂自然向两侧下垂并维持细链/软兵器绕腰的弧线",
    "031": "极低蹲伏，双膝深屈、肩背前弓，双手各持短刃向地面两侧展开，头部从眉下向前凝视",
    "032": "腾空向前，一膝高抬，双手在身体前下方控制巨大矩形斧刃，披风与衣摆向后上方扬起",
    "033": "宽脚站立，持短刀的手举在肩旁，另一拳自然下垂；胸腹保持原画伤痕和略转三分之四的姿态",
    "034": "虎皮猎手保持贴地兽形蹲伏，一手朝观者大幅伸出、另一臂支撑兵器，背部弓箭与虎皮固定不移",
    "035": "保持横向攀爬姿态：一手高举抓握虚拟上方支点、另一手向观者伸出，双腿弯曲贴近原画岩面方向；不绘制岩壁但不改攀爬肢体",
    "036": "腾空射击姿态，双手维持弓与箭的拉射关系，一膝高抬、另一腿向后，红色长巾和发丝向上后方展开",
    "037": "直立施术姿势，一手在胸肩前抬起并保持捏指手势，另一臂自然下垂，两把剑固定在背后；移除悬浮光球但保留手势",
    "038": "双腿前后站稳、躯干回转，双手把长鞭/绳索横向拉紧在身后与侧方，红披巾保持旋转形成的褶皱",
    "039": "骑乘疾驰黄棕马，骑手扭转胸腔并把长兵器高举在肩头上方准备挥击，另一手维持缰绳控制",
    "040": "骑乘黑马并向前俯身，持弯刀的手把刀刃压在马颈前方，另一手牵缰，红披风沿马后方展开",
    "041": "正向骑乘白马，骑手挺直上身并将长枪斜向前下方伸出，另一手牵缰，蓝色披巾和盔缨后扬",
    "042": "骑在斜向疾驰的棕马上并随马身前倾，一臂向外伸展长杆兵器，另一手维持缰绳，披风与马尾同向后掠",
    "043": "人物水平向前腾空，一手将长枪斜向前下方刺出、另一臂向后平衡，双腿一屈一伸并保持衣摆后飘",
    "044": "水下式悬浮姿态，一膝抬起、另一腿向下，双臂放松下垂，蓝色衣袍与绿色飘带保持向上漂浮；移除气泡与水景",
    "045": "人物低头向前迈步，双臂被宽大黑色披巾交叠包裹在胸前，红发、肩后带结与衣摆保持原画后扬",
    "046": "双膝跪坐，身体挺直；一手竖直扶持高大的毛笔/长杆，另一手托住横向板状器物，所有书写道具保持接触",
    "047": "单膝深屈的低位拔刀/突进姿势，一手把长剑后拉至肩旁，另一手向下平衡，长发和蓝白衣摆后甩",
    "048": "双脚站稳并略向后仰，双臂交叉抱胸，头部抬起，宽肩、腹甲与裤甲保持原画夸张体块",
    "049": "深弓步下压，双手沿同一根超长枪杆上下分握并将其近乎竖直刺向地面，绿色披风形成背后大弧线",
    "050": "壮汉保持低蹲，一膝高抬、另一腿屈曲承重；一手持弯刀向下，另一手靠近口鼻，红裤与腰巾外展",
    "051": "向前腾空冲刺，一臂伸直指向前方，另一臂控制后方长柄兵器，双腿前后分离、外袍向后展开",
    "052": "盘腿坐姿，骨盆落地、双膝横展；一手在膝前持短管状兵器，另一手放松支撑，黑色外袍敞开",
    "053": "单腿鹤立，另一膝高抬；一手在肩上方展示纸卷/账册，另一手在胸前固定算盘/筹码架，长袍围绕承重腿展开",
    "054": "骑乘高速前冲的深棕战马，骑手伏低身体并维持原画手中长兵器/缰绳关系，披巾和马鬃向后飞扬",
    "055": "骑乘白马并向马颈前方俯身，持剑手沿马身方向向前下方动作，另一手牵缰，白色大披风向后形成宽弧",
    "056": "放松侧坐在低矮支撑面上，双腿自然垂落，一手持小酒壶/瓶，另一手支撑身体；可用简洁无装饰坐面替代树桩场景",
    "057": "单膝跪地并俯身靠近前方木质支撑物，一手掌向外伸出、另一手维持葫芦/道具接触，长须和披肩自然下垂",
    "058": "宽幅低马步，前膝屈曲，长棍斜搭在肩后并由一手固定，另一手扶在髋腿附近，红头巾后飘",
    "059": "女性骑手端坐于马鞍，一手控制长兵器/缰绳，另一手维持原画姿态；粉紫长袍、披帛和发饰随马行进后扬",
    "060": "人物腾空前冲，一拳向前下方有力伸出，持剑手在头肩后方高举长剑，双腿屈伸分离，白色衣带后扬",
    "061": "腾空挥鞭，一手高举链鞭手柄过头，链条围绕身体形成固定弧线，另一臂向外平衡，一膝抬起",
    "062": "朝观者奔跃，一臂高举流星锤/链枷过头，链球保持原画轨迹，另一臂后摆，一膝高抬、后腿蹬伸",
    "063": "高抬膝/踢腿姿势，双手把长剑举过头顶，躯干略后仰，白色长袖、腰带和裤脚向外飘展",
    "064": "深蹲防御姿态，一膝接近地面；圆盾固定在身体前侧，长枪尖端触地，另一臂弯曲越过头后，背后投掷器具不移位",
    "065": "直立持枪，长枪斜穿身体并由高低两手控制，圆盾固定在背后，蓝色披巾与衣摆保持原画展开",
    "066": "跪坐在简洁工作台/石面前，一手高举铁锤、另一手固定凿具，工具篮与腰间工具保持位置；不绘制山岩场景",
    "067": "双脚站立在同一基线，双手把长笛横举至嘴边演奏，头部侧转，长发、袖口和腰后披带统一向后飘",
    "068": "赤膊人物侧向奔跑，一手把弯刀横搭在肩颈后方，另一臂向后摆，前膝抬起、后腿蹬伸",
    "069": "头朝下前方的倒置潜水姿势，一臂向观者伸出、另一臂靠近身体，骨盆和双腿翻至头顶上方并屈曲",
    "070": "宽幅投掷姿势，胸腔扭转，一臂向侧后方伸展、另一臂控制横过身体的双刃/短柄兵器，双腿一前一后承重",
    "071": "深弓步投掷，一臂朝前展开多枚细针/飞镖，另一臂在头顶后方高举余下暗器，长袖和黑发后扬",
    "072": "人物腾空跃进，双手前后分握同一根长枪并使枪尖斜向前下方，一膝前收、另一腿向后折叠，红巾和长发后甩",
    "073": "腾空屈膝，一手持短链/软兵器向外甩出，另一手固定短棒/刀柄，白裤和绿色披巾保持向后展开",
    "074": "缓步直立，双臂自然垂落，头部略转，背后长剑固定不变；黑色长袍与头巾保持原画静态垂坠",
    "075": "宽幅挥铲动作，双手前后分握长柄大铲并将铲刃斜压向地面，躯干和骨盆强烈扭转，双腿撑开",
    "076": "腾空舞扇，双臂分别向左右展开两把打开的白扇，一膝高抬、另一腿向后，蓝色衣袍和长带旋转展开",
    "077": "直立吹笛，双手把横笛保持在嘴边，头部侧转，黑红长袍在脚边展开；灯笼背景全部移除",
    "078": "低位蹲伏，双膝深屈；双手在腰前持续控制短剑/刀鞘的拔出关系，背后剑柄和披肩固定",
    "079": "双脚大幅分开、躯干后仰、头部上抬，一手持剑下垂、另一臂向外；移除穿身箭矢和血迹等叙事元素但保持受击姿态",
    "080": "人物腾空横跃，双手在身体两侧分握同一根长枪，枪杆斜跨头顶和髋部，双腿一屈一伸形成宽轮廓",
    "081": "宽脚站立，双手在胸前上下分握同一把大菜刀/斩刀，刀刃竖直，躯干微前倾",
    "082": "稳固直立，一手把直剑斜举至肩前，另一手握拳伸向侧方，红黑衣摆向两侧展开",
    "083": "单腿承重、另一膝高抬，一手在头侧保持张指手势，另一手控制斜向地面的长棍，披巾与裤甲维持原画关系",
    "084": "侧向疾跑突刺，一臂把长剑水平向前伸出，另一臂后摆，前腿迈出、后腿追随，红披风与长发统一后扬",
    "085": "直立结印，双手在胸前保持相扣手印，双肘外展，头部正向；紫色宽袖和外袍自然垂下",
    "086": "极低蹲姿，一膝贴近地面，一手伸向地面拾取小物，另一手支撑在大腿/髋部，裸露上身前倾",
    "087": "宽脚站立并略侧身，一臂弯曲贴近腰侧、另一臂放松下垂，巨大的紫红头巾/肩结保持在头肩后方展开",
    "088": "站立锻造姿势，双手持续控制锤、夹钳与铁砧上的工件，胸腔前倾、双腿分开承重；保留简洁铁砧作为接触实体",
    "089": "上身向前探，一臂从头顶弧形越过并压住长发，另一手向观者伸出；原图未见下身部分按中立结构作克制站姿补全",
    "090": "竖直悬浮，头部大幅后仰、胸腔展开，双拳在身体两侧紧握，双膝轻屈并保持蓝绿色裤袍向下飘垂",
    "091": "低姿高速冲刺，一臂向前下方摆动、另一臂高举向后，前膝接近胸口、后腿蹬伸，长发沿速度方向后扬",
    "092": "深蹲蓄力，一手把短柄斧扛在肩后，另一前臂横压在抬起的大腿上，双脚宽距承重",
    "093": "自然直立微笑，双手收拢在宽大袖中并置于腹前，双脚并立；移除酒坛和砖墙背景",
    "094": "单膝跪地冲击姿势，一拳支撑/砸向地面，另一手把长弯刀向后上方拉开，躯干前倾；移除碎石飞溅但保留姿态",
    "095": "双脚宽幅站稳，双手把巨大弯刀高举过头准备下劈，红色长袍和腰绳外展；移除人头木桩等叙事物",
    "096": "略驼背直立，一手高举木拍/短棍，另一手在髋旁持红色小道具，长红发和胡须向两侧垂落",
    "097": "身体斜向腾空，一手把长弯刀举在头顶后方，另一手向前下方伸出，双腿收拢屈曲，蓝色披风后扬",
    "098": "四点着地的低伏姿态：双手和双脚接触地面、膝部外展、骨盆抬起、头部向前，黑帽保持固定",
    "099": "低蹲在高处边缘的姿态，双臂向左右展开并各持一柄弯刀，一膝屈曲、一脚支撑；移除屋顶但保留蹲伏平衡",
    "100": "宽幅下蹲，双手分别控制两件短棍/双节兵器横过身体，双肘外展、双脚分开，披肩保持后垂",
    "101": "一脚踩在简洁低凳/台阶上，抬膝侧向打开，一手扶抬起的大腿、另一手叉腰，粉白长裙围绕双腿展开",
    "102": "放松坐地，一腿屈膝竖起、另一腿弯曲铺开，一手扶持长柄镐/锄靠在肩后，另一手支撑身体；移除树木背景",
    "103": "女性角色斜向腾空，双臂向左右展开并各持短刃，双腿向后屈曲，长发与红色腰带飘带后扬",
    "104": "朝观者冲刺，一臂在胸前横持短棒/短刃，另一手向下前方伸出，一膝高抬、后腿蹬伸；移除雷电与残影",
    "105": "正向稳固站立，一手竖直扶持巨大旗杆、另一手持弯刀向下，红披风下垂；旗面黑色笔触仅保留不可读抽象图形",
    "106": "低位蹲坐，一手伸入身侧木桶/容器内，另一手支撑在膝部，草帽和白色披衣保持原画遮挡；保留简洁木桶作为接触实体",
    "107": "悬挂攀爬姿态，一手高举抓握横向木梁，另一臂向外平衡，双腿屈曲并以脚部抵住竖向支撑，背后大布包固定；只保留最简支撑梁",
    "108": "人物侧身站立并贴靠黑马头颈，一手抚触马脸/缰绳，另一臂靠近身体，黑马从人物身后向前探头；腰间绳索与佩剑固定",
}
VIEWS = [
    "left-profile-counterclockwise-45-degree",
    "left-profile",
    "front",
    "back",
    "right-profile",
    "right-profile-clockwise-45-degree",
]

STYLE_POSITIVE = (
    "画风固定为1999–2000年中国水浒英雄收藏卡式二维手绘商业插画。使用深黑或深褐色、粗细有变化且略带手绘起伏的墨线："
    "外轮廓醒目，内部结构线清楚。保留原卡高饱和但非荧光的综合色彩和鲜明冷暖对比，以清晰基色色块塑造造型，每种主要材质使用约2至4档可辨认的结构阴影与高光；"
    "硬边色块为主，局部结合马克笔、水彩/水粉、喷笔式柔和过渡、短排线和干笔纹理。人物保持成年英雄漫画感、棱角明确的五官和扎实人体结构；"
    "皮肤、布料、金属、皮革、木材和毛发都以简洁的方向性手绘笔触区分。整体必须保持清楚二维轮廓、纸本手绘质感和复古商业卡画气质，但画面本身干净高清，不模拟旧印刷损伤。"
    "所有视角使用完全一致的描线、综合色阶、纹理密度和统一光源。"
)

STYLE_NEGATIVE = (
    "不要纯赛璐璐动画上色，不要只有单层硬阴影的扁平动漫图；不要无描线半厚涂、油画厚涂或现代手游宣传画；"
    "不要照片写实、电影概念艺术、3D、CGI、PBR、ZBrush雕塑感、塑料或树脂手办质感、平滑全局光照、景深和镜头炫光；"
    "不要现代萌系、幼态脸、统一网红脸、矢量图、等粗线、波普网点。不要纸张泛黄、扫描噪点、印刷网点、折痕、套色偏移、卡框、文字、标题或水印。"
)


def compact_list(values: list[str]) -> str:
    return "；".join(v.strip() for v in values if v.strip()) or "无额外记录"


def source_for(cid: str, spec: dict) -> Path:
    direct = WORKSPACE / "images" / f"{cid}.png"
    if direct.exists():
        return direct.resolve()
    return Path(spec["source"]).expanduser().resolve()


def entity_summary(spec: dict) -> tuple[str, str, str, bool, bool, bool]:
    entities = spec.get("entities", {})
    weapon = entities.get("weapon", {})
    mount = entities.get("mount", {})
    pet = entities.get("pet", {})
    wp = weapon.get("presence") == "present"
    mp = mount.get("presence") == "present"
    pp = pet.get("presence") == "present"
    return (
        compact_list(weapon.get("items", [])) if wp else "无武器或标志道具",
        compact_list(mount.get("items", [])) if mp else "无坐骑",
        compact_list(pet.get("items", [])) if pp else "无宠物",
        wp,
        mp,
        pp,
    )


def pose_record(cid: str, has_mount: bool) -> tuple[str, str, str]:
    if cid == "108":
        pose = (
            "冻结原画中人物侧身站立并贴靠黑马头颈的互动姿态：保持人物头部、视线、双肩、双臂、手指、胸腔、骨盆、双腿重心和脚部接地；"
            "保持人物与马头、马颈、肩部的相对位置及手部接触点。"
        )
        relation = (
            "同一匹黑马始终贴近人物身后与侧面，人物手部持续接触同一马头/马颈位置；缰绳、腰间绳索、佩剑与全部连接点共同旋转，不将互动改成骑乘。"
        )
    elif has_mount:
        pose = (
            "冻结原画可见的骑乘动作：保持人物头部、视线、双肩、双臂、手势、胸腔、骨盆、双腿夹持、膝踝角度、脚在马镫中的位置，以及坐骑头颈、躯干和四肢姿态。"
        )
        relation = (
            "人物、同一匹坐骑、鞍具、缰绳、马镫、腿部夹持、手部牵引以及原画中持续持握的武器组成一个冻结组合；所有接触点共同旋转，不换手、不换腿、不移动坐骑。"
        )
    else:
        pose = (
            "冻结原画可见动作：保持头部朝向与视线、左右肩肘腕、手势与抓握、胸腔和骨盆扭转、重心、双腿前后关系、膝踝角度及脚部接地或腾空状态；"
            "原图裁切或遮挡的肢体只按现有中立六视图作最克制、易修改的结构性补全。"
        )
        relation = (
            "人物与原画中持续持握、穿戴、牵引或倚靠的实体组成一个冻结组合；保持左右手身份、抓握点、实体长度、身体相对路径、收纳和接触位置，不添加无证据实体。"
        )
    hint = POSE_HINTS.get(cid)
    if hint:
        pose = f"原画具体姿态：{hint}。{pose}"
    motion = (
        "冻结原画可见的头发、头巾、披风、披帛、衣袖、衣摆、飘带及附着部件的根部连接、弧线、层叠和飘动方向；"
        "若原图没有明显飘动，则保持其自然静态。六列不得重新计算风向。"
    )
    return pose, motion, relation


def variant_for(cid: str, spec: dict) -> dict:
    _, _, _, _, has_mount, _ = entity_summary(spec)
    pose, motion, relation = pose_record(cid, has_mount)
    return {
        "id": "original-pose-turnaround",
        "kind": "original-pose-turnaround",
        "status": "approved" if cid in SAMPLE_IDS else "planned",
        "output": "character-turnaround-original-pose.png",
        "purpose": "保留原画动作、服装动态、手持物及人物与实体接触关系的独立六视图，不覆盖默认中立结构版。",
        "views": VIEWS,
        "pose": pose,
        "costume_motion": motion,
        "entity_relations": relation,
        "background": "plain warm light gray neutral; no narrative scenery, effects, text, labels, border, or watermark",
    }


def ensure_variant(spec: dict, cid: str) -> dict:
    generation = spec.setdefault("generation", {})
    variants = generation.setdefault("variants", [])
    for item in variants:
        if item.get("id") == "original-pose-turnaround" or item.get("kind") == "original-pose-turnaround":
            if cid in SAMPLE_IDS:
                item["kind"] = "original-pose-turnaround"
                item["status"] = "approved"
            elif item.get("status") == "planned":
                item.update(variant_for(cid, spec))
            return item
    item = variant_for(cid, spec)
    variants.append(item)
    return item


def ensure_style_profile(spec: dict) -> None:
    generation = spec.setdefault("generation", {})
    profile = generation.setdefault("style_profile", {})
    old_notes = profile.get("notes", [])
    if not isinstance(old_notes, list):
        old_notes = [str(old_notes)]
    note = "2026-08-21 用户确认原画姿态版三个样例；016 仅作为描线、上色、纹理密度、统一光源和版式完成度锚点，不提供当前角色设计。"
    if note not in old_notes:
        old_notes.append(note)
    profile.update(
        {
            "id": "xiaohuanxiong-shuihu-1999-2000-hand-painted-card",
            "status": "approved",
            "style_anchor_reference": str(STYLE_ANCHOR),
            "notes": old_notes,
        }
    )


def prompt_for(cid: str, spec: dict, variant: dict) -> str:
    character = spec.get("character", {})
    identity = character.get("identity", {})
    weapon, mount, pet, has_weapon, has_mount, has_pet = entity_summary(spec)
    anchors = character.get("asymmetric_anchors", [])
    identity_text = "；".join(
        f"{key}：{identity.get(key)}"
        for key in ("gender_presentation", "apparent_age", "face", "hair", "facial_hair", "body_type", "body_proportions")
        if identity.get(key)
    )
    refs = [
        "图1为当前角色原画，是姿态、手势、服装动态、抓握、骑乘/接触关系、身份、造型和配色的最高依据",
        "图2为当前角色中立六视图，只补充图1看不见的侧面与背面结构，不得继承中立站姿",
    ]
    next_index = 3
    if not (has_weapon and has_mount):
        refs.append(f"图{next_index}为当前角色头部四视图，只锁定身份、头饰与头颈比例")
        next_index += 1
    refs.append(
        f"图{next_index}为已批准的016姿态版风格锚点，只负责描线、上色、纹理密度、统一光源和版式；"
        f"禁止复制图{next_index}的人脸、发型、体型、服装、甲胄、配色或动作"
    )
    next_index += 1
    if has_weapon:
        refs.append(f"图{next_index}为当前角色武器表，只补充同一武器的完整轮廓、背面、握持和收纳结构")
        next_index += 1
    if has_mount:
        refs.append(f"图{next_index}为当前角色坐骑表，只补充同一坐骑及鞍具、缰绳和远侧结构；姿态仍以图1为准")
        next_index += 1
    if has_pet:
        refs.append(f"图{next_index}为当前角色宠物表，只补充同一宠物的远侧结构与尺度；互动仍以图1为准")

    return f"""Use case: stylized-concept
Asset type: 角色原画姿态版专业六视图设定表
Input images: {'；'.join(refs)}。若参考冲突，严格按图1原画可见事实 > 当前角色头部参考（若单独提供） > 图2结构性补全 > 016风格锚点处理。

为图1中的同一个角色制作独立原画姿态版六视图，不覆盖、改名或降级现有 character-turnaround.png。
角色身份：{identity_text}
必须保留：{compact_list(character.get('must_preserve', []))}
服装层级：{compact_list(character.get('costume_layers', []))}
原图可确认：{compact_list(spec.get('evidence', {}).get('confirmed', []))}
结构性推断：{compact_list(spec.get('evidence', {}).get('inferred', []))}
保持克制或未知：{compact_list(spec.get('evidence', {}).get('unknown', []))}
武器/标志道具：{weapon}
坐骑：{mount}
宠物：{pet}
非对称三维锚点：{json.dumps(anchors, ensure_ascii=False) if anchors else '无已记录的永久左右非对称锚点；仍须保持原画手势、抓握和肢体左右身份。'}

【冻结三维组合体】
姿态与手势：{variant['pose']}
服装与附着动态：{variant['costume_motion']}
实体与接触关系：{variant['entity_relations']}
六列必须是这一个冻结组合体从六个观察方向看到的结果。整个人物、四肢、手指、衣物动态、武器/道具、坐骑、宠物及所有接触点共同绕竖直轴旋转；不得逐列重新摆动作、换手、改变腿部前后关系、改变握持点、重算风向、移动实体或用表情变化代替视角变化。

画面从左到右严格且仅排列：
1. 只以第二列角色自身纯左面为基准，把完整冻结组合体绕竖直轴逆时针旋转45度；
2. 角色自身纯左面；
3. 纯正面，最接近原画可见动作关系；
4. 同一冻结组合体的纯背面；
5. 角色自身纯右面；
6. 只以第五列角色自身纯右面为基准，把完整冻结组合体绕竖直轴顺时针旋转45度。
第一列与第六列必须来自相反侧面基准，呈现相反近侧脸颊、肩膀、手臂、髋、腿、衣物透视、实体投影和远侧遮挡；不得复制、复用或水平翻转。第二列与第五列必须是相反解剖侧的纯侧面，第三列与第四列必须是纯正面与纯背面。每列内部的头、胸腔、骨盆、膝、脚、抬起肢体、衣物动态及实体共享同一偏航角。

原画中的雷电、火焰光环、岩石、烟雾、云层、水花、速度线、光球、题字牌、卡框、地面文字和纯叙事背景默认排除；只保留规格确认属于人物设计或持续接触的实体。使用非常宽的偏暖白或浅中性灰横向画布，六套冻结组合同尺度、同地面基准、均匀分栏。动作或长武器扩大轮廓时缩小整套组合并增加留白；完整展示头顶、手指、脚、衣摆、武器端点、坐骑和宠物，不得裁切或相邻重叠。

{STYLE_POSITIVE}

{STYLE_NEGATIVE}

不要标题、标签、编号、水印、边框、额外人物、额外动物、多余肢体、错误手指、重复武器、重复坐骑、融合结构或文字乱码。保持图1当前角色的独特脸型、年龄、体型、服装、纹样、配色和动作；绝不从016风格锚点复制任何人物设计。
"""


def refs_for(cid: str, spec: dict) -> list[str]:
    turnaround = (CHARACTERS / cid / "character-turnaround.png").resolve()
    head = (CHARACTERS / cid / "head-sheet.png").resolve()
    if not head.exists():
        # 008 and 021 keep the approved head views embedded in the turnaround.
        head = turnaround
    _, _, _, has_weapon, has_mount, has_pet = entity_summary(spec)
    refs = [str(source_for(cid, spec)), str(turnaround)]
    if not (has_weapon and has_mount):
        refs.append(str(head))
    refs.append(str(STYLE_ANCHOR))
    for present, name in (
        (has_weapon, "weapon-sheet.png"),
        (has_mount, "mount-sheet.png"),
        (has_pet, "pet-sheet.png"),
    ):
        path = (CHARACTERS / cid / name).resolve()
        if present and path.exists():
            refs.append(str(path))
    return refs


def main() -> None:
    jobs = []
    for spec_path in sorted(CHARACTERS.glob("*/character-spec.json")):
        cid = spec_path.parent.name
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        ensure_style_profile(spec)
        variant = ensure_variant(spec, cid)

        review = spec.setdefault("review", {}).setdefault("notes", [])
        if cid in SAMPLE_IDS:
            note = "2026-08-21 用户确认原画姿态版样例标准，变体状态更新为 approved。"
            if note not in review:
                review.append(note)

        spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        if cid in SAMPLE_IDS:
            continue
        prompt_path = spec_path.parent / "original-pose-prompt.txt"
        prompt_path.write_text(prompt_for(cid, spec, variant), encoding="utf-8")
        output = spec_path.parent / variant["output"]
        if not output.exists():
            refs = refs_for(cid, spec)
            missing = [ref for ref in refs if not Path(ref).exists()]
            if missing:
                raise FileNotFoundError(f"{cid}: missing references: {missing}")
            jobs.append(
                {
                    "id": cid,
                    "prompt": str(prompt_path.resolve()),
                    "references": refs,
                    "output": str(output.resolve()),
                }
            )

    (PROJECT / "original-pose-jobs.json").write_text(
        json.dumps({"count": len(jobs), "style_anchor": str(STYLE_ANCHOR), "jobs": jobs}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"prepared={len(jobs)} approved_samples={len(SAMPLE_IDS)} style_anchor={STYLE_ANCHOR}")


if __name__ == "__main__":
    main()
