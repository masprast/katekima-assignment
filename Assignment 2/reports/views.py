from datetime import datetime
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from items.models import Item
from purchases.models import PurchaseDetail
from sells.models import SellDetail

# Create your views here.


class StockReport(APIView):
    def get(self, request, item_code):
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        start_date = None
        end_date = None
        try:
            # Ambil data item berdasarkan kode menggunakan filter
            item = get_object_or_404(Item, code__iexact=item_code, is_deleted=False)
            # Parsing tanggal dari string ke objek datetime.date
            # Menggunakan format YYYY-MM-DD
            # Jika tidak ada tanggal yang diberikan, maka ambil semua data
            # Jika ada tanggal yang diberikan, filter berdasarkan tanggal tersebut
            if start_date_str:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            if end_date_str:
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            # Jika terjadi ValueError saat parsing tanggal
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."}, status=400
            )
            # atau jika item tidak ditemukan
        except Item.DoesNotExist or Item.is_deleted:
            return Response(
                {"error": f"Item with code '{item_code}' not found."}, status=404
            )

        # Filter data pembelian dan penjualan berdasarkan item_code
        # dan tanggal yang diberikan
        purchase_filters = Q(item_code__code__iexact=item_code)
        sell_filters = Q(item_code__code__iexact=item_code)

        if start_date:
            purchase_filters &= Q(header_code__date__gte=start_date)
            sell_filters &= Q(header_code__date__gte=start_date)
        if end_date:
            purchase_filters &= Q(header_code__date__lte=end_date)
            sell_filters &= Q(header_code__date__lte=end_date)

        report_items = []
        balance_qty = 0
        balance_amount = 0
        stock_history_qty = []
        stock_history_price = []
        stock_history_total = []

        # Purchase
        all_purchases = PurchaseDetail.objects.filter(purchase_filters).order_by(
            "header_code__date"
        )

        for purchase in all_purchases:
            report_items.append(
                {
                    "date": purchase.header_code.date.strftime("%d-%m-%Y"),
                    "description": purchase.header_code.description,
                    "code": purchase.header_code.code,
                    "in_qty": purchase.quantity,
                    "in_price": purchase.unit_price,
                    "in_total": purchase.quantity * purchase.unit_price,
                    "out_qty": 0,
                    "out_price": 0,
                    "out_total": 0,
                    "stock_qty": list(stock_history_qty),  # history stock saat ini
                    "stock_price": list(stock_history_price),
                    "stock_total": list(stock_history_total),
                    "balance_qty": balance_qty + purchase.quantity,
                    "balance": balance_amount
                    + (purchase.quantity * purchase.unit_price),
                }
            )
            balance_qty += purchase.quantity
            balance_amount += purchase.quantity * purchase.unit_price
            stock_history_qty.append(purchase.quantity)
            stock_history_price.append(purchase.unit_price)
            stock_history_total.append(purchase.quantity * purchase.unit_price)

        # Reser stock history untuk penjualan agar mencerminkan apa yang tersedia pada saat penjualan
        current_stock_qty = list(stock_history_qty)
        current_stock_price = list(stock_history_price)

        # Sell
        all_sells = SellDetail.objects.filter(sell_filters).order_by(
            "header_code__date"
        )

        for sell in all_sells:
            sold_price = 0
            qty_to_sell = sell.quantity
            temp_stock_qty = list(current_stock_qty)  # Stock waktu penjualan
            temp_stock_price = list(current_stock_price)

            # Simulasi FIFO untuk mendapatkan cost of goods sold (COGS)
            for i in range(len(current_stock_qty)):
                if qty_to_sell > 0 and current_stock_qty[i] > 0:
                    sell_qty = min(qty_to_sell, current_stock_qty[i])
                    sold_price += sell_qty * current_stock_price[i]
                    current_stock_qty[i] -= sell_qty
                    qty_to_sell -= sell_qty
                if qty_to_sell == 0:
                    break

            report_items.append(
                {
                    "date": sell.header_code.date.strftime("%d-%m-%Y"),
                    "description": sell.header_code.description,
                    "code": sell.header_code.code,
                    "in_qty": 0,
                    "in_price": 0,
                    "in_total": 0,
                    "out_qty": sell.quantity,
                    "out_price": (
                        int(sold_price / sell.quantity) if sell.quantity > 0 else 0
                    ),  # Average COGS
                    "out_total": sold_price,
                    "stock_qty": list(temp_stock_qty),  # Stock waktu penjualan
                    "stock_price": list(temp_stock_price),
                    "stock_total": [
                        qty * price
                        for qty, price in zip(temp_stock_qty, temp_stock_price)
                    ],
                    "balance_qty": balance_qty - sell.quantity,
                    "balance": balance_amount - sold_price,
                }
            )
            balance_qty -= sell.quantity
            balance_amount -= sold_price

        summary = {
            "in_qty": sum(item["in_qty"] for item in report_items),
            "out_qty": sum(item["out_qty"] for item in report_items),
            "balance_qty": balance_qty,
            "balance": balance_amount,
        }

        result = {
            "items": report_items,
            "item_code": item.code,
            "name": item.name,
            "unit": item.unit,
            "summary": summary,
        }

        return Response({"result": result})
