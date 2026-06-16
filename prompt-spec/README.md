# Prompt Layer — Data Contract Spec

> Astro 前端與 AI 生成層之間的介面契約。
> AI 批次產出 JSON → 寫入 `src/data/` → Astro build 時讀取 → 渲染靜態 HTML。

---

## 目錄

1. [`today-matches.json` — 每日總覽](#1-today-matchesjson--每日總覽)
2. [`matches/{id}.json` — 單場深度分析](#2-matchesidjson--單場深度分析)
3. [`standings.json` — 小組排名](#3-standingsjson--小組排名)

---

## 1. `today-matches.json` — 每日總覽

**對應頁面：** `index.astro`
**生成頻率：** 每日一次（早上）
**Prompt 輸入：** ESPN scoreboard（當日賽程） + ESPN odds + AI web search（全球媒體預測共識）

```jsonc
{
  "date": "2026-06-17",
  "matchday": 4,
  "stage": "Group Stage",
  "headline": "死亡之組開戰：英格蘭 vs 克羅埃西亞",
  "matches": [
    {
      "id": "760431",
      "homeTeam": "Jordan",
      "awayTeam": "Austria",
      "group": "E",
      "venue": "Rose Bowl, Pasadena",
      "kickoff": "2026-06-17T13:00Z",
      "status": "scheduled",            // scheduled | live | finished
      // ——— AI 預測區塊 ———
      "prediction": {
        "winner": "home",               // home | away | draw
        "confidence": 65,               // 0-100
        "homeWinPct": 45,               // 主勝 %
        "drawPct": 25,                  // 平局 %
        "awayWinPct": 30,               // 客勝 %
        "predictedScore": "2-1",
        "overUnder": "over 2.5",
        "analysis": "Jordan 在資格賽展現強大主場氣勢，但 Austria 經驗更豐富。預計雙方都有進球的小比分比賽。",
        "keyFactor": "Austria 中場控制力將決定比賽節奏"
      },
      // ——— 賠率分析 ———
      "oddsAnalysis": {
        "provider": "DraftKings",
        "homeOdds": 2.10,
        "drawOdds": 3.20,
        "awayOdds": 3.50,
        "spread": "-0.5",
        "overUnder": "2.5",
        "impliedHomeWinPct": 47.6,       // 賠率反推的市場隱含勝率
        "valueGap": -2.6,                // AI 勝率 - 市場勝率（負=市場更看好）
        "verdict": "市場輕微看好 Jordan，但差距在誤差範圍內"
      }
    }
    // ... 更多比賽
  ]
}
```

---

## 2. `matches/{id}.json` — 單場深度分析

**對應頁面：** `matches/[id].astro`
**生成頻率：** 每場比賽產一篇（賽前預測版 + 賽後更新版）
**Prompt 輸入：** ESPN summary（完整場次資料） + scoreboard（比分） + AI web search（兩隊近況、傷病、外電）

```jsonc
{
  "match": {
    "id": "760428",
    "homeTeam": "Spain",
    "awayTeam": "Cape Verde",
    "group": "H",
    "venue": "Mercedes-Benz Stadium, Atlanta",
    "kickoff": "2026-06-15T16:00Z",
    "status": "finished",
    "score": { "home": 0, "away": 0 },
    "highlights": "Cape Verde 爆冷逼平歐洲冠軍 Spain"
  },

  // ——— A：預測覆盤（賽後模式） ———
  "prediction": {
    "preMatchPrediction": { ... },       // 同 today-matches prediction 格式
    "postMatchReview": "AI 模型預測 Spain 勝率 72%，但 Cape Verde 鐵桶陣奏效。低估了 Cape Verde 的防守組織能力。",
    "accuracy": "wrong"                  // correct | wrong | partial
  },

  // ——— A：隊伍分析 ———
  "teamAnalysis": {
    "home": {
      "name": "Spain",
      "fifaRank": 8,
      "form": ["W", "W", "D", "W", "L"],    // 近五場
      "keyPlayers": [
        { "name": "Pedri", "role": "中場發動機", "stat": "傳球成功率 94%" }
      ],
      "strength": "控球主導，中場控制力頂尖",
      "weakness": "面對鐵桶陣缺乏破解手段",
      "webSummary": "從近期外電與社群媒體分析的隊伍狀態摘要（AI web search 摘要）"
    },
    "away": { /* 同上 */ }
  },

  // ——— B：故事短文 ———
  "story": {
    "title": "鐵桶陣的尊嚴：Cape Verde 如何讓歐洲冠軍踢了一場悶球",
    "narrative": "融合 commentary + keyEvents 淬煉的 300-500 字故事短文...",
    "dramaticMoment": "第 67 分鐘，Cape Verde 門將 Vozinha 撲出 Pedri 的禁區外冷箭——這球如果進了，比賽走向會完全不同。",
    "turningPoint": "上半場第 15 分鐘的 VAR 改判，改寫了比賽基調",
    "quote": "「我們不是來觀光的。」——Cape Verde 賽後訪問"
  },

  // ——— 賠率/數據分析 ———
  "oddsDeepDive": "從歷史數據來看，讓一球以上的強隊在 World Cup 小組賽的勝率僅 58%。Spain 讓 1.5 球的盤口，歷史同盤口的上盤率更低。Cape Verde 受讓是 statistical value bet。",
  "boxscoreSummary": "Spain 27 次射門 7 次射正 vs Cape Verde 6 次射門 1 次射正。控球率 74% vs 26%。典型的強攻 vs 死守數據。"
}
```

---

## 3. `standings.json` — 小組排名

**對應頁面：** `standings.astro`
**生成頻率：** 每日更新
**Prompt 輸入：** ESPN summary（standings 區塊） + AI 分析

```jsonc
{
  "date": "2026-06-17",
  "matchday": 4,
  "groups": [
    {
      "name": "A",
      "teams": [
        {
          "name": "Uruguay",
          "flag": "https://flagcdn.com/w80/uy.png",
          "gp": 1,           // games played
          "w": 0, "d": 1, "l": 0,
          "gf": 1, "ga": 1, "gd": 0,
          "pts": 1,
          "status": "alive"  // alive | eliminated | clinched
        }
        // ...
      ],
      "analysis": "A 組目前情勢混沌，Uruguay 與 Saudi Arabia 各取 1 分，第二輪將是分水嶺。",
      "predictedAdvancers": 2  // 預測幾隊能晉級
    }
    // ... 12 組
  ],
  "knockoutBracket": null  // 淘汰賽階段才填入
}
```

---

## Prompt 架構總覽

```
                      ┌─────────────────────────┐
                      │   ⑤ 總編輯 prompt        │
                      │   收斂所有產出，決定最終   │
                      │   版面配置與篇幅分配      │
                      └──────────┬──────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
  ┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
  │ ① 隊伍調查員  │    │ ② 勝率分析師      │    │ ③ 賠率解讀員      │
  │ input: 隊名   │    │ input: 兩隊統計    │    │ input: odds 數據  │
  │ output:      │    │ output: 勝率/讓球  │    │ output: 價值判斷  │
  │ 近況/傷兵/    │    │ /大小球預測       │    │ /歷史盤口對比     │
  │ 風格/關鍵球員 │    └──────────────────┘    └──────────────────┘
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │ ④ 故事作家    │
  │ input:       │
  │ commentary + │
  │ keyEvents    │
  │ output:      │
  │ 300-500 字   │
  │ 故事短文     │
  └──────────────┘
```

每個 prompt 的詳細規格（input 格式、output 格式、範例、注意事項）待逐一展開。
