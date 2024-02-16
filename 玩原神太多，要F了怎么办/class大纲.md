Settings类
Audio类
Camera类

UI类
    isLive
    UIStartX
    UIStartY
    - Skill类
        isSelect
    - DialogBox类
        text、fontColor、fontSize
        textStartX
        textStartY
        icon
        iconStartX
        iconStartY
    - SelectBox类（战斗时的选择框）
        isFixed（用于判断是敌方的还是我方的，我方的不是固定的，敌方的是固定的）

    - Tip类
        text、fontColor、fontSize
        textStartX
        textStartY
        isYorN

    - Commit类
    - Cancel类
    
    - Indicator类
    - EnergyBar类

    - HideBox类
    - Teleport类

    - Pager类（翻页器）

Scene类
    Menu类
        - UI类 -Tip类
    MainMap类
        - UI类 -DialogBox类
        - UI类 - Tip类
        - UI类 - EnergyBar类
        - Obstacle类
        - Player类
        - Enemy类
        - NPC类
    PreviewMap类
        - UI类 - Tip类
        - UI类 - HideBox类
        - UI类 - Teleport类
    BattleField类
        playerList=[Cake]
        enemyList=[Cake]
        - UI类 - Skill类
        - UI类 - SelectBox类
        - UI类 - EnergyBar类
        - UI类 - Indicator类
        - cake类
    Bag类
        - UI类 - SelectBox类
        - Pager类

Warehouse类
    - Cake类
    - Source类

Source类
    num

Cake类
    hp
    pp
    atk
    dfc
    flavor
    skillList=[Skill]
    - UI类 -Skill类

Obstacle类
    isLive
    isPassable

Player类
    isBattling
    isTalking
    cakeList=[Cake]
    - Cake类

Enemy类
    isBattling
    battleTimer
    - Cake类

NPC类
    isLive
    isTalking
    cakeList=[Cake]
    - Cake类

SceneManager类

GameLogic类
