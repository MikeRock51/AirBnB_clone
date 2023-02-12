#!/usr/bin/python3
"""Defines unittests for models/amenity.py"""


import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Amenity class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_class_attribute(self):
        amenity_instance = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", amenity_instance.__dict__)

    def test_two_amenities_unique_ids(self):
        amenity_instance = Amenity()
        amenity_instance2 = Amenity()
        self.assertNotEqual(amenity_instance.id, amenity_instance2.id)

    def test_two_amenities_different_created_at(self):
        amenity_instance = Amenity()
        sleep(0.05)
        amenity_instance2 = Amenity()
        self.assertLess(amenity_instance.created_at, amenity_instance2.created_at)

    def test_two_amenities_different_updated_at(self):
        amenity_instance = Amenity()
        sleep(0.05)
        amenity_instance2 = Amenity()
        self.assertLess(amenity_instance.updated_at, amenity_instance2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        amenity_instance = Amenity()
        amenity_instance.id = "123456"
        amenity_instance.created_at = amenity_instance.updated_at = dt
        amstr = amenity_instance.__str__()
        self.assertIn("[Amenity] (123456)", amstr)
        self.assertIn("'id': '123456'", amstr)
        self.assertIn("'created_at': " + dt_repr, amstr)
        self.assertIn("'updated_at': " + dt_repr, amstr)

    def test_args_unused(self):
        amenity_instance = Amenity(None)
        self.assertNotIn(None, amenity_instance.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """instantiation with kwargs test method"""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        amenity_instance = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(amenity_instance.id, "345")
        self.assertEqual(amenity_instance.created_at, dt)
        self.assertEqual(amenity_instance.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
    """Unittests for testing save method of the Amenity class."""

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
        amenity_instance = Amenity()
        sleep(0.05)
        first_updated_at = amenity_instance.updated_at
        amenity_instance.save()
        self.assertLess(first_updated_at, amenity_instance.updated_at)

    def test_two_saves(self):
        amenity_instance = Amenity()
        sleep(0.05)
        first_updated_at = amenity_instance.updated_at
        amenity_instance.save()
        second_updated_at = amenity_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        amenity_instance.save()
        self.assertLess(second_updated_at, amenity_instance.updated_at)

    def test_save_with_arg(self):
        amenity_instance = Amenity()
        with self.assertRaises(TypeError):
            amenity_instance.save(None)

    def test_save_updates_file(self):
        amenity_instance = Amenity()
        amenity_instance.save()
        amid = "Amenity." + amenity_instance.id
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())


class TestAmenity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Amenity class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        amenity_instance = Amenity()
        self.assertIn("id", amenity_instance.to_dict())
        self.assertIn("created_at", amenity_instance.to_dict())
        self.assertIn("updated_at", amenity_instance.to_dict())
        self.assertIn("__class__", amenity_instance.to_dict())

    def test_to_dict_contains_added_attributes(self):
        amenity_instance = Amenity()
        amenity_instance.middle_name = "Holberton"
        amenity_instance.my_number = 98
        self.assertEqual("Holberton", amenity_instance.middle_name)
        self.assertIn("my_number", amenity_instance.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        amenity_instance = Amenity()
        am_dict = amenity_instance.to_dict()
        self.assertEqual(str, type(am_dict["id"]))
        self.assertEqual(str, type(am_dict["created_at"]))
        self.assertEqual(str, type(am_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        amenity_instance = Amenity()
        amenity_instance.id = "123456"
        amenity_instance.created_at = amenity_instance.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(amenity_instance.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        amenity_instance = Amenity()
        self.assertNotEqual(amenity_instance.to_dict(), amenity_instance.__dict__)

    def test_to_dict_with_arg(self):
        amenity_instance = Amenity()
        with self.assertRaises(TypeError):
            amenity_instance.to_dict(None)


if __name__ == "__main__":
    unittest.main()
