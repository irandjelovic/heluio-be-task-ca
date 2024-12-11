from dynaconf import Dynaconf

settings: Dynaconf = Dynaconf(settings_files=["pyproject.toml"], environments=False)
