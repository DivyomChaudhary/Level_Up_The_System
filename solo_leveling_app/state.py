"""
state.py — Global AppState. Phase 4.
Fixes:
  • selected_gate default = fully-typed empty GateDisplayEntry
  • Streak: only +1 when ALL daily quests complete, -1 when any uncompleted
  • XP reversal on uncomplete (award_xp in reverse, not punishment)
  • Key popup show_key_popup flag + dismiss handler
  • Commitment wallet: wallet_balance, wallet_frozen, level-based cap
  • wallet freeze: 1% per missed daily quest per day
  • OpenAI quest planning hook (ready for API key)
  • App name branding var
"""
import reflex as rx
import random
import datetime
import os
from typing import TypedDict

# Load .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not required

_DEFAULT_UPI_ID: str = os.getenv("COMMITMENT_UPI_ID", "")
_OPENAI_KEY: str = os.getenv("OPENAI_API_KEY", "")


# ── Pure helper functions ─────────────────────────────────────────────

def _xp_for_level(n: int) -> int:
    if n <= 1:
        return 0
    return 50 * (n - 1) * (n + 2)


def _level_from_total_xp(total: int) -> int:
    level = 1
    while True:
        if total >= _xp_for_level(level + 1):
            level += 1
        else:
            break
    return level


def _mp_for_level(n: int) -> int:
    if n <= 1:
        return 0
    return 50 * (n - 1) * (n + 2)


def _mp_level_from_total(total: int) -> int:
    level = 1
    while True:
        if total >= _mp_for_level(level + 1):
            level += 1
        else:
            break
    return level


# ── TypedDicts ───────────────────────────────────────────────────────

class QuestItem(TypedDict):
    id: str
    title: str
    type: str   # "DSA" | "DEV" | "FITNESS" | "CUSTOM"
    done: bool
    xp: int


class HunterEntry(TypedDict):
    pos: int
    rank: str
    level: int
    name: str
    info: str
    region: str
    is_user: bool


class GateDisplayEntry(TypedDict):
    rank: str
    title: str
    desc: str
    mp: int
    type: str
    gate_type: str       # "persistent" | "iterative"
    status: str          # "active" | "cleared" | "refreshing" | "overdue"
    days_remaining: int


class PerformancePoint(TypedDict):
    day: str
    expected: int
    actual: int


# ── Static data ──────────────────────────────────────────────────────

_EMPTY_GATE: GateDisplayEntry = {
    "rank": "", "title": "", "desc": "", "mp": 0,
    "type": "", "gate_type": "iterative", "status": "active", "days_remaining": 0,
}

HUNTER_DATA: list[HunterEntry] = [
    {"pos": 1,  "rank": "S", "level": 99, "name": "Go Gun-hee",       "info": "Chairman of the Korean Hunters Association. His authority transcends ranks.",              "region": "South Korea", "is_user": False},
    {"pos": 2,  "rank": "S", "level": 97, "name": "Cha Hae-in",       "info": "Vice-Guild Master of the Hunters Guild. Unmatched swordsmanship and mana sensitivity.",    "region": "South Korea", "is_user": False},
    {"pos": 3,  "rank": "S", "level": 95, "name": "Choi Jong-in",     "info": "Master of the Hunters Guild. Fire-element specialist. Tactician before all else.",         "region": "South Korea", "is_user": False},
    {"pos": 4,  "rank": "S", "level": 93, "name": "Baek Yoon-ho",     "info": "Master of the White Tiger Guild. Beast Tamer — fights with the fury of a monarch.",       "region": "South Korea", "is_user": False},
    {"pos": 5,  "rank": "S", "level": 90, "name": "Sung Il-hwan",     "info": "Trapped in a dungeon for a decade — returned stronger. Jin-woo's father.",                "region": "South Korea", "is_user": False},
    {"pos": 6,  "rank": "S", "level": 91, "name": "Goto Ryuji",       "info": "Japan's strongest. Draw Sword Guild master. Cold, lethal, precise.",                       "region": "Japan",       "is_user": False},
    {"pos": 7,  "rank": "S", "level": 88, "name": "Min Byung-gu",     "info": "Retired S-Rank Healer. Saved countless lives — chose to step back from raids.",           "region": "South Korea", "is_user": False},
    {"pos": 8,  "rank": "S", "level": 87, "name": "Ma Dong-wuk",      "info": "Master of the Fame Guild. Iron-fisted tank — immovable in combat.",                       "region": "South Korea", "is_user": False},
    {"pos": 9,  "rank": "S", "level": 86, "name": "Lim Tae-gyu",      "info": "Master of the Fiend Guild. Cold and calculating — never acts without an angle.",           "region": "South Korea", "is_user": False},
    {"pos": 10, "rank": "S", "level": 85, "name": "Hwang Dong-soo",   "info": "Defected to US Scavenger Guild. Lethal close-range combatant. Brutal methods.",           "region": "South Korea", "is_user": False},
    {"pos": 11, "rank": "S", "level": 84, "name": "Eun Seok",         "info": "Fell during the Jeju Island Raid. His sacrifice held the line for survivors.",             "region": "South Korea", "is_user": False},
    {"pos": 12, "rank": "S", "level": 82, "name": "Reiji Sugimoto",   "info": "Draw Sword Guild elite. Precision sword techniques with surgical accuracy.",               "region": "Japan",       "is_user": False},
    {"pos": 13, "rank": "S", "level": 80, "name": "Atsushi Kumamoto", "info": "Draw Sword Guild. Brute strength specialist — sheer power over technique.",               "region": "Japan",       "is_user": False},
    {"pos": 14, "rank": "S", "level": 78, "name": "Kei",              "info": "Draw Sword Guild. Fastest blade in East Asia — speed is the only weapon.",                 "region": "Japan",       "is_user": False},
    {"pos": 15, "rank": "S", "level": 76, "name": "Kanae Tawata",     "info": "Draw Sword Guild. Barrier and barrier-break expert. Offense and defense in one.",          "region": "Japan",       "is_user": False},
    {"pos": 16, "rank": "S", "level": 74, "name": "Minoru Hoshino",   "info": "Draw Sword Guild. Tactical command specialist — the mind behind every raid.",              "region": "Japan",       "is_user": False},
    {"pos": 17, "rank": "S", "level": 72, "name": "Kenzo Tanaka",     "info": "Draw Sword Guild. Youngest S-Rank in Japan. Hungry, relentless, fearless.",               "region": "Japan",       "is_user": False},
    {"pos": 18, "rank": "A", "level": 46, "name": "Woo Jin-chul",     "info": "Chief of the Surveillance Team. Loyal enforcer — unwavering in duty.",                    "region": "South Korea", "is_user": False},
    {"pos": 19, "rank": "A", "level": 42, "name": "Kim Chul",         "info": "Elite tank from White Tiger Guild. Unbreakable under any assault.",                        "region": "South Korea", "is_user": False},
    {"pos": 20, "rank": "A", "level": 40, "name": "Lee Minsung",      "info": "Celebrity hunter. Fame before strength — but still dangerous in the field.",              "region": "South Korea", "is_user": False},
    {"pos": 21, "rank": "A", "level": 38, "name": "Park Heejin",      "info": "Mage-class White Tiger member. Devastating area-of-effect spells.",                       "region": "South Korea", "is_user": False},
    {"pos": 22, "rank": "B", "level": 28, "name": "Kang Taeshik",     "info": "Assassin-class Surveillance agent. Lethal instincts, zero hesitation.",                   "region": "South Korea", "is_user": False},
    {"pos": 23, "rank": "B", "level": 22, "name": "Lee Ju-hee",       "info": "Healer who refused high-rank raids after trauma. Her compassion is her strength.",        "region": "South Korea", "is_user": False},
    {"pos": 24, "rank": "C", "level": 15, "name": "Song Chi-yul",     "info": "Elderly mage-swordsman. Jin-woo's early mentor. Wisdom over raw power.",                  "region": "South Korea", "is_user": False},
    {"pos": 25, "rank": "C", "level": 12, "name": "Hwang Dong-suk",   "info": "Former C-Rank strike squad leader. Eliminated. The System does not forget.",              "region": "South Korea", "is_user": False},
    {"pos": 26, "rank": "D", "level": 8,  "name": "Yoo Jinho",        "info": "Jin-woo's closest companion. Ahjin Guild Vice-Master. Heart over stats.",                 "region": "South Korea", "is_user": False},
    {"pos": 27, "rank": "D", "level": 5,  "name": "Yoo Soo-hyun",     "info": "Jinho's cousin. Eager rookie still finding her footing in the system.",                   "region": "South Korea", "is_user": False},
]

