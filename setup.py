from cx_Freeze import setup, Executable


includes = []
excludes = []
# NOT WORKING RIGHT NOW
# NEED TO PUT THIS FILE FROM SITE-PACKAGES INTO BUILD BY HANDS
packages = ['lxml._elementpath']


setup(
    name="cstruct2xml",
    version="1.2",
    description="Converts descriptive C structures to XML",
    executables=[Executable("cstruct2xml.py")],
    options={
        "build.exe": {
            "includes": includes,
            "excludes": excludes,
            "packages": packages,
        }
    }
)
