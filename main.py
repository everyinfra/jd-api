"""京东 API 示例（JD.com API in Python）。

  python main.py search 咖啡机 --out items.csv       # 按关键词搜商品 / search products
  python main.py item <item_id> --out item.json      # 商品详情 / product detail
  python main.py price <item_id>                     # 商品当前价格 / current price
  python main.py reviews <item_id> --out reviews.csv # 商品评价 / buyer reviews
"""
import argparse

from everyinfra import fetch, report


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="按关键词搜商品 / search products by keyword")
    s.add_argument("keyword")
    i = sub.add_parser("item", help="商品详情 / one product")
    i.add_argument("item_id")
    pr = sub.add_parser("price", help="商品当前价格 / current price")
    pr.add_argument("item_id")
    r = sub.add_parser("reviews", help="商品评价 / buyer reviews")
    r.add_argument("item_id")
    for x in (s, i, pr, r):
        x.add_argument("--out", help="存成 .csv 或 .json / write .csv or .json")
    a = p.parse_args()

    if a.cmd == "search":
        rows, charged = fetch("search", {"keyword": a.keyword})
    elif a.cmd == "item":
        rows, charged = fetch("product_detail", {"item_id": a.item_id})
    elif a.cmd == "price":
        rows, charged = fetch("product_price", {"item_id": a.item_id})
    else:
        rows, charged = fetch("reviews", {"item_id": a.item_id})
    report(rows, charged, a.out)


if __name__ == "__main__":
    main()
