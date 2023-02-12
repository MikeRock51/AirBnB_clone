#!/usr/bin/python3
"""Defines unittests for file_storage"""


import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    def test_FileStorage_instantiation_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_private_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_objects_is_private_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        bm_instance = BaseModel()
        user_instance = User()
        state_instance = State()
        place_instance = Place()
        city_instance = City()
        amenity_instance = Amenity()
        review_instance = Review()
        models.storage.new(bm_instance)
        models.storage.new(user_instance)
        models.storage.new(state_instance)
        models.storage.new(place_instance)
        models.storage.new(city_instance)
        models.storage.new(amenity_instance)
        models.storage.new(review_instance)
        self.assertIn("BaseModel." + bm_instance.id,
                      models.storage.all().keys())
        self.assertIn(bm_instance, models.storage.all().values())
        self.assertIn("User." + user_instance.id, models.storage.all().keys())
        self.assertIn(user_instance, models.storage.all().values())
        self.assertIn("State." + state_instance.id,
                      models.storage.all().keys())
        self.assertIn(state_instance, models.storage.all().values())
        self.assertIn("Place." + place_instance.id,
                      models.storage.all().keys())
        self.assertIn(place_instance, models.storage.all().values())
        self.assertIn("City." + city_instance.id, models.storage.all().keys())
        self.assertIn(city_instance, models.storage.all().values())
        self.assertIn("Amenity." + amenity_instance.id,
                      models.storage.all().keys())
        self.assertIn(amenity_instance, models.storage.all().values())
        self.assertIn("Review." + review_instance.id,
                      models.storage.all().keys())
        self.assertIn(review_instance, models.storage.all().values())

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        bm_instance = BaseModel()
        user_instance = User()
        state_instance = State()
        place_instance = Place()
        city_instance = City()
        amenity_instance = Amenity()
        review_instance = Review()
        models.storage.new(bm_instance)
        models.storage.new(user_instance)
        models.storage.new(state_instance)
        models.storage.new(place_instance)
        models.storage.new(city_instance)
        models.storage.new(amenity_instance)
        models.storage.new(review_instance)
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + bm_instance.id, save_text)
            self.assertIn("User." + user_instance.id, save_text)
            self.assertIn("State." + state_instance.id, save_text)
            self.assertIn("Place." + place_instance.id, save_text)
            self.assertIn("City." + city_instance.id, save_text)
            self.assertIn("Amenity." + amenity_instance.id, save_text)
            self.assertIn("Review." + review_instance.id, save_text)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        bm_instance = BaseModel()
        user_instance = User()
        state_instance = State()
        place_instance = Place()
        city_instance = City()
        amenity_instance = Amenity()
        review_instance = Review()
        models.storage.new(bm_instance)
        models.storage.new(user_instance)
        models.storage.new(state_instance)
        models.storage.new(place_instance)
        models.storage.new(city_instance)
        models.storage.new(amenity_instance)
        models.storage.new(review_instance)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + bm_instance.id, objs)
        self.assertIn("User." + user_instance.id, objs)
        self.assertIn("State." + state_instance.id, objs)
        self.assertIn("Place." + place_instance.id, objs)
        self.assertIn("City." + city_instance.id, objs)
        self.assertIn("Amenity." + amenity_instance.id, objs)
        self.assertIn("Review." + review_instance.id, objs)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
