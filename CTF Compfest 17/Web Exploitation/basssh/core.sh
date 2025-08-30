#!/usr/bin/env bash
VERSION=v0.6.0

declare -A HTTP_HEADERS
declare -A FILE_UPLOADS
declare -A FILE_UPLOAD_TYPES
declare -A FILE_UPLOAD_NAMES
declare -A QUERY_PARAMS
declare -A FORM_DATA
declare -A PATH_VARS
declare -A COOKIES
declare -A SESSION

[[ -f 'config.sh' ]] && source config.sh

debug() {
    printf "%s\n" "$@" 1>&2
}

if [[ "${DEV:-true}" == true ]]; then
  USE_HMR="$(which inotifywait)"

  # disable HMR when using netcat
  if [[ "$TCP_PROVIDER" == "nc" ]]; then
    USE_HMR=""
  fi
fi

header() {
    printf "%s: %s\r\n" "$1" "$2"
}

respond() {
    CODE=$1
    shift
    printf "HTTP/1.1 %s %s\r\n" "$CODE" "$*"
    header Server "bash ${VERSION:-devbuild}"
    [[ ! -z "$SESSION_HEADER_TO_BE_WRITTEN" ]] && \
      printf "%s\n" "$SESSION_HEADER_TO_BE_WRITTEN"

}

end_headers() {
    printf "\r\n"
}

trim_quotes() {
    # Usage: trim_quotes "string"
    : "${1//\'}"
    printf '%s\n' "${_//\"}"
}

