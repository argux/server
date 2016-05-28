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

echo $SERVER/$REST_URI/graph/6

curl -X GET \
    -b $COOKIE_FILE \
    -H "Content-Type: application/json" \
    -H "X-CSRF-Token: $CSRF_TOKEN" \
    $SERVER/$REST_URI/graph/6?get_values=true
