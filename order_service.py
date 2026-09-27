from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

orders = []

BOOK_SERVICE_URL = "http://localhost:5001"


@app.route('/orders', methods=['POST'])
def create_order():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Data JSON tidak ditemukan"
        }), 400

    book_id = data.get('book_id')

    if book_id is None:
        return jsonify({
            "error": "book_id wajib diisi"
        }), 400

    print()
    print("Client")
    print("   ↓")
    print("Order Service :5002")
    print("   ↓")
    print("HTTP Request")
    print("   ↓")
    print("Book Service :5001")

    try:

        response = requests.get(
            f"{BOOK_SERVICE_URL}/books/{book_id}",
            timeout=5
        )

        if response.status_code == 200:

            book_data = response.json()

            print("   ↓")
            print("Data Buku:", book_data)

            if book_data.get('stock', 0) > 0:

                order = {
                    "id": len(orders) + 1,
                    "book_id": book_id,
                    "status": "berhasil"
                }

                orders.append(order)

                print("   ↓")
                print("Order berhasil dibuat:", order)
                print()

                return jsonify(order), 201

            return jsonify({
                "error": "Buku tidak tersedia atau stok habis"
            }), 400

        return jsonify({
            "error": "Buku tidak ditemukan"
        }), 404

    except requests.exceptions.ConnectionError:

        print("   X")
        print("Book Service sedang down!")
        print()

        return jsonify({
            "error": "Book Service sedang down!"
        }), 500

    except requests.exceptions.Timeout:

        return jsonify({
            "error": "Request ke Book Service timeout"
        }), 504

    except requests.exceptions.RequestException as e:

        return jsonify({
            "error": f"Terjadi kesalahan: {str(e)}"
        }), 500


if __name__ == '__main__':

    print("===================================")
    print("     ORDER SERVICE - PORT 5002")
    print("===================================")
    print("Book Service:", BOOK_SERVICE_URL)
    print("Order Service: http://localhost:5002")
    print()

    app.run(port=5002, debug=True)