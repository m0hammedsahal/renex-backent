from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True)  # Optional icon for each category
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class MainPlace(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    region = models.CharField(max_length=150, blank=True, null=True)  # Optional field for broader location (e.g., state/country)
    coordinates = models.CharField(max_length=255, blank=True, null=True)  # Optional latitude/longitude
    image = models.ImageField(upload_to='main_place_images/', blank=True, null=True)  # Image representing the place
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class PropertyListing(models.Model):
    CATEGORY_CHOICES = [
        ('apartments', 'Apartments'),
        ('builder_floors', 'Builder Floors'),
        ('farm_houses', 'Farm Houses'),
        ('pg', 'PG'),
    ]

    FURNISHING_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Un-Furnished'),
    ]

    STATUS_CHOICES = [
        ('new_launch', 'New Launch'),
        ('ready_to_move', 'Ready to Move'),
        ('under_construction', 'Under Construction'),
    ]

    BUY_OR_RENT_CHOICES = [
        ('buy', 'Buy'),
        ('rent', 'Rent'),
    ]

    LISTED_BY_CHOICES = [
        ('builder', 'Builder'),
        ('dealer', 'Dealer'),
        ('owner', 'Owner'),
    ]

    title = models.CharField(max_length=255, verbose_name="Ad Title")
    description = models.TextField(verbose_name="Description")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='properties')
    buy_or_rent = models.CharField(max_length=10, choices=BUY_OR_RENT_CHOICES, default='buy', verbose_name="Buy or Rent")
    
    bedrooms = models.PositiveIntegerField(null=True, blank=True, verbose_name="Bedrooms")
    bathrooms = models.PositiveIntegerField(null=True, blank=True, verbose_name="Bathrooms")

    furnishing = models.CharField(max_length=50, choices=FURNISHING_CHOICES, verbose_name="Furnishing")
    construction_status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name="Construction Status")

    super_built_up_area = models.FloatField(verbose_name="Super Built-up Area (ft)", null=True, blank=True)
    carpet_area = models.FloatField(verbose_name="Carpet Area (ft)", null=True, blank=True)
    maintenance = models.FloatField(verbose_name="Maintenance (Monthly)", null=True, blank=True)
    total_floors = models.PositiveIntegerField(verbose_name="Total Floors", null=True, blank=True)
    floor_no = models.PositiveIntegerField(verbose_name="Floor No", null=True, blank=True)
    facing = models.CharField(max_length=50, verbose_name="Facing", null=True, blank=True)
    projects_count = models.PositiveIntegerField(verbose_name="Number of Projects", null=True, blank=True)

    price = models.FloatField(verbose_name="Price")

    location = models.ForeignKey(MainPlace, on_delete=models.CASCADE, related_name='properties')
    ecxact_location = models.CharField(max_length=255, verbose_name="Location")

    listed_by_name = models.CharField(max_length=255, verbose_name="lname")
    listed_by = models.CharField(max_length=50, choices=LISTED_BY_CHOICES, verbose_name="Listed by")
    listed_by_photo = models.ImageField(upload_to="property_photos/", null=True, blank=True, verbose_name="Upload Photos")
    mobile_number = models.CharField(max_length=20, verbose_name="Mobile Number")

    mainphoto = models.ImageField(upload_to="property_photos/", null=True, blank=True, verbose_name="Upload Photos")
    photo1 = models.ImageField(upload_to="property_photos/", null=True, blank=True, verbose_name="Upload Photos")
    photo2 = models.ImageField(upload_to="property_photos/", null=True, blank=True, verbose_name="Upload Photos")
    photo3 = models.ImageField(upload_to="property_photos/", null=True, blank=True, verbose_name="Upload Photos")


    is_active = models.BooleanField(default=True)
    is_favarite = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
