#!/usr/bin/env python3
"""Pull everything the weekly roast needs from ESPN's public API (stdlib only).

Usage: python3 scripts/fetch_week.py [matchup_period] > week.json
Default period = currentMatchupPeriod - 1. Exits 2 (no JSON) if any game of the
week is UNDECIDED or scores look implausibly small: do NOT publish in that case.
"""
import json, sys, subprocess

BASE = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/fba/seasons/2027/segments/0/leagues/855206631"


def get(views, spid=None):
    url = BASE + "?" + "&".join("view=" + v for v in views)
    if spid:
        url += f"&scoringPeriodId={spid}"
    return json.loads(subprocess.check_output(["curl", "-s", url]))


def main():
    base = get(["mTeam", "mMatchupScore", "mSettings"])
    cur = base["status"]["currentMatchupPeriod"]
    wk = int(sys.argv[1]) if len(sys.argv) > 1 else cur - 1
    names = {t["id"]: t["name"].strip() for t in base["teams"]}
    games = [g for g in base["schedule"] if g["matchupPeriodId"] == wk]
    if not games or any(g.get("winner") not in ("HOME", "AWAY") for g in games):
        sys.exit(f"Matchup {wk}: games missing or UNDECIDED. Do not publish.")
    if any(g[s].get("totalPoints", 0) < 200 for g in games for s in ("home", "away")):
        sys.exit(f"Matchup {wk}: tiny scores. Do not publish.")

    # player totals: use a scoring period inside the week
    days = sorted(int(k) for k in games[0]["home"]["pointsByScoringPeriod"])
    box = get(["mBoxscore", "mMatchupScore", "mTeam"], days[-1])
    boxg = {(g["home"]["teamId"], g["away"]["teamId"]): g for g in box["schedule"] if g["matchupPeriodId"] == wk}

    def stars(side):
        ents = side.get("rosterForMatchupPeriod", {}).get("entries", [])
        pl = sorted(((e["playerPoolEntry"]["player"]["fullName"], e["playerPoolEntry"]["appliedStatTotal"]) for e in ents), key=lambda x: -x[1])
        return {"top": pl[:2], "all": pl}

    out = {"matchupPeriod": wk, "currentMatchupPeriod": cur, "scoringDays": days, "matchups": [], "scores": {}}
    for g in games:
        bg = boxg[(g["home"]["teamId"], g["away"]["teamId"])]
        w, l = ("home", "away") if g["winner"] == "HOME" else ("away", "home")
        sides = {}
        for s in (w, l):
            sides[s] = {"team": names[g[s]["teamId"]], "pts": g[s]["totalPoints"],
                        "byDay": g[s]["pointsByScoringPeriod"], **stars(bg[s])}
            out["scores"][names[g[s]["teamId"]]] = g[s]["totalPoints"]
        out["matchups"].append({"win": sides[w], "lose": sides[l], "margin": round(sides[w]["pts"] - sides[l]["pts"], 2)})

    # all-play (this week's scores only)
    sc = out["scores"]
    out["allPlay"] = {t: f"{sum(sc[t] > sc[o] for o in sc if o != t)}-{sum(sc[t] < sc[o] for o in sc if o != t)}" for t in sc}
    # biggest / lowest single day across all teams
    days_all = [(v, t, d) for m in out["matchups"] for s in m.values() if isinstance(s, dict) for t, d, v in [(s["team"], d, v) for d, v in s["byDay"].items()]]
    days_all.sort()
    out["lowestDay"], out["biggestDay"] = days_all[0], days_all[-1]
    # standings by season points for
    out["standings"] = sorted(({"team": names[t["id"]], "rec": f'{t["record"]["overall"]["wins"]}-{t["record"]["overall"]["losses"]}',
                                "pf": t["record"]["overall"]["pointsFor"]} for t in base["teams"]), key=lambda x: -x["pf"])
    # live (new, in-progress) week
    live = [g for g in base["schedule"] if g["matchupPeriodId"] == cur]
    out["live"] = [[names[g["home"]["teamId"]], g["home"].get("totalPoints", 0), g["away"].get("totalPoints", 0), names[g["away"]["teamId"]]] for g in live]
    out["liveScoringPeriod"] = base["scoringPeriodId"]
    json.dump(out, sys.stdout, indent=1)


main()
