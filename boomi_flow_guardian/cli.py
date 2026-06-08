import argparse
from pathlib import Path

from core.models import FlowSettings
from core.planner import build_plan


def parse_args():
    parser = argparse.ArgumentParser(description="Plan and validate a Boomi-style integration flow.")
    parser.add_argument("--source", required=True, help="Path to source schema JSON")
    parser.add_argument("--target", required=True, help="Path to target schema JSON")
    parser.add_argument("--system", default="salesforce", help="Target business system")
    parser.add_argument("--volume", type=int, default=18000, help="Estimated records per day")
    parser.add_argument("--schedule", type=int, default=15, help="Schedule interval in minutes")
    parser.add_argument("--retries", type=int, default=3, help="Retry count")
    parser.add_argument("--no-dead-letter", action="store_true", help="Disable failed record holding area")
    parser.add_argument("--no-encryption", action="store_true", help="Disable encryption flag for validation testing")
    return parser.parse_args()


def main():
    args = parse_args()
    settings = FlowSettings(
        system=args.system,
        volume_per_day=args.volume,
        schedule_minutes=args.schedule,
        retry_count=args.retries,
        has_dead_letter=not args.no_dead_letter,
        encryption_enabled=not args.no_encryption,
    )
    plan, artifacts = build_plan(Path(args.source), Path(args.target), settings, write_outputs=True)
    print(f"Plan: {plan.title}")
    print(f"Risk: {plan.risk_band} ({plan.risk_score})")
    print(f"Runtime estimate: {plan.runtime_minutes} minutes")
    print(f"Monthly cost estimate: ${plan.estimated_monthly_cost}")
    print(f"Report: {artifacts['report']}")


if __name__ == "__main__":
    main()

