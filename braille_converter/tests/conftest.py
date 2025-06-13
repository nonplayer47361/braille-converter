import logging
from pathlib import Path
import pytest

# 로그 디렉터리 절대 경로 설정
LOG_DIR = Path("/Users/oseungtae/Downloads/translator_final/braille_converter/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

def _get_logger(test_name: str) -> logging.Logger:
    logger = logging.getLogger(test_name)
    # 중복 handler 제거
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(LOG_DIR / f"{test_name}.log", encoding="utf-8")
    fmt = logging.Formatter("[%(levelname)s] %(asctime)s %(message)s", "%Y-%m-%d %H:%M:%S")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    return logger

@pytest.fixture(autouse=True)
def braille_logger(request):
    """
    각 테스트마다 고유 로그 파일 생성.
    테스트 코드 내에서 logger.info/debug/error 호출로
    과정(입력, 점자, 복원)과 디버깅 메시지를 기록할 수 있음.
    """
    test_name = request.node.name
    return _get_logger(test_name)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    테스트 실행 후 결과를 로그에 기록 (PASS/FAIL/ERROR).
    """
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        logger = logging.getLogger(item.name)
        if report.passed:
            logger.info("=== TEST RESULT: PASS ===\n")
        elif report.failed:
            logger.error("=== TEST RESULT: FAIL ===")
            if call.excinfo:
                # 예외 traceback도 함께 기록
                logger.error("Exception:\n" + call.excinfo.getrepr().text + "\n")
        elif report.skipped:
            logger.warning("=== TEST RESULT: SKIPPED ===\n")