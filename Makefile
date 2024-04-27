copy_env_file:
	if [ ! -f .env ]; then cp .env.example .env; fi

common: copy_env_file
	mkdir -p results

install_dependencies:
	pip3 install -r requirements.txt

animation: common
	python3 src/main.py

scenario_1: common
	GREEN_LIGHT_TIME=45 CROSSWALK_ROWS=6 RESULTS_FILE_NAME=scenario_1.csv \
	python3 src/run_scenario.py

scenario_2: common
	GREEN_LIGHT_TIME=30 CROSSWALK_ROWS=10 RESULTS_FILE_NAME=scenario_2.csv \
	python3 src/run_scenario.py