from django.test import TestCase
from django.contrib.auth.models import User
from .models import Customer, Category, SizeVariant, Product, Rating, Cart, OrderPlaced, Contact

############################################ Models TestCases ############################################
class ModelTestCase(TestCase):
    def setUp(self):
        # Create a user for testing Testcase
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a category Testcase
        self.category = Category.objects.create(name='Test Category')

        # Create a size variant Testcase
        self.size_variant = SizeVariant.objects.create(size='M', category='M')

        # Create a product Testcase
        self.product = Product.objects.create(
            title='Test Product',
            selling_price=100,
            discounted_price=80,
            description='Test Description',
            brand='Test Brand',
            category=self.category,
            product_image='shoppifly/app/static/app/images/product'
        )
        self.product.shoe_sizes.add(self.size_variant)

        # Create a rating Testcase
        self.rating = Rating.objects.create(
            user=self.user,
            product=self.product,
            rating=5
        )

        # Create a customer Testcase
        self.customer = Customer.objects.create(
            user=self.user,
            name='Test Customer',
            locality='Test Locality',
            city='Test City',
            zipcode=123456,
            state='STATE_CHOICES'
        )

        # Create a cart Testcase
        self.cart = Cart.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )

        # Create an order Testcase
        self.order = OrderPlaced.objects.create(
            user=self.user,
            customer=self.customer,
            product=self.product,
            quantity=1,
            status='Accepted'
        )

        # Create a contact 
        self.contact = Contact.objects.create(
            fullname='Test Contact',
            phone_number='1234567890',
            email='test@example.com',
            subject='Test Subject',
            message='Test Message'
        )

    def test_customer_model(self):
        self.assertEqual(str(self.customer), str(self.customer.id)) # type: ignore

    def test_category_model(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_size_variant_model(self):
        self.assertEqual(str(self.size_variant), 'M')

    def test_product_model(self):
        self.assertEqual(str(self.product), str(self.product.id)) # type: ignore

    def test_rating_model(self):
        self.assertEqual(str(self.rating), 'testuser - Test Product')

    def test_cart_model(self):
        self.assertEqual(str(self.cart), str(self.cart.id)) # type: ignore
        self.assertEqual(self.cart.total_cost, 2 * 80)

    def test_order_placed_model(self):
        self.assertEqual(self.order.total_cost, 1 * 80)

    def test_contact_model(self):
        self.assertEqual(str(self.contact), 'Test Contact')