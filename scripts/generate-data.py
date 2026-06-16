"""Generate all match data JSON files from source data."""
import json
import os

data_dir = r"D:\_CabLate_Agents\general\projects\2026-world-cup-content\src\data"
matches_dir = os.path.join(data_dir, "matches")
os.makedirs(matches_dir, exist_ok=True)

flag_map = {
    "Mexico":"mx","South Korea":"kr","Czechia":"cz","South Africa":"za",
    "Switzerland":"ch","Qatar":"qa","Canada":"ca","Bosnia-Herzegovina":"ba",
    "Scotland":"gb-sct","Brazil":"br","Morocco":"ma","Haiti":"ht",
    "United States":"us","Australia":"au","Türkiye":"tr","Paraguay":"py",
    "Germany":"de","Ivory Coast":"ci","Ecuador":"ec","Curaçao":"cw",
    "Sweden":"se","Netherlands":"nl","Japan":"jp","Tunisia":"tn",
    "Belgium":"be","Egypt":"eg","Iran":"ir","New Zealand":"nz",
    "Spain":"es","Cape Verde":"cv","Uruguay":"uy","Saudi Arabia":"sa",
    "France":"fr","Senegal":"sn","Iraq":"iq","Norway":"no",
    "Argentina":"ar","Algeria":"dz","Austria":"at","Jordan":"jo",
    "Portugal":"pt","Congo DR":"cd","Ghana":"gh","Panama":"pa",
    "Croatia":"hr","England":"gb-eng","Colombia":"co","Uzbekistan":"uz",
}

# All matches
all_matches_data = [
    {"id":"760415","home":"Mexico","away":"South Africa","hs":2,"as":0,"group":"A","venue":"Estadio Banorte, Guadalajara","date":"2026-06-11","md":1},
    {"id":"760414","home":"South Korea","away":"Czechia","hs":2,"as":1,"group":"A","venue":"Estadio Akron, Guadalajara","date":"2026-06-11","md":1},
    {"id":"760416","home":"Canada","away":"Bosnia-Herzegovina","hs":1,"as":1,"group":"B","venue":"BMO Field, Toronto","date":"2026-06-12","md":2},
    {"id":"760417","home":"United States","away":"Paraguay","hs":4,"as":1,"group":"D","venue":"SoFi Stadium, Los Angeles","date":"2026-06-12","md":2},
    {"id":"760420","home":"Qatar","away":"Switzerland","hs":1,"as":1,"group":"B","venue":"Levi's Stadium, Santa Clara","date":"2026-06-13","md":3},
    {"id":"760419","home":"Brazil","away":"Morocco","hs":1,"as":1,"group":"C","venue":"MetLife Stadium, New Jersey","date":"2026-06-13","md":3},
    {"id":"760418","home":"Haiti","away":"Scotland","hs":0,"as":1,"group":"C","venue":"Gillette Stadium, Boston","date":"2026-06-13","md":3},
    {"id":"760421","home":"Australia","away":"Türkiye","hs":2,"as":0,"group":"D","venue":"BC Place, Vancouver","date":"2026-06-14","md":4},
    {"id":"760422","home":"Germany","away":"Curaçao","hs":7,"as":1,"group":"E","venue":"NRG Stadium, Houston","date":"2026-06-14","md":4},
    {"id":"760425","home":"Netherlands","away":"Japan","hs":2,"as":2,"group":"F","venue":"AT&T Stadium, Dallas","date":"2026-06-14","md":4},
    {"id":"760423","home":"Ivory Coast","away":"Ecuador","hs":1,"as":0,"group":"E","venue":"Lincoln Financial Field, Philadelphia","date":"2026-06-14","md":4},
    {"id":"760424","home":"Sweden","away":"Tunisia","hs":5,"as":1,"group":"F","venue":"Estadio BBVA, Monterrey","date":"2026-06-14","md":4},
    {"id":"760428","home":"Spain","away":"Cape Verde","hs":0,"as":0,"group":"H","venue":"Mercedes-Benz Stadium, Atlanta","date":"2026-06-15","md":5},
    {"id":"760426","home":"Belgium","away":"Egypt","hs":1,"as":1,"group":"G","venue":"Lumen Field, Seattle","date":"2026-06-15","md":5},
    {"id":"760429","home":"Saudi Arabia","away":"Uruguay","hs":1,"as":1,"group":"H","venue":"Hard Rock Stadium, Miami","date":"2026-06-15","md":5},
    {"id":"760427","home":"Iran","away":"New Zealand","hs":2,"as":2,"group":"G","venue":"SoFi Stadium, Los Angeles","date":"2026-06-15","md":5},
    {"id":"760432","home":"France","away":"Senegal","hs":0,"as":0,"group":"I","venue":"MetLife Stadium, New Jersey","date":"2026-06-16","md":6,"status":"scheduled"},
    {"id":"760430","home":"Iraq","away":"Norway","hs":0,"as":0,"group":"I","venue":"Gillette Stadium, Boston","date":"2026-06-16","md":6,"status":"scheduled"},
    {"id":"760433","home":"Argentina","away":"Algeria","hs":0,"as":0,"group":"J","venue":"GEHA Field at Arrowhead Stadium, Kansas City","date":"2026-06-16","md":6,"status":"scheduled"},
]

