# JD.com API（京东 API）

[English](#english) · [中文](#中文)

## English

This repo reads public JD.com data with Python or curl. You can search products by keyword and read product details, the current price, and buyer reviews. You need one EveryInfra API key. You do not need a JD.com account or cookie. The same API also works as an MCP tool in Claude and Cursor. Billing is per call: these 4 capabilities cost $2.44 to $8.00 per 1,000 calls. Failed calls and empty results are not charged. The EveryInfra JD.com API has 7 capabilities, all listed on the platform page: <https://everyinfra.com/en/jd-api?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>

### Quick start

```bash
git clone https://github.com/everyinfra/jd-api.git
cd jd-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<your API key>
python main.py search 咖啡机 --out items.csv
python main.py item <item_id> --out item.json
python main.py price <item_id>
python main.py reviews <item_id> --out reviews.csv
```

- For `item`, `price`, and `reviews`, use the numeric `item_id` from a `search` result.
- `search` returns 5 rows by default. Every 5 rows count as one call.
- `price` returns the current `price` and its `currency`.
- Without `--out`, the command prints the first 3 rows as JSON. With `--out`, it saves a .csv or .json file. The CSV has a BOM, so Excel opens it without garbled text.
- Register at everyinfra.com, then create the API key in the console. Steps: <https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api#quickstart>

### curl

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"jd","action":"search","params":{"keyword":"咖啡机"}}'
```

All capabilities use the same URL. Change `action` and `params` to call another one. Examples for `product_detail`, `product_price`, and `reviews` are in [examples/curl.sh](examples/curl.sh).

### Claude and Cursor (MCP)

The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. EveryInfra runs the server, so you install no local program.

Claude Code:

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor and other clients that read `mcp.json` ([examples/mcp.json](examples/mcp.json)):

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Custom connectors in Claude on the web and desktop, and ChatGPT, accept only a URL. Enter <https://api.everyinfra.com/mcp/all>, sign in to EveryInfra when asked, and allow access. You do not need to enter a key. Full steps: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>

### Price

| `action` | Per 1,000 calls |
|---|---|
| `search` | $2.47 |
| `product_detail` | $2.44 |
| `product_price` | $5.56 |
| `reviews` | $8.00 |

- Billing is per call, about $0.0024 to $0.008 each. Failed calls, empty results, parameter errors, and authentication failures are not charged.
- `search` is billed by the rows you ask for: every 5 rows count as one call, and blocks that come back with no rows are not charged.
- A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>
- Prices for the other 3 JD.com capabilities are on the platform page: <https://everyinfra.com/en/jd-api?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>

### Fields

These are the fields that the 4 capabilities returned in our test. Each meaning is the first sentence of the field's entry in the API documentation. The link under each table has the full text.

#### `search` (keyword search)

| Field | Meaning |
|---|---|
| `item_id` | JD numeric product ID. |
| `url` | Link to the record on the platform. |
| `title` | Title. null when the platform has no titles (for example text-only posts). |
| `price` | Price as a number without a currency symbol; see currency. |
| `currency` | Currency code of the price (for example CNY, USD). |
| `review_count` | Review count as an integer (search), parsed from the approximate text JD shows in search results: 20k+ becomes 20000 and 500+ becomes 500. |
| `review_count_display` | Review count text exactly as JD shows it in search results (search): Chinese source text, such as JD's wording for 20k+. |
| `good_rate` | Public positive-review percentage shown by JD. |
| `shop_id` | JD numeric shop ID. |
| `shop_name` | Public shop name. |
| `shop_url` | Public JD shop page. |
| `is_jd_self` | Whether this is a JD self-operated (JD.com retail) product. |
| `category_ids` | JD category ID path. |
| `image_url` | Image URL: in search, product_detail, shop and skus it is the product's main (cover) image; in description_images it is the description image of that row (the full-size https image on JD's image host). |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/jd-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>

#### `product_detail` (product details)

| Field | Meaning |
|---|---|
| `item_id` | JD numeric product ID. |
| `url` | Link to the record on the platform. |
| `title` | Title. null when the platform has no titles (for example text-only posts). |
| `price_display` | Price string exactly as shown on the JD page; may be masked by login or membership conditions. |
| `price_masked` | Whether JD masked the price on the detail page. |
| `currency` | Currency code of the price (for example CNY, USD). |
| `available` | Whether the item could be bought when it was read (product_detail, product_price and shop rows); false when out of stock, null when the page did not say. |
| `shop_id` | JD numeric shop ID. |
| `shop_name` | Public shop name. |
| `shop_url` | Public JD shop page. |
| `category_id` | JD leaf category ID of the product (product_detail). |
| `stock` | Stock quantity JD shows publicly; null means the page did not give one, not zero. |
| `stock_state` | Public JD stock status code. |
| `color` | This SKU's color (or finish) as shown on the JD page. |
| `weight` | Product weight as written on the JD page (product_detail); null when the page gives none. |
| `image_url` | Image URL: in search, product_detail, shop and skus it is the product's main (cover) image; in description_images it is the description image of that row (the full-size https image on JD's image host). |
| `image_urls` | Product gallery image URLs (cover included, in the order shown on the JD page). |
| `brand` | Product brand. |
| `model` | Product model number. |
| `upc` | Product barcode (UPC/EAN). null when the page does not provide one. |
| `warranty` | Warranty terms, as written on the page. |
| `product_area` | Place of origin. |
| `is_jd_express` | Whether the item ships via JD Logistics. |
| `variant_count` | Number of variants (SKUs). null when there are none or it is not provided. |
| `variants` | Variant list. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/jd-api/product_detail?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>

#### `product_price` (product price)

| Field | Meaning |
|---|---|
| `item_id` | JD numeric product ID. |
| `url` | Link to the record on the platform. |
| `price` | Price as a number without a currency symbol; see currency. |
| `currency` | Currency code of the price (for example CNY, USD). |
| `available` | Whether the item could be bought when it was read (product_detail, product_price and shop rows); false when out of stock, null when the page did not say. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/jd-api/product_price?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>

#### `reviews` (reviews)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `item_id` | JD numeric product ID. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `rating` | Rating. **The scale varies by platform**: rating_scale on the same row gives the maximum (usually 5; Booking, Douban, iQIYI and NAVER use 10). |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `color` | This SKU's color (or finish) as shown on the JD page. |
| `useful_count` | How many other shoppers marked this review as useful (reviews). |
| `images` | Array of image links in the platform's display order; absent when there are no images. |
| `author_name` | Reviewer nickname, returned as JD shows it (JD may already partially mask it). |
| `author_avatar_url` | Reviewer avatar URL. |
| `author_is_plus` | Whether the reviewer is a JD PLUS member. |
| `buy_count` | How many times the reviewer bought this item, as the page shows ('purchased N times'). |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `next_page_token` | Page token: pass it back unchanged as `page_token`, with the other parameters the same, to fetch the next page; valid for 24 hours and only for the same product. |
| `rating_scale` | Maximum of rating in the same row: 5 for five-star scales, 10 for ten-point scales. |

All parameters and fields: <https://everyinfra.com/en/jd-api/reviews?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>

### FAQ

**Do I need a JD.com account or cookie to call the API?**

No. Send the `Authorization: Bearer` header with your API key. The request body holds `platform`, `action`, and the capability parameters. You do not scan a QR code, keep a login session, or open a browser.

**How much does it cost? Are failed calls charged? Is there a free allowance?**

Billing is per call, from $2.44 per 1,000 calls. Failed calls, empty results, parameter errors, and authentication failures are not charged. A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>

**Can I connect the JD.com API to Claude or Cursor?**

Yes. The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. You install no local program. Setup for Claude, Cursor, ChatGPT, and Claude Code: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>.

**What legal points apply when I use JD.com data?**

The EveryInfra Terms of Service require you to make sure your use of the data follows applicable law and the terms of the relevant platform. Do not use the data for anything illegal or anything that violates privacy or intellectual property rights. Do not use bulk scraping for harassment, fraud, or other abuse. When you use personal information such as nicknames and avatars, keep only the fields your business needs.

**Which JD.com data can I get?**

The EveryInfra JD.com API has 7 capabilities:

- keyword search
- product details
- reviews
- shop
- product price
- All SKUs with prices
- description images

Parameters and return fields for each capability are on the platform page: <https://everyinfra.com/en/jd-api?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>

### Tested

Before release, we ran the 4 commands in Quick start against the live API with this repo's code.

| Command | Time (Singapore, UTC+8) | Rows | Charged |
|---|---|---|---|
| `python main.py search 咖啡机 --out items.csv` | 2026-11-21 09:20 | 5 | $0.002472 |
| `python main.py item <item_id> --out item.json` | 2026-11-21 09:21 | 1 | $0.002444 |
| `python main.py price <item_id>` | 2026-11-21 09:21 | 1 | $0.005556 |
| `python main.py reviews <item_id> --out reviews.csv` | 2026-11-21 09:21 | 10 | $0.008000 |

## 中文

本仓库用 Python 或 curl 读京东公开数据：按关键词搜商品，读商品详情、当前价格和买家评价。只需一把 EveryInfra API Key，不用京东账号和 Cookie，也能作为 MCP 工具接进 Claude、Cursor。按调用次数计费，这 4 个能力每千次 $2.44 到 $8.00，失败和空结果不收费。京东共 7 个能力：<https://everyinfra.com/jd-api?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>

### 快速开始

```bash
git clone https://github.com/everyinfra/jd-api.git
cd jd-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<你的 API Key>
python main.py search 咖啡机 --out items.csv
python main.py item <item_id> --out item.json
python main.py price <item_id>
python main.py reviews <item_id> --out reviews.csv
```

- `item`、`price`、`reviews` 的 `item_id` 用 `search` 结果里的 `item_id`（数字）。
- `search` 默认返回 5 条，每 5 条算一次调用。
- `price` 返回当前价格 `price` 和币种 `currency`。
- 不加 `--out` 时打印前 3 条 JSON；加 `--out` 存成 .csv 或 .json。CSV 带 BOM，Excel 直接打开不乱码。
- API Key 在 everyinfra.com 注册后到控制台创建，步骤见 <https://everyinfra.com/docs?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api#quickstart>

### 用 curl 调

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"jd","action":"search","params":{"keyword":"咖啡机"}}'
```

