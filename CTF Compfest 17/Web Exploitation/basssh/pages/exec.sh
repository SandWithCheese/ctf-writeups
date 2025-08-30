source config.sh
echo ""

file_target=$(basename -s .py $(urldecode "${QUERY_PARAMS['file']}"))

if ! [[ -f "programs/${file_target}.py" ]]; then
  echo "Invalid file"
  exit 1
fi

input="${FORM_DATA[input]}"

if [[ -n "$input" ]]; then
    output=$(echo -e "$input" | python3 "programs/${file_target}.py" 2>&1)
else
    output="No input provided. Please enter some input in the textarea above."
fi

escaped_output=$(echo "$output" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')

echo "$escaped_output"
