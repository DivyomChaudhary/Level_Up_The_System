"""
state.py — Global AppState, user data, and quest logic.
All reactive state for The System lives here.
"""
import reflex as rx
from typing import TypedDict


# ─────────────────────────── TYPED MODELS ───────────────────────────
# Reflex 0.9.x requires typed vars for rx.foreach — plain list[dict] raises UntypedVarError.

class QuestItem(TypedDict):
    id: str
    title: str
    type: str
    done: bool
    xp: int


class HunterEntry(TypedDict):
    pos: int
    rank: str
    name: str
    info: str
    region: str


class GateEntry(TypedDict):
    rank: str
    title: str
    desc: str
    xp: int
    type: str


# ─────────────────────────── STATIC DATA ───────────────────────────

# Hunter data includes `pos` for safe display in rx.foreach (avoids .index() on Var)
HUNTER_DATA: list[dict] = [
    {"pos": 1,  "rank": "S", "name": "Go Gun-hee",      "info": "Chairman of the Korean Hunters Association",     "region": "South Korea"},
    {"pos": 2,  "rank": "S", "name": "Cha Hae-in",      "info": "Vice-Guild Master of the Hunters Guild",         "region": "South Korea"},
    {"pos": 3,  "rank": "S", "name": "Choi Jong-in",    "info": "Master of the Hunters Guild",                    "region": "South Korea"},
    {"pos": 4,  "rank": "S", "name": "Baek Yoon-ho",    "info": "Master of the White Tiger Guild",                "region": "South Korea"},
    {"pos": 5,  "rank": "S", "name": "Min Byung-gu",    "info": "Retired S-Rank Healer",                          "region": "South Korea"},
    {"pos": 6,  "rank": "S", "name": "Ma Dong-wuk",     "info": "Master of the Fame Guild",                       "region": "South Korea"},
    {"pos": 7,  "rank": "S", "name": "Lim Tae-gyu",     "info": "Master of the Fiend Guild",                      "region": "South Korea"},
    {"pos": 8,  "rank": "S", "name": "Hwang Dong-soo",  "info": "Defected to the US Scavenger Guild",             "region": "South Korea"},
    {"pos": 9,  "rank": "S", "name": "Eun Seok",        "info": "Deceased during an early Jeju Island Raid",      "region": "South Korea"},
    {"pos": 10, "rank": "S", "name": "Sung Il-hwan",    "info": "Trapped in a dungeon for a decade",              "region": "South Korea"},
    {"pos": 11, "rank": "S", "name": "Goto Ryuji",      "info": "Japan's strongest hunter",                       "region": "Japan"},
    {"pos": 12, "rank": "S", "name": "Reiji Sugimoto",  "info": "Draw Sword Guild",                               "region": "Japan"},
    {"pos": 13, "rank": "S", "name": "Atsushi Kumamoto","info": "Draw Sword Guild",                               "region": "Japan"},
    {"pos": 14, "rank": "S", "name": "Kei",             "info": "Draw Sword Guild",                               "region": "Japan"},
    {"pos": 15, "rank": "S", "name": "Kanae Tawata",    "info": "Draw Sword Guild",                               "region": "Japan"},
    {"pos": 16, "rank": "S", "name": "Minoru Hoshino",  "info": "Draw Sword Guild",                               "region": "Japan"},
    {"pos": 17, "rank": "S", "name": "Kenzo Tanaka",    "info": "Draw Sword Guild",                               "region": "Japan"},
    {"pos": 18, "rank": "A", "name": "Woo Jin-chul",    "info": "Chief of the Surveillance Team",                 "region": "South Korea"},
    {"pos": 19, "rank": "A", "name": "Kim Chul",        "info": "Elite tank from the White Tiger Guild",           "region": "South Korea"},
    {"pos": 20, "rank": "A", "name": "Lee Minsung",     "info": "Celebrity hunter",                               "region": "South Korea"},
    {"pos": 21, "rank": "A", "name": "Park Heejin",     "info": "Mage-class member of the White Tiger Guild",     "region": "South Korea"},
    {"pos": 22, "rank": "B", "name": "Kang Taeshik",    "info": "Assassin from the Surveillance Team",            "region": "South Korea"},
    {"pos": 23, "rank": "B", "name": "Lee Ju-hee",      "info": "Traumatised healer who stayed in low-tier raids", "region": "South Korea"},
    {"pos": 24, "rank": "C", "name": "Song Chi-yul",    "info": "Elderly Mage-class swordsman and mentor",        "region": "South Korea"},
    {"pos": 25, "rank": "C", "name": "Hwang Dong-suk",  "info": "Villainous C-Rank strike squad leader",          "region": "South Korea"},
    {"pos": 26, "rank": "D", "name": "Yoo Jinho",       "info": "Jin-woo's loyal companion and Ahjin Guild Vice-Master", "region": "South Korea"},
    {"pos": 27, "rank": "D", "name": "Yoo Soo-hyun",   "info": "Jinho's fashion-model cousin",                   "region": "South Korea"},
]

