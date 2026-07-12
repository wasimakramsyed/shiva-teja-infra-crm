from customers.models import Customer, CustomerProperty
from notifications.models import Notification
from bookings.services.activity_service import ActivityService


class CustomerService:

    @staticmethod
    def create_customer(booking):

        # -----------------------------------
        # Find Existing Customer
        # -----------------------------------

        customer = Customer.objects.filter(
            mobile_number=booking.mobile_number
        ).first()

        # -----------------------------------
        # Create Customer if not exists
        # -----------------------------------

        if not customer:

            customer = Customer.objects.create(

                customer_name=booking.booked_client_name,

                mobile_number=booking.mobile_number,

            )

        # -----------------------------------
        # Prevent Duplicate Property
        # -----------------------------------

        existing_property = CustomerProperty.objects.filter(
            booking=booking
        ).first()

        if existing_property:
            return existing_property

        # -----------------------------------
        # Create Property Ownership
        # -----------------------------------

        customer_property = CustomerProperty.objects.create(

            customer=customer,
            booking=booking,
            project=booking.project,
            plot=booking.plot,
            assigned_employee=booking.assigned_employee,
            assigned_team=booking.assigned_team,
            sale_amount=booking.booking_amount,
            paid_amount=(
                booking.booking_amount -
                booking.pending_amount
            ),
            pending_amount=booking.pending_amount,
            sale_status="fully_paid",
            purchase_date=booking.booking_date

)

        # -----------------------------------
        # Plot Sold
        # -----------------------------------

        booking.plot.status = "sold"
        booking.plot.save()

        # -----------------------------------
        # Notification
        # -----------------------------------

        Notification.objects.create(

            message=(
                f"{customer.customer_name} "
                f"purchased Plot "
                f"{booking.plot.plot_number}"
            )

        )

        # -----------------------------------
        # Timeline
        # -----------------------------------

        ActivityService.log(

            booking=booking,

            activity="Customer Created",

            description=(
                "Customer and Property "
                "created automatically."
            )

        )

        return customer_property