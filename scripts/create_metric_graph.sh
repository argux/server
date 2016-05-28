SERVER=http://localhost:7000
ARGUX_BASE=/
REST_URI=rest/1.0
HOST_URI=host

HOST_NAME=localhost

ARGUX_USERNAME=admin
ARGUX_PASSWORD=admin

UNAMESTR=`uname`

if [[ "$UNAMESTR" == "Darwin" ]]; then
MKTEMP='mktemp -t argux'
else
MKTEMP='mktemp'
fi

HEADER_FILE=`$MKTEMP`
COOKIE_FILE=`$MKTEMP`

curl -X POST \
    -c $COOKIE_FILE \
    -D $HEADER_FILE \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d "{\"username\":\"$ARGUX_USERNAME\",\"password\":\"$ARGUX_PASSWORD\"}" \
    $SERVER/$REST_URI/login

CSRF_TOKEN=`cat $HEADER_FILE | grep -i X-CSRF-TOKEN | awk -F : '{ print $2 }'`

curl -X POST \
    -b $COOKIE_FILE \
    -H "Content-Type: application/json" \
    -H "X-CSRF-Token: $CSRF_TOKEN" \
    -d "{
        \"name\" : \"CPU Load Average (Custom colors)\",
        \"items\": [
            {
                \"name\": \"cpu.load.avg[1]\",
                \"host\": \"localhost\",
                \"color\": \"0099fd\"
            },
            {
                \"name\": \"cpu.load.avg[5]\",
                \"host\": \"localhost\",
                \"color\": \"fd00aa\"
            },
            {
                \"name\": \"cpu.load.avg[15]\",
                \"host\": \"localhost\",
                \"color\": \"aafd00\"
            }
        ]
        }" \
    $SERVER/$REST_URI/graph

curl -X POST \
    -b $COOKIE_FILE \
    -H "Content-Type: application/json" \
    -H "X-CSRF-Token: $CSRF_TOKEN" \
    -d "{
        \"name\" : \"CPU Load Average (Automatic colors)\",
        \"items\": [
            {
                \"name\": \"cpu.load.avg[1]\",
                \"host\": \"localhost\"
            },
            {
                \"name\": \"cpu.load.avg[5]\",
                \"host\": \"localhost\"
            },
            {
                \"name\": \"cpu.load.avg[15]\",
                \"host\": \"localhost\",
            }
        ]
        }" \
    $SERVER/$REST_URI/graph
