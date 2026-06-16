# 2026 World Cup AI Content

**技術架構：** Astro 靜態站 · AI 批次生成內容 · 上傳即部署

## 專案方向（A+B）

- **A：每日世足 AI 預測** — 賽前預測比分/勝率/看點，賽後覆盤對比
- **B：足球放大鏡故事短文** — 每場關鍵比賽的戲劇張力短文

---

## 專案結構

```
src/
├── pages/
│   ├── index.astro              ← 每日總覽（賽程 + 預測卡片）
│   ├── standings.astro          ← 小組排名表
│   └── matches/
│       └── [id].astro           ← 單場深度分析（動態路由）
├── components/
│   ├── Header.astro             ← 導航列（含 matchday badge）
│   ├── Footer.astro             ← 免責聲明 + 版權
│   ├── MatchCard.astro          ← 比賽預測卡片（含賠率 details）
│   ├── PredictionMeter.astro    ← 勝率視覺化 bar
│   ├── TeamAnalysis.astro       ← 隊伍分析（近況/關鍵球員/外電）
│   ├── StandingsTable.astro     ← 小組積分表
│   ├── StorySection.astro       ← 故事短文區
│   └── OddsAnalysis.astro       ← 賠率深潛
├── layouts/
│   └── Base.astro               ← HTML shell + 全域樣式
├── data/
│   ├── today-matches.json       ← AI 產出：當日賽程 + 預測
│   ├── matches/{id}.json        ← AI 產出：單場深度分析
│   └── standings.json           ← AI 產出：小組排名
prompt-spec/
    └── README.md                ← Prompt input/output 契約
```

## 內容生產管線

```
ESPN API ──→ AI Layer（5 個專用 prompt）
                │
                ├─ ① 隊伍調查員 → 產出 teamAnalysis
                ├─ ② 勝率分析師 → 產出 prediction
                ├─ ③ 賠率解讀員 → 產出 oddsAnalysis
                ├─ ④ 故事作家   → 產出 story
                └─ ⑤ 總編輯     → 收斂為最終 JSON
                │
                ▼
        寫入 src/data/*.json
                │
                ▼
        astro build → dist/ → 部署
```

## 頁面

| 路由 | 頁面 | 資料來源 |
|------|------|---------|
| `/` | 每日總覽 | `today-matches.json` |
| `/standings` | 小組排名 | `standings.json` |
| `/matches/:id` | 單場分析 | `matches/{id}.json` |

---

## 資料來源總覽

### 來源一：ESPN 非官方 API ✅ 確認可用（即時）

| 項目 | 說明 |
|------|------|
| 網址 | `https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard` |
| 認證 | 不需任何 key，完全免費 |
| Rate limit | 無觀察到限制 |
| 狀態 | ✅ 確認回傳 2026 世足即時資料 |

**scoreboard 端點** — 拿每日賽程

```
GET /scoreboard
GET /scoreboard?dates=20260617         ← 指定日期（YYYYMMDD）
```

回傳欄位：
- `events[].id` — 比賽唯一 ID
- `events[].name` — 「Cape Verde at Spain」
- `events[].status.type.description` — "Full Time" / "Scheduled" / "In Progress"
- `events[].competitions[].venue.fullName` — 場館
- `events[].competitions[].broadcasts` — 轉播資訊
- `events[].competitions[].competitors` — 隊伍、比分

實測資料（2026-06-16）：
```
Cape Verde at Spain | Full Time | Mercedes-Benz Stadium
Egypt at Belgium    | Full Time | Lumen Field
Uruguay at Saudi Arabia | Full Time | Hard Rock Stadium
New Zealand at Iran | Full Time | SoFi Stadium
```

**summary 端點** — 單場詳細資料

```
GET https://site.web.api.espn.com/apis/site/v2/sports/soccer/fifa.world/summary?event={event_id}
```

回傳欄位（極豐富）：
| 欄位 | 內容 | 用途 |
|------|------|------|
| `header` | 比賽資訊（隊伍、比分、狀態） | A 預測 baseline |
| `boxscore` | 兩隊完整統計數據 | A 分析素材 |
| `commentary` | 逐球評述（實測 98 條/場） | B 故事短文原料 |
| `keyEvents` | 關鍵事件（進球、紅牌、VAR） | B 故事高光 |
| `leaders` | 最佳球員統計 | A 預測參考 |
| `odds` | 賠率 | A 預測參考 |
| `standings` | 小組排名 | A 分析 context |
| `rosters` | 球員名單 | 球隊分析 |
| `news` / `videos` / `article` | 媒體內容 | 額外素材 |
| `broadcasts` | 轉播資訊 | 發文附註 |

**commentary 實測範例**（Cape Verde vs Spain）：
```
Lineups are announced and players are warming up.
First Half begins.
Ryan Mendes (Cabo Verde) wins a free kick in the defensive half.
Foul by Marc Cucurella (Spain).
VAR Decision: Other Decision Cancelled.
```

> ⚠️ 非官方端點，無 SLA，可能隨時異動。

---

### 來源二：openfootball/worldcup.json ✅ 確認可用（靜態 baseline）

| 項目 | 說明 |
|------|------|
| 網址 | `https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json` |
| 授權 | CC0 公領域，完全免費 |
| Rate limit | 無（GitHub raw） |
| 更新頻率 | 每日 |
| 資料量 | 全 104 場比賽 |

