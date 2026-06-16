# Session Handoff — 2026-06-16

## 背景
2026 世界盃（6/11-7/19）期間的 AI 預測內容網站。Astro 靜態站 + 手寫分析內容。已上線 19 場比賽的繁體中文分析，包含賽程 timeline、小組排名、單場深度頁。

## 工作目錄
`D:\_CabLate_Agents\general\projects\2026-world-cup-content\`

## 進度

### 已完成
- 資料來源研究與驗證（ESPN API、openfootball、worldcup26.ir）— 結論：只要 ESPN API 就夠
- 設計系統建立（taste-skill 三 dials: VARIANCE=8, MOTION=6, DENSITY=4）
- 色彩系統：深海軍藍 #070b14 + 電光青 #00d4ff（禁止 AI 紫/藍模板）
- 字體：Plus Jakarta Sans（英數標題）+ Noto Sans TC（中文）+ JetBrains Mono（數字）
- 字級優化：html 16px 基底，各元件 text-xs ~ text-lg 統一放大
- 首頁（賽程 timeline + 今日預測 + 小組排名）— 繁體中文
- 小組排名頁（12 組完整積分表）— 繁體中文
- 19 場比賽單頁深度分析（全繁體中文，含 FIFA 排名、關鍵球員、優劣勢、故事、賠率分析）
- 顏色對比修復（text-muted 提亮、border 加亮、背景區分度增加）
- Astro + Tailwind v4 + @tailwindcss/vite

### 未完成
- 更換的頭像圖沒有優化壓縮（hero-bg.jpg 847KB，dist 總和 19MB 主要是 Noto Sans TC 字型）
- 其餘 10 場非焦點賽事的分析深度不如前 9 場（有資料但故事和細節較簡略）
- 每日 AI 預測 prompt 管線未實際運作過（5 個 prompt 規格已寫在 `prompt-spec/` 但還沒真的跑過一日完整流程）
- 賠率分析是手寫的市場觀察，不是真正的即時賠率 API 串接
- 無圖片素材（除了 hero-bg.jpg 外沒有比賽相關圖片）
- 無淘汰賽階段頁面（目前只做 Group Stage）

## 使用者的指示與修正 [P0]

### 關於工作方式
- 「刪掉這個py 我是要由你來驅動建立每一筆分析結果 不是要你寫py 你懂了沒」— 分析內容必須由 AI 親手寫，不能寫腳本自動化。寫腳本 = 逃避思考。
- 「這些就是都要由你直接跑啊 你就是AI耶」— 5 個 prompt 規格不是讓 Cab 自己跑，是要我執行。
- 「蝦 不是這樣」— 對錯誤方向的直接打斷。當我開始往自動化/腳本方向走的時候，方向性錯誤。

### 關於內容品質
- 「之前19場的資料品質完全不行 遺漏太多訊息」— 機器填入的資料被明確判定不合格。
- 「而且你要以繁體中文語境為主」— 全站必須是繁體中文，從隊名到分析到用語。
- 「字體font換一下 然後字的大小可以優化一下」— 字體和字級不符合需求後續修正。
- 「我注意到很多地方非常不清晰且排版有問題」— 顏色對比不足，後續修復。

### 關於技術選擇
- 「純前端html 我覺得不錯了」→「單檔html我怕爆開啦 可以考慮多檔案多頁面分開管理 用astro你覺得如何呢」— 初期單檔 HTML，後面改為 Astro 靜態站。
- Astro 專案已建好，使用 Tailwind v4 + @tailwindcss/vite

## 共識與認知 [P0]

- **ESPN API 足夠作為唯一資料源**：scoreboard 給賽程比分，summary 給 commentary + boxscore + odds + keyEvents + standings。不需要其他 API。
- **純靜態架構**：內容由 AI 批次產出 → 寫入 JSON → astro build → 部署。前端不串任何即時 API。沒有後端。
- **設計遵循 taste-skill 原則**：無 emoji、無 Inter 字體、無 AI 紫/藍、無置中 hero、不對稱布局、單一 accent color。
- **分析必須親自寫**：每一場比賽的分析、故事、預測都要親手撰寫。不能用腳本批次產生。
- **繁體中文語境**：隊名用中文通稱（阿根廷、法國、德國、英格蘭等），分析用台灣足球迷慣用語。

## 踩過的坑

- **PredictionMeter.astro 已被 RingGauge.astro 取代**（舊元件未移除導致 stale file）
- **Python 編碼問題**：Git Bash 的 /tmp/ 路徑在 Python 中不同（需用 `C:\Users\User\AppData\Local\Temp`），Windows cp950 編碼會讓 print 中文字失敗
- **Tailwind v4 + @astrojs/tailwind 不相容**：`@astrojs/tailwind` v6 不支援 Tailwind v4，需改用 `@tailwindcss/vite` 直接掛在 Vite plugins
- **JSON 格式錯誤**：部分比賽檔案的 prediction 欄位誤寫為 flat object 而非 `{ preMatchPrediction: {...}, postMatchReview: "...", accuracy: "..." }` 格式（已修復）
- **Component null safety**：TeamAnalysis.astro 的 `team.keyPlayers.map()` 和 `team.form.map()` 在資料為空時會 crash，需加 `|| []` fallback

## 技術細節

- Astro v6.4.7 + Tailwind v4.3.1 + @tailwindcss/vite
- 字體：Plus Jakarta Sans（via @fontsource）、Noto Sans TC（via @fontsource）、JetBrains Mono（via @fontsource）
- 設計 tokens 在 `src/styles/global.css` 的 `@theme`
- 資料檔案：`src/data/today-matches.json`、`src/data/standings.json`、`src/data/matches-by-date.json`、`src/data/matches/{id}.json`
- 頁面路由：`/`（首頁）、`/standings`（排名）、`/matches/:id`（單場）
- Components：Header、Footer、MatchCard、RingGauge、StandingsTable、TeamAnalysis、StorySection、OddsAnalysis
- Prompt 規格：`prompt-spec/01~05` + `DAILY-UPDATE-PIPELINE.md`
- Scripts：`scripts/generate-data.py`（資料批次產生）、`scripts/enrich-matches.py`（ESPN 資料匯入，已 deprecated）
- 開發伺服器：執行 `npx astro dev --port 8000` 在 http://localhost:8000/

## 下一步

1. **優化圖片與效能**：壓縮 hero-bg.jpg；評估 Noto Sans TC 是否要 subset 或改用系統字體減少 19MB bundle
2. **深度補齊 10 場次要比賽的分析**：把韓國 vs 捷克、加拿大 vs 波士尼亞等場次的故事寫到和焦點賽事同樣深度
3. **實際執行一日 AI 管線**：撈今日 ESPN 資料 → 執行 5 個 prompt（由我親手撰寫）→ 更新 JSON → build → 部署
4. **考慮明日賽程預測**：June 17 有 Croatia vs England、Portugal vs Congo DR 等 5 場比賽，需要賽前撰寫預測
5. **圖片素材**：考慮為重要比賽加上 AI 生成圖或國旗標誌組合圖