MOCK_AI_COMMITMENT = """\
══════════════════════════════════════════════════
         ⚡ SYSTEM COMMITMENT PLAN GENERATED ⚡
══════════════════════════════════════════════════

[FITNESS PROTOCOL — DAILY]
  ▸ Push-ups    : 100 reps (4 × 25)
  ▸ Pull-ups    : 50 reps  (5 × 10)
  ▸ Squats      : 150 reps (3 × 50)
  ▸ Core        : 10-min plank circuit

[DSA PROTOCOL]
  ▸ Daily       : 3 LeetCode problems
  ▸ Weekly      : 21 problems minimum
  ▸ Monthly     : 90 problems minimum

[DEV PROTOCOL — WEEKLY]
  ▸ 1 deployable project feature
  ▸ Minimum 300 lines of committed code

[PENALTY CLAUSE]
  ▸ Miss daily   → B-Rank Penalty Quest activated
  ▸ Miss weekly  → A-Rank Penalty Quest activated
  ▸ Miss monthly → S-Rank Penalty Quest activated

══════════════════════════════════════════════════
Do you accept these terms, Hunter?
══════════════════════════════════════════════════\
"""

GATES_DATA: list[dict] = [
    {"rank": "E", "title": "Echo Chamber",        "desc": "Solve 1 Easy LeetCode problem.",                        "xp": 50,   "type": "DSA"},
    {"rank": "E", "title": "Shadow Steps",        "desc": "20 push-ups + 20 squats in under 5 minutes.",           "xp": 50,   "type": "FITNESS"},
    {"rank": "D", "title": "Iron Curtain",        "desc": "Solve 2 Easy LeetCode problems.",                       "xp": 100,  "type": "DSA"},
    {"rank": "D", "title": "Stone Pillar",        "desc": "50 push-ups + 50 squats in under 10 minutes.",          "xp": 100,  "type": "FITNESS"},
    {"rank": "C", "title": "Abyssal Array",       "desc": "Solve 1 Medium LeetCode problem.",                      "xp": 200,  "type": "DSA"},
    {"rank": "C", "title": "Crimson Veil",        "desc": "Deploy a functioning mini-project (any stack).",        "xp": 200,  "type": "DEV"},
    {"rank": "B", "title": "Phantom Graph",       "desc": "Solve 2 Medium LeetCode problems.",                     "xp": 400,  "type": "DSA"},
    {"rank": "B", "title": "Dark Corridor",       "desc": "100 push-ups + 100 squats + 50 pull-ups.",              "xp": 400,  "type": "FITNESS"},
    {"rank": "A", "title": "Monarch's Trial",     "desc": "Solve 3 Medium LeetCode problems.",                     "xp": 800,  "type": "DSA"},
    {"rank": "A", "title": "Gate of Giants",      "desc": "Deploy a full-stack project with auth.",                "xp": 800,  "type": "DEV"},
    {"rank": "S", "title": "The Architect's Domain","desc": "Solve 1 Hard LeetCode problem.",                      "xp": 2000, "type": "DSA"},
    {"rank": "S", "title": "Dungeon of Endless Code","desc": "Ship a SaaS MVP with paying users.",                 "xp": 2000, "type": "DEV"},
]


# ─────────────────────────── APP STATE ───────────────────────────

