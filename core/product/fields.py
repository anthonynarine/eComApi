import imp

from django.core import checks
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from termcolor import colored


class OrderField(models.PositiveIntegerField):
    description = "Ordering field on a unique field"

    def __init__(self, unique_for_field=None, *args, **kwargs):
        self.unique_for_field = unique_for_field
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return [*super().check(**kwargs), *self._check_for_field_attribute(**kwargs)]

    def _check_for_field_attribute(self, **kwargs):
        if self.unique_for_field is None:
            return [
                checks.Error("OrderField must define a 'unique_for_frield' attribute")
            ]
        elif self.unique_for_field not in [
            field.name for field in self.model._meta.get_fields()
        ]:
            return [
                checks.Error("OrderField entered does not match existing model field")
            ]
        return []

    def pre_save(self, model_instance, add):
        print(colored("Hellooooo", "green"))
        print(colored(model_instance.product.name, "red"))

        # check if there is a value or not
        if getattr(model_instance, self.attname) is None:
            # print(getattr(model_instance, self.attname))
            # print(colored("NEED A VALUE", "green"))
            # if there is no value we want to generate one
            # prepare the query set
            query_set = self.model.objects.all()
            # try and grab some data and create the query
            try:
                # see notes below on this query
                query = {
                    self.unique_for_field: getattr(
                        model_instance, self.unique_for_field
                    )
                }
                print(colored(query, "green"))
                # run the query to filter out that particular product line
                # based on the unique for field specifies
                query_set = query_set.filter(**query)
                # grabs order attribute from productline.
                # filter using further method to grab the highest num asscoiated to an order field
                last_item = query_set.latest(self.attname)
                # print(colored(self.attname, "yellow"))
                value = last_item.order + 1

            except ObjectDoesNotExist:
                value = 1
            return value
        else:
            return super().pre_save(model_instance, add)


"""
query = {self.unique_for_field : getattr(model_instance, self.unique_for_field)}

what we're trying to do is to run a query that says
get all product line data where order Product equals whatever
the product is. So imagine this product line was associated to 
product one. we want to run a query whereby we say select all 
from product line where order or web product equals one. And 
that would then return all the product lines where there.
That particular product line record is related to that product one."""
