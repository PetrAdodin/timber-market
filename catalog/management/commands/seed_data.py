from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from catalog.models import Category, Supplier, TagProduct, TimberProduct


class Command(BaseCommand):
    help = 'Создает начальные данные для проекта Timber Market'

    def handle(self, *args, **options):
        author, created = User.objects.get_or_create(
            username='timber_user',
            defaults={
                'email': 'timber@example.com',
            },
        )

        if created:
            author.set_password('Timber12345')
            author.save()
            self.stdout.write(self.style.SUCCESS('Создан пользователь timber_user.'))
        else:
            author.email = 'timber@example.com'
            author.set_password('Timber12345')
            author.save()
            self.stdout.write(self.style.WARNING('Пользователь timber_user уже существовал. Пароль обновлен.'))

        categories_data = [
            ('Доска', 'doska'),
            ('Брус', 'brus'),
            ('Отделочные материалы', 'otdelochnye-materialy'),
            ('Листовые материалы', 'listovye-materialy'),
            ('Террасные материалы', 'terrasnye-materialy'),
        ]

        categories = {}
        for name, slug in categories_data:
            category, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name},
            )
            category.name = name
            category.save()
            categories[slug] = category

        tags_data = [
            ('сосна', 'sosna'),
            ('лиственница', 'listvennica'),
            ('сухой материал', 'suhoy-material'),
            ('строганый', 'stroganyy'),
            ('для строительства', 'dlya-stroitelstva'),
            ('для отделки', 'dlya-otdelki'),
            ('влагостойкий', 'vlagostoykiy'),
            ('премиум', 'premium'),
        ]

        tags = {}
        for tag_name, slug in tags_data:
            tag, _ = TagProduct.objects.get_or_create(
                slug=slug,
                defaults={'tag': tag_name},
            )
            tag.tag = tag_name
            tag.save()
            tags[slug] = tag

        suppliers_data = [
            ('СеверЛес', 'Архангельск', 18),
            ('ЭкоБрус', 'Киров', 12),
            ('Лиственница Профи', 'Иркутск', 15),
            ('Домострой Древо', 'Кострома', 20),
        ]

        suppliers = []
        for name, city, experience_years in suppliers_data:
            supplier, _ = Supplier.objects.get_or_create(
                name=name,
                defaults={
                    'city': city,
                    'experience_years': experience_years,
                },
            )
            supplier.city = city
            supplier.experience_years = experience_years
            supplier.save()
            suppliers.append(supplier)

        products_data = [
            {
                'title': 'Доска обрезная 50×150×6000 мм',
                'slug': 'doska-obreznaya-50x150x6000',
                'content': 'Обрезная доска из хвойных пород подходит для каркасного строительства, настилов, обрешетки и черновых конструкций. Материал отличается универсальностью, доступной ценой и удобством обработки.',
                'wood_type': 'Сосна',
                'size': '50×150×6000 мм',
                'grade': '1 сорт',
                'price': Decimal('14500.00'),
                'cat': categories['doska'],
                'tags': ['sosna', 'dlya-stroitelstva'],
                'supplier_index': 0,
            },
            {
                'title': 'Брус строганый 100×100 мм',
                'slug': 'brus-stroganyy-100x100',
                'content': 'Строганый брус применяется для несущих и декоративных конструкций. Гладкая поверхность позволяет использовать его в открытых интерьерных решениях и строительных узлах.',
                'wood_type': 'Ель',
                'size': '100×100×6000 мм',
                'grade': '1 сорт',
                'price': Decimal('21500.00'),
                'cat': categories['brus'],
                'tags': ['stroganyy', 'dlya-stroitelstva'],
                'supplier_index': 1,
            },
            {
                'title': 'Вагонка штиль из сосны',
                'slug': 'vagonka-shtil-iz-sosny',
                'content': 'Вагонка штиль создает ровную спокойную поверхность без выраженных полок. Материал подходит для внутренней отделки стен, потолков, лоджий и дачных помещений.',
                'wood_type': 'Сосна',
                'size': '14×120×3000 мм',
                'grade': 'Экстра',
                'price': Decimal('680.00'),
                'cat': categories['otdelochnye-materialy'],
                'tags': ['sosna', 'dlya-otdelki', 'premium'],
                'supplier_index': 2,
            },
            {
                'title': 'Фанера ФСФ влагостойкая',
                'slug': 'fanera-fsf-vlagostoykaya',
                'content': 'Влагостойкая фанера ФСФ используется в строительстве, производстве опалубки, настилов и конструкций, где требуется повышенная устойчивость к влаге.',
                'wood_type': 'Береза',
                'size': '1220×2440×18 мм',
                'grade': '2/3',
                'price': Decimal('2450.00'),
                'cat': categories['listovye-materialy'],
                'tags': ['vlagostoykiy', 'dlya-stroitelstva'],
                'supplier_index': 3,
            },
            {
                'title': 'Террасная доска из лиственницы',
                'slug': 'terrasnaya-doska-iz-listvennicy',
                'content': 'Террасная доска из лиственницы устойчива к перепадам температуры и влажности. Применяется для настилов, террас, веранд, пирсов и садовых дорожек.',
                'wood_type': 'Лиственница',
                'size': '28×140×4000 мм',
                'grade': 'Прима',
                'price': Decimal('1950.00'),
                'cat': categories['terrasnye-materialy'],
                'tags': ['listvennica', 'premium', 'vlagostoykiy'],
                'supplier_index': None,
            },
            {
                'title': 'Имитация бруса для отделки',
                'slug': 'imitaciya-brusa-dlya-otdelki',
                'content': 'Имитация бруса используется для внутренней и наружной отделки. Материал помогает создать эффект стены из массивного бруса при меньшем весе конструкции.',
                'wood_type': 'Сосна',
                'size': '20×145×6000 мм',
                'grade': 'АВ',
                'price': Decimal('920.00'),
                'cat': categories['otdelochnye-materialy'],
                'tags': ['sosna', 'dlya-otdelki'],
                'supplier_index': None,
            },
            {
                'title': 'Рейка монтажная сухая',
                'slug': 'reyka-montazhnaya-suhaya',
                'content': 'Сухая монтажная рейка применяется для обрешетки, монтажа панелей, декоративных элементов и вспомогательных строительных работ.',
                'wood_type': 'Ель',
                'size': '20×40×3000 мм',
                'grade': '1 сорт',
                'price': Decimal('95.00'),
                'cat': categories['doska'],
                'tags': ['suhoy-material', 'dlya-otdelki'],
                'supplier_index': None,
            },
            {
                'title': 'Половая доска камерной сушки',
                'slug': 'polovaya-doska-kamernoy-sushki',
                'content': 'Половая доска камерной сушки предназначена для устройства деревянных полов. Профиль шип-паз обеспечивает плотное соединение элементов.',
                'wood_type': 'Сосна',
                'size': '36×135×6000 мм',
                'grade': 'А',
                'price': Decimal('1250.00'),
                'cat': categories['otdelochnye-materialy'],
                'tags': ['sosna', 'suhoy-material', 'dlya-otdelki'],
                'supplier_index': None,
            },
            {
                'title': 'Клееный брус для домостроения',
                'slug': 'kleenyy-brus-dlya-domostroeniya',
                'content': 'Клееный брус применяется для строительства энергоэффективных домов, бань и коттеджей. Материал отличается стабильной геометрией и высокой прочностью.',
                'wood_type': 'Сосна',
                'size': '160×200×6000 мм',
                'grade': 'Премиум',
                'price': Decimal('42000.00'),
                'cat': categories['brus'],
                'tags': ['sosna', 'premium', 'dlya-stroitelstva'],
                'supplier_index': None,
            },
            {
                'title': 'OSB-плита для каркасного строительства',
                'slug': 'osb-plita-dlya-karkasnogo-stroitelstva',
                'content': 'OSB-плита используется в каркасном строительстве, устройстве стен, кровельных оснований, полов и временных конструкций.',
                'wood_type': 'Древесная щепа',
                'size': '1250×2500×12 мм',
                'grade': 'OSB-3',
                'price': Decimal('1150.00'),
                'cat': categories['listovye-materialy'],
                'tags': ['vlagostoykiy', 'dlya-stroitelstva'],
                'supplier_index': None,
            },
        ]

        for item in products_data:
            supplier = None
            supplier_index = item['supplier_index']
            if supplier_index is not None:
                supplier = suppliers[supplier_index]

            product, _ = TimberProduct.objects.update_or_create(
                slug=item['slug'],
                defaults={
                    'title': item['title'],
                    'content': item['content'],
                    'wood_type': item['wood_type'],
                    'size': item['size'],
                    'grade': item['grade'],
                    'price': item['price'],
                    'cat': item['cat'],
                    'supplier': supplier,
                    'author': author,
                    'is_published': TimberProduct.Status.PUBLISHED,
                },
            )

            product.tags.set([tags[tag_slug] for tag_slug in item['tags']])

        self.stdout.write(self.style.SUCCESS('Начальные данные Timber Market успешно созданы.'))