_GATES_RAW = [
    # DSA (persistent)
    {"rank": "E", "title": "Echo Chamber",           "desc": "Solve 1 Easy LeetCode problem. Persistent revision gate.",                    "mp": 200,  "type": "DSA",     "gate_type": "persistent"},
    {"rank": "D", "title": "Iron Curtain",            "desc": "Solve 2 Easy LeetCode problems. Returns every 7 days.",                       "mp": 400,  "type": "DSA",     "gate_type": "persistent"},
    {"rank": "C", "title": "Abyssal Array",           "desc": "Solve 1 Medium LeetCode problem. Persistent revision gate.",                  "mp": 800,  "type": "DSA",     "gate_type": "persistent"},
    {"rank": "B", "title": "Phantom Graph",           "desc": "Solve 2 Medium LeetCode problems. Returns every 7 days.",                     "mp": 1200, "type": "DSA",     "gate_type": "persistent"},
    {"rank": "A", "title": "Monarch's Trial",         "desc": "Solve 3 Medium LeetCode problems. Persistent mastery gate.",                  "mp": 1800, "type": "DSA",     "gate_type": "persistent"},
    {"rank": "S", "title": "The Architect's Domain",  "desc": "Solve 1 Hard LeetCode problem. Persistent — never truly conquered.",          "mp": 3000, "type": "DSA",     "gate_type": "persistent"},
    # FITNESS (persistent)
    {"rank": "E", "title": "Shadow Steps",            "desc": "20 push-ups + 20 squats in under 5 minutes. Persistent gate.",               "mp": 200,  "type": "FITNESS", "gate_type": "persistent"},
    {"rank": "D", "title": "Stone Pillar",            "desc": "50 push-ups + 50 squats in under 10 minutes. Returns every 7 days.",         "mp": 400,  "type": "FITNESS", "gate_type": "persistent"},
    {"rank": "B", "title": "Dark Corridor",           "desc": "100 push-ups + 100 squats + 50 pull-ups. Persistent endurance gate.",        "mp": 1200, "type": "FITNESS", "gate_type": "persistent"},
    # DEV (iterative)
    {"rank": "C", "title": "Crimson Veil",            "desc": "Deploy a functioning mini-project (any stack). Complete once.",              "mp": 800,  "type": "DEV",     "gate_type": "iterative"},
    {"rank": "A", "title": "Gate of Giants",          "desc": "Deploy a full-stack project with auth. One-time milestone.",                 "mp": 1800, "type": "DEV",     "gate_type": "iterative"},
    {"rank": "S", "title": "Dungeon of Endless Code", "desc": "Ship a SaaS MVP with paying users. The final iterative milestone.",         "mp": 3000, "type": "DEV",     "gate_type": "iterative"},
]


# ── AppState ─────────────────────────────────────────────────────────

