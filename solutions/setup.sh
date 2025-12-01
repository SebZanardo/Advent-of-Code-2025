RED='\033[0;31m'
GREEN='\033[0;32m'
MAGENTA='\033[0;35m'
OFF='\033[0m'

echo "\n${MAGENTA}Configuring Advent of Code files${OFF}\n"

# Only first twelve days of December this year ;(
for i in {1..12}; do

	# Name directory
	directory_name="$i"
	if [[ $i -lt 10 ]]; then
		directory_name="0$i"
	fi

	# Check if directory already exists
	if ! [[ -d "$directory_name" ]]; then
		# Create directory
		mkdir "$directory_name"

		# Copy template.py to new python file in directory
		cat template.py >> "$directory_name/main.py"

		# Create empty input files in directory
		touch "$directory_name/input.in"
		touch "$directory_name/test.in"

		echo "${GREEN}Created $directory_name directory!${OFF}"
	else
		echo "${RED}$directory_name directory already exists...${OFF}"
	fi
done

echo "\n${MAGENTA}Goodluck with this year's Advent of Code!${OFF}\n"