回傳結構：
```json
{
  "name": "World Cup 2026",
  "matches": [
    {
      "round": "Matchday 1",
      "date": "2026-06-11",
      "time": "13:00 UTC-6",
      "team1": "Mexico",
      "team2": "South Africa",
      "score": {"ft": [2, 0], "ht": [1, 0]},
      "goals1": [{"name": "Julián Quiñones", "minute": "9"}, ...],
      "goals2": [],
      "group": "Group A",
      "ground": "Mexico City"
    }
  ]
}
```

**適合用途：**
- 賽程表 baseline（誰對誰、何時、何地）
- 歷史比分查詢
- 每日 cron 拉一份當 ground truth

**不適合：**
- 即時比分（更新有延遲 12-24h）
- 詳細統計數據

---

### 來源三：worldcup26.ir API ✅ 確認可用（即時，最完整）

| 項目 | 說明 |
|------|------|
| 網址 | `https://worldcup26.ir/get/games` |
| 認證 | Read 端點不需 key（GitHub 作者聲明） |
| 文件 | `https://worldcup26.ir/api-docs/`（Swagger UI） |
| 原始碼 | `github.com/rezarahiminia/worldcup2026` |
| 技術棧 | Node.js + Express + MongoDB，開源可自架 |

端點列表：
| 端點 | 內容 |
|------|------|
| `GET /get/games` | 全 104 場比賽 |
| `GET /get/groups` | 12 組小組排名 |
| `GET /get/teams` | 48 隊資訊 |
| `GET /get/stadiums` | 16 球場資訊 |

**/get/games 單筆欄位：**
```json
{
  "id": "6",
  "home_team_id": "15",
  "away_team_id": "16",
  "home_score": "2",
  "away_score": "0",
  "home_scorers": "{\"Nestory Irankunda 27'\",\"C. Metcalfe 75'\"}",
  "away_scorers": "null",
  "group": "D",
  "matchday": "1",
  "local_date": "06/13/2026 21:00",
  "finished": "TRUE",
  "time_elapsed": "finished",
  "home_team_name_en": "Australia",
  "away_team_name_en": "Turkey",
  ...
}
```

**/get/groups 單筆：**
```json
{
  "name": "A",
  "teams": [{"team_id": "1", "mp": "1", "w": "1", "l": "0", "d": "0", "pts": "3", "gf": "2", "ga": "0", "gd": "2"}, ...]
}
```

**/get/teams 單筆：**
```json
{
  "name_en": "Mexico",
  "flag": "https://flagcdn.com/w80/mx.png",
  "fifa_code": "MEX",
  "iso2": "MX",
  "groups": "A"
}
```

> ⚠️ 小型專案，流量承載未經高壓驗證。建議當備援，必要時可自架。

---

### 來源四（次要）：Wikipedia

| 項目 | 說明 |
|------|------|
| 網址 | `en.wikipedia.org/wiki/2026_FIFA_World_Cup` |
| 擷取方式 | MediaWiki API `action=parse` |
| 優點 | 群眾維護，更新極即時，穩定 |
| 缺點 | Parse 成本較高，結構需清理 |

---

### 來源五（待驗證）：football-data.org

| 項目 | 說明 |
|------|------|
| 網址 | `api.football-data.org/v4/` |
| 免費 tier | 10 req/min |
| 世界盃涵蓋 | ⚠️ 不確定免費 tier 是否包含，需註冊驗證 |
| 建議 | 既有來源已足夠，此為備援選項 |

---

## 推薦資料串接架構

```
每天早上 8:00 cron：

1. ESPN scoreboard（當日賽程 + 前日結果）
   → 產出 A 素材：今天有哪些比賽

2. ESPN summary（昨日重點場次，逐場 call）
   → 產出 B 素材：commentary + keyEvents

3. openfootball worldcup.json（靜態 baseline，備援）
   → 比對 ESPN 資料一致性

4. worldcup26.ir（備援）
   → 當 ESPN 掛掉時的 fallback

5. AI 層：
   拿到資料後 → web research 球隊近況
             → 產出 A：每日預測圖文
             → 產出 B：故事短文
```

**實際上最簡可行：只要 ESPN API 一個來源就夠了。**
ESPN scoreboard 給賽程 + 比分，ESPN summary 給 commentary + stats + key events。其他都是備援。

---

## 每日生產管線（草案）

```
[資料層]                        [AI 層]                         [發佈層]
ESPN scoreboard ──→ 今日賽程  ──→ AI 預測分析      ──→ Threads 圖文 A
ESPN summary   ──→ 昨日戰報  ──→ AI 故事短文      ──→ Threads 短文 B
                         └──→ web research 球隊狀態
```

---

## 注意事項

1. **ESPN API 無 SLA** — 若掛掉，降級到 openfootball（延遲 12-24h）+ worldcup26.ir
2. **世界盃只有一個月**（6/11-7/19）— 內容生產節奏要快，錯過就沒了
3. **圖片素材** — 比賽圖片需其他來源（ESPN 不直接回傳圖片），可考慮：
   - 免費圖庫 + 球隊標誌 overlay
   - AI 生成示意圖（需注意版權）
