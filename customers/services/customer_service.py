from customers.models import Customer


class CustomerService:

    @staticmethod
    def create_customer(
        registration
    ):

        booking = registration.booking

        customer, created = Customer.objects.get_or_create(

            booking=booking,

            defaults={

                "customer_name":
                    booking.booked_client_name,

                "mobile_number":
                    booking.mobile_number,
            }

        )

        return customer