import logging
from pathlib import Path

# 1) 로그 디렉터리 자동 생성
LOGS_DIR = Path(__file__).parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# 2) 로거 설정: 파일과 콘솔에 동시에 로그를 남김
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / "braille_converter.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
# 패키지 전역에서 쓸 로거
logger = logging.getLogger("braille_converter")

# 이제 모듈 어디서든
# from braille_converter import logger
# logger.info("패키지가 로드되었습니다.")