
source config.sh

file_target=$(basename -s .py $(urldecode "${QUERY_PARAMS['file']}"))

chall_list() {
    echo "<div class='w-full'>"
    echo "  <div class='bg-[#141414] text-green-400 font-mono text-sm rounded-lg p-6 overflow-x-auto'>"
    echo "    <div class='flex flex-col space-y-1'>"
    echo "      <p class='text-white'><span class='text-green-400'>you@basssh</span>:<span class='text-cyan-500'>/app</span>$ tree -L 1 ./programs</p>"

    echo "      <span class='text-cyan-500'>.</span>"

    mapfile -t files < <(find programs/ -maxdepth 1 -type f -name "*.py" | sort)
    total=${#files[@]}

    for i in "${!files[@]}"; do
        file="${files[$i]}"
        filename=$(basename $file)
        if [ "$i" -eq $((total - 1)) ]; then
            branch="└──"
        else
            branch="├──"
        fi
        echo "      <p class='text-white'>$branch <a href='?file=$filename' class='text-yellow-400 hover:text-yellow-300 transition-colors duration-200'>$filename</a></p>"
    done

    if [ -z "$file_target" ]; then
        echo "      </br>"
        echo "      <p class='text-white'>No file selected.</p>"
        echo "      <p class='text-white'>Please select a file from the list above.</p>"
        echo "      <p class='text-white'>Example: <span class='text-yellow-400'>?file=example.py</span></p>"
        echo "      <p class='text-white'>Then click the <span class='text-green-400'>▶ Run</span> button.</p>"
        echo "    </div>"
        echo "  </div>"
        echo "</div>"
        return
    fi
    echo "      </br><p class='text-white'><span class='text-green-400'>you@basssh</span>:<span class='text-cyan-500'>/app</span>$ cat ./problems/$file_target.txt</p>"

    cat "problems/$file_target.txt" | while read -r line; do
      echo "      <p class='text-white'>$line</p>"
    done

    echo "    </div>"
    echo "  </div>"
    echo "</div>"
}


htmx_page << EOF
<body class="font-mono bg-[#1F1F1F] text-[#CE9178] mt-4">
  <div class="w-full flex flex-col md:flex-row border-2 divide-y-2 md:divide-y-0 md:divide-x-2 border-[#484848] divide-[#282828]">
    
    <!-- Left Card -->
    <div id="left-card" class="flex flex-col flex-1 max-w-xl justify-start items-start px-4 py-6">
      <pre class="overflow-auto text-sm leading-tight">
Welcome to,

██████╗░░█████╗░░██████╗░██████╗░██████╗██╗░░██╗
██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██║░░██║
██████╦╝███████║╚█████╗░╚█████╗░╚█████╗░███████║
██╔══██╗██╔══██║░╚═══██╗░╚═══██╗░╚═══██╗██╔══██║
██████╦╝██║░░██║██████╔╝██████╔╝██████╔╝██║░░██║
╚═════╝░╚═╝░░╚═╝╚═════╝░╚═════╝░╚═════╝░╚═╝░░╚═╝
      </pre>
      <p>Pretty much 1337code 101.</p>
      <br />
      $(chall_list)
      <p class="text-xs pt-2">^ not interactive, just a list of challenges.</p>
    </div>

    <!-- Right Card with Button -->
    <div class="flex-1 flex-col items-end px-4 py-6">
      <form hx-post="/exec/?file=$file_target.py" hx-target="#output" hx-swap="innerHTML">
        <button class="bg-[#CE9178] text-white text-sm py-1 px-2 border-2 border-transparent hover:bg-[#b87f68] hover:border-white transition ease-in-out duration-300" type="submit">
          ▶ Run
        </button>
        <div class="mt-4">
          <p class="text-white">Input:</p>
          <textarea name="input" id="input" class="w-full h-64 bg-[#141414] text-white p-6 rounded-lg border border-[#484848] resize-none"></textarea>
        </div>
      </form>
      <div class="mt-2">
        <p class="text-white">Output:</p>
        <textarea id="output" class="w-full h-44 bg-[#141414] text-white p-6 rounded-lg border border-[#484848] resize-none" readonly></textarea>
      </div>
    </div>

  </div>
</body>

EOF