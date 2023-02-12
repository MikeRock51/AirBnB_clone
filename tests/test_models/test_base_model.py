#!/usr/bin/python3
"""Defines unittests for base_model.py class."""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        instance1 = BaseModel()
        instance2 = BaseModel()
        self.assertNotEqual(instance1.id, instance2.id)

    def test_two_models_different_created_at(self):
        instance1 = BaseModel()
        sleep(0.05)
        instance2 = BaseModel()
        self.assertLess(instance1.created_at, instance2.created_at)

    def test_two_models_different_updated_at(self):
        instance1 = BaseModel()
        sleep(0.05)
        instance2 = BaseModel()
        self.assertLess(instance1.updated_at, instance2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        instance = BaseModel()
        instance.id = "123456"
        instance.created_at = instance.updated_at = dt
        instancestr = instance.__str__()
        self.assertIn("[BaseModel] (123456)", instancestr)
        self.assertIn("'id': '123456'", instancestr)
        self.assertIn("'created_at': " + dt_repr, instancestr)
        self.assertIn("'updated_at': " + dt_repr, instancestr)

    def test_args_unused(self):
        instance = BaseModel(None)
        self.assertNotIn(None, instance.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        instance = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(instance.id, "345")
        self.assertEqual(instance.created_at, dt)
        self.assertEqual(instance.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        instance = BaseModel(
            "12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(instance.id, "345")
        self.assertEqual(instance.created_at, dt)
        self.assertEqual(instance.updated_at, dt)


class TestBaseModel_save(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

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

    def test_one_save(self):
        instance = BaseModel()
        sleep(0.05)
        first_updated_at = instance.updated_at
        instance.save()
        self.assertLess(first_updated_at, instance.updated_at)

    def test_two_saves(self):
        instance = BaseModel()
        sleep(0.05)
        first_updated_at = instance.updated_at
        instance.save()
        second_updated_at = instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        instance.save()
        self.assertLess(second_updated_at, instance.updated_at)

    def test_save_with_arg(self):
        instance = BaseModel()
        with self.assertRaises(TypeError):
            instance.save(None)

    def test_save_updates_file(self):
        instance = BaseModel()
        instance.save()
        instanceid = "BaseModel." + instance.id
        with open("file.json", "r") as f:
            self.assertIn(instanceid, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        instance = BaseModel()
        self.assertTrue(dict, type(instance.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        instance = BaseModel()
        self.assertIn("id", instance.to_dict())
        self.assertIn("created_at", instance.to_dict())
        self.assertIn("updated_at", instance.to_dict())
        self.assertIn("__class__", instance.to_dict())

    def test_to_dict_contains_added_attributes(self):
        instance = BaseModel()
        instance.name = "Holberton"
        instance.my_number = 98
        self.assertIn("name", instance.to_dict())
        self.assertIn("my_number", instance.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        instance = BaseModel()
        instance_dict = instance.to_dict()
        self.assertEqual(str, type(instance_dict["created_at"]))
        self.assertEqual(str, type(instance_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        instance = BaseModel()
        instance.id = "123456"
        instance.created_at = instance.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(instance.to_dict(), tdict)

    def test_contrast_to_dict_under_dict(self):
        instance = BaseModel()
        self.assertNotEqual(instance.to_dict(), instance.__dict__)

    def test_to_dict_with_arg(self):
        instance = BaseModel()
        with self.assertRaises(TypeError):
            instance.to_dict(None)


if __name__ == "__main__":
    unittest.main()
