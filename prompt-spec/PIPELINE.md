# 每日內容生產管線

## 執行順序

```
Step 0: 撈資料
   curl ESPN scoreboard → 今日賽程列表
   curl ESPN summary → 每場詳細資料（for 故事短文）

Step 1: ① 隊伍調查員 → per match × 2 teams（可平行）
Step 2: ② 勝率分析師 → per match（需要 ① 的產出）
Step 3: ③ 賠率解讀員 → per match（需要 ② 的產出）
Step 4: ④ 故事作家 → per match（需要 raw commentary + keyEvents）
Step 5: ⑤ 總編輯 → 收斂所有產出，QC，寫入 JSON

Step 6: astro build → dist/
Step 7: 部署 dist/ 到伺服器
```

## 一次性啟動命令

```bash
# 開發
npm run dev

# 正式產出
# 1. 執行 AI pipeline → 寫入 src/data/*.json
# 2. npm run build
# 3. 上傳 dist/ 到部署目標
```

## 每個 prompt 的觸發條件

| Prompt | 觸發 | 可平行 |
|--------|------|--------|
| ① 隊伍調查員 | 拿到 ESPN data + web search 可用 | ✅ 每隊獨立 |
| ② 勝率分析師 | ① 完成（需要兩隊分析） | ✅ 每場獨立 |
| ③ 賠率解讀員 | ② 完成（需要 prediction） | ✅ 每場獨立 |
| ④ 故事作家 | 拿到 raw commentary | ✅ 每場獨立 |
| ⑤ 總編輯 | ①-④ 全部完成 | ❌ 單一收斂 |
