import logging
from pathlib import Path
import pytest

# 프로젝트 최상위 디렉터리 기준으로 logs 디렉터리 설정
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"

def pytest_configure(config):
    """
    pytest 세션 시작 시 logs 디렉터리 생성
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

def _sanitize_nodeid(nodeid: str) -> str:
    """
    pytest nodeid를 파일명으로 안전하게 변환
    ('tests/test_x.py::test_y[param]' → 'tests_test_x.py_test_y_param')
    """
    return nodeid.replace("::", "_").replace("/", "_") \
                 .replace("[", "_").replace("]", "")

def _get_logger(test_name: str) -> logging.Logger:
    """
    test_name 기반의 전용 로거를 구성.
    이전에 붙인 FileHandler만 제거하여 중복 등록 방지.
    """
    logger_name = f"braille_{test_name}"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # 기존에 같은 logs 디렉터리로 붙인 FileHandler만 제거
    for h in list(logger.handlers):
        if isinstance(h, logging.FileHandler) and Path(h.baseFilename).parent == LOG_DIR:
            logger.removeHandler(h)

    # 새로운 FileHandler 등록
    log_path = LOG_DIR / f"{test_name}.log"
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fmt = logging.Formatter("[%(levelname)s] %(asctime)s %(message)s", "%Y-%m-%d %H:%M:%S")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    return logger

@pytest.fixture(autouse=True)
def braille_logger(request):
    """
    각 테스트마다 고유 로그 파일 생성 및 로거 제공.
    사용 예) braille_logger.info("..."), error, warning 등
    """
    nodeid = request.node.nodeid
    test_name = _sanitize_nodeid(nodeid)
    return _get_logger(test_name)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    테스트 실행 후 PASS/FAIL/SKIPPED 결과를 해당 로그에 기록.
    """
    outcome = yield
    report = outcome.get_result()
    # 실제 테스트 실행 단계(call)에서만 기록
    if report.when == "call":
        nodeid = item.nodeid
        test_name = _sanitize_nodeid(nodeid)
        logger = logging.getLogger(f"braille_{test_name}")

        if report.passed:
            logger.info("=== TEST RESULT: PASS ===\n")
        elif report.failed:
            logger.error("=== TEST RESULT: FAIL ===")
            if call.excinfo:
                # 예외 traceback 기록
                logger.error("Exception:\n" + call.excinfo.getrepr().text + "\n")
        elif report.skipped:
            logger.warning("=== TEST RESULT: SKIPPED ===\n")