所有能力都发到同一个地址，换 `action` 和 `params` 就行；`product_detail`、`product_price`、`reviews` 的写法见 [examples/curl.sh](examples/curl.sh)。

### 接进 Claude、Cursor（MCP）

远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key；服务器由 EveryInfra 运行，不用装本地程序。

Claude Code：

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor 等读 `mcp.json` 的客户端（[examples/mcp.json](examples/mcp.json)）：

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Claude 网页版和桌面版的自定义连接器、ChatGPT 只能填网址：填 <https://api.everyinfra.com/mcp/all>，连接时登录 EveryInfra 并允许，不用填 Key。完整步骤见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>

### 价格

| 能力 | `action` | 每千次 |
|---|---|---|
| 关键词搜索 | `search` | $2.47 |
| 商品详情 | `product_detail` | $2.44 |
| 商品价格 | `product_price` | $5.56 |
| 评价 | `reviews` | $8.00 |

- 按调用次数计费，每次约 $0.0024 到 $0.008；失败、空结果、参数错误和鉴权失败都不收费。
- `search` 按要的条数计费，每 5 条算一次调用，没返回数据的部分不收费。
- 新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>
- 京东其他 3 个能力的单价见平台页 <https://everyinfra.com/jd-api?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>

### 返回字段

下面是这 4 个能力实测返回的字段，含义取自接口文档每条说明的第一句，完整说明在每张表下面的链接里。

