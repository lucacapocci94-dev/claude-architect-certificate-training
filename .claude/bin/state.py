#!/usr/bin/env python3
"""State management for the Claude Architect training program.

Subcommands:
  init                     Create profile.json / progress.json from templates if missing.
  session-start            Print a compact briefing for the SessionStart hook.
  show                     Print a human-friendly progress report (for /progress).
  syllabus                 Print the full curriculum with status flags.
  set-profile  --name N --level L [--goal G]...
                           Update the student profile (name, level, goals).
  complete     <lesson-id> [--notes "..."]
                           Mark a lesson as completed and advance the pointer.
  set-current  --track T --module M [--next CMD]
                           Update the current pointer (resume position).
  add-note     "free text"
                           Append a remembered note (project context, goals, blockers).
  reset        [--hard]
                           Reset progress (and profile if --hard).
  next                     Print the suggested next command for the student.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # .claude/
STATE_DIR = ROOT / "state"
SCHEMA_DIR = STATE_DIR / "schema"
PROFILE = STATE_DIR / "profile.json"
PROGRESS = STATE_DIR / "progress.json"
NOTES = STATE_DIR / "notes.md"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_template(name: str) -> dict:
    with open(SCHEMA_DIR / f"{name}.template.json", encoding="utf-8") as f:
        return json.load(f)


def load_json(path: Path, fallback: dict) -> dict:
    if not path.exists():
        return fallback
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return fallback


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def ensure_init() -> tuple[dict, dict]:
    """Make sure profile.json and progress.json exist; return both loaded."""
    profile_default = load_template("profile")
    progress_default = load_template("progress")
    if not PROFILE.exists():
        profile_default["started_at"] = now_iso()
        save_json(PROFILE, profile_default)
    if not PROGRESS.exists():
        save_json(PROGRESS, progress_default)
    profile = load_json(PROFILE, profile_default)
    progress = load_json(PROGRESS, progress_default)
    return profile, progress


def cmd_init(_args) -> int:
    profile, progress = ensure_init()
    print("Initialized state files:")
    print(f"  - {PROFILE}")
    print(f"  - {PROGRESS}")
    print(f"profile.name={profile.get('name')} progress.current={progress.get('current')}")
    return 0


def _completed_ids(progress: dict) -> set[str]:
    return {entry["id"] for entry in progress.get("completed", [])}


def _all_lessons(progress: dict) -> list[tuple[str, str]]:
    """Return [(track_key, lesson_id)] in canonical order."""
    out: list[tuple[str, str]] = []
    for tk, t in progress.get("tracks", {}).items():
        for lid in t.get("lessons", []):
            out.append((tk, lid))
    return out


def cmd_session_start(_args) -> int:
    """Inject a brief, structured state report at the top of the session.

    The hook stdout becomes additional context for the model. Keep this
    compact — every token costs the student money.
    """
    profile, progress = ensure_init()
    name = profile.get("name")
    level = profile.get("level")
    completed = _completed_ids(progress)
    total = len(_all_lessons(progress))
    current = progress.get("current", {})

    lines = []
    lines.append("<training-state>")
    if not name:
        lines.append("  status: NEW_STUDENT — no profile yet. Open the session with /start to collect name and level.")
    else:
        lines.append(f"  student: {name}")
        lines.append(f"  level: {level or 'unknown'}")
        lines.append(f"  completed: {len(completed)}/{total} lessons")
        if current.get("track"):
            lines.append(f"  current_track: {current.get('track')}")
        if current.get("module"):
            lines.append(f"  current_module: {current.get('module')}")
        nxt = current.get("next_suggested") or "/syllabus"
        lines.append(f"  next_suggested: {nxt}")
        if completed:
            recent = list(completed)[-3:]
            lines.append(f"  recent_completed: {', '.join(recent)}")
    if NOTES.exists() and NOTES.stat().st_size > 0:
        lines.append(f"  has_notes: true ({NOTES})")
    lines.append("</training-state>")
    lines.append("")
    lines.append("Follow the orchestrator protocol in CLAUDE.md: greet the student by name if known, ")
    lines.append("offer to resume from next_suggested, and call .claude/bin/state.py complete <id> when a lesson finishes.")
    print("\n".join(lines))
    return 0


def _resolve_track(progress: dict, key: str) -> str | None:
    """Accept either a track key, a short alias, or a lesson id; return the track key."""
    if not key:
        return None
    tracks = progress.get("tracks", {})
    if key in tracks:
        return key
    aliases = {
        "foundations": "foundations",
        "foundation": "foundations",
        "zero": "foundations",
        "core": "core-concepts",
        "core-concepts": "core-concepts",
        "concepts": "core-concepts",
        "workflow": "workflow",
        "plugins": "plugins",
        "plugin": "plugins",
        "domains": "domains",
        "domain": "domains",
        "cert": "domains",
        "certification": "domains",
    }
    if key in aliases and aliases[key] in tracks:
        return aliases[key]
    # Maybe they passed a lesson id — find its track.
    for tk, t in tracks.items():
        if key in t.get("lessons", []):
            return tk
    return None


def cmd_show(args) -> int:
    profile, progress = ensure_init()
    name = profile.get("name") or "(unset)"
    level = profile.get("level") or "(unset)"
    completed = _completed_ids(progress)
    track_filter = _resolve_track(progress, getattr(args, "track", None))
    if getattr(args, "track", None) and not track_filter:
        valid = ", ".join(progress.get("tracks", {}).keys())
        print(f"ERROR: unknown track '{args.track}'. Valid tracks: {valid}", file=sys.stderr)
        return 2
    print("=" * 60)
    title = f" Training progress for: {name}   (level: {level})"
    if track_filter:
        title += f"   [filter: {track_filter}]"
    print(title)
    print("=" * 60)
    for tk, t in progress.get("tracks", {}).items():
        if track_filter and tk != track_filter:
            continue
        lessons = t.get("lessons", [])
        done = sum(1 for lid in lessons if lid in completed)
        print(f"\n[{tk}] {t.get('label', tk)}   {done}/{len(lessons)}")
        for lid in lessons:
            mark = "[x]" if lid in completed else "[ ]"
            print(f"  {mark} {lid}")
    cur = progress.get("current", {})
    print()
    if not track_filter:
        print(f"Current track : {cur.get('track')}")
        print(f"Current module: {cur.get('module')}")
        print(f"Next suggested: {cur.get('next_suggested')}")
        if profile.get("goals"):
            print(f"Goals: {', '.join(profile['goals'])}")
    return 0


def cmd_syllabus(args) -> int:
    """Print the curriculum, optionally filtered to one track."""
    _, progress = ensure_init()
    completed = _completed_ids(progress)
    track_filter = _resolve_track(progress, getattr(args, "track", None))
    if getattr(args, "track", None) and not track_filter:
        valid = ", ".join(progress.get("tracks", {}).keys())
        print(f"ERROR: unknown track '{args.track}'. Valid tracks: {valid}", file=sys.stderr)
        return 2
    n = 0
    for tk, t in progress.get("tracks", {}).items():
        if track_filter and tk != track_filter:
            # Still increment the counter so numbering across the full
            # curriculum stays stable when a filter is applied.
            n += len(t.get("lessons", []))
            continue
        print(f"\n## {t.get('label', tk)}")
        for lid in t.get("lessons", []):
            n += 1
            mark = "x" if lid in completed else " "
            print(f"  [{mark}] {n:>2}. {lid}")
    return 0


def cmd_set_profile(args) -> int:
    profile, _ = ensure_init()
    if args.name:
        profile["name"] = args.name
    if args.level:
        allowed = profile.get("_levels_allowed") or load_template("profile")["_levels_allowed"]
        if args.level not in allowed:
            print(f"ERROR: level must be one of: {', '.join(allowed)}", file=sys.stderr)
            return 2
        profile["level"] = args.level
    if args.goal:
        existing = profile.get("goals") or []
        for g in args.goal:
            if g not in existing:
                existing.append(g)
        profile["goals"] = existing
    profile["last_active"] = now_iso()
    if not profile.get("started_at"):
        profile["started_at"] = now_iso()
    save_json(PROFILE, profile)
    print(f"profile updated: name={profile.get('name')} level={profile.get('level')} goals={profile.get('goals')}")
    return 0


def cmd_complete(args) -> int:
    profile, progress = ensure_init()
    lid = args.lesson_id
    # Validate lesson exists somewhere
    all_ids = {l for _, l in _all_lessons(progress)}
    if lid not in all_ids:
        print(f"WARNING: '{lid}' is not in the canonical syllabus. Recording anyway.", file=sys.stderr)
    completed = progress.get("completed", [])
    if any(e["id"] == lid for e in completed):
        print(f"already completed: {lid}")
    else:
        completed.append({"id": lid, "completed_at": now_iso(), "notes": args.notes or ""})
        progress["completed"] = completed
    # Advance pointer to next uncompleted lesson in the same track if possible
    track = None
    for tk, l in _all_lessons(progress):
        if l == lid:
            track = tk
            break
    done_ids = {e["id"] for e in progress["completed"]}
    next_id = None
    if track:
        for l in progress["tracks"][track]["lessons"]:
            if l not in done_ids:
                next_id = l
                break
    if not next_id:
        # Look across all tracks
        for _, l in _all_lessons(progress):
            if l not in done_ids:
                next_id = l
                break
    progress["current"] = {
        "track": track,
        "module": lid,
        "next_suggested": f"/lesson {next_id}" if next_id else "/syllabus",
    }
    save_json(PROGRESS, progress)
    profile["last_active"] = now_iso()
    save_json(PROFILE, profile)
    print(f"completed: {lid}; next suggested: {progress['current']['next_suggested']}")
    return 0


def cmd_set_current(args) -> int:
    _, progress = ensure_init()
    cur = progress.get("current", {})
    if args.track:
        cur["track"] = args.track
    if args.module:
        cur["module"] = args.module
    if args.next:
        cur["next_suggested"] = args.next
    progress["current"] = cur
    save_json(PROGRESS, progress)
    print(f"current updated: {cur}")
    return 0


def cmd_add_note(args) -> int:
    ensure_init()
    NOTES.parent.mkdir(parents=True, exist_ok=True)
    with open(NOTES, "a", encoding="utf-8") as f:
        f.write(f"- [{now_iso()}] {args.text}\n")
    print(f"note appended to {NOTES}")
    return 0


def cmd_reset(args) -> int:
    if PROGRESS.exists():
        PROGRESS.unlink()
    if args.hard and PROFILE.exists():
        PROFILE.unlink()
    if args.hard and NOTES.exists():
        NOTES.unlink()
    ensure_init()
    print("state reset" + (" (hard — profile and notes wiped)" if args.hard else ""))
    return 0


def cmd_next(_args) -> int:
    _, progress = ensure_init()
    print(progress.get("current", {}).get("next_suggested") or "/syllabus")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="state.py")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init").set_defaults(fn=cmd_init)
    sub.add_parser("session-start").set_defaults(fn=cmd_session_start)

    sp = sub.add_parser("show")
    sp.add_argument("--track", help="Limit to one track (key or alias).")
    sp.set_defaults(fn=cmd_show)

    sp = sub.add_parser("syllabus")
    sp.add_argument("--track", help="Limit to one track (key or alias).")
    sp.set_defaults(fn=cmd_syllabus)

    sub.add_parser("next").set_defaults(fn=cmd_next)

    sp = sub.add_parser("set-profile")
    sp.add_argument("--name")
    sp.add_argument("--level")
    sp.add_argument("--goal", action="append")
    sp.set_defaults(fn=cmd_set_profile)

    sp = sub.add_parser("complete")
    sp.add_argument("lesson_id")
    sp.add_argument("--notes", default="")
    sp.set_defaults(fn=cmd_complete)

    sp = sub.add_parser("set-current")
    sp.add_argument("--track")
    sp.add_argument("--module")
    sp.add_argument("--next")
    sp.set_defaults(fn=cmd_set_current)

    sp = sub.add_parser("add-note")
    sp.add_argument("text")
    sp.set_defaults(fn=cmd_add_note)

    sp = sub.add_parser("reset")
    sp.add_argument("--hard", action="store_true")
    sp.set_defaults(fn=cmd_reset)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
