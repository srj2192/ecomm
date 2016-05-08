from decimal import Decimal
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.utils.safestring import mark_safe

# Create your models here.

class ProductQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)


class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model,using=self._db)

	def all(self):
		return self.get_queryset().active()

	def get_related(self,instance):
		products_one=self.get_queryset().filter(categories__in=instance.categories.all())
		products_two=self.get_queryset().filter(default=instance.default)
		product_active=self.get_queryset().filter(active=True)
		qs=(products_one&product_active|products_two&product_active).exclude(id=instance.id).distinct()
		return qs



class Product(models.Model):
	title=models.CharField(max_length=120)
	description=models.TextField(blank=True,null=True)
	price=models.DecimalField(decimal_places=2,max_digits=12)
	active=models.BooleanField(default=True)
	categories=models.ManyToManyField('Category',blank=True)
	default=models.ForeignKey('Category',related_name='default_category',blank=True,null=True)

	objects=ProductManager()

	class Meta:
		ordering=["-title"]

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('product_detail',kwargs={"pk":self.pk})

	def get_image_url(self):
		img=self.productimage_set.first()
		if img:
			return img.image.url
		return img #None


class Variation(models.Model):
	product=models.ForeignKey(Product)
	title=models.CharField(max_length=120)
	price=models.DecimalField(decimal_places=2,max_digits=12)
	sale_price=models.DecimalField(decimal_places=2,max_digits=12,null=True,blank=True)
	active=models.BooleanField(default=True)
	inventory=models.IntegerField(null=True,blank=True)  # refers to unimited

	def __unicode__(self):
		return self.title

	def get_price(self):
		if self.sale_price is not None:
			return self.sale_price
		else:
			return self.price


	def get_html_price(self):
		if self.sale_price is not None:
			html_text="<span class='sale-price'>%s</span><span class='og-price'>%s</span>"%(str(self.sale_price)+" ",self.price)
		else:
			html_text="<span class='sale-price'>%s"%(self.price)
		return mark_safe(html_text)


	def get_absolute_url(self):
		return self.product.get_absolute_url()

	def add_to_cart(self):
		return "%s?item=%s&qty=1" %(reverse("cart"),self.id)


	def remove_from_cart(self):
		return "%s?item=%s&qty=1&delete=True" %(reverse("cart"),self.id)

	def get_title(self):
		return "%s - %s" %(self.product.title,self.title)


def product_post_saved_receiver(sender,instance,created,*args,**kwargs):
	print sender
	product = instance
	variations=product.variation_set.all()
	#the above statement is same as:	 variations=Variations.objects.filter(product=product)
	if variations.count()==0:
		new_var=Variation()
		new_var.product=product
		new_var.title="Default"
		new_var.price=product.price
		new_var.save()
	print created


post_save.connect(product_post_saved_receiver,sender=Product)

# Product Images
# Need to install PILLOW for imagefield to work


def image_upload_to(instance,filename):
	title=instance.product.title
	slug=slugify(title)
	basename,file_extension=filename.split('.')
	new_filename="%s-%s.%s"%(basename,instance.id,file_extension)
	return "products/%s/%s"%(slug,new_filename)

class ProductImage(models.Model):
	product=models.ForeignKey(Product)
	image=models.ImageField(upload_to=image_upload_to)

	def __unicode__(self):
		return self.product.title



#Product Category
class Category(models.Model):
	title=models.CharField(max_length=120,unique=True)
	slug=models.SlugField(unique=True)
	description=models.TextField(blank=True,null=True)
	active=models.BooleanField(default=True)
	timestamp=models.DateTimeField(auto_now_add=True,auto_now=False)

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('category_detail',kwargs={"slug":self.slug})

def image_upload_to_featured(instance,filename):
	title=instance.product.title
	slug=slugify(title)
	basename,file_extension=filename.split('.')
	new_filename="%s-%s.%s"%(basename,instance.id,file_extension)
	return "products/%s/featured/%s"%(slug,new_filename)

class ProductFeatured(models.Model):
	product=models.ForeignKey(Product)
	image=models.ImageField(upload_to=image_upload_to_featured)
	title=models.CharField(max_length=120,null=True,blank=True)
	text=models.CharField(max_length=120,null=True,blank=True)
	text_right=models.BooleanField(default=False)
	text_css_color=models.CharField(max_length=16,null=True,blank=True)
	show_price=models.BooleanField(default=False)
	make_image_background=models.BooleanField(default=False)
	active=models.BooleanField(default=True)

	def __unicode__(self):
		return self.product.title