class AppState(rx.State):

    # ── Onboarding ────────────────────────────────────────────────────
    awakened: bool = False
    onboarding_step: int = 0
    user_name: str = ""
    fitness_goal: str = ""
    main_class: str = ""
    dsa_per_day: int = 2
    projects_per_week: int = 1
    custom_quests: list[str] = []
    new_quest_input: str = ""
    extra_activities: str = ""
    # OpenAI planner
    openai_api_key: str = ""
    quest_plan_loading: bool = False

    # ── Navigation ────────────────────────────────────────────────────
    active_page: str = "dashboard"
    profile_open: bool = False

    # ── Quests ────────────────────────────────────────────────────────
    daily_quests: list[QuestItem] = []
    weekly_quests: list[QuestItem] = [
        {"id": "w_rev",     "title": "Weekend revision session",  "type": "DSA",     "done": False, "xp": 500},
        {"id": "w_fitness", "title": "Fitness: 7-day streak",     "type": "FITNESS", "done": False, "xp": 500},
    ]
    monthly_quests: list[QuestItem] = [
        {"id": "m1", "title": "Complete 30-day challenge",        "type": "DSA",     "done": False, "xp": 2000},
        {"id": "m2", "title": "Fitness: 30-day streak",           "type": "FITNESS", "done": False, "xp": 2000},
    ]

    # ── Quest verification popup ──────────────────────────────────────
    verify_quest_id: str = ""
    verify_quest_type: str = ""
    verify_link_1: str = ""
    verify_link_2: str = ""
    verify_link_3: str = ""
    verify_error: str = ""

    # ── Quest adding form ─────────────────────────────────────────────
    add_quest_mode: str = ""        # "daily" | "weekly" | "monthly" | ""
    new_add_quest_title: str = ""
    new_add_quest_type: str = "DSA"

    # ── Penalties ─────────────────────────────────────────────────────
    penalty_active: bool = False
    penalty_rank: str = "B"
    penalty_message: str = ""
    penalty_quest_title: str = ""

    # ── XP ────────────────────────────────────────────────────────────
    total_xp: int = 0          # backend only, never shown
    current_xp: int = 0
    level: int = 1
    hunter_rank: str = "E"

    # ── MP ────────────────────────────────────────────────────────────
    total_mp: int = 0          # backend only
    current_mp: int = 0
    mp_level: int = 1

    # ── Stats ─────────────────────────────────────────────────────────
    strength: float = 0.0
    intelligence: float = 0.0
    perception: float = 0.0

    # ── Streak ────────────────────────────────────────────────────────
    streak: int = 0

    # ── Punishment ───────────────────────────────────────────────────
    missed_strength_days: int = 0
    missed_intelligence_days: int = 0
    missed_perception_days: int = 0

    # ── Instance dungeon ─────────────────────────────────────────────
    instance_dungeon_key_count: int = 0
    show_key_popup: bool = False

    # ── Leaderboard ───────────────────────────────────────────────────
    leaderboard: list[HunterEntry] = HUNTER_DATA

    # ── Gates ─────────────────────────────────────────────────────────
    selected_gate: GateDisplayEntry = _EMPTY_GATE
    gate_proof_url: str = ""
    gate_cleared_ids: list[str] = []
    persistent_gate_cleared_titles: list[str] = []
    persistent_gate_cleared_dates: list[str] = []
    gate_verify_message: str = ""
    verification_url: str = ""
    verification_message: str = ""

    # ── Commitment Wallet ─────────────────────────────────────────────
    wallet_balance: float = 0.0       # total committed (≤ level × 10)
    wallet_frozen: float = 0.0        # frozen due to missed quests
    add_commitment_amount: str = ""   # input field (string for rx.input)
    commitment_history: list[str] = []
    commitment_upi_id: str = ""       # filled by user in commitment page
    show_commitment_qr: bool = False
    commitment_qr_amount: float = 0.0

    # ────────────────── COMPUTED VARS ────────────────────────────────

    @rx.var
    def xp_to_level_up(self) -> int:
        return 200 + (self.level - 1) * 100

    @rx.var
    def xp_progress_pct(self) -> int:
        needed = 200 + (self.level - 1) * 100
        return min(int((self.current_xp / needed) * 100), 100) if needed else 0

    @rx.var
    def mp_to_level_up(self) -> int:
        return 200 + (self.mp_level - 1) * 100

    @rx.var
    def mp_progress_pct(self) -> int:
        needed = 200 + (self.mp_level - 1) * 100
        return min(int((self.current_mp / needed) * 100), 100) if needed else 0

    @rx.var
    def perception_is_sinful(self) -> bool:
        return self.missed_perception_days >= 2

    @rx.var
    def chart_data(self) -> list[PerformancePoint]:
        expected = self.dsa_per_day + 1
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        result: list[PerformancePoint] = []
        for i, day in enumerate(days):
            days_back = 6 - i
            if self.streak > days_back:
                actual = expected
            elif self.streak == days_back:
                actual = max(0, expected - 1)
            else:
                actual = max(0, expected - 2)
            result.append({"day": day, "expected": expected, "actual": actual})
        return result

    @rx.var
    def is_on_track(self) -> bool:
        return self.streak >= 3

    @rx.var
    def strength_pct(self) -> int:
        return min(int(self.strength), 100)

    @rx.var
    def strength_display(self) -> int:
        return int(self.strength)

    @rx.var
    def intelligence_pct(self) -> int:
        return min(int(self.intelligence), 100)

    @rx.var
    def intelligence_display(self) -> int:
        return int(self.intelligence)

    @rx.var
    def perception_pct(self) -> int:
        return min(int(self.perception), 100)

    @rx.var
    def perception_display(self) -> int:
        return int(self.perception)

    @rx.var
    def completed_daily_count(self) -> int:
        return sum(1 for q in self.daily_quests if q["done"])

    @rx.var
    def total_daily_count(self) -> int:
        return len(self.daily_quests)

    @rx.var
    def daily_progress_pct(self) -> int:
        total = len(self.daily_quests)
        if not total:
            return 0
        return int((sum(1 for q in self.daily_quests if q["done"]) / total) * 100)

    @rx.var
    def all_daily_done(self) -> bool:
        """True iff every daily quest is completed."""
        if not self.daily_quests:
            return False
        return all(q["done"] for q in self.daily_quests)

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
        }.get(self.hunter_rank, "rank-e")

    @rx.var
    def verify_is_open(self) -> bool:
        return self.verify_quest_id != ""

    @rx.var
    def recommended_dsa(self) -> int:
        return 2 if self.main_class == "Shadow Mage" else 1

    @rx.var
    def recommended_projects(self) -> int:
        return 1 if self.main_class == "Shadow Mage" else 2

    @rx.var
    def dsa_is_recommended(self) -> bool:
        return self.dsa_per_day == self.recommended_dsa

    @rx.var
    def projects_is_recommended(self) -> bool:
        return self.projects_per_week == self.recommended_projects

    @rx.var
    def commitment_plan_text(self) -> str:
        name = self.user_name if self.user_name else "Hunter"
        lines = [
            "══════════════════════════════════════════════════",
            f"   SYSTEM CONFIGURATION  //  {name.upper()[:22]}",
            "══════════════════════════════════════════════════",
            "",
            f"  MAIN CLASS  ▸  {self.main_class or '???'}",
            "",
            "  [ DSA PROTOCOL ]",
            f"    ▸ Weekdays  : {self.dsa_per_day} LeetCode problem(s) per day",
            "    ▸ Weekends  : Revision only — no new problems",
            "",
            "  [ PROJECT PROTOCOL ]",
            f"    ▸ Weekly   : {self.projects_per_week} project deployment(s)",
        ]
        if self.fitness_goal:
            lines += ["", "  [ FITNESS ]", f"    ▸ {self.fitness_goal[:60]}"]
        if self.custom_quests:
            lines += ["", "  [ CUSTOM QUESTS ]"]
            for q in self.custom_quests:
                lines.append(f"    ▸ {q[:55]}")
        if self.extra_activities:
            lines += ["", "  [ EXTRACURRICULARS ]", f"    ▸ {self.extra_activities[:60]}"]
        lines += [
            "",
            "  [ PENALTY PROTOCOL ]",
            "    ▸ Missed daily (FITNESS)     → -0.33 STR, -100 XP",
            "    ▸ Missed daily (DSA/DEV)     → -0.20 INT, -100 XP",
            "    ▸ Missed daily (CUSTOM)      → -0.50 PER, -100 XP",
            "    ▸ 2+ missed CUSTOM days      → SINFUL status",
            "    ▸ Missed quest               → 1% wallet frozen",
            "",
            "══════════════════════════════════════════════════",
        ]
        return "\n".join(lines)

    @rx.var
    def leaderboard_with_user(self) -> list[HunterEntry]:
        """Inserts the current user into the hunter leaderboard by level."""
        user_entry: HunterEntry = {
            "pos": 0,
            "rank": self.hunter_rank,
            "level": self.level,
            "name": (self.user_name + " ★") if self.user_name else "You ★",
            "info": "The System is watching. That is you. Keep climbing.",
            "region": "Your Desk",
            "is_user": True,
        }
        all_hunters: list[HunterEntry] = [
            {
                "pos": h["pos"], "rank": h["rank"], "level": h["level"],
                "name": h["name"], "info": h["info"], "region": h["region"],
                "is_user": False,
            }
            for h in HUNTER_DATA
        ] + [user_entry]
        sorted_hunters = sorted(all_hunters, key=lambda h: h["level"], reverse=True)
        result: list[HunterEntry] = []
        for i, h in enumerate(sorted_hunters):
            result.append({
                "pos": i + 1,
                "rank": h["rank"],
                "level": h["level"],
                "name": h["name"],
                "info": h["info"],
                "region": h["region"],
                "is_user": h["is_user"],
            })
        return result

    @rx.var
    def gate_display_list(self) -> list[GateDisplayEntry]:
        today = datetime.date.today()
        result: list[GateDisplayEntry] = []
        for gate in _GATES_RAW:
            title = gate["title"]
            gtype = gate["gate_type"]

            if gtype == "iterative":
                status = "cleared" if title in self.gate_cleared_ids else "active"
                result.append({
                    "rank": gate["rank"], "title": title, "desc": gate["desc"],
                    "mp": gate["mp"], "type": gate["type"], "gate_type": gtype,
                    "status": status, "days_remaining": 0,
                })
            else:  # persistent
                if title in self.persistent_gate_cleared_titles:
                    idx = self.persistent_gate_cleared_titles.index(title)
                    if idx < len(self.persistent_gate_cleared_dates):
                        try:
                            cleared = datetime.date.fromisoformat(
                                self.persistent_gate_cleared_dates[idx])
                            days_ago = (today - cleared).days
                            days_left = max(0, 7 - days_ago)
                            status = "refreshing" if days_ago <= 7 else "overdue"
                            result.append({
                                "rank": gate["rank"], "title": title, "desc": gate["desc"],
                                "mp": gate["mp"], "type": gate["type"], "gate_type": gtype,
                                "status": status, "days_remaining": days_left,
                            })
                            continue
                        except Exception:
                            pass
                result.append({
                    "rank": gate["rank"], "title": title, "desc": gate["desc"],
                    "mp": gate["mp"], "type": gate["type"], "gate_type": gtype,
                    "status": "active", "days_remaining": 0,
                })
        return result

    @rx.var
    def wallet_cap(self) -> int:
        return self.level * 10

    @rx.var
    def wallet_available(self) -> float:
        return max(0.0, self.wallet_balance - self.wallet_frozen)

    @rx.var
    def wallet_room_left(self) -> float:
        return max(0.0, float(self.wallet_cap) - self.wallet_balance)

    @rx.var
    def wallet_frozen_pct(self) -> int:
        if self.wallet_balance <= 0:
            return 0
        return min(100, int((self.wallet_frozen / self.wallet_balance) * 100))

    @rx.var
    def wallet_available_pct(self) -> int:
        if self.wallet_balance <= 0:
            return 0
        return min(100, int((self.wallet_available / self.wallet_balance) * 100))

    @rx.var
    def upi_qr_url(self) -> str:
        """Google Charts QR URL for UPI deep link."""
        if not self.commitment_upi_id or self.commitment_qr_amount <= 0:
            return ""
        upi_link = (
            f"upi://pay?pa={self.commitment_upi_id}"
            f"&pn=Leveling+Up+Commitment"
            f"&am={self.commitment_qr_amount:.2f}"
            f"&cu=INR"
            f"&tn=Commitment+Wallet+Deposit"
        )
        import urllib.parse
        encoded = urllib.parse.quote(upi_link, safe="")
        return (
            f"https://api.qrserver.com/v1/create-qr-code/"
            f"?size=220x220&data={encoded}&bgcolor=080808&color=00d4ff&margin=2"
        )

    @rx.var
    def selected_gate_is_open(self) -> bool:
        return self.selected_gate["title"] != ""

    # ── INTERNAL HELPERS ─────────────────────────────────────────────

    def _award_xp(self, amount: int):
        self.total_xp += amount
        self.current_xp += amount
        self._check_level_up()
        # wallet cap increases on level up
        # (wallet_cap is computed, no explicit update needed)

    def _reverse_xp(self, amount: int):
        """Reverse an XP gain. May level down. Used for uncomplete."""
        self.total_xp = max(0, self.total_xp - amount)
        self.current_xp = max(0, self.current_xp - amount)
        # check if we crossed a level boundary going backward
        new_level = _level_from_total_xp(self.total_xp)
        if new_level < self.level:
            self.level = new_level
            xp_at_level = _xp_for_level(new_level)
            self.current_xp = max(0, self.total_xp - xp_at_level)
        self._update_rank()

    def _check_level_up(self):
        while True:
            xp_needed = 200 + (self.level - 1) * 100
            if self.current_xp >= xp_needed:
                self.current_xp -= xp_needed
                self.level += 1
            else:
                break
        self._update_rank()

    def _apply_punishment_xp(self, amount: int):
        self.total_xp = max(0, self.total_xp - amount)
        new_level = _level_from_total_xp(self.total_xp)
        if new_level != self.level:
            self.level = new_level
        xp_at_level = _xp_for_level(self.level)
        self.current_xp = max(0, self.total_xp - xp_at_level)
        self._update_rank()

    def _update_rank(self):
        if   self.level >= 50: self.hunter_rank = "S"
        elif self.level >= 35: self.hunter_rank = "A"
        elif self.level >= 20: self.hunter_rank = "B"
        elif self.level >= 10: self.hunter_rank = "C"
        elif self.level >= 5:  self.hunter_rank = "D"
        else:                  self.hunter_rank = "E"

    def _award_mp(self, amount: int):
        self.total_mp += amount
        self.current_mp += amount
        self._check_mp_level_up()

    def _check_mp_level_up(self):
        while True:
            needed = 200 + (self.mp_level - 1) * 100
            if self.current_mp >= needed:
                self.current_mp -= needed
                self.mp_level += 1
            else:
                break

    def _deduct_mp(self, amount: int):
        self.total_mp = max(0, self.total_mp - amount)
        new_level = _mp_level_from_total(self.total_mp)
        self.mp_level = new_level
        self.current_mp = max(0, self.total_mp - _mp_for_level(new_level))

    def _stat_gain_for_type(self, qt: str, multiplier: int):
        """Add or remove stat points based on quest type."""
        gain = float(multiplier * max(1, self.level))
        if qt == "FITNESS":
            self.strength = max(0.0, min(9999.0, self.strength + gain))
        elif qt in ("DSA", "DEV"):
            self.intelligence = max(0.0, min(9999.0, self.intelligence + gain))
        elif qt == "CUSTOM":
            self.perception = max(0.0, min(9999.0, self.perception + gain))

    # ── ONBOARDING EVENTS ─────────────────────────────────────────────

    def set_user_name(self, v: str):        self.user_name = v
    def set_fitness_goal(self, v: str):     self.fitness_goal = v
    def set_extra_activities(self, v: str): self.extra_activities = v
    def set_new_quest_input(self, v: str):  self.new_quest_input = v
    def set_openai_api_key(self, v: str):   self.openai_api_key = v

    def next_step(self):  self.onboarding_step += 1
    def prev_step(self):
        if self.onboarding_step > 1: self.onboarding_step -= 1

    def choose_class(self, cls: str):
        self.main_class = cls
        if cls == "Shadow Mage":
            self.dsa_per_day = 2;  self.projects_per_week = 1
        else:
            self.dsa_per_day = 1;  self.projects_per_week = 2
        self.onboarding_step = 3

    def increment_dsa(self):
        if self.dsa_per_day < 3: self.dsa_per_day += 1

    def decrement_dsa(self):
        if self.dsa_per_day > 1: self.dsa_per_day -= 1

    def increment_projects(self):
        if self.projects_per_week < 3: self.projects_per_week += 1

    def decrement_projects(self):
        if self.projects_per_week > 1: self.projects_per_week -= 1

    def add_custom_quest(self):
        q = self.new_quest_input.strip()
        if q:
            self.custom_quests = self.custom_quests + [q]
            self.new_quest_input = ""

    def remove_custom_quest(self, quest: str):
        self.custom_quests = [q for q in self.custom_quests if q != quest]

    def handle_quest_key(self, key: str):
        if key == "Enter": self.add_custom_quest()

    def handle_name_key(self, key: str):
        if key == "Enter" and self.user_name.strip(): self.onboarding_step = 2

    def accept_awakening(self):
        """Build quests from user inputs. Calls OpenAI for smart planning."""
        fitness_text = self.fitness_goal.strip()
        extras_text  = self.extra_activities.strip()

        # If user typed "default" or nothing, use a standard beginner plan
        if not fitness_text or fitness_text.lower() == "default":
            fitness_text = "50 push-ups, 30 squats, 20 sit-ups, and a 10-minute walk every day"

        quests: list[QuestItem] = [
            {"id": "d_dsa", "title": f"LeetCode: {self.dsa_per_day} problem(s) today",           "type": "DSA",     "done": False, "xp": 100},
            {"id": "d_dev", "title": f"Project work ({self.projects_per_week} deploy/wk goal)",  "type": "DEV",     "done": False, "xp": 100},
        ]

        for i, cq in enumerate(self.custom_quests):
            quests.append({"id": f"d_cq{i}", "title": cq[:60], "type": "CUSTOM", "done": False, "xp": 100})

        # ── OpenAI smart planner ──────────────────────────────
        if _OPENAI_KEY:
            try:
                import openai
                client = openai.OpenAI(api_key=_OPENAI_KEY)
                prompt = (
                    f"You are a strict habit coach for a gamified leveling app called 'The System'.\n"
                    f"Generate specific DAILY tasks for this hunter.\n"
                    f"  Name: {self.user_name}\n"
                    f"  Fitness plan: {fitness_text}\n"
                    f"  Extra pursuits: {extras_text if extras_text else 'none'}\n\n"
                    f"Rules:\n"
                    f"- Break the fitness plan into 2-3 concrete daily tasks (exact reps/duration).\n"
                    f"- Break each extra pursuit into 1 specific daily action.\n"
                    f"- Format ONLY: TYPE|TITLE  (TYPE = FITNESS or CUSTOM, TITLE max 55 chars)\n"
                    f"- Max 5 lines total. No intro, no numbering, no explanations."
                )
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=300,
                    temperature=0.7,
                )
                lines = response.choices[0].message.content.strip().split("\n")
                for idx, line in enumerate(lines[:5]):
                    if "|" in line:
                        parts = line.split("|", 1)
                        qt = parts[0].strip().upper()
                        title = parts[1].strip()[:60]
                        if qt not in ("FITNESS", "CUSTOM", "DSA", "DEV"):
                            qt = "CUSTOM"
                        quests.append({"id": f"d_ai{idx}", "title": title, "type": qt, "done": False, "xp": 100})
            except Exception:
                for i, item in enumerate(fitness_text.split(",")[:3]):
                    item = item.strip()
                    if item:
                        quests.append({"id": f"d_fit{i}", "title": item[:60], "type": "FITNESS", "done": False, "xp": 100})
                if extras_text:
                    for i, item in enumerate(extras_text.replace("\n", ",").split(",")[:2]):
                        item = item.strip()
                        if item:
                            quests.append({"id": f"d_ex{i}", "title": item[:60], "type": "CUSTOM", "done": False, "xp": 100})
        else:
            for i, item in enumerate(fitness_text.split(",")[:3]):
                item = item.strip()
                if item:
                    quests.append({"id": f"d_fit{i}", "title": item[:60], "type": "FITNESS", "done": False, "xp": 100})
            if extras_text:
                for i, item in enumerate(extras_text.replace("\n", ",").split(",")[:2]):
                    item = item.strip()
                    if item:
                        quests.append({"id": f"d_ex{i}", "title": item[:60], "type": "CUSTOM", "done": False, "xp": 100})

        self.daily_quests = quests

        weekly_dsa = self.dsa_per_day * 5
        weekly: list[QuestItem] = [
            {"id": "w_dsa", "title": f"LeetCode: {weekly_dsa} problems (weekdays total)", "type": "DSA",     "done": False, "xp": 500},
            {"id": "w_dev", "title": f"Deploy {self.projects_per_week} project(s) this week",  "type": "DEV",     "done": False, "xp": 500},
            {"id": "w_rev", "title": "Weekend revision session",                               "type": "DSA",     "done": False, "xp": 500},
            {"id": "w_fit", "title": "Fitness: 7-day streak",                                  "type": "FITNESS", "done": False, "xp": 500},
        ]
        if self.extra_activities.strip():
            weekly.append({"id": "w_extras", "title": f"Weekly: {self.extra_activities[:45]}", "type": "CUSTOM", "done": False, "xp": 500})
        self.weekly_quests = weekly
        self.awakened = True
        self.active_page = "dashboard"

    # ── NAVIGATION ────────────────────────────────────────────────────

    def navigate_to(self, page: str):
        self.active_page = page;  self.profile_open = False

    def toggle_profile(self):  self.profile_open = not self.profile_open
    def close_profile(self):   self.profile_open = False

    # ── QUEST VERIFICATION POPUP ──────────────────────────────────────

    def quest_click(self, quest_id: str):
        """Click a daily quest: open verify if not done, undo reward if done."""
        for q in self.daily_quests:
            if q["id"] == quest_id:
                if q["done"]:
                    # -- UNCOMPLETE: check if all were done before this --
                    all_done_before = all(qq["done"] for qq in self.daily_quests)

                    updated = []
                    for qq in self.daily_quests:
                        if qq["id"] == quest_id:
                            # Reverse XP (not punishment — just undo the gain)
                            self._reverse_xp(100)
                            # Reverse stat gain
                            stat_gain = float(2 * max(1, self.level))
                            qt = qq["type"]
                            if qt == "FITNESS":
                                self.strength = max(0.0, self.strength - stat_gain)
                            elif qt in ("DSA", "DEV"):
                                self.intelligence = max(0.0, self.intelligence - stat_gain)
                            elif qt == "CUSTOM":
                                self.perception = max(0.0, self.perception - stat_gain)
                            qq = {**qq, "done": False}
                        updated.append(qq)
                    self.daily_quests = updated

                    # If all were done before this uncomplete, lose 1 streak day
                    if all_done_before:
                        self.streak = max(0, self.streak - 1)
                else:
                    # -- OPEN VERIFY POPUP --
                    self.verify_quest_id = quest_id
                    self.verify_quest_type = q["type"]
                    # FITNESS and CUSTOM skip the verify popup — complete instantly
                    if q["type"] in ("FITNESS", "CUSTOM"):
                        self.verify_link_1 = "__skip__"
                        self.submit_quest_verify()
                        return
                    self.verify_link_1 = "";  self.verify_link_2 = ""
                    self.verify_link_3 = "";  self.verify_error = ""
                break

    def set_verify_link_1(self, v: str):  self.verify_link_1 = v;  self.verify_error = ""
    def set_verify_link_2(self, v: str):  self.verify_link_2 = v;  self.verify_error = ""
    def set_verify_link_3(self, v: str):  self.verify_link_3 = v;  self.verify_error = ""

    def cancel_verify(self):
        self.verify_quest_id = "";  self.verify_quest_type = ""
        self.verify_link_1 = "";  self.verify_link_2 = "";  self.verify_link_3 = ""
        self.verify_error = ""

    def submit_quest_verify(self):
        if not self.verify_quest_id: return
        # DSA and DEV require a link; FITNESS and CUSTOM do not
        qt = self.verify_quest_type
        if qt in ("DSA", "DEV") and not self.verify_link_1.strip():
            self.verify_error = "At least 1 solution / proof link is required."; return

        stat_gain = 2 * max(1, self.level)
        all_done_before = all(q["done"] for q in self.daily_quests)

        updated = []
        for q in self.daily_quests:
            if q["id"] == self.verify_quest_id:
                q = {**q, "done": True}
                self._award_xp(100)
                self._stat_gain_for_type(qt, 2)
                # 12.5% random dungeon key — truly random via os.urandom seed
                if random.SystemRandom().random() < 0.125:
                    self.instance_dungeon_key_count += 1
                    self.show_key_popup = True
            updated.append(q)
        self.daily_quests = updated

        # Streak: only count when ALL quests are now done
        all_done_after = all(q["done"] for q in updated)
        if not all_done_before and all_done_after:
            self.streak += 1

        self.cancel_verify()

    def dismiss_key_popup(self):
        self.show_key_popup = False

    # ── RESET DAY ─────────────────────────────────────────────────────

    def reset_daily_quests(self):
        """End-of-day: punish missed quests, freeze wallet, reset quests."""
        missed_count = 0
        for q in self.daily_quests:
            if not q["done"]:
                missed_count += 1
                self._apply_punishment_xp(100)
                qt = q["type"]
                if qt == "FITNESS":
                    self.strength = max(0.0, self.strength - 0.33)
                    self.missed_strength_days += 1
                elif qt in ("DSA", "DEV"):
                    self.intelligence = max(0.0, self.intelligence - 0.2)
                    self.missed_intelligence_days += 1
                elif qt == "CUSTOM":
                    self.perception = max(0.0, self.perception - 0.5)
                    self.missed_perception_days += 1

        # Freeze 1% of wallet per missed quest
        if missed_count > 0 and self.wallet_balance > 0:
            new_freeze = min(
                self.wallet_balance,
                self.wallet_frozen + self.wallet_balance * 0.01 * missed_count,
            )
            added = new_freeze - self.wallet_frozen
            self.wallet_frozen = new_freeze
            if added > 0:
                self.commitment_history = [
                    f"❄ Rs. {added:.2f} frozen — {missed_count} quest(s) missed"
                ] + self.commitment_history

        # Reset daily quests
        self.daily_quests = [{**q, "done": False} for q in self.daily_quests]

    # ── WEEKLY / MONTHLY QUEST TOGGLES ───────────────────────────────

    def toggle_weekly_quest(self, quest_id: str):
        updated = []
        for q in self.weekly_quests:
            if q["id"] == quest_id:
                new_done = not q["done"]
                q = {**q, "done": new_done}
                if new_done:
                    self._award_xp(500)
                    self._stat_gain_for_type(q["type"], 2)
                else:
                    self._reverse_xp(500)
                    self._stat_gain_for_type(q["type"], -2)
            updated.append(q)
        self.weekly_quests = updated

    def toggle_monthly_quest(self, quest_id: str):
        updated = []
        for q in self.monthly_quests:
            if q["id"] == quest_id:
                new_done = not q["done"]
                q = {**q, "done": new_done}
                if new_done:
                    self._award_xp(2000)
                    self._stat_gain_for_type(q["type"], 4)
                else:
                    self._reverse_xp(2000)
                    self._stat_gain_for_type(q["type"], -4)
            updated.append(q)
        self.monthly_quests = updated

    # ── QUEST ADDING FROM DASHBOARD ───────────────────────────────────

    def open_add_quest_form(self, mode: str):
        self.add_quest_mode = mode
        self.new_add_quest_title = ""
        self.new_add_quest_type = "DSA"

    def close_add_quest_form(self):
        self.add_quest_mode = ""
        self.new_add_quest_title = ""

    def set_new_add_quest_title(self, v: str):  self.new_add_quest_title = v
    def set_new_add_quest_type(self, v: str):   self.new_add_quest_type = v

    def submit_add_quest(self):
        title = self.new_add_quest_title.strip()
        if not title: return
        qtype = self.new_add_quest_type
        mode = self.add_quest_mode

        if mode == "daily":
            new_id = f"d_custom_{len(self.daily_quests)}"
            self.daily_quests = self.daily_quests + [
                {"id": new_id, "title": title, "type": qtype, "done": False, "xp": 100}
            ]
        elif mode == "weekly":
            new_id = f"w_custom_{len(self.weekly_quests)}"
            self.weekly_quests = self.weekly_quests + [
                {"id": new_id, "title": title, "type": qtype, "done": False, "xp": 500}
            ]
        elif mode == "monthly":
            new_id = f"m_custom_{len(self.monthly_quests)}"
            self.monthly_quests = self.monthly_quests + [
                {"id": new_id, "title": title, "type": qtype, "done": False, "xp": 2000}
            ]
        self.close_add_quest_form()

    # ── PENALTY EVENTS ────────────────────────────────────────────────

    def trigger_penalty(self, rank: str, missed_quest: str):
        self.penalty_rank = rank
        self.penalty_quest_title = missed_quest
        msgs = {
            "B": f"[SYSTEM WARNING] You failed: '{missed_quest}'. B-Rank Penalty Quest is now active.",
            "A": f"[SYSTEM ALERT] Weekly objective FAILED: '{missed_quest}'. A-Rank Penalty engaged.",
            "S": f"[SYSTEM CRITICAL] Monthly objective FAILED: '{missed_quest}'. S-RANK PENALTY PROTOCOL ENGAGED.",
        }
        self.penalty_message = msgs.get(rank, "Penalty assigned.")
        self.penalty_active = True

    def dismiss_penalty(self): self.penalty_active = False

    # ── GATE EVENTS ───────────────────────────────────────────────────

    def select_gate(self, gate: GateDisplayEntry):
        self.selected_gate = gate
        self.gate_proof_url = ""
        self.gate_verify_message = ""

    def set_gate_proof_url(self, v: str):  self.gate_proof_url = v

    def clear_gate(self):
        self.selected_gate = _EMPTY_GATE
        self.gate_proof_url = ""

    def submit_gate_clear(self):
        title = self.selected_gate.get("title", "")
        gtype = self.selected_gate.get("gate_type", "iterative")
        gt = self.selected_gate.get("type", "")
        if not title: return

        # No proof needed for FITNESS gates (no URL)
        if gt not in ("FITNESS", "CUSTOM") and not self.gate_proof_url.strip():
            self.gate_verify_message = "ERROR: Proof URL required."; return

        mp_reward = self.selected_gate.get("mp", 0)
        self._award_mp(mp_reward)

        if gtype == "iterative":
            if title not in self.gate_cleared_ids:
                self.gate_cleared_ids = self.gate_cleared_ids + [title]
        else:
            today = datetime.date.today().isoformat()
            if title in self.persistent_gate_cleared_titles:
                idx = self.persistent_gate_cleared_titles.index(title)
                dates = list(self.persistent_gate_cleared_dates)
                if idx < len(dates):
                    dates[idx] = today
                else:
                    dates.append(today)
                self.persistent_gate_cleared_dates = dates
            else:
                self.persistent_gate_cleared_titles = self.persistent_gate_cleared_titles + [title]
                self.persistent_gate_cleared_dates = self.persistent_gate_cleared_dates + [today]

        self.gate_verify_message = f"GATE CLEARED: {title} | +{mp_reward} MP"
        self.selected_gate = _EMPTY_GATE
        self.gate_proof_url = ""

    def check_persistent_gate_penalties(self):
        today = datetime.date.today()
        still_t: list[str] = []
        still_d: list[str] = []
        for i, title in enumerate(self.persistent_gate_cleared_titles):
            if i >= len(self.persistent_gate_cleared_dates):
                continue
            try:
                cleared = datetime.date.fromisoformat(self.persistent_gate_cleared_dates[i])
                if (today - cleared).days > 7:
                    self._deduct_mp(700)
                else:
                    still_t.append(title)
                    still_d.append(self.persistent_gate_cleared_dates[i])
            except Exception:
                pass
        self.persistent_gate_cleared_titles = still_t
        self.persistent_gate_cleared_dates = still_d

    # ── COMMITMENT WALLET EVENTS ──────────────────────────────────────

    def set_add_commitment_amount(self, v: str):
        self.add_commitment_amount = v

    def set_commitment_upi_id(self, v: str):
        self.commitment_upi_id = v

    def open_commitment_qr(self):
        """Validate amount, show QR code for UPI payment."""
        try:
            amount = float(self.add_commitment_amount)
        except (ValueError, TypeError):
            return
        if amount < 1:
            return
        room = float(self.wallet_cap) - self.wallet_balance
        amount = min(amount, room)
        if amount <= 0:
            return
        self.commitment_qr_amount = amount
        self.show_commitment_qr = True

    def confirm_commitment_paid(self):
        """User confirms they scanned and paid — add to balance."""
        amount = self.commitment_qr_amount
        if amount <= 0:
            return
        self.wallet_balance = min(self.wallet_balance + amount, float(self.wallet_cap))
        ts = datetime.date.today().isoformat()
        self.commitment_history = [
            f"✓ Rs. {amount:.2f} added — {ts}"
        ] + self.commitment_history
        self.show_commitment_qr = False
        self.commitment_qr_amount = 0.0
        self.add_commitment_amount = ""

    def cancel_commitment_qr(self):
        self.show_commitment_qr = False
        self.commitment_qr_amount = 0.0

    # ── MISC ──────────────────────────────────────────────────────────

    def set_verification_url(self, v: str):   self.verification_url = v
    def clear_verification_message(self):     self.verification_message = ""