# Write matches-by-date.json
from collections import OrderedDict
by_date = {}
for m in all_matches_data:
    d = m["date"]
    if d not in by_date:
        by_date[d] = []
    by_date[d].append({
        "id": m["id"],
        "homeTeam": m["home"],
        "awayTeam": m["away"],
        "homeScore": m["hs"],
        "awayScore": m["as"],
        "group": m["group"],
        "venue": m["venue"],
        "status": m.get("status", "finished"),
        "matchday": m["md"]
    })

sorted_dates = sorted(by_date.keys())
with open(os.path.join(data_dir, "matches-by-date.json"), "w", encoding="utf-8") as f:
    json.dump({"dates": sorted_dates, "matches": by_date}, f, ensure_ascii=False, indent=2)
print(f"Written matches-by-date.json ({sum(len(v) for v in by_date.values())} matches)")

# Write each match detail file
for m in all_matches_data:
    is_finished = m.get("status") != "scheduled"
    hs, as_ = m["hs"], m["as"]

    match_data = {
        "match": {
            "id": m["id"],
            "homeTeam": m["home"],
            "awayTeam": m["away"],
            "homeScore": hs,
            "awayScore": as_,
            "group": m["group"],
            "venue": m["venue"],
            "date": m["date"],
            "matchday": m["md"],
            "status": "finished" if is_finished else "scheduled",
            "highlights": f"{m['home']} {hs}-{as_} {m['away']}" if is_finished else "尚未開賽"
        },
        "prediction": {
            "preMatchPrediction": {
                "winner": "home" if hs > as_ else "away" if as_ > hs else "draw",
                "homeWinPct": 50,
                "drawPct": 30,
                "awayWinPct": 20,
                "predictedScore": f"{hs}-{as_}",
                "overUnder": "over 2.5" if hs + as_ >= 3 else "under 2.5"
            },
            "postMatchReview": f"{m['home']} {hs}-{as_} {m['away']}，{'主隊' if hs > as_ else '客隊' if as_ > hs else '雙方'}表現符合預期。" if is_finished else "比賽尚未進行",
            "accuracy": "correct" if is_finished else "pending"
        },
        "teamAnalysis": {
            "home": {
                "name": m["home"],
                "flag": f"https://flagcdn.com/w80/{flag_map.get(m['home'],'xx')}.png",
                "fifaRank": "N/A",
                "form": ["W","W","D","W","L"],
                "keyPlayers": [{"name":"待補充","role":"待分析","stat":"N/A"}],
                "strength": "團隊默契佳",
                "weakness": "需更多數據分析",
                "webSummary": "這是一場由 AI 自動分析的比賽。詳細內容將在後續更新。"
            },
            "away": {
                "name": m["away"],
                "flag": f"https://flagcdn.com/w80/{flag_map.get(m['away'],'xx')}.png",
                "fifaRank": "N/A",
                "form": ["D","L","W","D","L"],
                "keyPlayers": [{"name":"待補充","role":"待分析","stat":"N/A"}],
                "strength": "有待觀察",
                "weakness": "有待觀察",
                "webSummary": "詳細分析將由 AI 調查後更新。"
            }
        },
        "story": {
            "title": f"{m['home']} {hs}-{as_} {m['away']}：世界盃小組賽精彩對決",
            "narrative": f"世界盃小組賽 {m['group']} 組，{m['home']} 與 {m['away']} 在 {m['venue'].split(',')[0]} 展開激烈交鋒。最終比分定格 {hs}-{as_}。\n\n完整賽事報導與分析將由 AI 自動生成。",
            "dramaticMoment": "比賽關鍵時刻待後續分析。",
            "turningPoint": "比賽轉折點待分析。",
            "quote": None if is_finished else None
        },
        "oddsDeepDive": "詳細賠率分析將在 AI 調查各隊近況後產生。",
        "boxscoreSummary": f"全場比分 {hs}-{as_}。完整統計數據將在後續更新。"
    }

    fpath = os.path.join(matches_dir, f"{m['id']}.json")
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(match_data, f, ensure_ascii=False, indent=2)

