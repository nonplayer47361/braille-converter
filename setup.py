from setuptools import setup, find_packages

setup(
    name="braille-converter",
    version="0.1.0",
    description="Text ↔︎ Braille converter for English/Korean",
    packages=find_packages(include=["braille_converter", "braille_converter.*"]),
    install_requires=[
        # 캐시를 재생성할 때만 필요합니다. 런타임 브라유 변환/역변환에는 JSON만 사용
        "louis",
    ],
    python_requires=">=3.8",
)