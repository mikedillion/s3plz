# -*- coding: utf-8 -*-
import unittest
import s3pyo

MY_TEST_BUCKET = 's3://enigma-euclid'

class TestS3PO(unittest.TestCase):
	
	def test_s3po(self):
		"""
		simple sanity tests on all methods.
		"""
		s3 = s3pyo.connect(MY_TEST_BUCKET, 
			serializer="json.gz",
			public = False
		)	
		obj1 = {"key": "value"}
		filepathformat = 's3pyotest/{@date_path}/{key}/{@timestamp}.json.gz'

		# check put method
		fp1 = s3.put(obj1, filepathformat, **obj1)

		# check exists method
		assert(s3.exists(fp1) is not False)

		# check get method
		obj2 =  s3.get(fp1)
		
		# check whether serialization / deserialization works
		assert(obj1 == obj2)

		# check filepath formatting.
		for fp in s3.ls('s3pyotest/'):
			assert('value' in fp)

		# check streaming method 
		for fp, obj in s3.stream('s3pyotest/'):
			assert("key" in obj)
			assert(isinstance(obj, dict))
			assert("value" in fp)

		# check upsert method / whether 
		# updates to contextual time variables
		# are reflected in formatted filepaths.
		fp2 = s3.upsert(obj1, filepathformat, **ob1)
		assert(fp2 is not False)
		assert(fp1 != fp2)

		# check whether delete method works 
		for fp in s3.ls('s3pyotest/'):
			s3.delete(fp)



	def test_json(self):
		obj1 = {"key": "value"}
		jsonstring = s3pyo.utils.to_json(obj1)
		obj2 = s3pyo.utils.from_json(jsonstring)
		assert(obj1 == obj2)

	def test_gz(self):
		string1 = "uqbar"
		gzstring = s3pyo.utils.to_gz(string1)
		string2 = s3pyo.utils.from_gz(gzstring)
		assert(string1 == string2)






