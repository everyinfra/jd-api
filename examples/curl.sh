#!/usr/bin/env bash
# 京东 API 的 curl 示例：所有能力都发到同一个地址，只换 action 和 params。
# curl examples for the JD.com API: every capability uses the same URL; only action and params change.
#
#   export EVERYINFRA_API_KEY=<your API key>
#   bash examples/curl.sh search 咖啡机
#   bash examples/curl.sh product_detail <item_id> # search 结果里的 item_id / the item_id from a search result
#   bash examples/curl.sh product_price <item_id>
#   bash examples/curl.sh reviews <item_id>
#
# 翻页：把响应里的 next_page_token 放进 params.page_token 再调一次，每页算一次调用。
# Next page: send the response's next_page_token back as params.page_token. Each page is one call.
set -euo pipefail
: "${EVERYINFRA_API_KEY:?Set EVERYINFRA_API_KEY first: https://everyinfra.com/docs#quickstart}"
action=${1:?"usage: bash examples/curl.sh <search|product_detail|product_price|reviews> <value>"}
value=${2:?"value: a keyword or an item_id"}

case "$action" in
  search)                                   params="{\"keyword\":\"$value\"}" ;;
  product_detail | product_price | reviews) params="{\"item_id\":\"$value\"}" ;;
  *) echo "unknown action: $action (use search, product_detail, product_price or reviews)" >&2; exit 2 ;;
esac

curl -sS -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"platform\":\"jd\",\"action\":\"$action\",\"params\":$params}"
echo
