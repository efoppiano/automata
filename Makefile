install_dependencies:
	pip3 install -r requirements.txt

copy_env_file:
	if [ ! -f .env ]; then cp .env.example .env; fi

common: copy_env_file
	mkdir -p results

animation: common
	python3 src/main.py

scenario_1: common
	GREEN_LIGHT_TIME=50 CROSSWALK_ROWS=6 \
	python3 src/run_scenario.py

scenario_2: common
	GREEN_LIGHT_TIME=35 CROSSWALK_ROWS=10 \
	python3 src/run_scenario.py