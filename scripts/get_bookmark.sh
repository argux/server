SERVER=http://localhost:7000
ARGUX_BASE=/
REST_URI=rest/1.0
HOST_URI=host

HOST_NAME=localhost
BOOKMARK_HASH=21e901d2d33947159879cc4a2b6df799246118f3

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

curl -X GET \
    -b $COOKIE_FILE \
    -H "Content-Type: application/json" \
    -H "X-CSRF-Token: $CSRF_TOKEN" \
    $SERVER/$REST_URI/user/bookmark/$BOOKMARK_HASH