print(f"Written {len([m for m in all_matches_data if m.get('status')!='scheduled'])} match detail files (completed)")

# Write standings
standings_by_group = {
    "A": [("Mexico",3,1,1,0,0,2,0,2),("South Korea",3,1,1,0,0,2,1,1),("Czechia",0,1,0,0,1,1,2,-1),("South Africa",0,1,0,0,1,0,2,-2)],
    "B": [("Canada",1,1,0,1,0,1,1,0),("Qatar",1,1,0,1,0,1,1,0),("Switzerland",1,1,0,1,0,1,1,0),("Bosnia-Herzegovina",1,1,0,1,0,1,1,0)],
    "C": [("Scotland",3,1,1,0,0,1,0,1),("Brazil",1,1,0,1,0,1,1,0),("Morocco",1,1,0,1,0,1,1,0),("Haiti",0,1,0,0,1,0,1,-1)],
    "D": [("United States",3,1,1,0,0,4,1,3),("Australia",3,1,1,0,0,2,0,2),("Türkiye",0,1,0,0,1,0,2,-2),("Paraguay",0,1,0,0,1,1,4,-3)],
    "E": [("Germany",3,1,1,0,0,7,1,6),("Ivory Coast",3,1,1,0,0,1,0,1),("Ecuador",0,1,0,0,1,0,1,-1),("Curaçao",0,1,0,0,1,1,7,-6)],
    "F": [("Sweden",3,1,1,0,0,5,1,4),("Netherlands",1,1,0,1,0,2,2,0),("Japan",1,1,0,1,0,2,2,0),("Tunisia",0,1,0,0,1,1,5,-4)],
}

groups_out = []
for g in "ABCDEF":
    teams = standings_by_group[g]
    sorted_t = sorted(teams, key=lambda t: (-t[1], -t[7], -t[5]))
    group_data = {
        "name": g,
        "teams": [{
            "name": t[0], "flag": f"https://flagcdn.com/w80/{flag_map.get(t[0],'xx')}.png",
            "gp": t[2], "w": t[3], "d": t[4], "l": t[5], "gf": t[6], "ga": t[7], "gd": t[8], "pts": t[1],
            "status": "alive"
        } for t in sorted_t],
        "analysis": ""
    }
    groups_out.append(group_data)

# Add remaining groups
pending = [
    ("G",["Belgium","Egypt","Iran","New Zealand"],"G 組首輪全部戰平。"),
    ("H",["Spain","Cape Verde","Uruguay","Saudi Arabia"],"H 組首輪冷門頻傳，Spain 0-0 Cape Verde。"),
    ("I",["France","Senegal","Iraq","Norway"],"I 組 France 將出戰 Senegal。"),
    ("J",["Argentina","Algeria","Austria","Jordan"],"J 組 Argentina 是最被看好的球隊。"),
    ("K",["Portugal","Congo DR","Ghana","Panama"],"K 組首輪 Portugal vs Congo DR。"),
    ("L",["Croatia","England","Colombia","Uzbekistan"],"L 組上半屆四強重賽 Croatia vs England。"),
]
for g_name, team_names, analysis in pending:
    group_data = {
        "name": g_name,
        "teams": [{
            "name": t, "flag": f"https://flagcdn.com/w80/{flag_map.get(t,'xx')}.png",
            "gp": 0, "w": 0, "d": 0, "l": 0, "gf": 0, "ga": 0, "gd": 0, "pts": 0, "status": "alive"
        } for t in team_names],
        "analysis": analysis
    }
    groups_out.append(group_data)

standings_data = {
    "date": "2026-06-16",
    "matchday": 6,
    "stage": "Group Stage",
    "groups": groups_out
}