class AppState(rx.State):
    """Single source of truth for The System."""

    # ── Onboarding ──
    awakened: bool = False
    onboarding_step: int = 1
    user_name: str = "Hunter"
    fitness_goal: str = ""
    dsa_daily: str = "3"
    dsa_weekly: str = "21"
    dsa_monthly: str = "90"
    dev_goal: str = ""
    extracurricular: str = ""
    github_id: str = ""
    leetcode_id: str = ""
    ai_plan_visible: bool = False
    ai_plan_loading: bool = False
    commitment_plan: str = ""

    # ── Navigation ──
    active_page: str = "dashboard"  # dashboard | gates | leaderboard

    # ── Quests ──
    daily_quests: list[QuestItem] = [
        {"id": "d1", "title": "Push-ups: 100 reps",           "type": "FITNESS", "done": False, "xp": 50},
        {"id": "d2", "title": "LeetCode: 3 problems",         "type": "DSA",     "done": False, "xp": 150},
        {"id": "d3", "title": "Commit 300+ lines of code",    "type": "DEV",     "done": False, "xp": 100},
        {"id": "d4", "title": "Core: 10-min plank circuit",   "type": "FITNESS", "done": False, "xp": 30},
    ]
    weekly_quests: list[QuestItem] = [
        {"id": "w1", "title": "LeetCode: 21 problems",        "type": "DSA",     "done": False, "xp": 500},
        {"id": "w2", "title": "Deploy 1 project feature",     "type": "DEV",     "done": False, "xp": 400},
        {"id": "w3", "title": "Fitness: 7-day streak",        "type": "FITNESS", "done": False, "xp": 300},
    ]
    monthly_quests: list[QuestItem] = [
        {"id": "m1", "title": "LeetCode: 90 problems",        "type": "DSA",     "done": False, "xp": 2000},
        {"id": "m2", "title": "Ship a full project",          "type": "DEV",     "done": False, "xp": 1500},
        {"id": "m3", "title": "Fitness: 30-day streak",       "type": "FITNESS", "done": False, "xp": 1000},
    ]

    # ── Penalties ──
    penalty_active: bool = False
    penalty_rank: str = "B"
    penalty_message: str = ""
    penalty_quest_title: str = ""

    # ── Gamification ──
    streak: int = 7
    total_xp: int = 1450
    hunter_rank: str = "D"
    level: int = 12

    # ── Leaderboard ──
    leaderboard: list[HunterEntry] = HUNTER_DATA

    # ── Verification ──
    verification_url: str = ""
    verification_message: str = ""

    # ── Gates ──
    gates: list[GateEntry] = GATES_DATA
    selected_gate: GateEntry = {}
    gate_proof_url: str = ""
    gate_cleared_ids: list[str] = []

    # ─── COMPUTED VARS ───

    @rx.var
    def completed_daily_count(self) -> int:
        return sum(1 for q in self.daily_quests if q["done"])

    @rx.var
    def total_daily_count(self) -> int:
        return len(self.daily_quests)

    @rx.var
    def daily_progress_pct(self) -> int:
        if not self.total_daily_count:
            return 0
        return int((self.completed_daily_count / self.total_daily_count) * 100)

    @rx.var
    def completed_weekly_count(self) -> int:
        return sum(1 for q in self.weekly_quests if q["done"])

    @rx.var
    def total_weekly_count(self) -> int:
        return len(self.weekly_quests)

    @rx.var
    def weekly_progress_pct(self) -> int:
        total = len(self.weekly_quests)
        if not total:
            return 0
        return int((sum(1 for q in self.weekly_quests if q["done"]) / total) * 100)

    @rx.var
    def completed_monthly_count(self) -> int:
        return sum(1 for q in self.monthly_quests if q["done"])

    @rx.var
    def total_monthly_count(self) -> int:
        return len(self.monthly_quests)

    @rx.var
    def monthly_progress_pct(self) -> int:
        total = len(self.monthly_quests)
        if not total:
            return 0
        return int((sum(1 for q in self.monthly_quests if q["done"]) / total) * 100)

    @rx.var
    def rank_color_class(self) -> str:
        return {
            "S": "rank-s", "A": "rank-a", "B": "rank-b",
            "C": "rank-c", "D": "rank-d", "E": "rank-e",
        }.get(self.hunter_rank, "rank-d")

    @rx.var
    def xp_to_next(self) -> int:
        return (self.level + 1) * 200

    @rx.var
    def xp_progress_pct(self) -> int:
        base = self.level * 200
        return min(int(((self.total_xp - base) / 200) * 100), 100)

    @rx.var
    def gates_cleared_count(self) -> int:
        return len(self.gate_cleared_ids)

    @rx.var
    def gates_total(self) -> int:
        return len(self.gates)

    # ─── ONBOARDING EVENTS ───

    def set_user_name(self, v: str):        self.user_name = v
    def set_fitness_goal(self, v: str):     self.fitness_goal = v
    def set_dsa_daily(self, v: str):        self.dsa_daily = v
    def set_dsa_weekly(self, v: str):       self.dsa_weekly = v
    def set_dsa_monthly(self, v: str):      self.dsa_monthly = v
    def set_dev_goal(self, v: str):         self.dev_goal = v
    def set_extracurricular(self, v: str):  self.extracurricular = v
    def set_github_id(self, v: str):        self.github_id = v
    def set_leetcode_id(self, v: str):      self.leetcode_id = v

    def next_step(self):
        if self.onboarding_step < 5:
            self.onboarding_step += 1

    def prev_step(self):
        if self.onboarding_step > 1:
            self.onboarding_step -= 1

    def generate_ai_plan(self):
        self.ai_plan_loading = True
        self.ai_plan_visible = False
        self.commitment_plan = ""

    def finish_ai_loading(self):
        self.ai_plan_loading = False
        self.commitment_plan = MOCK_AI_COMMITMENT
        self.ai_plan_visible = True

    def accept_awakening(self):
        self.awakened = True
        self.active_page = "dashboard"
        self.ai_plan_visible = False

    def decline_plan(self):
        self.ai_plan_visible = False
        self.onboarding_step = 1

    # ─── NAVIGATION ───

    def navigate_to(self, page: str):
        self.active_page = page

    # ─── QUEST EVENTS ───

    def _award_xp(self, amount: int):
        self.total_xp += amount
        self._recalculate_level()

    def _deduct_xp(self, amount: int):
        self.total_xp = max(0, self.total_xp - amount)
        self._recalculate_level()

    def _recalculate_level(self):
        self.level = max(1, self.total_xp // 200)
        if self.level >= 50:   self.hunter_rank = "S"
        elif self.level >= 35: self.hunter_rank = "A"
        elif self.level >= 20: self.hunter_rank = "B"
        elif self.level >= 10: self.hunter_rank = "C"
        elif self.level >= 5:  self.hunter_rank = "D"
        else:                  self.hunter_rank = "E"

    def toggle_daily_quest(self, quest_id: str):
        updated = []
        for q in self.daily_quests:
            if q["id"] == quest_id:
                new_done = not q["done"]
                q = {**q, "done": new_done}
                if new_done:
                    self._award_xp(q["xp"])
                else:
                    self._deduct_xp(q["xp"])
            updated.append(q)
        self.daily_quests = updated

    def toggle_weekly_quest(self, quest_id: str):
        updated = []
        for q in self.weekly_quests:
            if q["id"] == quest_id:
                new_done = not q["done"]
                q = {**q, "done": new_done}
                if new_done:
                    self._award_xp(q["xp"])
                else:
                    self._deduct_xp(q["xp"])
            updated.append(q)
        self.weekly_quests = updated

    def toggle_monthly_quest(self, quest_id: str):
        updated = []
        for q in self.monthly_quests:
            if q["id"] == quest_id:
                new_done = not q["done"]
                q = {**q, "done": new_done}
                if new_done:
                    self._award_xp(q["xp"])
                else:
                    self._deduct_xp(q["xp"])
            updated.append(q)
        self.monthly_quests = updated

    # ─── PENALTY EVENTS ───

    def trigger_penalty(self, rank: str, missed_quest: str):
        self.penalty_rank = rank
        self.penalty_quest_title = missed_quest
        msgs = {
            "B": f"[SYSTEM WARNING] You failed: '{missed_quest}'. A B-Rank Penalty Quest is now active. Complete it within 24 hours.",
            "A": f"[SYSTEM ALERT] Weekly objective FAILED: '{missed_quest}'. An A-Rank Penalty Quest is now ACTIVE. The System does not forgive weakness.",
            "S": f"[SYSTEM CRITICAL] Monthly objective FAILED: '{missed_quest}'. S-RANK PENALTY PROTOCOL ENGAGED. This is your final warning, Hunter.",
        }
        self.penalty_message = msgs.get(rank, "Penalty assigned.")
        self.penalty_active = True

    def dismiss_penalty(self):
        self.penalty_active = False

    # ─── VERIFICATION ───

    def set_verification_url(self, v: str):
        self.verification_url = v

    def submit_verification(self, quest_id: str):
        if not self.verification_url.strip():
            self.verification_message = "ERROR: No proof URL provided."
            return
        self.toggle_daily_quest(quest_id)
        self.streak += 1
        self.verification_url = ""
        self.verification_message = "VERIFICATION ACCEPTED. Quest marked complete."

    def clear_verification_message(self):
        self.verification_message = ""

    # ─── GATES ───

    def select_gate(self, gate: dict):
        self.selected_gate = gate
        self.gate_proof_url = ""
        self.verification_message = ""

    def set_gate_proof_url(self, v: str):
        self.gate_proof_url = v

    def clear_gate(self):
        self.selected_gate = {}
        self.gate_proof_url = ""

    def submit_gate_clear(self):
        if not self.gate_proof_url.strip():
            self.verification_message = "ERROR: Proof URL required to clear this gate."
            return
        title = self.selected_gate.get("title", "")
        if title and title not in self.gate_cleared_ids:
            self.gate_cleared_ids = self.gate_cleared_ids + [title]
            xp = self.selected_gate.get("xp", 0)
            self._award_xp(xp)
            self.verification_message = f"GATE CLEARED: {title} | +{xp} XP awarded."
        self.selected_gate = {}
        self.gate_proof_url = ""
