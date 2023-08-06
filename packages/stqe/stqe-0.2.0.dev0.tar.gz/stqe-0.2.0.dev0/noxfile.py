import nox


@nox.session(python=["3.6", "3.9", "3.11"])
def tests(session: nox.Session) -> None:
    """Runs pytest"""
    session.install("-e", ".")
    session.install("pytest", "pytest-cov")
    session.run(
        "pytest",
        "--cov=stqe",
        "--cov-config",
        "pyproject.toml",
        "--cov-report=",
        *session.posargs,
        env={"COVERAGE_FILE": f".coverage.{session.python}"},
    )
    session.notify("coverage")


@nox.session
def coverage(session) -> None:
    """Coverage analysis"""
    session.install("coverage[toml]")
    session.run("coverage", "combine")
    session.run("coverage", "report")
    session.run("coverage", "erase")


@nox.session
def stqe_test(session) -> None:
    """Test stqe-test cli"""
    session.run("stqe-test", "run", "--fmf", "--norun", "--path", "lvm/device_mapper_persistent_data/thin")
    session.run("stqe-test", "run", "--fmf", "--norun", "-f", "component:lvm")
    session.run("stqe-test", "list", "--fmf", "--path", "lvm/device_mapper_persistent_data/", "tests")
