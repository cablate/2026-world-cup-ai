# 每日更新管線（AI 執行流程）

## 每日生產流程

### Step 0：撈 ESPN 資料

```bash
# 拿今日賽程（換日期即可）
curl "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard?dates=20260617"

# 拿每場詳細資料（for 故事短文）
curl "https://site.web.api.espn.com/apis/site/v2/sports/soccer/fifa.world/summary?event={id}"

# 拿昨日賽果（換日期）
curl "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard?dates=20260616"
```

### Step 1 ~ 5：AI 內容生產

依序執行以下 prompt，每個 prompt 的規格見對應檔案：

| 步驟 | Prompt 檔 | Input 來源 | Output 目標 | 可平行？ |
|------|-----------|-----------|-----------|---------|
| 1 | `01-team-investigator.md` | ESPN scoreboard + summary + web search | 兩隊 teamAnalysis JSON | ✅ 每隊獨立 |
| 2 | `02-win-rate-analyst.md` | 兩隊 teamAnalysis + ESPN odds + H2H | prediction JSON | ✅ 每場獨立 |
| 3 | `03-odds-interpreter.md` | prediction + odds + teamAnalysis | oddsAnalysis JSON | ✅ 每場獨立 |
| 4 | `04-story-writer.md` | ESPN commentary + keyEvents + boxscore | story JSON | ✅ 有完成比賽才做 |
| 5 | `05-editor-in-chief.md` | 所有產出 + ESPN raw data + 系統日期 | 3 個最終 JSON 檔 | ❌ 單一收斂 |

### Step 6：寫入資料檔

```json
src/data/today-matches.json     ← 今日賽程 + 預測
src/data/matches/{id}.json      ← 單場深度（每場一個檔）
src/data/matches-by-date.json   ← 所有比賽按日期歸檔（自動更新）
src/data/standings.json         ← 小組排名（從 ESPN summary 獲取）
```

### Step 7：Build & Deploy

```bash
npm run build    # → dist/
# 上傳 dist/ 到部署目標
```

---

## 每日工作清單

### 早上（賽前）

- [ ] 撈今日 ESPN scoreboard（確認賽程無異動）
- [ ] 撈昨日 ESPN scoreboard（確認前日結果）
- [ ] 每個未開賽的比賽：
  - [ ] Web search 兩隊近況（傷兵、近期戰績、外媒評價）
  - [ ] 執行 prompt ①（隊伍調查員）
  - [ ] 執行 prompt ②（勝率分析師）
  - [ ] 執行 prompt ③（賠率解讀員）
- [ ] 執行 prompt ⑤（總編輯）→ 寫入 today-matches.json
- [ ] `npm run build`
- [ ] 部署

### 晚上（賽後）

- [ ] 每個完成的比賽：
  - [ ] 撈 ESPN summary（commentary + keyEvents + boxscore）
  - [ ] 執行 prompt ①（隊伍調查員，用真實統計）
  - [ ] 執行 prompt ②（勝率分析師，覆盤準確度）
  - [ ] 執行 prompt ④（故事作家）
- [ ] 更新 standings.json（從 ESPN summary 最新資料）
- [ ] 更新 matches-by-date.json
- [ ] 執行 prompt ⑤ → 更新 matches/{id}.json
- [ ] `npm run build`
- [ ] 部署

---

## 資料檔案結構

### `src/data/today-matches.json`
```jsonc
{
  "date": "2026-06-17",
  "matchday": 4,
  "stage": "Group Stage",
  "headline": "死亡之組開戰：英格蘭 vs 克羅埃西亞",
  "matches": [
    {
      "id": "760437",
      "homeTeam": "Croatia",
      "awayTeam": "England",
      "group": "L",
      "venue": "Allegiant Stadium, Las Vegas, Nevada",
      "kickoff": "2026-06-17T19:00Z",
      "status": "scheduled",
      "prediction": { /* ② 產出，含 winner/confidence/homeWinPct/drawPct/awayWinPct/predictedScore/overUnder/analysis/keyFactor */ },
      "oddsAnalysis": { /* ③ 產出，含 provider/homeOdds/drawOdds/awayOdds/spread/overUnder/impliedHomeWinPct/valueGap/verdict */ }
    }
  ]
}
```

### `src/data/matches/{id}.json`
```jsonc
{
  "match": {
    "id": "760428",
    "homeTeam": "Spain",
    "awayTeam": "Cape Verde",
    "homeScore": 0,
    "awayScore": 0,
    "group": "H",
    "venue": "Mercedes-Benz Stadium, Atlanta",
    "date": "2026-06-15",
    "matchday": 5,
    "status": "finished",
    "highlights": "Cape Verde 爆冷逼平歐洲冠軍 Spain"
  },
  "prediction": {
    "preMatchPrediction": { /* 賽前預測完整資料 */ },
    "postMatchReview": "賽後檢討文字...",
    "accuracy": "correct"
  },
  "teamAnalysis": {
    "home": { /* ① 產出 */ },
    "away": { /* ① 產出 */ }
  },
  "story": { /* ④ 產出 */ },
  "oddsDeepDive": "賠率分析文字段落...",
  "boxscoreSummary": "統計摘要文字..."
}
```

### `src/data/matches-by-date.json`
```jsonc
{
  "dates": ["2026-06-11", "2026-06-12", ...],
  "matches": {
    "2026-06-11": [
      { "id": "760415", "homeTeam": "Mexico", "awayTeam": "South Africa", "homeScore": 2, "awayScore": 0,
        "group": "A", "venue": "...", "status": "finished", "matchday": 1 }
    ]
  }
}
```

### `src/data/standings.json`
```jsonc
{
  "date": "2026-06-16",
  "matchday": 6,
  "stage": "Group Stage",
  "groups": [
    {
      "name": "A",
      "teams": [
        { "name": "Mexico", "flag": "https://flagcdn.com/w80/mx.png",
          "gp": 1, "w": 1, "d": 0, "l": 0, "gf": 2, "ga": 0, "gd": 2, "pts": 3, "status": "alive" }
      ],
      "analysis": "文字分析..."
    }
  ]
}
```

---

## 新增比賽日的操作

當新的一天有比賽：

1. **撈資料**：`curl ...scoreboard?dates=YYYYMMDD`
2. **更新 matches-by-date.json**：在對應日期 array 加入新比賽
3. **更新 today-matches.json**：改 date、matchday、headline、matches array
4. **執行 AI pipeline**（Step 1-5）
5. **更新 standings.json**：從 summary 取得最新小組排名
6. **Build**

## 目前已完成資料（seed）

| 日期 | Matchday | 比賽數 | 狀態 |
|------|---------|--------|------|
| 2026-06-11 | 1 | 2 | ✅ 完成（Mexico 2-0 South Africa, South Korea 2-1 Czechia） |
| 2026-06-12 | 2 | 2 | ✅ 完成 |
| 2026-06-13 | 3 | 3 | ✅ 完成 |
| 2026-06-14 | 4 | 5 | ✅ 完成 |
| 2026-06-15 | 5 | 4 | ✅ 完成 |
| 2026-06-16 | 6 | 3 | 🔄 今日（進行中） |

共 19 場比賽，12 組小組，48 隊。