urlencode() {
    # Usage: urlencode "string"
    local LC_ALL=C
    for (( i = 0; i < ${#1}; i++ )); do
        : "${1:i:1}"
        case "$_" in
            [a-zA-Z0-9.~_-])
                printf '%s' "$_"
            ;;

            *)
                printf '%%%02X' "'$_"
            ;;
        esac
    done
    printf '\n'
}

urldecode() {
    # Usage: urldecode "string"
    : "${1//+/ }"
    printf '%b\n' "${_//%/\\x}"
}

function create_or_resume_session() {
  local KEY
  local VAL
  if [[ -z "${COOKIES[_session]}" ]]; then
    SESSION_ID="$(tr -dc A-Za-z0-9 </dev/urandom | head -c 32 ; echo '')"
    SESSION_HEADER_TO_BE_WRITTEN=$(header Set-Cookie "_session=$SESSION_ID; Path=/; Secure; HttpOnly")
  else
    SESSION_ID=$(echo "${COOKIES[_session]}" | tr -dc A-Za-z0-9)
  fi
  if [[ -f "sessions/$SESSION_ID" ]]; then
    while IFS= read -r line; do
      KEY="$(echo "$line" | cut -f1)"
      VAL="$(echo "$line" | cut -f2-)"
      SESSION["$KEY"]="$VAL"
    done < "sessions/$SESSION_ID"
  fi
}

function save_session() {
  if [[ "${ENABLE_SESSIONS:-false}" != true ]]; then
    debug "Error: You must set ENABLE_SESSIONS=true before calling save_session!"
    return
  fi
  local KEY
  if [[ -z "$SESSION_ID" ]]; then
    return
  fi
  touch "sessions/$SESSION_ID"
  for KEY in ${!SESSION[@]}; do
    printf "%s\t%s\n" "$KEY" "${SESSION[$KEY]}"
  done > "sessions/$SESSION_ID"
}

function _inject_hmr() {
  if [[ -z "$USE_HMR" ]]; then
    return
  fi
  cat <<-EOF
  <div style="display:none" hx-ext="sse" sse-connect="/hmr" sse-swap="none">
    <div hx-trigger="sse:reload" hx-post="/hmr"></div>
  </div>
EOF
}

function htmx_page() {
  if [[ -z "$NO_STYLES" ]]; then
    if [[ -z "$TAILWIND" ]]; then
      STYLE_TEXT='<link rel="stylesheet" href="/static/style.css">'
    else
      STYLE_TEXT='<link rel="stylesheet" href="/static/tailwind.css">'
    fi
  fi
  [[ ${HTTP_HEADERS["hx-request"]} == "true" ]] || [[ "$INTERNAL_REQUEST" == "true" ]] || cat <<-EOF
  <!doctype html>
  <html>
  <head>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta charset="UTF-8">
  ${STYLE_TEXT}
  <script src="https://unpkg.com/htmx.org@1.9.3/dist/htmx.min.js" integrity="sha384-lVb3Rd/Ca0AxaoZg5sACe8FJKF0tnUgR2Kd7ehUOG5GCcROv5uBIZsOqovBAcWua" crossorigin="anonymous"></script>
  <script src="https://unpkg.com/hyperscript.org@0.9.8"></script>
  <script src="https://unpkg.com/htmx.org/dist/ext/sse.js"></script>
  </head>
  <body>
  $(_inject_hmr)
EOF

cat # meow
}
# usage: subscribe [topic]
# returns: handle of a fifo (via stdout)
function subscribe() {
  local TOPIC
  TOPIC="$1"
  if [[ -z "$TOPIC" ]]; then
    debug "ATTEMPTED TO SUBSCRIBE ON EMPTY TOPIC"
    return
  fi
  mkdir -p pubsub/"${TOPIC}"
  tmppipe=$(mktemp -up pubsub/"${TOPIC}")
  mkfifo -m 600 "$tmppipe"
  echo "$tmppipe"
}

function unsubscribe() {
  local TOPIC
  TOPIC="$1"
  if [[ "$TOPIC" != "pubsub/"* ]]; then
    debug "FAILED TO UNSUBSCRIBE"
    return
  fi
  rm -f "$TOPIC"
}

function publish() {
  local TOPIC
  local line
  TOPIC="$1"
  if [[ -z "$TOPIC" ]]; then
    return
  fi
  if [[ ! -d "pubsub/${TOPIC}" ]]; then
    return
  fi
  TEE_ARGS=$(find pubsub/"${TOPIC}" -type p)
  if [[ -z "$TEE_ARGS" ]]; then
    return
  fi
  tee $TEE_ARGS > /dev/null
}

event() {
  printf "event: %s\ndata: %s\n\n" "$@"
}


# encode result
# can encode the following status codes as unix return codes:
# 200-263
# 300-363
# 400-463
# 500-563
function status_code() {
  A=${1:0:1}
  B=${1:1:2}
  echo $(( ((A - 2) << 6) + B ))
}

function decode_result() {
  ENCODED=${1}
  printf "%d%02d" $(((ENCODED >> 6) + 2)) $(( ENCODED & 63 ))
}

function component() {
  if [[ "$1" == "$REQUEST_PATH" ]]; then
    echo "<!-- RECURSION DETECTED -->"
    return
  fi
  local REQUEST_PATH
  local REQUEST_METHOD
  local ROUTE_SCRIPT
  REQUEST_PATH="$1"
  REQUEST_METHOD="GET"
  matchRoute "$REQUEST_PATH"
  INTERNAL_REQUEST=true
  if [[ -f "pages/${ROUTE_SCRIPT}" ]]; then
    result=$(source "pages/${ROUTE_SCRIPT}")
    echo "$result"
  else
    echo "<!-- MISSING COMPONENT: $1 -->"
  fi
}

readonly URI_REGEX='(/[^?#]*)(\?([^#]*))?'

parseHttpRequest() {
  local line

  # Read request line
  read -r REQUEST_METHOD REQUEST_PATH_WITH_PARAMS HTTP_VERSION
  HTTP_VERSION="${HTTP_VERSION%%$'\r'}"
  debug "$REQUEST_METHOD $REQUEST_PATH_WITH_PARAMS $HTTP_VERSION"
  [[ "$REQUEST_PATH_WITH_PARAMS" =~ $URI_REGEX ]]
  REQUEST_PATH="${BASH_REMATCH[1]}"
  REQUEST_QUERY="${BASH_REMATCH[3]}"

  # Parse query parameters
  if [[ ! -z "$REQUEST_QUERY" ]]; then
    while read -r -d '&' line; do
      local VARNAME="${line%%=*}"
      [[ -z "$VARNAME" ]] && continue
      QUERY_PARAMS["$VARNAME"]=$(urldecode "${line#*=}")
    done <<< "${REQUEST_QUERY}&"
  fi

  # Read headers
  while IFS= read -r line; do
    line="${line%%$'\r'}"
    [[ -z "$line" ]] && break
    KEY="${line%%:*}"
    HTTP_HEADERS["${KEY,,}"]="${line#*: }"
  done

  # Parse multipart Form Data
  if [[ ${HTTP_HEADERS["content-type"]} == "multipart/form-data; "* ]]; then
      BOUNDARY="${HTTP_HEADERS["content-type"]}"
      BOUNDARY="${BOUNDARY#*=}"
  fi

  # Read cookies (yum!)
  if [[ ! -z "${HTTP_HEADERS["cookie"]}" ]]; then
    while read -r -d ';' line; do
      COOKIES["${line%%=*}"]=$(urldecode "${line#*=}")
    done <<< "${HTTP_HEADERS[cookie]};"
  fi

  CLEN=${HTTP_HEADERS["content-length"]}

  # Read multipart body
  if [[ ! -z "$BOUNDARY" ]]; then
      matchRoute "$REQUEST_PATH"
      ALLOW_UPLOADS=false
      if directive_test=$(head -1 "pages/${ROUTE_SCRIPT}"); then
        if [[ "$directive_test" == "# allow-uploads" ]]; then
          ALLOW_UPLOADS=true
        fi
      fi
      if [[ "$ALLOW_UPLOADS" != "true" ]]; then
        respond 403 Forbidden
        end_headers
        return
      fi
      state="start"
      reader="reading"
      local -A MULTIPART_HEADERS
      local -A DISPOSITIONS
      while read -n2 byte; do
        # we have to implement our own readline because of reasons
        if [[ "$reader" == "reading" ]]; then
          if [[ "$byte" == "0a" ]]; then
            reader="flushing-newline"
          elif [[ "$byte" == "00" ]]; then
            reader="flushing-null"
          else
            line="${line}${byte}"
          fi
        fi
        if [[ "$reader" == "flushing"* ]]; then
          PARSED="$(echo -n $line | xxd -r -p)"
          if [[ "$state" == "start" ]] && [[ "$PARSED" == "--$BOUNDARY"* ]]; then
            state="headers"
            MULTIPART_HEADERS=()
            DISPOSITIONS=()
          elif [[ "$state" == "headers" ]]; then
            PARSED="${PARSED%%$'\r'}"
            if [[ -z "$PARSED" ]]; then
              UPLOAD_TO=$(mktemp -p uploads)
              state="body"
            else
              KEY="${PARSED%%:*}"
              MULTIPART_HEADERS["${KEY,,}"]="${PARSED#*: }"
            fi
          elif [[ "$state" == "body" ]]; then
            if [[ "$reader" == "flushing-null" ]]; then
              # this is a null char
              echo -n "${line}00" | xxd -r -p >> "$UPLOAD_TO"
            else
              # this is a newline char
              if [[ "$PARSED" == "--$BOUNDARY"* ]]; then
                while read -r -d ';' line; do
                  DISPOSITIONS["${line%%=*}"]=$(urldecode "${line#*=}")
                done <<< "${MULTIPART_HEADERS["content-disposition"]};"
                NAME=$(trim_quotes "${DISPOSITIONS[name]}")
                FILENAME=$(trim_quotes "${DISPOSITIONS[filename]}")
                FILE_UPLOADS["$NAME"]="$UPLOAD_TO"
                FILE_UPLOAD_NAMES["$NAME"]="$FILENAME"
                FILE_UPLOAD_TYPES["$NAME"]="${MULTIPART_HEADERS[content-type]}"
                MULTIPART_HEADERS=()
                DISPOSITIONS=()
                state="headers"
                if [[ "$PARSED" == "--$BOUNDARY--"* ]]; then
                  # i dont know how, but we made it out alive
                  break
                fi
              else
                echo -n "${line}0a" | xxd -r -p >> "$UPLOAD_TO"
              fi
            fi
          fi
          reader="reading"
          line=''
        fi
        # wheeeeeeeeeeeeeeeee
      done < <(stdbuf -o0 -i0 hexdump -v -e '/1 "%02x"' -n $CLEN)
  else
    # Read body
    [[ "$CLEN" =~ ^[0-9]+$ ]] && \
      test $CLEN -gt 0 && read -rN $CLEN REQUEST_BODY;
  fi
  # Parse Form Data
  if [[ ! -z "$REQUEST_BODY" ]] && \
    [[ ${HTTP_HEADERS["content-type"]} == "application/x-www-form-urlencoded" ]]; then
    while read -r -d '&' line; do
      FORM_DATA["${line%%=*}"]=$(urldecode "${line#*=}")
    done <<< "${REQUEST_BODY}&"
  fi

}

writeHttpResponse() {
  if [[ "$REQUEST_PATH" == "/static/"* ]]; then
    FILE_PATH=".${REQUEST_PATH}"

    if [[ ! -f "$FILE_PATH" ]]; then
      respond 404 Not Found
      end_headers
      return
    fi
    REALPATH="$(realpath --relative-to="./static" "$FILE_PATH")"
    FIRST_THREE="${REALPATH:0:3}"
    if [[ "$FIRST_THREE" == "../" ]]; then
      respond 403 FORBIDDEN
      end_headers
      return
    fi
    debug "$REALPATH"
    respond 200 OK
    if [[ "$REQUEST_PATH" == *".css" ]]; then
      header Content-Type "text/css"
    else
      header Content-Type "$(file -b --mime-type "$FILE_PATH")"
    fi
    end_headers
    cat "$FILE_PATH"
    return
  fi
  matchRoute "$REQUEST_PATH"

  [[ "${ENABLE_SESSIONS:-false}" == "true" ]] && create_or_resume_session

  if [[ ! -z "$USE_HMR" ]] && [[ "$REQUEST_PATH" == "/hmr" ]]; then
    if [[ "$REQUEST_METHOD" == "POST" ]]; then
      respond 204 OK
      header HX-Redirect "${HTTP_HEADERS[hx-current-url]}"
      end_headers
      return
    fi
    respond 200 OK
    header Content-Type "text/event-stream"
    end_headers
    output() {
      killthehmr() {
        kill "$HMR_PID" &> /dev/null
        wait "$HMR_PID" &> /dev/null
        exit 0
      }
      trap 'killthehmr' TERM
      while true; do
        inotifywait -e MODIFY -r pages static &> /dev/null &
        HMR_PID=$!
        wait "$HMR_PID" &> /dev/null
        event "reload"
      done
    }
    output &
    PID=$!


    while IFS= read -r line; do
      :
    done

    kill $PID &>/dev/null
    wait $PID &>/dev/null

    return
  elif [[ -z "$ROUTE_SCRIPT" ]]; then
    debug "404 no match found"
    respond 404 Not Found
    end_headers
    return
  fi


  if directive_test=$(head -1 "pages/${ROUTE_SCRIPT}"); then
    if [[ "$directive_test" == "# sse" ]]; then
      respond 200 OK
      header Content-Type "text/event-stream"
      end_headers
      source "pages/${ROUTE_SCRIPT}"
      TOPIC="$(topic)"
      if [[ -z "$TOPIC" ]]; then
        debug "ERROR: EMPTY TOPIC"
        return
      fi
      SUB_FD=$(subscribe "$TOPIC")
      output() {
        curiosity() {
          kill "$CAT_PID" &> /dev/null
          wait "$CAT_PID" &> /dev/null
          exit 0
        }
        trap 'curiosity' TERM
        while true; do
          cat "$SUB_FD" &
          CAT_PID=$!
          wait "$CAT_PID" &> /dev/null
        done
      }
      output &
      PID=$!

      [[ $(type -t on_open) == function ]] && on_open 1>&2

      while IFS= read -r line; do
        :
      done

      kill "$PID" &>/dev/null
      wait "$PID" &>/dev/null

      unsubscribe "$SUB_FD"
      [[ $(type -t on_close) == function ]] && on_close 1>&2

      return
    elif [[ "$directive_test" == "# headers" ]]; then
      CUSTOM_HEADERS=1
    fi
  fi
  result=$(source "pages/${ROUTE_SCRIPT}")
  CODE=$?
  respond $(decode_result $CODE)
  [[ -z $CUSTOM_HEADERS ]] && header Content-Type "text/html" && end_headers
  printf "%s" "$result"
}

findRoutes() {
  if [[ -z $ROUTES_CACHE ]] || [[ $(stat -c "%s" $ROUTES_CACHE) -eq 0 ]]; then
    cd pages
    find . -type f,l -iname '*.sh' | sed 's@^\./@@' | tee $ROUTES_CACHE
  else
    cat $ROUTES_CACHE
  fi
}

findPredefinedRoutes() {
  findRoutes | grep -v '\['
}

findDynamicRoutes() {
  findRoutes | grep '\[[^\.]' | grep -v '\[\.\.\.'
}

findCatchAllRoutes() {
  findRoutes | grep '\[\.\.\.'
}

matchRoute() {

  if [[ "$1" == "/" ]] && [[ -f "pages/index.sh" ]]; then
    ROUTE_SCRIPT="index.sh"
    return
  fi

  local route
  local sanitized

  # for our sanity
  sanitized="${1%%/}"
  while IFS= read -r route; do
    if [[ "/${route%.sh}" == "$sanitized" ]]; then
      ROUTE_SCRIPT="$route"
      return
    fi
  done < <(findPredefinedRoutes)
  while IFS= read -r route; do
    routeRegex="/${route%.sh}"
    routeRegex="^$(echo "$routeRegex" | sed 's@\[[^]]*\]@([^\/]+)@g')$"
    if [[ "$sanitized" =~ $routeRegex ]]; then
      local -a PATH_VALS
      PATH_VALS=("${BASH_REMATCH[@]}")
      ROUTE_SCRIPT="$route"
      [[ "/${route%.sh}" =~ $routeRegex ]]
      for (( i=1; i<${#BASH_REMATCH[@]}; i++ )); do
        local KEY
        KEY="${BASH_REMATCH[$i]}"
        KEY="${KEY//\[}"
        KEY="${KEY//\]}"
        PATH_VARS[$KEY]=${PATH_VALS[$i]}
      done
      return
    fi
  done < <(findDynamicRoutes)
  while IFS= read -r route; do
    routeRegex="/${route%.sh}"
    routeRegex="^${routeRegex//\/\[\[...*\]\]/\(\/.*\)?}$"
    routeRegex="${routeRegex//\//\\/}"
    routeRegex="${routeRegex//\[...*\]/\(.+\)}"
    routeRegex="${routeRegex//\[*\]/\([^\/]+\)}"
    if [[ "$sanitized" =~ $routeRegex ]]; then
      local -a PATH_VALS
      PATH_VALS=("${BASH_REMATCH[@]}")
      ROUTE_SCRIPT="$route"
      [[ "/${route%.sh}" =~ $routeRegex ]]
      for (( i=1; i<${#BASH_REMATCH[@]}; i++ )); do
        local KEY
        local VAL
        KEY="${BASH_REMATCH[$i]}"
        KEY="${KEY//\[}"
        KEY="${KEY//\]}"
        KEY="${KEY//\.}"
        KEY="${KEY//\/}"
        VAL=${PATH_VALS[$i]}
        VAL=${VAL#\/}
        PATH_VARS[$KEY]="$VAL"
      done
      return
    fi
  done < <(findCatchAllRoutes)
}

export -f status_code
export -f component
export -f debug
export -f subscribe
export -f unsubscribe
export -f publish
export -f header
export -f end_headers
export -f event
export -f htmx_page
export -f findPredefinedRoutes
export -f findDynamicRoutes
export -f findCatchAllRoutes
export -f matchRoute
export -f save_session

parseHttpRequest
writeHttpResponse
