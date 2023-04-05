mkdir -p styles
for f in `fd . ./scss -e scss`; do
	# remove extension
	file_name=${f%.*}
	# remove path
	file_name=${file_name##*/}
	sass $f ./styles/$file_name.css
done