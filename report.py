import pandas as pd
from datetime import datetime


def generate_statistics(filename):

    df = pd.read_csv(filename)

    lines = []
    lines.append("PDN LOAD TRANSIENT TEST REPORT")
    lines.append(f"Generated: {datetime.now().isoformat()}")
    lines.append("=" * 50)

    overall_pass = True

    for rail, group in df.groupby("Rail"):
        n_total = len(group)
        n_pass = (group["Status"] == "PASS").sum()
        rail_pass = n_pass == n_total
        overall_pass = overall_pass and rail_pass

        lines.append(f"\nRail: {rail}")
        lines.append(f"  Captures        : {n_total}   Pass: {n_pass}   Fail: {n_total - n_pass}")
        lines.append(f"  Deviation %     : mean={group['Deviation_pct'].mean():.2f}  "
                      f"max={group['Deviation_pct'].max():.2f}  "
                      f"std={group['Deviation_pct'].std():.2f}")
        lines.append(f"  Result          : {'PASS' if rail_pass else 'FAIL'}")

        if not rail_pass:
            fails = group[group["Status"] == "FAIL"]
            for _, row in fails.iterrows():
                lines.append(f"    - capture {row['Capture']}: "
                              f"dev={row['Deviation_pct']}%  settle={row['SettlingTime_us']}us")

    lines.append("\n" + "=" * 50)
    lines.append(f"OVERALL RESULT: {'PASS' if overall_pass else 'FAIL'}")

    report_text = "\n".join(lines)
    print(report_text)

    report_path = f"results/reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_path, "w") as f:
        f.write(report_text)

    return report_path
