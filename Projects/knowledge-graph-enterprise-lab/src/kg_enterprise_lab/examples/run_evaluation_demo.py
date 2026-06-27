from kg_enterprise_lab.evaluation.evaluation_runner import run_all_evaluations


def main() -> None:
    for report in run_all_evaluations():
        print(f"{report.suite}: {report.pass_rate}")


if __name__ == "__main__":
    main()
