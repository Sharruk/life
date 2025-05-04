from app import app, db
from models import Restaurant, MenuItem, Order, OrderItem


def delete_restaurants_by_names(restaurant_names):
    try:
        with app.app_context():
            for name in restaurant_names:
                # Find restaurant by name
                restaurant = Restaurant.query.filter_by(name=name).first()

                if restaurant:
                    # Delete associated menu items
                    MenuItem.query.filter_by(
                        restaurant_id=restaurant.id).delete()

                    # Delete associated order items and orders
                    orders = Order.query.filter_by(
                        restaurant_id=restaurant.id).all()
                    for order in orders:
                        OrderItem.query.filter_by(order_id=order.id).delete()
                    Order.query.filter_by(restaurant_id=restaurant.id).delete()

                    # Delete restaurant
                    db.session.delete(restaurant)
                    print(f"Successfully deleted restaurant: {name}")
                else:
                    print(f"Restaurant not found: {name}")

            # Commit the changes
            db.session.commit()
            print("All specified restaurants deleted successfully.")

    except Exception as e:
        print(f"Error deleting restaurants: {str(e)}")


if __name__ == "__main__":
    # Example usage: provide a list of restaurant names to delete
    restaurants_to_delete = [
        "SSN Main Canteen", "Rishub's Food Court", "z's Restaurant",
        "Ashwin's Food Court"
    ]  # Add your restaurant names here
    delete_restaurants_by_names(restaurants_to_delete)
