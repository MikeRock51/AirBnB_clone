#!/usr/bin/python3
"""Defines unittests for models/place.py"""


import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Place class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Place, type(Place()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_is_public_class_attribute(self):
        place_instance = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(place_instance))
        self.assertNotIn("city_id", place_instance.__dict__)

    def test_user_id_is_public_class_attribute(self):
        place_instance = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(place_instance))
        self.assertNotIn("user_id", place_instance.__dict__)

    def test_name_is_public_class_attribute(self):
        place_instance = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(place_instance))
        self.assertNotIn("name", place_instance.__dict__)

    def test_description_is_public_class_attribute(self):
        place_instance = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(place_instance))
        self.assertNotIn("description", place_instance.__dict__)

    def test_number_rooms_is_public_class_attribute(self):
        place_instance = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(place_instance))
        self.assertNotIn("number_rooms", place_instance.__dict__)

    def test_number_bathrooms_is_public_class_attribute(self):
        place_instance = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(place_instance))
        self.assertNotIn("number_bathrooms", place_instance.__dict__)

    def test_max_guest_is_public_class_attribute(self):
        place_instance = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(place_instance))
        self.assertNotIn("max_guest", place_instance.__dict__)

    def test_price_by_night_is_public_class_attribute(self):
        place_instance = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(place_instance))
        self.assertNotIn("price_by_night", place_instance.__dict__)

    def test_latitude_is_public_class_attribute(self):
        place_instance = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(place_instance))
        self.assertNotIn("latitude", place_instance.__dict__)

    def test_longitude_is_public_class_attribute(self):
        place_instance = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(place_instance))
        self.assertNotIn("longitude", place_instance.__dict__)

    def test_amenity_ids_is_public_class_attribute(self):
        place_instance = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(place_instance))
        self.assertNotIn("amenity_ids", place_instance.__dict__)

    def test_two_places_unique_ids(self):
        pl1 = Place()
        pl2 = Place()
        self.assertNotEqual(pl1.id, pl2.id)

    def test_two_places_different_created_at(self):
        pl1 = Place()
        sleep(0.05)
        pl2 = Place()
        self.assertLess(pl1.created_at, pl2.created_at)

    def test_two_places_different_updated_at(self):
        pl1 = Place()
        sleep(0.05)
        pl2 = Place()
        self.assertLess(pl1.updated_at, pl2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        place_instance = Place()
        place_instance.id = "123456"
        place_instance.created_at = place_instance.updated_at = dt
        plstr = place_instance.__str__()
        self.assertIn("[Place] (123456)", plstr)
        self.assertIn("'id': '123456'", plstr)
        self.assertIn("'created_at': " + dt_repr, plstr)
        self.assertIn("'updated_at': " + dt_repr, plstr)

    def test_args_unused(self):
        place_instance = Place(None)
        self.assertNotIn(None, place_instance.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        place_instance = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(place_instance.id, "345")
        self.assertEqual(place_instance.created_at, dt)
        self.assertEqual(place_instance.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_save(unittest.TestCase):
    """Unittests for testing save method of the Place class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        place_instance = Place()
        sleep(0.05)
        first_updated_at = place_instance.updated_at
        place_instance.save()
        self.assertLess(first_updated_at, place_instance.updated_at)

    def test_two_saves(self):
        place_instance = Place()
        sleep(0.05)
        first_updated_at = place_instance.updated_at
        place_instance.save()
        second_updated_at = place_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        place_instance.save()
        self.assertLess(second_updated_at, place_instance.updated_at)

    def test_save_with_arg(self):
        place_instance = Place()
        with self.assertRaises(TypeError):
            place_instance.save(None)

    def test_save_updates_file(self):
        place_instance = Place()
        place_instance.save()
        plid = "Place." + place_instance.id
        with open("file.json", "r") as f:
            self.assertIn(plid, f.read())


class TestPlace_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Place class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        place_instance = Place()
        self.assertIn("id", place_instance.to_dict())
        self.assertIn("created_at", place_instance.to_dict())
        self.assertIn("updated_at", place_instance.to_dict())
        self.assertIn("__class__", place_instance.to_dict())

    def test_to_dict_contains_added_attributes(self):
        place_instance = Place()
        place_instance.middle_name = "Holberton"
        place_instance.my_number = 98
        self.assertEqual("Holberton", place_instance.middle_name)
        self.assertIn("my_number", place_instance.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        place_instance = Place()
        pl_dict = place_instance.to_dict()
        self.assertEqual(str, type(pl_dict["id"]))
        self.assertEqual(str, type(pl_dict["created_at"]))
        self.assertEqual(str, type(pl_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        place_instance = Place()
        place_instance.id = "123456"
        place_instance.created_at = place_instance.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(place_instance.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        place_instance = Place()
        self.assertNotEqual(place_instance.to_dict(), place_instance.__dict__)

    def test_to_dict_with_arg(self):
        place_instance = Place()
        with self.assertRaises(TypeError):
            place_instance.to_dict(None)


if __name__ == "__main__":
    unittest.main()