#### `search`（关键词搜索）

| 字段 | 含义 |
|---|---|
| `item_id` | 京东商品数字 ID；search 可把它直接交给详情、评价或价格能力。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `title` | 标题。 |
| `price` | 价格数值，不含货币符号；币种见 currency。 |
| `currency` | 价格币种代码（如 CNY、USD）。 |
| `review_count` | 搜索列表上的评价数，整数（search）：把京东显示的约数文本转成数字，「2万+」→ 20000，「500+」→ 500。 |
| `review_count_display` | 京东搜索列表上显示的评价数原文（search），如「2万+」，原样返回；列表没给这个文本时不返回此列。 |
| `good_rate` | 京东公开的好评率百分比。 |
| `shop_id` | 京东店铺数字 ID。 |
| `shop_name` | 公开店铺名称。 |
| `shop_url` | 京东店铺公开页面。 |
| `is_jd_self` | 是否为京东自营商品。 |
| `category_ids` | 京东类目 ID 路径。 |
| `image_url` | 图片链接：search、product_detail、shop、skus 里是商品主图（封面）；description_images 里是这一行的那张详情图（京东图床的 https 原图）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/jd-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>

#### `product_detail`（商品详情）

| 字段 | 含义 |
|---|---|
| `item_id` | 京东商品数字 ID；search 可把它直接交给详情、评价或价格能力。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `title` | 标题。 |
| `price_display` | 京东页面显示的价格原文；可能因登录或会员条件被遮罩。 |
| `price_masked` | 详情页价格是否被京东遮罩；为 true 时不要把 price_display 当精确成交价。 |
| `currency` | 价格币种代码（如 CNY、USD）。 |
| `available` | 采集时是否可售（product_detail、product_price、shop 的商品行）；缺货时为 false，null 表示页面没给。 |
| `shop_id` | 京东店铺数字 ID。 |
| `shop_name` | 公开店铺名称。 |
| `shop_url` | 京东店铺公开页面。 |
| `category_id` | 商品所在的京东末级类目 ID（product_detail）。 |
| `stock` | 京东页面公开的库存数量；null 表示页面没给，不是 0。 |
| `stock_state` | 京东公开的库存状态码。 |
| `color` | 京东页面上这个 SKU 的颜色（或外观）属性值。 |
| `weight` | 京东页面上的商品重量原文（product_detail）；null 表示页面没写。 |
| `image_url` | 图片链接：search、product_detail、shop、skus 里是商品主图（封面）；description_images 里是这一行的那张详情图（京东图床的 https 原图）。 |
| `image_urls` | 商品图集链接列表（含主图，按京东页面上的顺序）；单数 image_url 是其中第一张。 |
| `brand` | 商品品牌。 |
| `model` | 商品型号。 |
| `upc` | 商品条码（UPC/EAN）；null 表示页面未提供。 |
| `warranty` | 保修说明原文。 |
| `product_area` | 产地。 |
| `is_jd_express` | 是否由京东物流配送。 |
| `variant_count` | 变体（SKU）数量；null 表示无变体或未提供。 |
| `variants` | 变体列表，每项含名称、SKU、价格、库存状态等；null 表示无变体或未提供。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/jd-api/product_detail?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>

