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

# Items
curl -X POST \
    -b $COOKIE_FILE \
    -H "Content-Type: application/json" \
    -H "X-CSRF-Token: $CSRF_TOKEN" \
    -d "{
        \"name\":\"CPU Load (1 minute average)\",
        \"description\":\"1 Minute average of CPU load\",
        \"type\":\"float\"
        }" \
    $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/item/cpu.load.avg\\\[1\\\]

curl -X POST \
    -b $COOKIE_FILE \
    -H "Content-Type: application/json" \
    -H "X-CSRF-Token: $CSRF_TOKEN" \
    -d "{
        \"name\":\"CPU Load (5 minute average)\",
        \"description\":\"5 Minute average of CPU load\",
        \"type\":\"float\"
        }" \
    $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/item/cpu.load.avg\\\[5\\\]

curl -X POST \
    -b $COOKIE_FILE \
    -H "Content-Type: application/json" \
    -H "X-CSRF-Token: $CSRF_TOKEN" \
    -d "{
        \"name\":\"CPU Load (15 minute average)\",
        \"description\":\"15 Minute average of CPU load\",
        \"type\":\"float\"
        }" \
    $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/item/cpu.load.avg\\\[15\\\]



# Store item with name and description
curl -X POST \
    -b $COOKIE_FILE \
    -H "Content-Type: application/json" \
    -H "X-CSRF-Token: $CSRF_TOKEN" \
    -d "{
        \"name\":\"System uptime\",
        \"description\":\"System Uptime\",
        \"type\":\"int\"
        }" \
    $SERVER/$REST_URI/$HOST_URI/$HOST_NAME/item/sys.uptime

unlink $COOKIE_FILE
unlink $HEADER_FILE
