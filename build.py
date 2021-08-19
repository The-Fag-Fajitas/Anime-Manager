import json
import backend.helpers.data as data


class Build:
    payload = json.dumps(data.paths, indent=4)

    @staticmethod
    def build():
        with open("settings.json", "w") as f:
            f.write(Build.payload)


if __name__ == '__main__':
    Build.build()