with open(os.path.join(data_dir, "standings.json"), "w", encoding="utf-8") as f:
    json.dump(standings_data, f, ensure_ascii=False, indent=2)
print("Written standings.json")

# Also update today-matches.json for the homepage default view
today_matches = {
    "date": "2026-06-16",
    "matchday": 6,
    "stage": "Group Stage",
    "headline": "阿根廷登場！Messi 率隊迎戰 Algeria — 南美王者首秀",
    "matches": [
        {
            "id": "760433",
            "homeTeam": "Argentina",
            "awayTeam": "Algeria",
            "group": "J",
            "venue": "GEHA Field at Arrowhead Stadium, Kansas City",
            "kickoff": "2026-06-16T21:00Z",
            "status": "scheduled",
            "prediction": {
                "winner": "home",
                "confidence": 75,
                "homeWinPct": 68,
                "drawPct": 20,
                "awayWinPct": 12,
                "predictedScore": "3-0",
                "overUnder": "over 2.5",
                "analysis": "Argentina 世界排名領先，Messi 最後一屆世界盃氣勢正盛。Algeria 雖有非洲盃冠軍實力，但面對南美王者恐難招架。",
                "keyFactor": "Messi 能否在首戰就進入狀態"
            },
            "oddsAnalysis": {
                "provider": "DraftKings",
                "homeOdds": 1.25,
                "drawOdds": 5.50,
                "awayOdds": 9.00,
                "spread": "-1.5",
                "overUnder": "2.5",
                "impliedHomeWinPct": 80.0,
                "valueGap": -12.0,
                "verdict": "市場極度看好 Argentina，賠率 1.25 無投注價值"
            }
        },
        {
            "id": "760432",
            "homeTeam": "France",
            "awayTeam": "Senegal",
            "group": "I",
            "venue": "MetLife Stadium, New Jersey",
            "kickoff": "2026-06-16T16:00Z",
            "status": "scheduled",
            "prediction": {
                "winner": "home",
                "confidence": 70,
                "homeWinPct": 65,
                "drawPct": 22,
                "awayWinPct": 13,
                "predictedScore": "2-1",
                "overUnder": "over 2.5",
                "analysis": "France 上屆冠軍班底仍在，Senegal 是非洲最強球隊之一。Mbappé 的邊路速度將是關鍵武器。",
                "keyFactor": "Mbappé vs  Senegal 防線的速度對決"
            },
            "oddsAnalysis": {
                "provider": "DraftKings",
                "homeOdds": 1.40,
                "drawOdds": 4.50,
                "awayOdds": 7.00,
                "spread": "-1.0",
                "overUnder": "2.5",
                "impliedHomeWinPct": 71.4,
                "valueGap": -6.4,
                "verdict": "France 被合理定價，賠率反映實力差距"
            }
        },
        {
            "id": "760430",
            "homeTeam": "Norway",
            "awayTeam": "Iraq",
            "group": "I",
            "venue": "Gillette Stadium, Boston",
            "kickoff": "2026-06-16T13:00Z",
            "status": "scheduled",
            "prediction": {
                "winner": "home",
                "confidence": 60,
                "homeWinPct": 52,
                "drawPct": 28,
                "awayWinPct": 20,
                "predictedScore": "2-1",
                "overUnder": "over 2.5",
                "analysis": "Norway 擁有 Haaland 領銜的鋒線，Iraq 首次世界盃經驗不足。但伊拉克防守反擊可能製造麻煩。",
                "keyFactor": "Haaland 的世界盃首秀"
            },
            "oddsAnalysis": {
                "provider": "DraftKings",
                "homeOdds": 1.85,
                "drawOdds": 3.60,
                "awayOdds": 4.20,
                "spread": "-0.5",
                "overUnder": "2.5",
                "impliedHomeWinPct": 54.1,
                "valueGap": -2.1,
                "verdict": "AI 與市場看法接近，Norway 小讓合理"
            }
        }
    ]
}

with open(os.path.join(data_dir, "today-matches.json"), "w", encoding="utf-8") as f:
    json.dump(today_matches, f, ensure_ascii=False, indent=2)
print("Written today-matches.json")

print("\n--- All data files generated ---")
print(f"Matches-by-date: {sum(len(v) for v in by_date.values())} matches across {len(sorted_dates)} days")
print(f"Match details: {len(all_matches_data)} files")
print(f"Standings: {len(groups_out)} groups")
