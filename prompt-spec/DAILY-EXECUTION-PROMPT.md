# 每日執行品質標準

我會在每一天的工作開始時，使用下方標準自我校準。這是我的品質控制系統，不是要自動化，而是確保每一次分析都有足夠的深度與廣度。

---

## 第一步：資料收集

```
curl "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard?dates=YYYYMMDD"
curl "https://site.web.api.espn.com/apis/site/v2/sports/soccer/fifa.world/summary?event={id}"
```

從 ESPN API 取得：賽程、比分、boxscore、commentary、keyEvents、odds、standings。

---

## 第二步：每場比賽的品質標準

每場比賽的分析必須涵蓋以下所有維度，缺一不可。

### 1. 賽前預測（prediction）

| 欄位 | 品質標準 |
|------|---------|
| `homeWinPct / drawPct / awayWinPct` | 三項總和 = 100。差距要有數據支撐（FIFA 排名差、近期戰績、歷史對戰），不憑感覺亂給 |
| `predictedScore` | 要合理。不給 8-0、7-0 這種誇張比數。最多差 4 球（如 4-0、5-1） |
| `confidence` | AI 對自己預測的信心值。當三項機率接近（如 35/30/35）時 confidence < 50；當某一方明顯佔優時 confidence > 70 |
| `analysis` | **至少 3 句話**：雙方實力對比 → 關鍵對決 → 預期的比賽劇本。不做「A 隊較強」一句話打發 |
| `keyFactor` | 要寫出具體可觀察的因子（特定球員對決、戰術環節、定位球、體能），不寫空話 |

### 2. 隊伍分析（teamAnalysis）

每隊的分析必須包含：

**2a. 關鍵球員（至少 2 人，重要比賽 3-4 人）**
- 名字（英文）、角色（中文）、一項有說服力的數據或背景
- 不好的範例：`{"name":"Neymar","role":"前鋒","stat":"N/A"}`
- 好的範例：`{"name":"Neymar","role":"傳奇 10 號","stat":"34 歲，隊史進球王，爭議性入選"}`

**2b. 優勢與劣勢**
- 各一句，要具體到可以被數據驗證
- 不好的範例：`"strength":"表現穩健"`（每個人都可以說表現穩健）
- 好的範例：`"strength":"控球主導、中場控制力"`（對照 possessionPct 可驗證）

**2c. webSummary（外電分析）**
- **至少 100 字**的完整段落
- 包含：FIFA 排名、近期戰績、核心戰術風格、本屆世界盃的目標或看點
- 要像球評寫的賽前分析，不是填空
- 如果不確定某支球隊的資訊，要用 web search 查，不要亂編

### 3. 比賽故事（story）

| 欄位 | 品質標準 |
|------|---------|
| `title` | 要有張力，格式：「事件：具體說明」。不超過 30 字 |
| `narrative` | **至少 300 字**。完整的比賽敘事，有開頭中段結尾。開頭用最戲劇性的瞬間（in medias res），中段拆解關鍵轉折，結尾留白不做總結 |
| `dramaticMoment` | 從 commentary 或 keyEvents 中挑一個最關鍵的時刻，一句話描述 |
| `turningPoint` | 「如果這件事沒發生，結果可能完全不同」的時刻 |
| `quote` | 有可靠來源才放。沒有就 null。**不能編造** |

**narrative 的禁止事項：**
- 不能只是 commentary 的流水帳
- 禁止使用：「讓我們把目光轉向」「值得一提的是」「毋庸置疑」
- 禁止破折號（——）連續使用
- 禁止驚嘆號！！！
- 不要分段小標題
- 數據要織入敘事，不要列舉

### 4. 賠率分析（oddsDeepDive）

- **至少 50 字**。解讀市場定價 vs AI 分析的差異
- 提到具體數字（讓球盤、賠率、大小球）
- 好的範例：`「DraftKings 開出阿根廷讓 1.5 球的盤口，主勝賠率 -230（隱含勝率約 70%）。這個定價與 AI 分析的 65% 接近。有趣的是大小球開 2.5⋯⋯」`

### 5. 統計摘要（boxscoreSummary）

- 從 ESPN boxscore 提取：控球率、射門數、射正數、傳球成功率
- 有進場人數時要加上

---

## 第三步：全貌分析標準

每輪比賽結束後，必須產出以下巨觀分析：

### 小組情勢
- 該小組目前的積分狀況
- 哪些隊伍晉級情勢樂觀、哪些危險
- 下一輪的關鍵對決

### 賽會脈絡
- 這一天有沒有爆冷？（如 Spain 0-0 Cape Verde）
- 有沒有球員突破紀錄？
- 這一天的結果如何影響淘汰賽階段的可能對戰組合？

範例（好的全貌分析）：
```
H 組首輪最冷門：Spain 被 FIFA 排名 64 的 Cape Verde 0-0 逼平。
歐洲冠軍全場 74% 控球率、27 次射門卻只射正 7 次。
Uruguay 與 Saudi Arabia 1-1 握手言和，讓 H 組出線情勢完全開放。
下一輪 Spain vs Uruguay 將是決定性的對決。
```

---

## 第四步：品質自檢（完成每場比賽後執行）

每寫完一場分析，逐項檢查：

- [ ] 預測三項勝率總和 = 100？
- [ ] predictedScore 是否合理（沒有 8-0）？
- [ ] homeWinPct 和 confidence 是否搞混？（homeWinPct=主勝率，confidence=AI 對自己預測的信心）
- [ ] 每隊 keyPlayers 至少 2 人？
- [ ] webSummary 至少 100 字？
- [ ] narrative 至少 300 字？
- [ ] title 有張力且不超過 30 字？
- [ ] 有沒有用禁止用語？
- [ ] 繁體中文用語一致（隊名用台灣通稱、沒有大陸用語）？
- [ ] 全貌分析有涵蓋小組情勢和賽會脈絡？
- [ ] 所有 JSON 欄位格式正確（prediction 有 preMatchPrediction 包裹）？

---

## 檔案更新順序

1. `src/data/matches/{id}.json` — 單場深度分析
2. `src/data/today-matches.json` — 今日賽程總覽（含預測與賠率摘要）
3. `src/data/matches-by-date.json` — 所有比賽按日期歸檔
4. `src/data/standings.json` — 小組排名更新
5. `npx astro build` — 編譯靜態檔
