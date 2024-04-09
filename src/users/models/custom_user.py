from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('athlete', 'Athlete'),
        ('scout', 'Scout'),
        ('admin', 'Admin'),
    )

    username = models.CharField(max_length=50, primary_key=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    password = models.CharField(max_length=128, blank=True) # protect password
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups'  # Unique related_name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions'  # Unique related_name
    )

    class Meta:
        db_table = "user"
        app_label = 'users'

    def __str__(self):
        return f"User: {self.username}"


class Athlete(models.Model):
    POSITION_CHOICES = (
        ('GK', 'Goalkeeper'),
        ('CB', 'Center Back'),
        ('LB', 'Left Back'),
        ('RB', 'Right Back'),
        ('CM', 'Center Midfield'),
        ('LM', 'Left Midfield'),
        ('RM', 'Right Midfield'),
        ('CAM', 'Center Attacking Midfield'),
        ('LW', 'Left Wing'),
        ('RW', 'Right Wing'),
        ('ST', 'Striker'),
    )

    HOMWTOWN_CHOICES = [
        ('Amnat Charoen', 'Amnat Charoen'),
        ('Ang Thong', 'Ang Thong'),
        ('Bangkok', 'Bangkok'),
        ('Bueng Kan', 'Bueng Kan'),
        ('Buri Ram', 'Buri Ram'),
        ('Chachoengsao', 'Chachoengsao'),
        ('Chai Nat', 'Chai Nat'),
        ('Chaiyaphum', 'Chaiyaphum'),
        ('Chanthaburi', 'Chanthaburi'),
        ('Chiang Mai', 'Chiang Mai'),
        ('Chiang Rai', 'Chiang Rai'),
        ('Chon Buri', 'Chon Buri'),
        ('Chumphon', 'Chumphon'),
        ('Kalasin', 'Kalasin'),
        ('Kamphaeng Phet', 'Kamphaeng Phet'),
        ('Kanchanaburi', 'Kanchanaburi'),
        ('Khon Kaen', 'Khon Kaen'),
        ('Krabi', 'Krabi'),
        ('Lampang', 'Lampang'),
        ('Lamphun', 'Lamphun'),
        ('Loei', 'Loei'),
        ('Lopburi', 'Lopburi'),
        ('Mae Hong Son', 'Mae Hong Son'),
        ('Maha Sarakham', 'Maha Sarakham'),
        ('Mukdahan', 'Mukdahan'),
        ('Nakhon Nayok', 'Nakhon Nayok'),
        ('Nakhon Pathom', 'Nakhon Pathom'),
        ('Nakhon Phanom', 'Nakhon Phanom'),
        ('Nakhon Ratchasima', 'Nakhon Ratchasima'),
        ('Nakhon Sawan', 'Nakhon Sawan'),
        ('Nakhon Si Thammarat', 'Nakhon Si Thammarat'),
        ('Nan', 'Nan'),
        ('Narathiwat', 'Narathiwat'),
        ('Nong Bua Lam Phu', 'Nong Bua Lam Phu'),
        ('Nong Khai', 'Nong Khai'),
        ('Nonthaburi', 'Nonthaburi'),
        ('Pathum Thani', 'Pathum Thani'),
        ('Pattani', 'Pattani'),
        ('Phangnga', 'Phangnga'),
        ('Phatthalung', 'Phatthalung'),
        ('Phayao', 'Phayao'),
        ('Phetchabun', 'Phetchabun'),
        ('Phetchaburi', 'Phetchaburi'),
        ('Phichit', 'Phichit'),
        ('Phitsanulok', 'Phitsanulok'),
        ('Phra Nakhon Si Ayutthaya', 'Phra Nakhon Si Ayutthaya'),
        ('Phrae', 'Phrae'),
        ('Phuket', 'Phuket'),
        ('Prachin Buri', 'Prachin Buri'),
        ('Prachuap Khiri Khan', 'Prachuap Khiri Khan'),
        ('Ranong', 'Ranong'),
        ('Ratchaburi', 'Ratchaburi'),
        ('Rayong', 'Rayong'),
        ('Roi Et', 'Roi Et'),
        ('Sa Kaeo', 'Sa Kaeo'),
        ('Sakon Nakhon', 'Sakon Nakhon'),
        ('Samut Prakan', 'Samut Prakan'),
        ('Samut Sakhon', 'Samut Sakhon'),
        ('Samut Songkhram', 'Samut Songkhram'),
        ('Saraburi', 'Saraburi'),
        ('Satun', 'Satun'),
        ('Sing Buri', 'Sing Buri'),
        ('Sisaket', 'Sisaket'),
        ('Songkhla', 'Songkhla'),
        ('Sukhothai', 'Sukhothai'),
        ('Suphan Buri', 'Suphan Buri'),
        ('Surat Thani', 'Surat Thani'),
        ('Surin', 'Surin'),
        ('Tak', 'Tak'),
        ('Trang', 'Trang'),
        ('Trat', 'Trat'),
        ('Ubon Ratchathani', 'Ubon Ratchathani'),
        ('Udon Thani', 'Udon Thani'),
        ('Uthai Thani', 'Uthai Thani'),
        ('Uttaradit', 'Uttaradit'),
        ('Yala', 'Yala'),
        ('Yasothon', 'Yasothon'),
    ]

    username = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    age = models.IntegerField()
    position = models.CharField(choices=POSITION_CHOICES, max_length=20, blank=True, null=True)
    birth_date = models.DateTimeField()
    hometown = models.CharField(max_length=100, choices=HOMWTOWN_CHOICES)
    education = models.CharField(max_length=100)
    description = models.TextField()
    club = models.ForeignKey('Organization', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = "athlete"

    def __str__(self):
        return f"Athlete: {self.username.username}"


class Scout(models.Model):

    HOMWTOWN_CHOICES = [
        ('Amnat Charoen', 'Amnat Charoen'),
        ('Ang Thong', 'Ang Thong'),
        ('Bangkok', 'Bangkok'),
        ('Bueng Kan', 'Bueng Kan'),
        ('Buri Ram', 'Buri Ram'),
        ('Chachoengsao', 'Chachoengsao'),
        ('Chai Nat', 'Chai Nat'),
        ('Chaiyaphum', 'Chaiyaphum'),
        ('Chanthaburi', 'Chanthaburi'),
        ('Chiang Mai', 'Chiang Mai'),
        ('Chiang Rai', 'Chiang Rai'),
        ('Chon Buri', 'Chon Buri'),
        ('Chumphon', 'Chumphon'),
        ('Kalasin', 'Kalasin'),
        ('Kamphaeng Phet', 'Kamphaeng Phet'),
        ('Kanchanaburi', 'Kanchanaburi'),
        ('Khon Kaen', 'Khon Kaen'),
        ('Krabi', 'Krabi'),
        ('Lampang', 'Lampang'),
        ('Lamphun', 'Lamphun'),
        ('Loei', 'Loei'),
        ('Lopburi', 'Lopburi'),
        ('Mae Hong Son', 'Mae Hong Son'),
        ('Maha Sarakham', 'Maha Sarakham'),
        ('Mukdahan', 'Mukdahan'),
        ('Nakhon Nayok', 'Nakhon Nayok'),
        ('Nakhon Pathom', 'Nakhon Pathom'),
        ('Nakhon Phanom', 'Nakhon Phanom'),
        ('Nakhon Ratchasima', 'Nakhon Ratchasima'),
        ('Nakhon Sawan', 'Nakhon Sawan'),
        ('Nakhon Si Thammarat', 'Nakhon Si Thammarat'),
        ('Nan', 'Nan'),
        ('Narathiwat', 'Narathiwat'),
        ('Nong Bua Lam Phu', 'Nong Bua Lam Phu'),
        ('Nong Khai', 'Nong Khai'),
        ('Nonthaburi', 'Nonthaburi'),
        ('Pathum Thani', 'Pathum Thani'),
        ('Pattani', 'Pattani'),
        ('Phangnga', 'Phangnga'),
        ('Phatthalung', 'Phatthalung'),
        ('Phayao', 'Phayao'),
        ('Phetchabun', 'Phetchabun'),
        ('Phetchaburi', 'Phetchaburi'),
        ('Phichit', 'Phichit'),
        ('Phitsanulok', 'Phitsanulok'),
        ('Phra Nakhon Si Ayutthaya', 'Phra Nakhon Si Ayutthaya'),
        ('Phrae', 'Phrae'),
        ('Phuket', 'Phuket'),
        ('Prachin Buri', 'Prachin Buri'),
        ('Prachuap Khiri Khan', 'Prachuap Khiri Khan'),
        ('Ranong', 'Ranong'),
        ('Ratchaburi', 'Ratchaburi'),
        ('Rayong', 'Rayong'),
        ('Roi Et', 'Roi Et'),
        ('Sa Kaeo', 'Sa Kaeo'),
        ('Sakon Nakhon', 'Sakon Nakhon'),
        ('Samut Prakan', 'Samut Prakan'),
        ('Samut Sakhon', 'Samut Sakhon'),
        ('Samut Songkhram', 'Samut Songkhram'),
        ('Saraburi', 'Saraburi'),
        ('Satun', 'Satun'),
        ('Sing Buri', 'Sing Buri'),
        ('Sisaket', 'Sisaket'),
        ('Songkhla', 'Songkhla'),
        ('Sukhothai', 'Sukhothai'),
        ('Suphan Buri', 'Suphan Buri'),
        ('Surat Thani', 'Surat Thani'),
        ('Surin', 'Surin'),
        ('Tak', 'Tak'),
        ('Trang', 'Trang'),
        ('Trat', 'Trat'),
        ('Ubon Ratchathani', 'Ubon Ratchathani'),
        ('Udon Thani', 'Udon Thani'),
        ('Uthai Thani', 'Uthai Thani'),
        ('Uttaradit', 'Uttaradit'),
        ('Yala', 'Yala'),
        ('Yasothon', 'Yasothon'),
    ]

    username = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    tier = models.BooleanField()
    birth_date = models.DateTimeField()
    hometown = models.CharField(max_length=100, choices=HOMWTOWN_CHOICES)
    age = models.IntegerField()
    club = models.ForeignKey('Organization', on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField()

    class Meta:
        db_table = "scout"

    def __str__(self):
        return f"Scout: {self.username.username}"


class Admin_organization(models.Model):
    username = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        db_table = "admin"

    def __str__(self):
        return f"Admin: {self.username.username}"


class Organization(models.Model):
    admin = models.ForeignKey(Admin_organization, on_delete=models.CASCADE, blank=True, null=True)
    club_name = models.CharField(max_length=100, primary_key=True)

    class Meta:
        db_table = "organization"

    def __str__(self):
        return f"Organization: {self.username.username}"


