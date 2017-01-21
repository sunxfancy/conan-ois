from conan.packager import ConanMultiPackager
import platform

if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name="OIS:shared", pure_c=False)
    # Disable Linux 32 bit for now
    builder.builds = [
        [settings, options]
        for settings, options in builder.builds
        if not (platform.system() == "Linux" and settings["arch"] == "x86")
    ]
    builder.run()

