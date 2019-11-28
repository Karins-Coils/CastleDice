#.DEFAULT_GOAL := all

export_django_default_setting = DJANGO_SETTINGS_MODULE=config.settings.local

manage_cmd = python3 manage.py
django_test_settings_location = config.settings.test
django_local_settings_location = config.settings.local

# pass in the command to run with `make manage CMD=some_command_and_args`
.PHONY: manage
manage:
	$(export_django_default_setting) $(manage_cmd) $(CMD)


# pass in target files (optionally) with `make test TARGET=target_things`
.PHONY: test
test:
	$(manage_cmd) test --settings $(django_test_settings_location) $(TARGET)

.PHONY: migrate
migrate: migrate_local migrate_test

.PHONY: migrate_local
migrate_local:
	$(manage_cmd) migrate --settings $(django_local_settings_location)

.PHONY: migrate_test
migrate_test:
	$(manage_cmd) migrate --settings $(django_test_settings_location)