#### `product_price`（商品价格）

| 字段 | 含义 |
|---|---|
| `item_id` | 京东商品数字 ID；search 可把它直接交给详情、评价或价格能力。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `price` | 价格数值，不含货币符号；币种见 currency。 |
| `currency` | 价格币种代码（如 CNY、USD）。 |
| `available` | 采集时是否可售（product_detail、product_price、shop 的商品行）；缺货时为 false，null 表示页面没给。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/jd-api/product_price?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>

#### `reviews`（评价）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `item_id` | 京东商品数字 ID；search 可把它直接交给详情、评价或价格能力。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `rating` | 评分。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `color` | 京东页面上这个 SKU 的颜色（或外观）属性值。 |
| `useful_count` | 这条评价被其他买家点「有用」的次数（reviews）。 |
| `images` | 图片链接数组，按平台展示顺序；没有图片时不出现这个字段。 |
| `author_name` | 评价人昵称，按京东页面原样返回（京东可能已部分打码）。 |
| `author_avatar_url` | 评价人头像链接。 |
| `author_is_plus` | 评价人是否为京东 PLUS 会员。 |
| `buy_count` | 评价人购买该商品的次数（页面显示的「购买 N 次」。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `next_page_token` | 翻页令牌：作为下一次请求的 page_token 原样传回取下一页（其余参数不变，24 小时内有效，只能用于同一个商品）；同一页每行的值相同，响应顶层也有同一个 next_page_token。 |
| `rating_scale` | 上一列 `rating` 的满分。 |

完整参数和字段：<https://everyinfra.com/jd-api/reviews?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>

### 常见问题

**调用时要不要提供京东账号或 Cookie？**

不用，请求头带 `Authorization: Bearer` 和 API Key 就能调，请求体写 `platform`、`action` 和能力参数。不用扫码、维护登录状态，也不用开浏览器。

**怎么收费？失败了收不收钱？有免费额度吗？**

按调用次数计费，每千次 $2.44 起。失败、空结果、参数错误和鉴权失败都不收费。新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见定价页 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>

**能把京东接口接进 Claude、Cursor 吗？**

能，远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key，不用装本地程序。Claude、Cursor、ChatGPT、Claude Code 配置见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>。

**用京东数据要注意哪些合规问题？**

EveryInfra 服务条款要求你自行确保数据用法符合适用法律和相关平台条款，禁止用于违法、侵犯隐私或知识产权，或批量抓取用于骚扰、欺诈等恶意用途。用到昵称、头像等个人信息时，只留业务用得上的字段。

**可以拿到京东的哪些数据？**

京东有 7 个能力：关键词搜索、商品详情、评价、店铺资料、商品价格、全部 SKU 与价格、商品介绍详情图。每个能力的参数和返回字段见平台页 <https://everyinfra.com/jd-api?utm_source=github&utm_medium=example_repo&utm_campaign=jd-api>

### 实测记录

发布前用本仓的代码对线上接口跑过一遍，命令就是「快速开始」里的 4 条。

| 命令 | 时间（新加坡时间） | 返回条数 | 扣费 |
|---|---|---|---|
| `python main.py search 咖啡机 --out items.csv` | 2026-11-21 09:20 | 5 | $0.002472 |
| `python main.py item <item_id> --out item.json` | 2026-11-21 09:21 | 1 | $0.002444 |
| `python main.py price <item_id>` | 2026-11-21 09:21 | 1 | $0.005556 |
| `python main.py reviews <item_id> --out reviews.csv` | 2026-11-21 09:21 | 10 | $0.008000 |

`product_detail` 返回的一条（标题、店铺字段和打码的展示价 `price_display` 没放进来）：

```json
{
  "item_id": "100107723113",
  "currency": "CNY",
  "available": false,
  "stock_state": "out_of_stock",
  "color": "【灰金】一键奶咖|6款冷热饮品",
  "weight": "10.05kg",
  "brand": "飞利浦（PHILIPS）",
  "model": "EP3341",
  "warranty": "2年质保",
  "product_area": "中国",
  "variant_count": 3
}
```

## License

MIT
